---
title: jswat无源码动态调试
date: 2019-12-06 11:51:53
categories:
  - 逆向
tags:
	- 逆向
---

[Android 无源码动态调试](http://blog.csdn.net/douniwan5788/article/details/17657665) 

[jswat无源码动态调试](http://bbs.pediy.com/showthread.php?p=1277276) 

## rooadb + jswat(AndBug,jdb)  ##

Android无原码动态调试无敌了！ 

rootadb 可以以root启动adbd并使用其自带工具setpropex修改ro.debuggable = 1。（droid4x海马玩模拟器自带调试属性也可以）

jswat、andbug、jdb都是可以无源码调试java的debuger

1. jswat有GUI，java写的跨平台
2. AndBug Linux下编译比较方便，Windows要自己搭建mingw环境
3. jdb最强大。而且是jdk的一部分，免费且跨平台。命令行操作

		gdbserver在ndk目录下的prebuilt文件夹，选择对应cpu即可
		gdb是GNU开源组织发布的一个强大的UNIX下的程序调试工具。
		也可以自己下载编译，同时获得gdb的客户端和服务端。

链接

[rootadb下载](https://github.com/poliva/rootadb)
	
[jswat下载](https://drive.google.com/folderview?id=0B8-CbCFlTA3nOVhZREhIcXBvT2c&usp=sharing)
	
	google 编译好的版本：如果是windows建议下exe安装版本,jar安装版好像环境变量有点问题
		
[AndBug下载](https://github.com/swdunlop/AndBug)
	

## 附加进程 session--attach ##

附加进程有多中方式，下面是最常用的两种

1. attach by socket（默认）

	host： localhost

	port：运行端口。千万不要写调试端口（所有app调试端口默认8700，这样就会附加到第一个找到的进程上）

		android device monitor 设备/进程为空，先打开monitor，再打开模拟器可解决

2. attach to process
	process id填 pid。adb shell ps 可查到
	
## 窗口 ##

classes可以看到调用的所有类（混淆后的名字），可以直接展开在上面下类/方法断点

variables可以看到断点方法的变量

breakpoints可以查看所有断点

callstack 调用堆栈

debuggerConsole 控制台输出，包括断点、单步调用的方法过程（如果单步调试中的话）

## 断点 ##

### 方法断点 ###

	android.view.View.setOnClickListener(android.view.View$OnClickListener)断点
	package: android.view
	class: View
	method: setOnClickListener
	parameters: android.view.View$OnClickListener 参数不填也可以（系统补*表示任意参数类型）
