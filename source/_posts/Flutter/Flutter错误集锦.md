---
title: Flutter错误集锦
date: 2018-12-16 11:18:29
tags:
	- Flutter
---

# 下载依赖失败
`flutter doctor` `flutter packages get`等，下载依赖卡住，没进度

解决方案：使用镜像

[官方解决方案](https://github.com/flutter/flutter/wiki/Using-Flutter-in-China)

	export PUB_HOSTED_URL=https://pub.flutter-io.cn
	
	export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn

# Waiting for another flutter command to release the startup lock

项目异常关闭，或者android studio用任务管理器强制关闭

`rm ./flutter/bin/cache/lockfile`