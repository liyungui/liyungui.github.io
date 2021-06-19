---
title: 深入了解OpenGL之EGL
date: 2020-04-02 14:52:14
categories:
  - OpenGL
tags:
  - OpenGL
---

# 关于EGL

OpenGL ES定义了平台无关的GL绘图指令

EGL则定义了统一的平台接口：

- **Display(EGLDisplay)** 实际显示设备的抽象，用于操作设备窗口。
- **Surface(EGLSurface)** 存储图像的内存区域 FrameBuffer 的抽象
	- 渲染缓存，一块内存空间，所有要渲染到屏幕上的图像数据，都要先缓存在EGLSurface上。
	- 包括：
		- Color Buffer 颜色
		- Stencil Buffer 模板
		- Depth Buffer  深度
- **Context(EGLContext)** OpenGL上下文，用于存储OpenGL的绘制状态信息、数据。
- **EGLConfig** EGL配置，如rgba位数

初始化EGL的过程其实就是配置以上几个信息的过程。

# 为什么学习EGL

Android平台中 **GLSurfaceView**，封装好了EGL环境(提供了对Display,Surface,Context 的管理)，为什么还要学习EGL？

- 加深对OpenGL认识
- Android视频硬编码必须要使用EGL
- FFmpeg编解码都需要用到EGL相关的知识

在JNI层，Android并没有实现一个类似GLSurfaceView的工具，来帮我们隐藏EGL相关的内容。因此，如果你需要在C++层实现FFmpeg的编解码，那么就需要自己去实现整个OpenGL的渲染流程。

这才是学习EGL的真正目的，如果只是用于渲染视频画面，GLSurfaceView已经足够我们使用了。

## 使用EGL的绘图的一般步骤

- 获取EGLDisplay对象
- 初始化与EGLDisplay 之间的连接。
- 获取EGLConfig对象
- 创建EGLContext 实例
- 创建EGLSurface实例
- 连接EGLContext和EGLSurface.
- 使用GL指令绘制图形
- 断开并释放与EGLSurface关联的EGLContext对象
- 删除EGLSurface对象
- 删除EGLContext对象
- 终止与EGLDisplay之间的连接。

一般来说，Android平台大部分OpenGL ES开发，无需直接按照上述步骤来使用OpenGL ES绘制图形。



- 初始化显示设备(创建与本地窗口系统的连接)
	- 调用 eglGetDisplay 方法得到 EGLDisplay
- 初始化 EGL
	- 调用 eglInitialize 方法初始化
- 确定渲染表面的配置信息
	- 有两种方法可以确定可用的渲染表面配置
		- 调用 eglChooseConfig 方法得到 EGLConfig。方便
		- 通过 eglGetConfigs 方法获取 所有渲染表面配置，再用 eglGetConfigAttrib 查询每个 EGLConfig 的信息
- 创建渲染上下文
	- 通过 EGLDisplay 和 EGLConfig ，调用 eglCreateContext 方法创建渲染上下文，得到 EGLContext
- 创建渲染表面
	- 通过 EGLDisplay 和 EGLConfig ，调用 eglCreateWindowSurface 方法创建渲染表面，得到 EGLSurface
	- 通过 EGLDisplay 和 EGLConfig ，调用 eglCreatePbufferSurface 方法创建**离屏渲染**表面，得到 EGLSurface
- 绑定上下文
	- 通过 eglMakeCurrent 方法将 EGLSurface、EGLContext、EGLDisplay 三者和**当前线程**绑定，接下来就可以使用 OpenGL 进行绘制了。
	- 绑定后，在渲染线程中调用任何OpenGL ES的API，OpenGL会自动根据当前线程，切换上下文
	- 这也是 **为什么OpenGL可以在多个GLSurfaceView中正确绘制**
- 交换缓冲
	- 当用 OpenGL 绘制结束后，使用 eglSwapBuffers 方法交换前后缓冲，将绘制内容显示到屏幕上
- 释放 EGL 环境
	- 绘制结束，不再需要使用 EGL 时，取消 eglMakeCurrent 的绑定，销毁 EGLDisplay、EGLSurface、EGLContext。

# 参考&扩展

- [深入了解OpenGL之EGL](https://juejin.cn/post/6844904008935538702) 由浅入深，封装一个gl线程
- [OpenGL 之 EGL 使用实践](https://glumes.com/post/opengl/opengl-egl-usage/)结构清晰
- [从源码角度剖析Android系统EGL及GL线程](https://cloud.tencent.com/developer/article/1035505)
- [Android OpenGL ES 开发教程(5)：关于EGL](http://www.guidebee.info/wordpress/?p=1873) EGL关键类介绍(Display,Surface,Context)
- [Android OpenGL 开发---EGL 的使用](https://www.cnblogs.com/wellcherish/p/12727906.html) EGL初始化
- [OpenGL ES: (3) EGL、EGL绘图的基本步骤、EGLSurface、ANativeWindow](https://www.cnblogs.com/yongdaimi/p/11244950.html) 图文，详细，逻辑清晰