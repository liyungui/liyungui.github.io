---
title: Media Playback
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# Handling audio focus #

android 2.2(API 8) 开始引入 `audio focus`协作机制 来管理音频播放

## `audio focus`协作机制 ##

- 获得焦点，播放
- 失去焦点，停止/暂停播放
- 仅是建议协作，以获得更好用户体验；但非强制，有的APP可能不遵守

## 示例 ##

	public int AudioManager.requestAudioFocus(OnAudioFocusChangeListener listener, int streamType, int durationHint)

	public interface OnAudioFocusChangeListener {
		public void onAudioFocusChange(int focusChange);
	}
		
**the type of focus change**, one of 

- AUDIOFOCUS_GAIN  
- AUDIOFOCUS_LOSS
- AUDIOFOCUS_LOSS_TRANSIENT   短暂丢失
- AUDIOFOCUS_LOSS_TRANSIENT_CAN_DUCK  短暂丢失，你可以不停止播放，而是降低音量就可以

# Handle Changes in the Audio Output Hardware #
# Handling the AUDIO_BECOMING_NOISY Intent #

当蓝牙断开或耳机拔出，系统会自动使用扬声器播放，这在某些场景会造成噪音惊喜。万幸系统会发出 `ACTION_AUDIO_BECOMING_NOISY` 广播

	private class NoisyAudioStreamReceiver extends BroadcastReceiver {
	    @Override
	    public void onReceive(Context context, Intent intent) {
	        if (AudioManager.ACTION_AUDIO_BECOMING_NOISY.equals(intent.getAction())) {
	            // Pause the playback
	        }
	    }
	}
	
	private IntentFilter intentFilter = new IntentFilter(AudioManager.ACTION_AUDIO_BECOMING_NOISY);
	
	private void startPlayback() {
	    registerReceiver(myNoisyAudioStreamReceiver(), intentFilter);
	}
	
	private void stopPlayback() {
	    unregisterReceiver(myNoisyAudioStreamReceiver);
	}

