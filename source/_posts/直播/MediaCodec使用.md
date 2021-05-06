---
title: MediaCodec使用
date: 2020-04-02 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# 概述

Android16(4.1)推出的硬件编解码API

# ByteBuffer和Surface

支持两种方式对数据编解码

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
- AudioReocod声音采集
- Mediacodec编码为h264、AAC
- MediaMuxer封装为mp4

**MediaMuxer 要Android18(4.3)以上才支持**

# 参考&扩展

- [音视频开发总结之二Android平台相关](https://www.jianshu.com/p/a1ce4418e2b5)采集流程、采集方案对比、编码方案对比、播放方案对比、滤镜特效
- [Android短视频中如何实现720P磨皮美颜录制](https://blog.csdn.net/xiaoying5558/article/details/80132276)网易云短视频SDK
- [libstreaming](https://github.com/fyhertz/libstreaming) 开源库，提到了MediaCodec的两种使用方式
- [Android视频处理之MediaCodec-1-简介](https://mp.weixin.qq.com/s?__biz=MzUxODQ3MTk5Mg==&mid=2247483866&idx=1&sn=f5600690c3c034d7d6585a30311a1587&chksm=f989298dcefea09b77fad1d244e722f21d196ffed9da2317866511032f23ea37c4e01bc16cf5&scene=38#wechat_redirect)
- [Android音视频开发之MediaCodec编解码](https://mp.weixin.qq.com/s?__biz=MzI1NDc5MzIxMw==&mid=2247486073&idx=1&sn=9006ae3e0149ebbea2438a83873c4887) 58技术
- [MediaCodec 之——踩坑](https://blog.csdn.net/gb702250823/article/details/81669684) 关键帧失效等