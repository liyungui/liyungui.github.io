---
title: android录音和播放
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# 录音

 必须在AndroidManifest中设置相应的权限：android:name="android.permission.RECORD_AUDIO" 

 Android提供了两个API用于实现录音功能

## AudioRecord ##

	主要是实现边录边播（AudioRecord+AudioTrack）以及对音频的实时处理（如会说话的汤姆猫、语音）
	优点：语音的实时处理，可以用代码实现各种音频的封装
	缺点：输出是PCM语音数据，如果保存成音频文件，是不能够被播放器播放的，所以必须先写代码实现数据编码以及压缩
	示例：使用AudioRecord类录音，并实现WAV格式封装。录音20s，输出的音频文件大概为3.5M左右（已写测试代码）
		主要api：audioRecord.startRecording()，audioRecord.read，audioRecord.stop()，audioRecord.release()
		开始录制
		int sampleRateInHz= 44100;  //44.1KHz,普遍使用的频率   
		int channelConfig = AudioFormat.CHANNEL_IN_STEREO;
		int audioFormat = AudioFormat.ENCODING_PCM_16BIT;
		 // 获得缓冲区字节大小  
        int bufferSizeInBytes = AudioRecord.getMinBufferSize(sampleRateInHz, channelConfig, audioFormat);
		int audioSource = MediaRecorder.AudioSource.MIC;
        // 创建AudioRecord对象  
        audioRecord = new AudioRecord(audioSource, sampleRateInHz, channelConfig, audioFormat, bufferSizeInBytes);
		audioRecord.startRecording();
		// 开启线程将音频流写入文件  
        new Thread(new AudioRecordThread()).start();  
		
		class AudioRecordThread implements Runnable {  
			@Override 
			public void run() {  
				writeDateTOFile();//往文件中写入裸数据  
				copyWaveFile(AudioName, NewAudioName);//给裸数据加上头文件  
			}  
		} 
		private void writeDateTOFile() {  
			// new一个byte数组用来存一些字节数据，大小为前面获得的缓冲区大小  
			byte[] audiodata = new byte[bufferSizeInBytes];  
			FileOutputStream fos = null;  
			int readsize = 0;  
			try {  
				File file = new File(AudioName);  //AudioName为sd卡根目录下test.raw
				if (file.exists()) {  
					file.delete();  
				}  
				fos = new FileOutputStream(file);// 建立一个可存取字节的文件  
			} catch (Exception e) {  
				e.printStackTrace();  
			}  
			while (isRecord == true) {  
				readsize = audioRecord.read(audiodata, 0, bufferSizeInBytes);  
				if (AudioRecord.ERROR_INVALID_OPERATION != readsize && fos != null) {  
					try {  
						fos.write(audiodata);  
					} catch (IOException e) {  
						e.printStackTrace();  
					}  
				}  
			}  
			try {
				if(fos != null)
					fos.close();// 关闭写入流  
			} catch (IOException e) {  
				e.printStackTrace();  
			}  
		} 
		private void copyWaveFile(String inFilename, String outFilename) {  
			FileInputStream in = null;  
			FileOutputStream out = null;  
			long totalAudioLen = 0;  
			long totalDataLen = totalAudioLen + 36;  //wave头44字节，36实在不懂
			long longSampleRate = sampleRateInHz;  //上面的44100
			int channels = 2;  
			long byteRate = 16 * sampleRateInHz * channels / 8;  
			byte[] data = new byte[bufferSizeInBytes];  
			try {  
				in = new FileInputStream(inFilename);  
				out = new FileOutputStream(outFilename);  
				totalAudioLen = in.getChannel().size();  
				totalDataLen = totalAudioLen + 36;  
				WriteWaveFileHeader(out, totalAudioLen, totalDataLen,  
						longSampleRate, channels, byteRate);  
				while (in.read(data) != -1) {  
					out.write(data);  
				}  
				in.close();  
				out.close();  
			} catch (FileNotFoundException e) {  
				e.printStackTrace();  
			} catch (IOException e) {  
				e.printStackTrace();  
			}  
		}  
		private void WriteWaveFileHeader(FileOutputStream out, long totalAudioLen,  
            long totalDataLen, long longSampleRate, int channels, long byteRate)  
            throws IOException {  
			byte[] header = new byte[44];  //wave文件头44字节
			header[0] = 'R'; // RIFF/WAVE header  
			header[1] = 'I';  
			header[2] = 'F';  
			header[3] = 'F';  
			header[4] = (byte) (totalDataLen & 0xff);  
			header[5] = (byte) ((totalDataLen >> 8) & 0xff);  
			header[6] = (byte) ((totalDataLen >> 16) & 0xff);  
			header[7] = (byte) ((totalDataLen >> 24) & 0xff);  
			header[8] = 'W';  
			header[9] = 'A';  
			header[10] = 'V';  
			header[11] = 'E';  
			header[12] = 'f'; // 'fmt ' chunk  
			header[13] = 'm';  
			header[14] = 't';  
			header[15] = ' ';  
			header[16] = 16; // 4 bytes: size of 'fmt ' chunk  
			header[17] = 0;  
			header[18] = 0;  
			header[19] = 0;  
			header[20] = 1; // format = 1  
			header[21] = 0;  
			header[22] = (byte) channels;  
			header[23] = 0;  
			header[24] = (byte) (longSampleRate & 0xff);  
			header[25] = (byte) ((longSampleRate >> 8) & 0xff);  
			header[26] = (byte) ((longSampleRate >> 16) & 0xff);  
			header[27] = (byte) ((longSampleRate >> 24) & 0xff);  
			header[28] = (byte) (byteRate & 0xff);  
			header[29] = (byte) ((byteRate >> 8) & 0xff);  
			header[30] = (byte) ((byteRate >> 16) & 0xff);  
			header[31] = (byte) ((byteRate >> 24) & 0xff);  
			header[32] = (byte) (2 * 16 / 8); // block align  
			header[33] = 0;  
			header[34] = 16; // bits per sample  
			header[35] = 0;  
			header[36] = 'd';  
			header[37] = 'a';  
			header[38] = 't';  
			header[39] = 'a';  
			header[40] = (byte) (totalAudioLen & 0xff);  
			header[41] = (byte) ((totalAudioLen >> 8) & 0xff);  
			header[42] = (byte) ((totalAudioLen >> 16) & 0xff);  
			header[43] = (byte) ((totalAudioLen >> 24) & 0xff);  
			out.write(header, 0, 44);  
		} 
		停止录制
		audioRecord.stop();  
		audioRecord.release();//释放资源  
		audioRecord = null;  

## MediaRecorder ##
	已经集成了录音、录像、编码、压缩等，支持少量的录音音频格式，大概有.aac（API = 16以上） .amr .3gp
	优点：大部分已经集成，直接调用相关接口即可，代码量小
	缺点：无法实时处理音频；输出的音频格式不是很多，例如没有输出mp3格式文件
	示例：使用MediaRecorder类录音，输出amr格式文件。录音20s，输出的音频文件大概为33K（已写测试代码）
		开始录制
		mRecorder = new MediaRecorder();
		mRecorder.setAudioSource(MediaRecorder.AudioSource.MIC);
		mRecorder.setOutputFormat(MediaRecorder.OutputFormat.DEFAULT);//Android默认就是amr
		mRecorder.setAudioEncoder(MediaRecorder.AudioEncoder.DEFAULT);
		mRecorder.setOutputFile(outputFilePath);
		try {
			mRecorder.prepare();
		} catch (Exception e) {
			e.printStackTrace();
		} 
		mRecorder.start();
		停止录制
		mRecorder.stop();
		mRecorder.release();
		mRecorder = null;
		
		开始播放
		mPlayer = new MediaPlayer();
		try {
			mPlayer.setDataSource(fileName);
			mPlayer.prepare();
			mPlayer.start();
		} catch (IOException e) {
			e.printStackTrace();
		}
		停止播放
		mPlayer.stop();
		mPlayer.release();
		mPlayer = null;

# 播放

## MediaPlayer音频视频播放 ##

MediaPlayer支持：AAC、AMR、FLAC、MP3、MIDI、OGG、PCM、WAV等格式 

资源占用量较高、延迟时间较长、不支持多个音频同时播放等

### 简单示例 ###

	public void startPlay(String fileName) {
		mPlayer = new MediaPlayer();
		try {
			mPlayer.setDataSource(fileName);
			mPlayer.prepare();
			mPlayer.start();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public void stopPlay() {
		mPlayer.stop();
		mPlayer.release();
		mPlayer = null;
	}

### 使用 ###

	MediaPlayer 的使用介绍（翻译官方文档，详细） http://blog.csdn.net/songshizhuyuan/article/details/32900965

#### MediaPlayer ####

    这个类包含用于播放声音和视频的主要API
    
Raw下的元数据

	//直接创建，不需要设置setDataSource
	mMediaPlayer=MediaPlayer.create(this, R.raw.audio);
	mMediaPlayer.start();

#### AudioManager ####

	这个类用于管理音源，并在设备上的音频输出。

#### 处理音频焦点 ####

音频焦点是合作性。也就是说，应用程序应该尽量配合，以符合音频焦点的指引，但规则不是由系统执行。如果应用程序失去音讯焦点后，大声播放音乐，系统也不会阻止。

	http://blog.csdn.net/dadoneo/article/details/8252933

AudioFocus的申请与释放
	
安卓2.2(api8)开始 新增 `AudioManager.requestAudioFocus（）`

AudioFocus被抢占与重新获得

	http://www.android100.org/html/201510/08/188724.html



#### 外放、听筒、耳机 模式切换 ####

	AudioManager audioManager = (AudioManager) this.getSystemService(Context.AUDIO_SERVICE);
	audioManager.setMicrophoneMute(false);
	audioManager.setSpeakerphoneOn(true);//使用扬声器外放，即使已经插入耳机
	audioManager.setMode(AudioManager.STREAM_MUSIC);
	
## SoundPool

支持多个音频文件同时播放(组合音频也是有上限的)，延时短，比较适合短促、密集的场景，是游戏开发中音效播放的福音。

`SoundPool(int maxStreams, int streamType, int srcQuality)`

区分2个概念
 
1. soundID：加载音乐资源时的返回值，int load(String path, int priority),这个int返回值就是soundID 
2. streamID：播放时返回的值，即play()方法的返回值

这两个值都很重要，需要缓存下来

某些采样频率会导致播放错误(不能播放，只能播放部分)

## AsyncPlayer

AsyncPlayer就是对MediaPlayer的一次简单的封装，对MediaPlaer所有的操作都在新开线程中执行。不影响调用线程任何操作。

AsyncPlayer只适合简单的异步播放，不能控制进度，只能开始或停止播放。如果再次调用play()方法，AsyncPlayer会停止当前播放，开始新的播放。

## AudioTrack播放音频

AudioTrack属于更偏底层的音频播放，MediaPlayerService的内部就是使用了AudioTrack。

AudioTrack用于单个音频播放和管理，相比于MediaPlayer具有：精炼、高效的优点。

更适合实时产生播放数据的情况，如加密的音频，
MediaPlayer是束手无策的，AudioTrack却可以。

AudioTrack用于播放PCM(PCM无压缩的音频格式)音乐流的回放，
如果需要播放其它格式音频，需要响应的解码器，
这也是AudioTrack用的比较少的原因，需要自己解码音频。

### AudioTreack的2种播放模式

#### 静态模式—static

数据一次性交付给接收方。好处是简单高效，只需要进行一次操作就完成了数据的传递;缺点当然也很明显，对于数据量较大的音频回放，显然它是无法胜任的，因而通常只用于播放铃声、系统提醒等对内存小的操作

#### 流模式streaming

流模式和网络上播放视频是类似的，即数据是按照一定规律不断地传递给接收方的。理论上它可用于任何音频播放的场景，不过我们一般在以下情况下采用：

- 音频文件过大

- 音频属性要求高，比如采样率高、深度大的数据

- 音频数据是实时产生的，这种情况就只能用流模式了

通过write(byte[], int, int), write(short[], int, int)
write(float[], int, int, int)等方法推送解码数据到AudioTrack

## Ringtone和RingtoneManager

Ringtone为铃声、通知和其他类似声音提供快速播放的方法

RingtoneManager提供系统铃声列表检索方法，Ringtone实例需要从RingtoneManager获取

### RingtoneManager

```java
1. // 两个构造方法
RingtoneManager(Activity activity)
RingtoneManager(Context context)

2. // 获取指定声音类型(铃声、通知、闹铃等)的默认声音的Uri
static Uri getDefaultUri(int type)

3. // 获取系统所有Ringtone的cursor
Cursor getCursor()

4. // 获取cursor指定位置的Ringtone uri
Uri getRingtoneUri(int position)

5. // 判断指定Uri是否为默认铃声
static boolean isDefault(Uri ringtoneUri)

6. //获取指定uri的所属类型
static int getDefaultType(Uri defaultRingtoneUri)

7. //将指定Uri设置为指定声音类型的默认声音
static void setActualDefaultRingtoneUri(Context context, int type, Uri ringtoneUri)
```

## JetPlayer播放音频

用于播放 ”.jet”文件

JET常用于控制游戏的声音特效，采用MIDI（Musical Instrument Digital Interface）格式。

## 总结

	对于延迟度要求不高，并且希望能够更全面的控制音乐的播放，MediaPlayer比较适合
	
	声音短小，延迟度小，并且需要几种声音同时播放的场景，适合使用SoundPool
	
	对于简单的播放，不需要复杂控制的播放，可以给使用AsyncPlayer，所有操作均在子线程不阻塞UI
	
	播放大文件音乐，如WAV无损音频和PCM无压缩音频，可使用更底层的播放方式AudioTrack。它支持流式播放，可以读取(可来自本地和网络)音频流，却播放延迟较小。 
	ps：据我测试AudioTrack直接支持WAV和PCM，其他音频需要解码成PCM格式才能播放。(其他无损格式没有尝试，有兴趣可以使本文提供的例子测试一下)
	
	.jet的音频比较少见(有的游戏中在使用)，可使用专门的播放器JetPlayer播放
	
	对于系统类声音的播放和操作，Ringtone更适合(RingtoneManager)



	
