---
title: adb logcat 使用
date: 2019-12-06 13:41:53
categories:
  - 逆向
tags:
	- 逆向
---

logcat [options] [filterspecs]

**options include:**

	-s	Set default filter to silent.Like specifying filterspec '*:s'

**filterspecs**

	V    Verbose
	D    Debug
	I    Info
	W    Warn
	E    Error
	F    Fatal
	S    Silent (supress all output)



1. 查看warning以上的log

	adb logcat *:w

2. 过滤查看dalvikvm标签的log

	logcat的过滤方式有点儿怪异，要设定为silent,在此基础上设置的tag过滤才成功。
	
	adb logcat -s dalvikvm 或者 adb logcat dalvikvm *:s 或者 adb logcat -s dalvikvm:D

	结果如下 D/dalvikvm( 257): GC freed 1191 objects / 343344 bytes in 65ms

3. 过滤多个app 的log

	adb logcat -s dalvikvm vold

4. 过滤exception栈

	new Exception("lyg").printStackTrace(); tag是System.err 级别为Warn
	
	adb logcat -s System.err：W

5. log保存到文件

	adb logcat > 1.txt (">"是windows用的数据流导向符号）