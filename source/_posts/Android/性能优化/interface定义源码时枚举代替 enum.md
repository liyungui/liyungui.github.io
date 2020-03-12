---
title: interface定义源码时枚举代替 enum
date: 2019-03-01 14:10:53
categories:
  - Android
tags:
  - 性能优化
---

[@interface定义源码时枚举代替 enum](http://caimuhao.com/2017/03/31/Avoid-Used-Enum/)

# 使用 Enum 的缺点 #

每一个枚举值都是一个对象

Enum 会增加 DEX 文件的大小,会造成运行时更多的开销（比常量多5到10倍的内存占用）

一些旧设备(<=2.2),一些性能问题就是由于 Enum 引起的

	public enum Season {
		WINTER, SPRING, SUMMER, FALL 
	}

# TypeDef #

Android 提供了 **TypeDef** 注解库,这个注解确保特定的参数,返回值,或者变量引用为一个指定的集合范围

## 使用 ##

依赖

	dependencies { 
		compile ‘com.android.support:support-annotations:24.2.0’ 
	}

声明 `@IntDef` 常量

	// Constants
	public static final int WINTER = 0;
	public static final int SPRING = 1;
	public static final int SUMMER = 2;
	public static final int FALL = 3;

	// Declare the @IntDef for these constants
	@IntDef({WINTER, SPRING, SUMMER, FALL})
	@Retention(RetentionPolicy.SOURCE)
	public @interface Season {
    }

	//使用定义的注解
	public AnnotationSeason(@Season int season) {
        System.out.println("Season :" + season);
    }

