---
title: 无法U盘启动-uefi-gpt
date: 2018-12-20 08:57:53
categories:
  - 电脑使用
tags:
  - U盘启动
---

现在新型的主板都是 UEFI Secure Boot启动（区别于传统的bios启动更快）

uefi + GPT磁盘格式 + win8，颠覆开机速度

这样是无法U盘启动的

要把uefi关闭（改回传统bios启动），磁盘改为mbr格式

	Security 选项卡 Secure Boot项 设为disable
	startup选项卡 UEFI/Legacy Boot项 设为Legacy Only 默认灰色 UEFI only，而且禁止修改
	main选项卡 UEFI Secure Boot 变为off 默认on
	保存退出，重启
	选择usb hdd 启动（Lenovo e431 按f12）
	pe系统中，使用DiskGenius分区软件重新格式化分区，转换分区表类型为MBR格式