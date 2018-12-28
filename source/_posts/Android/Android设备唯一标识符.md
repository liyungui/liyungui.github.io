---
title: Android设备唯一标识符
date: 2018-12-06 17:18:53
tags: 
	- Android
---

# 常用的获取设备唯一标识符的方法

- **IMEI** International Mobile Equipment Identity 
	- 无插卡模块的设备无法获取。如pad
	- 需要用户授权。获取Android 6 开始动态权限获取
- **SIM Serial Num**
	- 对应 SIM卡。不插卡时无法获取， CDMA卡支持不充分
- **Mac** Media Access Control Address
	- 网卡地址
	- 手机必须具有上网功能
	- Android6.0 运行时权限修改geMacAddress()返回的mac地址永远是一样的， 但是可以其他途径获取。 
	- 属于Android系统的保护信息，高版本系统获取的话容易失败，返回0000000
- **ANDROID_ID**
	- 设备首次运行(恢复出厂设置)，系统会随机生成一64位的数字(16进制保存)
	- 部分定制ROM bug，所有设备都一样
	- `Settings.System.getString(getContentResolver(), Settings.System.ANDROID_ID); `
- **DEVICE_ID**
	- 根据不同的手机设备返回IMEI，MEID或者ESN码
	- 非手机设备(没有通话硬件，如Wifi设备，TV，音乐播放器)没有
	- 需要用户授权。获取Android 6 开始动态权限获取DEVICE_ID 
	- 部分定制ROM bug，所有设备都一样
	- `((TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE)).getDeviceId();`
- **Serial Number** 设备序列号 
	- 部分定制ROM bug。比如比如红米手机返回的就是连续的非随机数	- `android.os.Build.SERIAL` 
- **UniquePsuedoID**
	- 硬件信息拼装而成
- **Installtion ID**
	- 程序首次运行时生成一个ID。重装会变化，常用来跟踪应用安装量

# 方案一

ANDROID_ID 拼接 	Serial Number。不需要权限

	String androidID = Settings.Secure.getString(context.getContentResolver(), Settings.Secure.ANDROID_ID);
    String id = androidID + Build.SERIAL;
