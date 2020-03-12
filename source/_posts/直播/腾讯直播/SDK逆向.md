---
title: SDK逆向
date: 2019-11-25 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# SDK版本

移动直播（Mobile Live Video Broadcasting，MLVB）SDK 

LiteAVSDK_Professional_6.6.7458 

# 类图

{% asset_img 类图.png %}

## 下载

```java	
//音视频数据处理接口 com.tencent.liteav.network.h
public interface IDownloaderCallback {
    void onPullAudio(a var1);

    void onPullNAL(TXSNALPacket var1);
}
```	

```java
public abstract class TXIStreamDownloader {
	startDownload()
	stopDownload()
	onRecvVideoData()
	onRecvAudioData()
	onRecvSEIData()
	onRecvMetaData()
	PushVideoFrame()
	PushAudioFrame()
	getCurrentTS()
	getLastIFrameTS()
}	
```

```java
public class TXCFLVDownloader extends TXIStreamDownloader { 
	//线程名 FlvThread
	nativeInitFlvHander() 创建flvOriginThread线程
	nativeParseData()
	nativeCleanData()
	nativeGetAudioBytes()
	nativeGetVideoBytes()
	nativeGetVideoGop()
	nativePushAudioFrame()
	nativePushVideoFrame()
}

public class TXCRTMPDownloader extends TXIStreamDownloader {
	//线程名 RTMPDownLoad
}
```

```
//StreamRecvThread.cpp

init
writeData
clear
```

```
//FlvContainer.cpp

threadLoop
readTagHeader
parseMetaData
findIFrameOffset
parseVideoData
checkState
```

```
//FlvParserInternal.cpp

reallocBuffer
copyDataTo26xCache
parseData
```
## 解码&渲染

```java
//视频解码器接口 com.tencent.liteav.videodecoder.a
public interface IVideoDecoder{

}
```

```
//视频解码回调接口 com.tencent.liteav.videodecoder.c
public interface VideoDecodeListener {
    void onDecodeFrame(TXSVideoFrame var1, int var2, int var3, long var4, long var6, int var8);

    void onDecodeFailed(int var1);

    void onVideoSizeChange(int var1, int var2);
}
```

```java
//Ffmpeg解码器
public class TXCVideoFfmpegDecoder implements IDecoder {

}
```

```java
//MediaCodecDecoder解码器 com.tencent.liteav.videodecoder.b;
public class MediaCodecDecoder implements IDecoder {
 
}
```

```java
//TXCVideoDecoder解码器
public class TXCVideoDecoder implements DecodeListener {
 
}
```

```java
public class TXCRenderAndDec implements DecodeListener{
	setVideoRender(com.tencent.liteav.renderer.f var1)//设置Render，开始渲染
	setRenderAndDecDelegate()
	setVideoFrameListener(com.tencent.liteav.s var1) 设置渲染TXSVideoFrame的监听
	setConfig()
	setDecListener()
	enableDecoderChange()
	start()
	startVideo()
	isRendering()
	decVideo(TXSNALPacket var1)
	startDecode()
	switchToSoftDecoder()
	requestKeyFrame()
}
```

```
//TXCVideoJitterBuffer.cpp

Start
Stop
PushFrame
PullFrame
DropFrame
getVideoDecoderSink
OnNotifyLoadingEvent
SetHWCacheFrameCount
```

```
// TXCVideoDecoder.cpp

Start
Stop
EnableDecodeChange
OnReceiveVideoFrame
SetStreamType
SetID
onDecodeDone
```

```
//TXCAudioJitterBuffer.cpp

adjustThreshold
```

```
//TXCFFmpegAACDecoder.cpp

Init
DoDecode
```

```
//TXCTraeAudioEngine.cpp

ThreadLoop100ms
OnQueryPcmToPlay
```

## 播放器

```java
com.tencent.liteav.r 基类TXIPlayer

TXLivePlayer
com.tencent.rtmp.a //TXLivePlayer的实现类的代理类
com.tencent.liteav.g //TXLivePlayer的实现类

TXVodPlayer
com.tencent.liteav.n //TXVodPlayer的实现类

TXCloudVideoView
TXCVodVideoView
```

## 数据日志

```
TXCEventRecorderProxy
TXCKeyPointReportProxy
TXCLog
```

# 时序图

{% asset_img 时序图.png %}

StreamRecvThread.cpp writeData

## API调用过程

```
TXLivePlayer startPlay

TXLivePlayerImpDelegate a

AudioEngImplTRAE a

TXCTraeAudioEngine.cpp a

liteav.renderer.f b(TextureView paramTextureView)

TXCRenderAndDec setVideoRender((f paramf))

TXCRenderAndDec start(boolean paramBoolean)

TXCVideoDecoder.cpp Start

TXCAudioJitterBuffer.cpp 

TXCFLVDownloader startDownload

liteav.renderer.f b(Surface paramSurface)

liteav.basic.datareport.TXCDRApi

tx_dr_base.cpp RecvResponse

tx_dr_base.cpp txReportDAU

jni_audio_play.cpp Java_com_tencent_liteav_audio_impl_TXCJitter_nativeSetJitterListener

TXCRenderAndDec setVideoFrameListener

TXCVideoJitterBuffer.cpp Start

TXCVideoJitterBuffer.cpp getVideoDecoderSink

StreamRecvThread.cpp threadLoop flv play parse the flv tag head at 0

TXCFFmpegAACDecoder.cpp Init
TXCFFmpegAACDecoder.cpp DoDecode init soft aac decoder success sr[44100|48000] , ch[2|2]!

FlvContainer.cpp parseVideoData flv parse the I Frame

TXCFFmpegAACDecoder.cpp DoDecode aac soft dec first frame success with audio info : samplerate[44100|48000] , channel [2|2]

TXCVideoJitterBuffer.cpp OnNotifyLoadingEvent recv loading event 0

TXCVideoDecoder.cpp OnReceiveVideoFrame trtc_play:decode: push first i frame

TXCVideoDecoder.cpp onDecodeDone trtc_play:decode: decode first frame success

TXCTextureViewWrapper vrender: set video size:1280,720

TXCVideoRender trtc_render render first frame
TXCVideoRender play:vrender: texture available

TXCTextureViewWrapper vrender: set view size:2061,1080

TXCVideoRender play:vrender: start render thread

TXCVideoRenderThread vrender: init egl

TXCTextureViewWrapper vrender: set view size:2061,1080
TXCTextureViewWrapper vrender: set video size:1280,720

TXCYuvTextureRender frame type 0 matrix_test videoRange
```

# 线程
|线程名| 作用|
|---|---|
|`FlvThread`  音视频数据接收线程java| 网络下载|
|`FlvOriginThread` 音视频数据接收线程c| 接收java层数据|
|`video_jitter_buffer` 视频解码线程| 解码和缓冲视频帧|
|`TXCLogUploader` 日志上传线程| 上传日志|

# FLV下载

{% asset_img FLVDownloader.png %}

# FLV解析

{% asset_img FLV解析.jpg %}

# 音频播放

使用ffmpeg解码aac为pcm

使用audiotrack播放

# ITXLivePlayListener.onNetStatus

网络状态、帧率等的通知，通知的内容（key，value）格式

开始播放回调一次，然后每两秒回调一次


```java
// com.tencent.liteav.g TXLivePlayer的实现类 TXLivePlayerImp

public int a(String var1, int var2) {
	//开始播放
	this.u();//首次调用onNetStatus
}

private void u() {
    this.L = true;
    if (this.h != null) {
        this.h.postDelayed(new Runnable() {
            public void run() {
                if (g.this.L) {
                    g.this.w();
                }

            }
        }, 2000L);
    }

}

private void w() {
	//构建通知的内容（key，value）格式
	//通过onNotifyEvent回调到onNetStatus
	com.tencent.liteav.basic.util.b.a(this.e, 15001, var9);
	//循环调用自身
    if (this.h != null && this.L) {
        this.h.postDelayed(new Runnable() {
            public void run() {
                if (g.this.L) {
                    g.this.w();
                }

            }
        }, 2000L);
    }

}

public static void a(WeakReference<a> var0, String var1, int var2, Bundle var3) {
    if (var0 != null) {
        a var4 = (a)var0.get();
        if (var4 != null) {
            var3.putString("EVT_USERID", var1);
            var4.onNotifyEvent(var2, var3);
        }

    }
}

public void onNotifyEvent(int var1, Bundle var2) {
    if (var1 == 15001) {
        if (this.a != null) {
            this.a.setLogText(var2, (Bundle)null, 0);
        }

        if (this.e != null) {
            this.e.onNetStatus(var2);
        }
    }
    ...
}
```
