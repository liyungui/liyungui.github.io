---
title: Linux命令行更新SDK
date: 2018-08-31 18:22:53
tags: 
	- Android
---

# android

只能更新SDK；无法安装更新ndk，cmake等

	cd ~/android-sdk-linux/tools/
	./android list sdk --extended
		输出
			Packages available for installation or update: 11
			----------
			id: 1 or "android-28"
			     Type: Platform
			     Desc: Android SDK Platform 28
			           Revision 6
			----------
			id: 2 or "android-27"
			     Type: Platform
			     Desc: Android SDK Platform 27
			           Revision 3
	./android update sdk -u -f --filter android-27
	
# sdkmanager

sdkmanager命令行工具 可以查看、安装、更新、卸载 Android SDK 的软件包

位置 `{Android_SDK}/tools/bin/`

	列出所有 已安装的包、有效的包 和 可以更新包
	sdkmanager --list 
	
	安装多个包(包名就是list命令查询出来的Path)
	sdkmanager "build-tools;28.0.3" "platforms;android-28" 
	
	sdkmanager --update 更新所有已安装的软件包；也可指定包名
	
	卸载多个包
	sdkmanager --uninstall "build-tools;28.0.0" "platforms;android-26"
# 参考&扩展

- [sdkmanager 命令行工具的使用](https://blog.csdn.net/xietansheng/article/details/85092056)
	