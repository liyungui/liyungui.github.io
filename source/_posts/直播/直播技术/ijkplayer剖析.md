---
title: ijkplayer剖析
date: 2019-08-05 15:22:14
categories:
  - 直播
tags:
  - 直播
---

# 概述

ijkplayer 是一款比较出众的开源 Android/IOS 跨平台播放器，基于 ffplay，API 易于集成，可定制编译控制体积。

本文基于 **0.8.8** 版本的 ijkplayer ，对其源码进行剖析，涉及到不同平台下的封装接口或处理方式时，均以 **Android** 为例。

ijkplayer android 集成了三种播放器实现：

- **AndroidMediaPlayer**：即安卓系统自带的播放器 **MediaPlayer**，基于 MediaCodec、AudioTrack 等安卓系统 API.
- **IjkExoMediaPlayer**：即谷歌新推出的 **ExoPlayer**，同样是基于 MediaCodec、AudioTrack 等安卓系统 API，但相比 MediaPlayer 具有支持 DASH、高级 HLS、自定义扩展等优点。
- **IjkMediaPlayer**：基于 FFmpeg 的 **ffplay**，集成了 MediaCodec 硬解码器、Opengl 渲染方式等。

一般而言， ijkplayer 就是指 **IjkMediaPlayer**，本文分析的对象就是 IjkMediaPlayer.

## 目录结构

```
ijkplayer（项目文件夹）
	├──tools  - 初始化项目工程脚本
	├──config - 编译ffmpeg使用的配置文件
	├──extra - 存放编译ijkplayer所需的依赖源文件, 如ffmpeg、openssl等
	├──ijkmedia - 核心代码
		├──ijkplayer - 播放器数据下载及解码相关
		├──ijksdl - 音视频数据渲染相关
	├──android -  android平台上的上层接口封装以及平台相关方法
	├──ios - iOS平台上的上层接口封装以及平台相关方法

```

## 功能实现的平台差异

iOS和Android平台的差异主要表现在

- 视频硬件解码
- 音频渲染
- 视频渲染

|Platform|Hardware Codec|Video Render|Audio Output|
|---|---|---|---|
|Android|MediaCodec|OpenGL ES、MediaCodec|OpenSL ES、AudioTrack|
|iOS|VideoToolBox|OpenGL ES|AudioQueue|

# IjkMediaPlayer和Native交互

**播放控制**相关的 `start、pause、stop` 等，调用 对应的 native 方法

**底层状态信息的上报(比如底层的播放状态回调)**相关的 `postEventFromNative` 等，这些方法由底层主动调用(有`@CalledByNative` 注解)

{% asset_img IjkMediaPlayer和Native交互.png %}

# 初始化

```java
public final class IjkMediaPlayer extends AbstractMediaPlayer {
    private void initPlayer(IjkLibLoader libLoader) {
        loadLibrariesOnce(libLoader);
        initNativeOnce();

        Looper looper;
        if ((looper = Looper.myLooper()) != null) {
            mEventHandler = new EventHandler(this, looper);
        } else if ((looper = Looper.getMainLooper()) != null) {
            mEventHandler = new EventHandler(this, looper);
        } else {
            mEventHandler = null;
        }

        /*
         * Native setup requires a weak reference to our object. It's easier to
         * create it here than in C++.
         */
        native_setup(new WeakReference<IjkMediaPlayer>(this));
    }
}
```

`initPlayer` 方法，共做了四件事：

- 加载 so 库
- 静态初始化底层，底层其实什么都没做
- 初始化 Message Handler，处理底层状态信息的上报
- 初始化底层，这部分做的工作最多

## 初始化底层

c代码

 `ijkplayer/android/ijkplayer/ijkplayer-armv7a/src/main/jni/ijkmedia/ijkplayer/android/`
 
主要逻辑位于

 `ijkpalyer_android.c` 的 `ijkmp_android_create` 方法

```
// 创建底层播放器对象，设置消息处理函数
IjkMediaPlayer *mp = ijkmp_create(msg_loop, saveMode, hard_mux);

// 创建图像渲染对象
mp->ffplayer->vout = SDL_VoutAndroid_CreateForAndroidSurface();

// 初始化视频解码器（软/硬）、音频输出设备（opensles/audioTrack）
mp->ffplayer->pipeline = ffpipeline_create_from_android(mp->ffplayer); 
```

### 软硬解码选择

跟踪 `pipeline/ffpipeline_android.c` 的 `ffpipeline_create_from_android` 方法

发现是 用函数指针记录 类 IjkMediaPlayer.setOption() 设置的属性

# 配置

初始化后 IjkMediaPlayer 后，可以对其进行一系列配置，例如:

```java
// 设置硬解码
mIjkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "mediacodec", 1);

// 设置 opensles 方式输出音频
mIjkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "opensles", 1);
```
setOption() 会调用到底层 ff_ffplay.c 的 ffp_set_option() 方法

# 播放

{% asset_img 播放器基本框图.png %}

播放器必然是通过**多线程**同时进行解封装、解码、视频渲染等工作的，对于 Ijkplayer 来说，开辟的线程如下：

{% asset_img 线程.jpeg %}


当对播放器设置视频源路径、解码方式、输出模式等播放选项后，就可以开始播放了， 播放入口方法为 `ffp_prepare_async_l`，此方法中调用了比较重要的两个方法：

```c
 // 打开音频输出设备
    ffp->aout = ffpipeline_open_audio_output(ffp->pipeline, ffp);
    ...
    // 创建音/视频数据解码前/后队列， 创建解封装和视频渲染线程
    VideoState *is = stream_open(ffp, file_name, NULL);
```

stream_open 方法则相当重要了，梳理一下该方法中涉及到的关键方法：

{% asset_img stream_open方法.png %}

# 音视频同步

对于播放器来说，音视频同步是一个关键点，同时也是一个难点，同步效果的好坏，直接决定着播放器的质量。

通常音视频同步的解决方案就是选择一个**参考时钟**，播放时读取音视频帧上的时间戳，同时参考当前时钟参考时钟上的时间来安排播放。如下图所示：

{% asset_img 音视频同步示意图.png %}

如果音视频帧的播放时间大于当前参考时钟上的时间，则不急于播放该帧，直到参考时钟达到该帧的时间戳；如果音视频帧的时间戳小于当前参考时钟上的时间，则需要“尽快”播放该帧或丢弃，以便播放进度追上参考时钟。

## 参考时钟的选择

有多种方式：

- 选取视频时间戳作为参考时钟源
- 选取音频时间戳作为参考时钟源
- 选取外部时间作为参考时钟源

考虑人对视频、和音频的敏感度，在存在音频的情况下，**优先选择音频**作为主时钟源。

ijkplayer在**默认**情况下也是使用**音频**作为参考时钟源

# 事件处理

在播放过程中，某些行为的完成或者变化，如prepare完成，开始渲染等，需要以事件形式通知到外部，以便上层作出具体的业务处理。

播放器底层上报事件时，实际上就是将待发送的消息放入消息队列，另外有一个线程会不断从队列中取出消息，上报给外部

# 参考&扩展

- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979)
- [ijkplayer框架深入剖析](https://www.jianshu.com/p/
)