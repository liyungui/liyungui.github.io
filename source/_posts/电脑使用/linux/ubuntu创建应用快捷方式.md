---
title: Ubuntu创建应用快捷方式
date: 2018-12-20 09:07:53
categories:
  - 电脑使用
tags:
  - Linux
---
	sudo vim /usr/share/applications/Studio.desktop

内容如下：

	[Desktop Entry]
	Name = Studio
	Comment= android studio
	Exec=/home/lyg/android-studio/bin/studio.sh //应用路径
	Icon=/home/lyg/android-studio/bin/studio.png //图标路径
	Terminal=false
	Type=Application
**特别注意：**

- 文件内容每行都不允许有空格
	- 有空格不是有效的桌面快捷方式
		- 双击，会报 `应用启动出错`
		- 软件中心找不到该快捷方式
		- 无法拖到Laugh，拖过去会回弹
