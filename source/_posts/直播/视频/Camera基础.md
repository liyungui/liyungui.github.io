---
title: Camera基础
date: 2020-04-02 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# Camera

- `android.hardware.Camera `
	- 旧版 API，现已弃用，在Android5.0以下使用。
	- 不够灵活，无法满足需求
- `android.hardware.camera2.CameraManager`
	- 新 API，Android5.0以上使用
	- 使用复杂
- CameraX
	- 基于Camera 2 API封装，简化了开发流程，并增加生命周期控制

# 基本操作

## 打开摄像头

open(int cameraId) 

open() 打开后置摄像头

## 设置Camera.Parameters参数

getParameters方法获取摄像头已有的参数信息，然后进行相关设置，比如尺寸大小，方向，数据格式等信息。

setParameters(Parameters)把设置好的参数信息设置回去

```
setRecordingHint(true)

对焦
setFocusMode
getSupportedFocusModes
	Camera.Parameters.FOCUS_MODE_AUTO
	Camera.Parameters.FOCUS_MODE_CONTINUOUS_VIDEO

闪光
setFlashMode
getFlashMode
	Camera.Parameters.FLASH_MODE_TORCH
	Camera.Parameters.FLASH_MODE_OFF

预览fps
setPreviewFpsRange	
getSupportedPreviewFpsRange
	[15000,20000] 表示15帧至20帧

预览size
setPreviewSize
getSupportedPreviewSizes

预览格式
setPreviewFormat
	getSupportedPreviewFormats
	ImageFormat.NV21 默认
	ImageFormat.YV12	
	
照片size
setPictureSize
getSupportedPictureSizes

照片格式
setPictureFormat
getSupportedPictureFormats
	ImageFormat.NV21，ImageFormat.RGB_565，ImageFormat.JPEG

视频size	
getSupportedVideoSizes

拍照图像方向	
setRotation
	0, 90, 180 or 270	
```

## 设置摄像头的预览界面

可以不设置

设置预览一般有两种方式：

- setPreviewDisplay(SurfaceHolder)
	- 一般是使用**SurfaceView**
	- 无法自定义渲染
- setPreviewTexture(SurfaceTexture)
	- 一般是使用**GLSurfaceView或TextureView**
	- 可以自定义渲染，美颜等

### 预览显示方向

setDisplayOrientation

## 设置预览数据回调

美颜、人脸检测等，一般都是从这里获取 `byte[]` 数据

```
public interface PreviewCallback{
	void onPreviewFrame(byte[] data, Camera camera);
}

setPreviewCallback(PreviewCallback)
每一帧数据准备好了就会调用onPreviewFrame，调用时机不可控制

setPreviewCallbackWithBuffer(PreviewCallback)
手动调用addCallbackBuffer(byte[] callbackBuffer)方法，才会回调调用onPreviewFrame
两个地方要手动调用addCallbackBuffer：一个是在startPreview之前，一个是在onPreviewFrame中
```

## 开始预览

调用startPreview开始预览效果

## 释放

停止预览 stopPreview
释放 release

# 相机方向问题

## 屏幕显示方向(自然方向)

{% asset_img 屏幕显示顺时针旋转角度.png %}

**永远向上**。即手机屏幕垂直于地面向上，坐标的原点永远在当前屏幕的左上角

默认情况下，平板的自然方向是横屏，而手机的自然方向是竖屏方向。

### 屏幕显示顺时针旋转角度(设备逆时针旋转角度)

`Context.getDisplay().getRotation()` 

比如 逆时针旋转设备90度，那么屏幕为了保持竖直向上就需要顺时针旋转90度

返回值只有以下四个值。因为要把手机旋转90度，屏幕才会旋转

```
Surface
public static final int ROTATION_0 = 0;
public static final int ROTATION_90 = 1;
public static final int ROTATION_180 = 2;
public static final int ROTATION_270 = 3;
```

还可以通过给View设置`OrientationEventListener`监听设备方向

`onOrientationChanged(int orientation)` 返回0到359的角度。实现原理是封装了 `SensorManager`

## 摄像头安装方向

{% asset_img 摄像头显示顺时针旋转角度.png %}

**固定**。安装时就固定了

主流的手机安装方向是：朝向手机竖直握持的右边

### 为什么安装在右侧

猜测：历史遗留原因和兼容。

#### 历史遗留

**安装在右侧符合人类肉眼视野**

横向(设备逆时针旋转90度)拍照可以带来更广的水平视野，更加符合我们的肉眼正常视野。所以摄像头硬件的设计是按照横向来进行设计。

安装在有右侧，横向(设备逆时针旋转90度)时，手机的屏幕方向和摄像头方向就一致了，就不需要处理方向问题。

如果现在需要更改这个摄像头的安装方向，那么更改的是整个供应链的设计标准，显然不可能。

#### 兼容

android设备没有办法做到统一。A厂商摄像头安装在右侧，那么B厂商完全可以安装在左侧。为了兼容不同的设备情况，android提供api让开发者去适配这些情况。

### 摄像头显示顺时针旋转角度(摄像头顺时针夹角)

`Camera.CameraInfo.orientaion`

**竖直拍摄正向显示顺时针旋转角度(设备竖直方向摄像头安装方向的顺时针夹角)**

- **右侧：90**
- **左侧：270**

## 预览与成片方向错乱的本质原因

摄像头中没有传感器，所以无法感知自己当前的方向

## 拍摄角度

- **后置摄像头**
	- 拍摄角度和我们一致
	- **逆时针旋转设备，后置摄像头跟着逆时针旋转**
- **前置摄像头**
	- 拍摄角度和我们相反(站在我们对面)
	- 和我们的视野 **左右镜像**
	- **逆时针旋转设备，前置摄像头其实是顺时针旋转**
	- **在前置摄像头角度，他的成像方向其实是向左**(我们视角，前后相机都是向右)
	- **另外：前置相机预览的图像是相机采集到的图像的Y轴(左右)镜像**
		- 即，前置相机预览在显示和旋转之前，会以手机自然方向Y轴(左右)镜像翻转。

所以，我们上面谈的关于安装方向向右，隐含语境是我们视角的左右。

下图是前后相机竖屏状态下，采集和预览的图像内容

{% asset_img 拍摄角度.png %}

## 如何解决方向错乱问题

解决方向有两个：预览方向与成片方向

这两者的旋转有不同的算法，且两者参数不互相影响。设置预览方向并不会改变拍出照片的方向。

### 相机预览方向

默认情况下，和摄像头传感器方向一致

`Camaer.setDisplayOrientation(int orientation)` 设置预览画面顺时针旋转的角度(`0、90、180、270`)

### 相机拍照方向

`Parameters.setRotation(int rotation)` 设置图片顺时针旋转的角度(`0、90、180、270`)

## 角度适配计算

我们先明确两个参数：

- `Context.getDisplay().getRotation()`
	- screenOrientation
	- 屏幕显示顺时针旋转角度(设备逆时针旋转角度)
- `Camera.CameraInfo.orientaion`
	- cameraOrientation
	- 摄像头显示顺时针旋转角度(摄像头顺时针夹角)

### 后置摄像头

| cameraOrientation|screenOrientation|适配角度|
|---|---|---|
|90 固定向右|0 |90|
|90|90 设备逆时针旋转|0|
|90|180|270|
|90|270|180|

**预览方向和成片反向 一致：两者之差求360度的正相位**

`(cameraOrientation-screenOrientation +360)%360`

逆时针旋转设备的时候，摄像头也跟着逆时针旋转，相机得到的图片会进行逆时针旋转。恢复到自然方向需要顺时针旋转cameraOrientation，而逆时针旋转会抵掉摄像头的旋转。那么最终的结果就是两者之差(需要顺时针旋转的角度)求360度的正相位(+360取模)。

### 前置摄像头

逆时针旋转设备的时候，前置摄像头是顺时针旋转，相机得到的图片会进行顺时针旋转。恢复到自然方向需要顺时针旋转cameraOrientation，而逆时针旋转会增加摄像头的旋转。那么最终的结果就是两者之和(需要顺时针旋转的角度)(取模)。

图片：`(cameraOrientation+screenOrientation)%360`

前置相机预览在显示和旋转之前，会以手机自然方向Y轴(左右)镜像翻转。所以我们需要再翻转一下

预览：`(360 - (cameraOrientation+screenOrientation)%360) %360`

# 参考&扩展

- [摄像头Camera视频源数据采集解析](http://www.cxyzjd.com/article/chupu2979/100616420)
- [预览图片前置后置角度？别傻傻弄不清｜android相机角度解析](https://juejin.cn/post/6976220868003233829) 图文，原理上解释清楚
- [Android Camera-相机尺寸、方向和图像数据](https://juejin.cn/post/6844904064568803341) 结合上面的原理，一起看很好理解