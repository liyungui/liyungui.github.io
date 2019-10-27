---
title: NDK开发
date: 2019-10-24 11:08:53
tags: 
	- NDK
categories:
	- Android
---

# 背景

android的ndk开发一直被认为是很痛苦的一件事情，除了android程序员对c++的陌生外，还有一个主要原因是Android开发IDE对NDK开发支持度不如c++的IDE完善（代码提示补全，断点调试）。

# NDK开发环境支持

AS 2.2 开始支持NDK开发与断点调试

下载并安装 LLDB、Cmake、NDK三个工具

- 打开"SDK Manager"
- 右边选项卡选择"SDK Tools"
- 勾选 "CMake"、"LLDB"、"NDK"这3项，下载安装

# 创建NDK项目

AS 3.3之前，新建一个Android项目，勾选"Include C++ support”

AS 3.3及以上，新建项目时选择 "Native C++" 模板即可创建NDK项目

# 构建方式

AS 其实是支持 `ndk-build`（Android老构建方式） 和 `cmake`（官方推荐，通用跨平台编译方案） 两种构建方式的

# 调试

两种调试方式

- debug模式运行
- 运行，attach进程，选 "auto"，即可支持NDK断点调试

**特别注意**：部分华为手机无法支持NDK断点调试，错误如下

`failed to set breakpoint site at 0x759cbac688 for breakpoint 2.1: error: 0 sending the breakpoint request`