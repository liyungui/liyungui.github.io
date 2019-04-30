---
title: RN稳定性优化-升级JavaScriptCore版本
date: 2019-03-08 11:14:26
categories:
	- Android
tags:
	- RN
---

# 目的

解决RN的 libjsc.so 相关报错引起的崩溃

携程技术中心的文章 [《干货 | 近万字长文详述携程大规模应用RN的工程化实践》](https://mp.weixin.qq.com/s/Z1GUJW3qBqDGH1jnGt5qAg) 提到

```
这是由于RN自带的JavaScriptCore版本为2014年的版本，
兼容性和稳定性较差，
建议参考开源的jsc-android-buildscrips项目，
将JavaScriptCore升级到2017年11月的版本(WebkitGTK Revision 225067)，
我们升级到该版本后，发现该错误降低了90%；
```

# jsc-android-buildscripts

[github](https://github.com/react-native-community/jsc-android-buildscripts)

[npm](https://www.npmjs.com/package/jsc-android)

目前，最新的稳定版本为 **236355.1.1**

## 在RN项目中使用

1. `npm install jsc-android`
2. 添加本地maven的JSC依赖

		Android工程根目录/build.gradle
			allprojects {
    			repositories {
    				maven {
			            // All of React Native (JS, Obj-C sources, Android binaries) is installed from npm
			            url "$rootDir/node_modules/react-native/android"
			        }
			        maven {
			            // Local Maven repo containing AARs with JSC library built for Android
			            url "$rootDir/node_modules/jsc-android/dist"
			        }
			        
3. 强制指定JSC版本(覆盖[RN默认的版本](https://github.com/facebook/react-native/blob/e8df8d9fd579ff14224cacdb816f9ff07eef978d/ReactAndroid/build.gradle#L289))

		app/build.gradle
			android {
				configurations.all {
					resolutionStrategy{
		            force 'org.webkit:android-jsc:r236355'
		        }
		        
### 如何验证是否成功使用新版本的JSC

加载过程会在logcat 输出 JSC版本，过滤tag为 `JavaScriptCore.Version`。

实例日志如下：

    D/JavaScriptCore.Version: 236355.1.0
    
### 可能遇到的问题

Compile errors of the sort:

	More than one file was found with OS independent path 'lib/armeabi-v7a/libgnustl_shared.so'
	
Add the following to your app/build.gradle, under android:

	packagingOptions {
	    pickFirst '**/libgnustl_shared.so'
	}		
