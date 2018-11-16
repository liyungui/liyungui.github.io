---
title: AndroidStudio在Mac端使用
date: 2018-11-06 18:40:53
tags: 
	- Android
	- AndroidStudio
---

# Java安装

## Java目录

`/System/Libray/Frameworks/JavaVM.Framwork/Versions`目录下是已经安装了的不同版本的jdk。

![](http://upload-images.jianshu.io/upload_images/1814304-771fec34bb725b50.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

`/Library/Java/JavaVirtualMachines`目录下是已经安装了的不同版本的jdk。

# AndroidStudio3无法打开Android device monitor

首先提示安装 jdk 6

	直接点更多信息跳转安装即可

再次打开，报错

![](http://upload-images.jianshu.io/upload_images/1814304-9eda3efb3c659f0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

	安装 jdk8

打开，发现白屏

	发现安装的是jdk1.8.0_191
	降到 jdk1.8.0_144
		要删除较高版本的jdk，因为它会默认使用较高版本的。
		需要重启，source只能让环境变量对当前线程生效
	搞定




