---
title: gikdbg动态调试dex和so工具使用
date: 2019-12-06 13:41:53
categories:
  - 逆向
tags:
	- 逆向
---
	
	官网下载 gikdbg.art
	唯一4.4.2版本，root，开启art模式，可以调试dex和so库
	
运行模拟器

打开gikdbg.art.exe，执行ART Debug -- server -- adb device 选择设备，双击， 连接到设备

第一次连接到该远程设备，会提示安装gikdbg.apk（位于artserver目录下）
	也可以自己手动安装
	
设备上运行需要调试的apk

ART Debug -- file -- attach 选择进程，双击，进入该进程

ART Debug -- view -- module（alt + m）打开模块，选择要调试的dex或so模块，双击，进入到该模块

右键--search--function 搜索函数，断点，运行（f9必须快捷键）

发现断不下来（不知道是因为没找对函数地址还是真的断不下来。看不懂arm汇编码）