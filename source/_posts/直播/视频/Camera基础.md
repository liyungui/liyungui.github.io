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
	- 旧版 API，现已弃用，在Android5.0以下使用
- `android.hardware.camera2.CameraManager`
	- 新 API，Android5.0以上使用
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

# 相机方向

## 屏幕自然方向

每个设备都有一个自然方向

默认情况下，手机的自然方向是竖屏方向，平板的自然方向是横屏。

Android系统可以通过给View设置`OrientationEventListener`监听设备方向

`onOrientationChanged(int orientation)` 返回0到359的角度，其中0表示自然方向。

实现原理是封装了 `SensorManager`

## 屏幕坐标方向

Android系统中，以屏幕自然方向的左上角为坐标系统的原点(0,0)坐标，该坐标系是固定不变的，不会因为设备方向的变化而改变。

## 摄像头传感器方向

摄像头传感器在被固定到手机上后有一个默认的取景方向，方向一般是和手机横屏方向一致

## 相机预览方向

默认情况下，和摄像头传感器方向一致，可以通过Camera API进行改变。

Camaer 1 是 `setDisplayOrientation(int orientation)`

`orientation` 就是摄像头传感器方向顺时针旋转到屏幕自然方向的角度。

不同的摄像头位置，orientation是不一样的

- 后置摄像头
	- 横屏：0 屏幕的自然方向和相机的摄像头传感器方向一致的
	- 竖屏：90 预览图像逆时针旋转了90度，因此预览方向需顺时针旋转90度
- 前置摄像头

## 相机拍照方向

设置预览方向并不会改变拍出照片的方向。

对于后置相机，相机采集到的图像和相机预览的图像是一样的，只需要旋转后置相机orientation度。

对于前置相机来说，相机预览的图像和相机采集到的图像是镜像关系。

采集的图像：顺时针旋转270度后，与屏幕自然方向一致。

预览的图像：顺时针旋转90度后，与屏幕自然方向一致。


# 参考&扩展

- [摄像头Camera视频源数据采集解析](http://www.cxyzjd.com/article/chupu2979/100616420)
- [Android Camera-相机尺寸、方向和图像数据](https://juejin.cn/post/6844904064568803341)
