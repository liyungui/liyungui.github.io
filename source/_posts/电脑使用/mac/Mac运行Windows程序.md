---
title: Mac运行Windows程序
date: 2018-12-06 11:32:09
tags: Mac
---

# 可选方案

根据方便程度和难度，有以下四种

- CrossOver。 最简单。收费

- Wineskin。 难一些。免费，制作/移植为Mac程序

- 虚拟机。 耗资源

- 双系统。 需重启切换

# CrossOver使用

- 安装运行
- 创建容器
- 选择创建的容器
- 选择exe文件

# Wineskin使用

[下载安装](http://wineskin.urgesoftware.com)

安装Engines

update Wrapper Version

Create New Blank Wrapper 一路install，初始化完成

View wrapper in Finder，看APP 包的位置(/Users/‘用户名目录’/Applications/Wineskin)

右键显示包内容

把Windows程序所有文件拷贝到drive_c 目录下(右键，显示原身)

双击包内容根目录下的Wineskin.app开始配置程序 -- Advanced

	Windows Ext -- 选择刚才的exe文件
	Custom Commands -- 中填写export LANG=zh_CN.UTF-8 代表设置系统语言为中文
	Set Screen Option -- 关闭检测GPU，其他默认 -- Done
	Test Run -- 试运行 能够看到效果
	
如果出现乱码，说明没有下载中文字库。在配置中选择Tools 工具。Winetricks 配置基础环境。在字库中增加中文字库，选择fonts中的cjkfonts。选中后Run 即可
	


