---
title: AMR音频在Android和iOS跨平台应用
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---	
	
	AMR音频在Android和iOS上的应用  http://shaoyuan1943.github.io/2016/02/26/chat-in-game-three/

AMR格式的文件大小比AAC更小，经过测试之后发现的确如此，10s左右的语音采用AMR格式的文件大小可以稳定在15k左右。

现实情况**Android支持AMR**，但是**iOS4.3.x**版本之后不再支持AMR，**剔除了AMR的硬解**。但通过opencore这个codec依旧可以在iOS平台上对AMR进行软解，以实现AMR转换到其他的格式可以播放。

最终确定采用AMR作为两平台的语音交互格式，不同的是，在iOS平台上需要进行WAV和AMR之间的转换。好在libopencore可以解决这个事情。

在折腾过程中也踩到一个坑，我把**Android上录制的AMR放到iOS上进行转换播放时会出现问题，无法进行转换。尝试调整了各种参数也无法解决**

偶然想到是不是因为两者解码时的文件参数不一样，于是下载了MediaInfo对比了Android和iOS上录制的AMR文件，发现两者参数不一样，于是我尝试去调整一下Android上录制AMR的参数：

	recorder.setOutputFormat(MediaRecorder.OutputFormat.AMR_NB);
	recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
	recorder.setAudioChannels(1);
**一定要输出和编码格式都是AMR_NB格式的，才能在两者正常通用。**
