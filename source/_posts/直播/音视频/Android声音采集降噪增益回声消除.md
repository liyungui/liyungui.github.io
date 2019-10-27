---
title: Android声音采集降噪增益回声消除
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

[Android手机直播（三）声音采集](http://www.jianshu.com/p/2cb75a71009f)

[项目github](https://github.com/LaiFeng-Android/SopCastComponent)

# 一、基础知识 #

## 麦克风降噪 ##
![](http://upload-images.jianshu.io/upload_images/924057-0c83cc87d86f846f.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
底部的麦是用来提供清晰通话，而顶部的麦是用来消除噪音

两个麦克风所拾取的背景噪声音量是基本相同的，而记录的人声会有6dB左右的音量差。顶端麦收集噪声后，通过解码生成补偿信号后就可以用来消除噪音了

## 回声消除 ##

回声消除就是在麦克风录制外音的时候去除掉手机自身播放出来的声音，这样就将对方的声音从采集的声音中过滤出去，从而就避免了回声的产生
![](http://upload-images.jianshu.io/upload_images/924057-395c4cb4f1deb4ff.png?imageMogr2/auto-orient/strip)

# 二、声音采集 #

想要将声音用计算机语言表述，则必须将声音进行数字化。

将声音数字化，最常见的方式是通过脉冲编码调制PCM(Pulse Code Modulation) 。

抽样、量化、编码三个过程中三个参数：**采样频率、采样位数和声道数**

# 三、Android声音录制 #

## 音频源 ##

	/** 默认声音 **/
	public static final int DEFAULT = 0;

	/** 麦克风声音 */
	public static final int MIC = 1;

	/** 通话上行声音 */
	public static final int VOICE_UPLINK = 2;

	/** 通话下行声音 */
	public static final int VOICE_DOWNLINK = 3;

	/** 通话上下行声音 */
	public static final int VOICE_CALL = 4;

	/** 根据摄像头转向选择麦克风*/
	public static final int CAMCORDER = 5;

	/** 对麦克风声音进行声音识别，然后进行录制 */
	public static final int VOICE_RECOGNITION = 6;

	/** 对麦克风中类似ip通话的交流声音进行识别，默认会开启回声消除和自动增益 */
	public static final int VOICE_COMMUNICATION = 7;

	/** 录制系统内置声音 */
	public static final int REMOTE_SUBMIX = 8;

## 采样率 ##

几种常见的采样率：

	8000, 11025, 16000, 22050, 44100, 48000

Android官方文档要求所有的手机需要对44100Hz的采样率进行支持，可是国内极其少数的手机依然不支持44100Hz的采样率

在设置采样率之前需要对手机对设置的采样率是否支持进行**检测**

	for (int rate : new int[] {8000, 11025, 16000, 22050, 44100}) {  // add the rates you wish to check against
        int bufferSize = AudioRecord.getMinBufferSize(rate, AudioFormat.CHANNEL_CONFIGURATION_DEFAULT, AudioFormat.ENCODING_PCM_16BIT);
        if (bufferSize > 0) {
            // buffer size is valid, Sample rate supported
        }
    }

## 采样位数 ##

**ENCODING_PCM_16BIT** 可以保证兼容所有Android手机。

## 声道 ##

**AudioFormat.CHANNEL_CONFIGURATION_MONO（单声道）** 可以保证兼容所有Android手机。

# 四、Android回声消除 #

三种方式进行处理：

1. 通过**VOICE_COMMUNICATION**模式进行录音，自动实现回声消除；**效果最好，兼容性也较好**

	- 将AudioManager设置模式为MODE_IN_COMMUNICATION
	- 将麦克风打开。
			
			AudioManager audioManager = (AudioManager)mContext.getSystemService(Context.AUDIO_SERVICE);
			audioManager.setMode(AudioManager.MODE_IN_COMMUNICATION);
			audioManager.setSpeakerphoneOn(true);

	- 音频采样率必须设置8000或者16000
	- 通道数必须设为1个

2. 利用Android自身带的**AcousticEchoCanceler**进行回声消除处理；**很少手机支持**

	- 录制声音的时候可以通过AudioRecord得到AudioSessionId，
	- 创建AudioTrack的时候也可以传入一个AudioSessionId，
	- 将这个统一的AudioSessionId传入AcousticEchoCanceler，AcousticEchoCanceler进行回声消除

3. 使用第**三方库**（Speex、Webrtc）进行回声消除处理；**理论上兼容性最好，但是设置合适的延时间隔很难**


