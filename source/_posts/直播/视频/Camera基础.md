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

方向	
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

# 参考&扩展

- [摄像头Camera视频源数据采集解析](http://www.cxyzjd.com/article/chupu2979/100616420)
