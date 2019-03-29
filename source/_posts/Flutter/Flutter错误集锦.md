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

# 找不到设备/设备视图消失

Android Studio 3.0.1 的flutter项目找不到设备 - no connected device

仔细观察，发现as顶部工具栏的右边少了设备框【Flutter Device Selection】

{% asset_img 找不到设备.png %}

仔细回想了一下，刚刚添加了一个images目录，并且修改了pubspec.yaml文件。检查发现assets的缩进弄错了。把缩进改成2个空格后，设备框就出现了。

由此可见，as对pubspec.yaml文件十分敏感