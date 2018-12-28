---
title: VMware10安装Mac10.9系统
date: 2018-12-20 10:46:53
categories:
  - 电脑使用
tags:
  - Mac
  - VMware10
---

## vmware10 安装mac10.9系统 ##

开始下载了一个mac10.10 的iso格式镜像，发现vmware10最高支持mac10.9，强装也是失败。

	超详细VMware Workstation 10安装OS X Mavericks http://www.oschina.net/question/1039213_158319?fromerr=KYsGXefA


一路下一步，选择磁盘步骤，点击mac的磁盘工具，选择磁盘，分区，完毕，退出磁盘工具，选择刚才分区的磁盘，下一步。

键盘布局选择 中文-简体

传输信息到这台mac 选择 不传输任何信息

Apple id登录 选择 不登录跳过

## 安装darwin6.iso 实现拖拽文件和自动适应分辨率 ##

关机，虚拟机--cd/dvd--设置 选择 D:\down\darwin6.iso

开机，桌面双击 VMware tools，安装


## VMsvga2_v1.2.5_OS_10.6-10.8.pkg 的作用： ##

要观看优酷之类在线视频或玩小游戏得安装vm显卡驱动VMsvga2_Docs

安装此驱动会出现不能自动适应分辨率 ，分辨率 要手动调整

但显示dock图标滑动比较流畅