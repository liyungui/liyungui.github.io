---
title: xposed脱壳
date: 2020-07-22 17:40:53
categories:
  - 逆向
tags:
	- 逆向
---

# FDex2

[FDex2](https://bbs.pediy.com/thread-224105.htm) 支持 安卓4.4以上

## 原理

Hook `ClassLoader.loadClass()`，反射调用getDex()取得com.android.dex.Dex对象，再将里面的dex写出

# dumpDex

[dumpDex](https://github.com/WrBug/dumpDex)，一个开源的 Android 脱壳插件工具

支持市面上大多数**加密壳**(腾讯乐固、360加固、爱加密、梆梆加固、百度加固)

## 使用教程

- 安装 dumpDex.apk
- 拷贝so库
	- `lib/armeabi-v7a/libnativeDump.so` 复制到 `/data/local/tmp/libnativeDump.so`
- 设置so库权限为777
	- 命令 `chmod 777 /data/local/tmp/libnativeDump.so`
- 应用xposed模块
- 重启
- 运行加固的应用
- 插件会自动将dex文件dump到 `/data/data/包名/dump` 目录
	- 会有很多dex；需要花点时间筛查

## 可能遇到的问题

### 无法找到`libnativeDump64.so`

根据xposed日志报错，说明当前是64位的cpu，直接把so库重命名即可

### map segment权限问题

报错日志

```
java.lang.UnsatisfiedLinkError: dlopen failed: couldn't map "/data/local/tmp/libnativeDump64.so" 
segment 1: Permission denied
```

解决方案

```
1. adb shell
2. su
3. getenforce  这时候输出是Enforcing
4.setenforce 0
5.getenforce  这时候输出是Permissive 
```

## 脱壳原理

- 检测当前运行的 APP 是否存在 dumpDex 支持的加密壳
- 存在则进行脱壳
	- Android 8.0 及以上手机走 NDK 方式
	- 低版本手机则走 Hook 方式；
		- Hook `android.app.Instrumentation.newApplication()`
			- 加固壳用自定义Application加载原Application
		- Hook `ClassLoader.loadClass()`
			- 加固壳加载原启动Activity  
- 脱壳后的 dex 文件存放到 APP 所在路径的 dump 子文件夹里

## 优化方向

仅当加载的 Application 或 Activity 为当前运行的 APP 类时才进行 dex 的导出。

这样可以减少生成的 dex 文件数。

# 参考&扩展

- [dumpDex 脱壳原理](http://liteng1220.com/blog/articles/dumpdex-principle/)
- [Android逆向之路---脱壳360加固原理解析](https://juejin.im/post/5c1934226fb9a04a0b221c3c) 更加详细的dumpDex 脱壳原理