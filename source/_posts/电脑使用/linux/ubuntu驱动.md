---
title: Ubuntu驱动
date: 2018-12-20 09:07:53
categories:
  - 电脑使用
tags:
  - Linux
---
# 是否已经成功安装显卡驱动 #

	sudo apt-get install mesa-utils  //安装mesa-utils
	glxinfo | grep rendering
	如果结果是“yes”，证明显卡 驱动已经成功安装。