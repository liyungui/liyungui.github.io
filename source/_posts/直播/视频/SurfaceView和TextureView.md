---
title: SurfaceView和TextureView
date: 2020-11-05 15:28:14
categories:
  - 视频
tags:
  - 视频
---

# SurfaceView

**拥有独立绘图层(Surface)的特殊View** 

- **View的子类** 即和view相同
	- 可以嵌入到View结构树中
	- 可以设定它的大小
- 提供了一个**独立的绘图层（直接绘制到屏幕上）** 即和view不相同
	- 不能执行Transition，Rotation，Scale等转换
	- 不能进行Alpha透明度运算

## SurfaceView的Surface

**Surface 绘图层，其实就是内存中的一段绘图缓冲区。**

## SurfaceHolder

**顾名思义就是Surface的持有者**

SurfaceView就是通过过SurfaceHolder来对Surface进行管理控制的。

SurfaceView.getHolder方法可以获取SurfaceView相应的SurfaceHolder。

## 和普通View的展示的区别

- 普通View
	- 组成View hierachy的 **树结构**
	- 树结构 添加到 Activity的 **DecorView**
	- DecorView
		- 对 **WMS** 可见，有一个对应的 **WindowState**
		- 在 **SF** 中有对应的 **Layer**
- SurfaceView
	- 自带一个Surface
		- 对 **WMS** 可见，有一个对应的 **WindowState**
		- 在 **SF** 中有对应的 **Layer**

**在Client端(App)它仍在View hierachy中**

**在Server端（WMS和SF）中，它与宿主窗口是分离的**

{% asset_img SurfaceView.png %}

## Surface创建时机

Surface是在SurfaceView所在的**Window可见的时候创建**的。

我们可以使用SurfaceHolder.addCallback方法来监听Surface的创建与销毁的事件。

需要注意的是SurfaceHolder.Callback的所有回调方法都是在**主线程**中回调的。

## Surface在Window中的层级

Window有一层**View树的绘图层**Surface

SurfaceView的Surface排在**View树的绘图层的下面**

SurfaceView嵌入到Window的View结构树中就好像在Window的Surface上强行打了个洞让自己显示到屏幕上

## Surface线程

SurfaceView**另起一个线程**对自己的Surface进行刷新

Surface的渲染可以放到单独线程去做，渲染时可以有自己的GL context。

这对于一些游戏、视频等性能相关的应用非常有益，因为它不会影响主线程对事件的响应。

## Surface双缓冲机制

SurfaceView中具有**两个Surface**，也就是我们所说的双缓冲机制

android普通窗口的视图绘制机制是一层一层的，任何一个子元素或者是局部的刷新都会导致整个视图结构全部重绘一次，因此效率非常低下，适用于普通应用界面

**SurfaceView** 创建一个置于应用窗口之后的**新窗口**。

这种方式的效率非常高，因为SurfaceView窗口刷新的时候不需要重绘应用程序的窗口

# GLSurfaceView

**SurfaceView的子类**

GLSurfaceView作为SurfaceView的补充，可以看作是SurfaceView的一种典型使用模式。

在SurfaceView的基础上，它加入了**EGL**的管理，并自带了渲染线程。

另外它定义了用户需要实现的Render接口，提供了用Strategy pattern更改具体Render行为的灵活性。作为GLSurfaceView的Client，只需要将实现了渲染函数的Renderer的实现类设置给GLSurfaceView即可。


# SurfaceTexture

SurfaceTexture和SurfaceView不同的是，它对图像流的处理并不直接显示，而是**转为GL外部纹理**，因此可用于图像流数据的**二次处理**（如Camera滤镜，桌面特效等）。比如Camera的预览数据，变成纹理后可以交给GLSurfaceView直接显示，也可以通过SurfaceTexture交给TextureView作为View heirachy中的一个硬件加速层来显示。首先，SurfaceTexture从图像流（来自Camera预览，视频解码，GL绘制场景等输出）中获得帧数据，当调用updateTexImage()时，根据内容流中最近的图像更新SurfaceTexture对应的GL纹理对象，接下来，就可以像操作普通GL纹理一样操作它了。

# TextureView

**View的子类** 内部包含一个 SurfaceTexture

专门用来渲染像视频或OpenGL场景之类的数据的，而且TextureView只能用在具有**硬件加速**的Window中，如果使用的是软件渲染，TextureView将什么也不显示。也就是说对于没有**GPU**的设备，TextureView完全不可用。

## 为什么要用TextureView

SurfaceView有一些非常不便的限制。

因为SurfaceView的内容不在应用窗口上，所以不能使用变换（平移、缩放、旋转等）。也难以放在ListView或者ScrollView中，不能使用UI控件的一些特性比如View.setAlpha()。

为了解决这个问题 **Android 4.0**中引入了TextureView。

它不会在WMS中单独创建窗口，而是作为View hierachy中的一个普通View，因此可以和其它普通View一样进行移动，旋转，缩放，动画等变化。

# TextureView

## 使用

使用非常简单，唯一要做的就是获取用于渲染内容的SurfaceTexture

```java
创建TextureView对象
textureView.setSurfaceTextureListener(new TextureView.SurfaceTextureListener() {
    @Override
    public void onSurfaceTextureAvailable(SurfaceTexture surfaceTexture, int width, int height) {
        LogUtil.i(TAG, "onSurfaceTextureAvailable");
        //获取TextureView
        //这里自定义SurfaceTexture给TextureView
        //也可以使用默认的
        int[] arr = new int[1];
        GLES20.glGenTextures(1, arr, 0);
        int texName = arr[0];
        mSurfaceTexture = new MySurfaceTexture(texName);
        setSurfaceTexture(mSurfaceTexture);
        
        //创建Surface接收视频数据
        mSurface = new Surface(mSurfaceTexture);
        LogUtil.i(TAG, "setSurface " + mSurface);
        mMediaPlayer.setSurface(mSurface);
    }

    @Override
    public void onSurfaceTextureSizeChanged(SurfaceTexture surface, int width, int height) {
    }

    @Override
    public boolean onSurfaceTextureDestroyed(SurfaceTexture surface) {
        LogUtil.i(TAG, "onSurfaceTextureDestroyed");
        mSurfaceTexture = null;
        mSurface = null;
        mMediaPlayer = null;
        return true;
    }

    @Override
    public void onSurfaceTextureUpdated(SurfaceTexture surface) {
    }
});
```

## 黑色背景

在没有渲染内容的时候，默认是黑色的背景

TextureView 不支持设置背景

解决方案：透明化(显示父View背景)，在开始渲染的时候再设为非透明

`setAlpha(0.0f);//0不透明，即全透明`

## 无缝衔接播放

不跨页面场景：全屏/小屏播放

跨页面场景：视频列表中播放，点击进入视频详情页

### 核心：复用SurfaceTexture

接收player产生的视频流的对象是SurfaceTexture，而不是TextureView。TextureView只是作为一个硬件加速层来展示。

所以TextureView复不复用没关系然用。一定要保证SurfaceTexture的复用。

即，TextureView可以new 一个新的，但textureView.setSurfaceText()传入的需是老的SurfaceTexture。

如果复用TextureView，需要从界面原来的ViewGroup中remove掉，然后把textureView添加到新的ViewGroup中。

在remove textureView时，textureView 中的surfaceTexture成员变量会置为空。所以在textureView重新添加到页面view时，仍然需要把老的SurfaceTexture设置给TextureView

## SurfaceTexture

TextureView的draw()方法执行时，如果SurfaceTexture为空，就会初始化它。初始化完成，就会回调onSurfaceTextureAvailable接口。

所以，复用设置SurfaceTexture时机：

- draw()方法之前，比如preDraw()中
	- 把老的SurfaceTexture给到新的textureview
	- 那么就不会生成新的surfaceTexture了
	- onSurfaceTextureAvailable接口也不会回调
- onSurfaceTextureAvailable接口中

# playerView中肯定需要player

ExoplayerView等也是持有player的。

需要等到 onSurfaceTextureAvailable()方法回调时，才能生成Surface并设置给player。如果player中已有surface，且需要复用，那么就不用设置了，但需要保证把老的surfaceTexture设置到textureview

player一些回调需要操作playerview内部view(内部实现即可；也有些需要外界的特定界面处理)。

**所以更科学的设计是playerView持有player，对外暴露playerView。也有利于复用**

# 参考&扩展

- [TextureView的两种使用场景](https://www.jianshu.com/p/4e2916889f27) 着重无缝衔接播放(包括跨页面)
- [SurfaceView, TextureView, SurfaceTexture等的区别](https://juejin.cn/post/6844903878450741262)
- [Android 视频展示控件之 SurfaceView、GLSurfaceView、SurfaceTexture、TextureView 对比总结](https://www.shuzhiduo.com/A/amd086wkdg/)