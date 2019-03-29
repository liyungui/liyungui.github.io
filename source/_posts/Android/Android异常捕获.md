---
title: Android 异常捕获
date: 2019-03-25 17:15:53
categories:
  - Android
tags:
  - Android
---

参考

- [安卓捕获RuntimeException,ANR,Native信号异常](https://www.jianshu.com/p/bb658019f97b)
- [Android端线上NativeCrash收集的两种方法(上)](https://blog.csdn.net/yeyuwuhen1203/article/details/73556813)

# Java crash

Uncaught异常发生时会终止线程，调用 `UncaughtExceptionHandler.uncaughtException()`

如果该handler没有被显式设置，则会调用对应线程组的默认handler。
    
`Thread.setDefaultUncaughtExceptionHandler(myCrashHandler);`
        
# ANR

收听ANR的广播 `String ACTION_ANR = "android.intent.action.ANR"`

# NativeCrash

Native崩溃日志存储在手机的 `/data/tombstones` 目录下，需要root权限

# 三方 

## buglyg 

Java crash 和 ANR

# google-breakpad

NativeCrash