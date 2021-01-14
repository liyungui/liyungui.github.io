---
title: NDK开发常见错误
date: 2019-10-24 11:08:53
tags: 
	- NDK
categories:
	- Android
---

# UnsatisfiedLinkError 

加载so库失败。

有以下两种情况

## 找不到so库

一般会有详细的提示 `couldn't find "libijkffmpeg.so"`

- so库没有打包到apk
	- so库目录设置是否正确
- 没有找到相应CPU架构的so库
	- 做CPU架构兼容适配

## 找不到so库中Native方法

一般有类似提示 `java.lang.UnsatisfiedLinkError: JNI_ERR returned from JNI_OnLoad in "/data/app/com.zy.course-XnN_DSxaRUBhBSpsrZagAQ==/lib/arm/libijksdl.so`

- Java类包名是否正确
- 混淆规则是否正确


# 参考&扩展

- [UnsatisfiedLinkError](https://blog.csdn.net/ruizhenggang/article/details/97136813)