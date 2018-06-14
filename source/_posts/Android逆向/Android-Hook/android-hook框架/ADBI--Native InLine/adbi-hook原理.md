---
title: adbi hook原理
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[Android平台下hook框架adbi的研究（下） ](http://blog.csdn.net/roland_sun/article/details/36049307)

# native函数hook原理 #

**native函数hook要解决两个问题**

1. 找到这个函数在内存中的位置
2. 修改函数偷梁换柱。

读取“/proc/<进程号>/maps”内存映射文件，找到函数库的起始位置和路径。

mprotect()为该库内存段加上可写（PROT_WRITE）属性

打开库文件，解析出符号表，从符号表中找到目标函数（其后是偏移地址，加上库起始地址就是内存地址），接下来就是判断Arm与Thumb指令集，hook了。