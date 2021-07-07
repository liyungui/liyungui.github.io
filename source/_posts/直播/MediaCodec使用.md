---
title: MediaCodec使用
date: 2020-04-02 14:52:14
categories:
  - 直播
tags:
  - 直播
---

```
private static final String MIME_TYPE = "video/avc";
private static final int FRAME_RATE = 25;
private static final float BPP = 0.25f;

// 创建MediaFormat
MediaFormat format = MediaFormat.createVideoFormat(MIME_TYPE, mWidth, mHeight);
format.setInteger(MediaFormat.KEY_COLOR_FORMAT, MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface);	// API >= 18
format.setInteger(MediaFormat.KEY_BIT_RATE, calcBitRate());
format.setInteger(MediaFormat.KEY_FRAME_RATE, FRAME_RATE);
format.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL, 10);

mMediaCodec = MediaCodec.createEncoderByType(MIME_TYPE);
// 配置编解码 编码
mMediaCodec.configure(format, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE);
// 获取编解码器 输入Surface
mSurface = mMediaCodec.createInputSurface();	// API >= 18
// 开始编解码
mMediaCodec.start();

private int calcBitRate() {
	final int bitrate = (int)(BPP * FRAME_RATE * mWidth * mHeight);
	return bitrate;
}
```

# 相机帧数据

Android上相机有2种返回帧数据的方式：

- 一种是以**byte数组**的方式返回
	- `setPreviewDisplay(SurfaceView的SurfaceHolder)` 系统帮我们处理了相机采集的各种角度同时进行了绘制
- 一种是以**texture**的方式返回
	- `setPreviewTexture(SurfaceTexture)`自定义处理数据与绘制，比如滤镜美颜、贴纸

## PreviewCallback

```
setPreviewCallback(PreviewCallback)
public interface PreviewCallback{
	void onPreviewFrame(byte[] data, Camera camera);
}
```

## SurfaceTexture

`public SurfaceTexture(int texture)`

texture是一个int类的值

可以认为SurfaceTexture是将texture包了一层

texture和surfaceTexture都是我们自己创建的，然后设置给camera。

### 创建texture

既然要创建texture，那就需要OpenGL环境

注意这里使用GLES创建texture，不是普通的texture，是**OES**类型的texture

相机和视频硬解码出来的内容，都需要用OES类型的texture承载，否则会报错。

### 创建SurfaceTexture

做OpenGL渲染，一般会用GLSurfaceView(SurfaceView子类)，它自带了OpenGL环境，不需要我们再去创建

但是有缺陷：不是普通的View，无法放到view树上，无法移动等

所以可以封装一个带有OpenGL环境的TextureView（TextureView内含一个SurfaceTexture）

# ByteBuffer和Surface

Android硬件编解码API支持两种方式对数据编解码

- ByteBuffer
	- 效率：低
	- 访问原始视频数据帧：方便
	- 兼容性：弱。颜色格式等等的问题
	- 系统版本：Android16(4.1)
	- 核心API：dequeueInputBuffer(),queueInputBuffer()
- Surface
	- 效率：高
	- 访问原始视频数据帧：不能直接访问；只能访问非安全的原始帧
	- 兼容性：强。
	- 系统版本：Android18(4.3)
	- 核心API：createInputSurface()

Surface直接使用本地视频数据缓存（native video buffers），而没有映射或复制数据到ByteBuffers，因此，这种方式会更加高效。

在使用Surface的时候，通常不能直接访问原始视频数据，但是可以使用ImageReader类来访问非安全的解码（原始）视频帧。这仍然比使用ByteBuffers更加高效，因为一些本地缓存（native buffer）可以被映射到 direct ByteBuffers。

当使用ByteBuffer模式，你可以利用Image类和getInput/OutputImage(int)方法来访问到原始视频数据帧。

# MediaCodec视频采集步骤

- MediaCodec**创建Surface**(用于输入)
- camera预览时的上下文EGL**创建OpenGL的环境**
- 根据上面得到的Surface**创建EGLSuface**
- camera预览时的绑定的纹理id，进行**纹理绘制**
- 交换数据，让数据输入新Surface
- AudioRecord声音采集
- Mediacodec编码为h264、AAC
- MediaMuxer封装为mp4

**MediaMuxer 要Android18(4.3)以上才支持**

# 滤镜以及本地绘制

本地绘制主要靠openGL进行绘制，我们需要先在Camera的采集回调线程上创建一个EGLContext以及EGLDisplay和EGLSurface， 其中EGLContext是openGL在该线程上的上下文，EGLDisplay是一块GPU中的虚拟显示区，主要用于缓存GPU上的视频数据，EGLSurface为具体显示的View到openGL上的映射，是真正绘制到View上的工具。

当接受到Camera采集回调的一帧数据后，我们先通过SurfaceTexture.updateTexImage()方法，将Camera采集的数据映射到SurfaceTexture。然后根据glsl语言将TextureID对应的数据绘制到EGLDisplay上，这里需要注意的是，Camera采集是有角度的，横竖屏下角度不同，可以通过SurfaceTexture的getTransformMatrix方法获取角度矩阵，然后把矩阵传给EGLDisplay进行旋转。EGLDisplay旋转绘制完成后通过eglSwapBuffers方法就可以将EGLDisplay上的数据拷贝到EGLSurface上进行显示了。Android 系统中的GLSurfaceView最后就是通过eglSwapBuffers将数据显示到我们看到的屏幕上的。

# 硬件编码

先通过MediaCodec创建一个Surface，然后将这个Surface绑定到一个EGLSurface，当Camera采集的数据回调时，我们只要重复一次绘制模块的操作，将Camera采集到SurfaceTexture上的数据swapBuffers到EGLSurface 上就可以了。然后循环MediaCodec输出缓冲区，MediaCodec就会将编码后的数据返回给我们了。这样做的好处就是将显示和编码完全分离了，即使我们没有UI View的情况下也可以进行编码，比如在不同Activity之间切换也不会影响我们的正常编码。

# 参考&扩展

- [音视频开发总结之二Android平台相关](https://blog.csdn.net/unreliable_narrator/article/details/92577005)采集流程、采集方案对比、编码方案对比、播放方案对比、滤镜特效
- [Android短视频中如何实现720P磨皮美颜录制](https://blog.csdn.net/xiaoying5558/article/details/80132276)网易云短视频SDK
- [libstreaming](https://github.com/fyhertz/libstreaming) 开源库，提到了MediaCodec的两种使用方式
- [Android视频处理之MediaCodec-1-简介](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483866&idx=1&sn=f5600690c3c034d7d6585a30311a1587&chksm=f989298dcefea09b77fad1d244e722f21d196ffed9da2317866511032f23ea37c4e01bc16cf5&scene=38#wechat_redirect)
- [Android音视频开发之MediaCodec编解码](https://mp.weixin.qq.com/s?__biz=MzI1NDc5MzIxMw==&mid=2247486073&idx=1&sn=9006ae3e0149ebbea2438a83873c4887) 58技术
- [MediaCodec 之——踩坑](https://blog.csdn.net/gb702250823/article/details/81669684) 关键帧失效等