---
title: ijkplayer系列一-开篇
date: 2019-08-05 15:22:14
categories:
  - 直播
tags:
  - 直播
---

# 概述

ijkplayer 是一款比较出众的开源 Android/IOS 跨平台播放器，基于 ffplay，API 易于集成，可定制编译控制体积。

本系列基于 **0.8.8** 版本(目前**最新**版本)的 ijkplayer ，对其源码进行剖析，涉及到不同平台下的封装接口或处理方式时，均以 **Android** 为例。

ijkplayer android 集成了三种播放器实现：

- **AndroidMediaPlayer**：即安卓系统自带的播放器 **MediaPlayer**，基于 MediaCodec、AudioTrack 等安卓系统 API.
- **IjkExoMediaPlayer**：即谷歌新推出的 **ExoPlayer**，同样是基于 MediaCodec、AudioTrack 等安卓系统 API，但相比 MediaPlayer 具有支持 DASH、高级 HLS、自定义扩展等优点。
- **IjkMediaPlayer**：基于 FFmpeg 的 **ffplay**，集成了 MediaCodec 硬解码器、Opengl 渲染方式等。

一般而言， ijkplayer 就是指 **IjkMediaPlayer**，本文分析的对象就是 IjkMediaPlayer.

# 目录结构

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

# 功能实现的平台差异

iOS和Android平台的差异主要表现在

- 视频硬件解码
- 音频渲染
- 视频渲染

|Platform|Hardware Codec|Video Render|Video Output |Audio Output|
|---|---|---|---|---|
|Android|MediaCodec|OpenGL ES、MediaCodec| NativeWindow、OpenGL ES|OpenSL ES、AudioTrack|
|iOS|VideoToolBox|OpenGL ES||AudioQueue|

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
