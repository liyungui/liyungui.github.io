---
title: RTSP推流库源码分析
date: 2020-04-02 14:52:14
categories:
  - 直播
tags:
  - 直播
---
# libstreaming 和 Endoscope

Endoscope 使用libstreaming实现Android推流直播

libstreaming 不是gradle项目，是古老的ant 脚本编译

Android使用的话，建议直接使用 Endoscope

# libstreaming 原理

## 获取视频编码数据的三种方式

- **MediaRecorder** API and a simple hack.
	- 并非为了实时推流设计的
	- 关键：
		- 使用 `LocalSocket` 代替常规的文件。
		- 安全原因，Android 5.0 开始禁用LocalSocket，用 `ParcelFileDescriptor` 代替
	- 缺陷：
		- 音画同步不精确
		- MediaRecorder internal buffers 导致卡顿
- **MediaCodec** API and the buffer-to-buffer method
	- requires Android 4.1.
	- 关键：
		- `dequeueInputBuffer` and `queueInputBuffer`
	- 缺陷：
		- color formats 各不相同，需要做兼容
- **MediaCodec** API and the surface-to-buffer method 
	- requires Android 4.3.
	- 关键：
		- `createInputSurface`

libstreaming 默认使用方法2，预览使用的Surface，所以不支持后台采集和息屏采集（会中断）

libstreaming 的方法3，有缺陷：结束采集时会产生 Native崩溃

{% asset_img 类图.png %}

{% asset_img 时序图.png %}

# 参考&扩展

- [libstreaming github](https://github.com/fyhertz/libstreaming)
- [Endoscope github](https://github.com/hypeapps/Endoscope) 使用libstreaming实现Android推流直播
- [libstreaming局域网构建Android相机实时流媒体流程分析](https://blog.csdn.net/asahinokawa/article/details/80500098?utm_medium=distribute.pc_relevant.none-task-blog-baidujs_title-2&spm=1001.2101.3001.4242) 源码分析
