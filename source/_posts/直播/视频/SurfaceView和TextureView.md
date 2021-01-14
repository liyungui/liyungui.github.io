---
title: SurfaceView和TextureView
date: 2020-11-05 15:28:14
categories:
  - 视频
tags:
  - 视频
---

# 概述

## SurfaceView

android普通窗口的视图绘制机制是一层一层的，任何一个子元素或者是局部的刷新都会导致整个视图结构全部重绘一次，因此效率非常低下，适用于普通应用界面

**SurfaceView** 创建一个置于应用窗口之后的**新窗口**。

这种方式的效率非常高，因为SurfaceView窗口刷新的时候不需要重绘应用程序的窗口

## TextureView

SurfaceView有一些非常不便的限制。

因为SurfaceView的内容不在应用窗口上，所以不能使用变换（平移、缩放、旋转等）。也难以放在ListView或者ScrollView中，不能使用UI控件的一些特性比如View.setAlpha()。

为了解决这个问题 **Android 4.0**中引入了TextureView。

# TextureView

**必须在硬件加速的窗口中使用**

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