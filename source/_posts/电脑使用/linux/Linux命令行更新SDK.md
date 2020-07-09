---
title: Linux命令行更新SDK
date: 2018-08-31 18:22:53
tags: 
	- Android
---

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
	