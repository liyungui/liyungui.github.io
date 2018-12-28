---
title: Linux U盘启动制作
date: 2018-12-20 08:58:53
categories:
  - 电脑使用
tags:
  - Linux
---
# 启动盘制作工具 #

主要的功能就是将系统ISO写到U盘

**Universal-USB-Installer**

**Unetbootin**

将Liux操作系统ISO写到U盘

有Windows版和Linux版

Unetbootin-windows

**ULtraISO**

还能修复MBR。有些U盘无法启动(黑屏光标一闪一闪)就是因为MBR问题

**Win32 Disk Imager**

Windows平台兼容性更强。

Kali 2.17.3 镜像用ULtraISO写到U盘在一台计算机上能启动，在另外一台计算机启动报 `Failed to load ldlinux.c32` 错误

# 制作方法 #

CDlinux 为例，Ubuntu，Kali 都一样

需要的软件有：ULtraISO, Unetbootin-windows-latest

需要的硬件有: 一个1GB以上的U盘，（先格式化为F32格式))，并检测是否带有MBR扇区（没有则无法启动）

需要的镜像有：CDlinux0.9.7.1_SSE.ISO

1. FAT32格式化U盘，快速格式化。
2. 写入CDlinux ISO 到U盘
	1. 启动Unetbootin-windows-latest
	2. 磁盘镜像选择CDlinux ISO文件
	3. 驱动器选择U盘。
	4. 点击确定按钮就开始制作。
	5. 制作完成，选择“退出”按钮
3. 配置 syslinux.cfg文件(非必须)

		default vesamenu.c32
		prompt 0
		menu title Please select the startup mode--Jack
		timeout 100
		
		label unetbootindefault
		menu label Default Chinese
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=zh_CN.UTF-8
		
		label unetbootindefault
		menu label Default No Parameters Mode
		kernel /ubnkern
		append initrd=/ubninit 
		
		label ubnentry0
		menu label Safe Graphics Mode
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_SAFEG=yes
		
		label ubnentry1
		menu label (de_DE) Deutsch
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=de_DE.UTF-8
		
		label ubnentry2
		menu label (en_CA) English
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=en_CA.UTF-8
		
		label ubnentry3
		menu label (en_GB) English
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=en_GB.UTF-8
		
		label ubnentry4
		menu label (en_US) English
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=en_US.UTF-8
		
		label ubnentry5
		menu label (fr_CA) French
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=fr_CA.UTF-8
		
		label ubnentry6
		menu label (fr_CH) French
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=fr_CH.UTF-8
		
		label ubnentry7
		menu label (fr_FR) French
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=fr_FR.UTF-8
		
		label ubnentry8
		menu label (ja_JP) Japanese
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=ja_JP.UTF-8
		
		label ubnentry9
		menu label (ko_KR) Korean
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=ko_KR.UTF-8
		
		label ubnentry10
		menu label (ru_RU) Russian
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=ru_RU.UTF-8
		
		label ubnentry11
		menu label (zh_CN) Chinese
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=zh_CN.UTF-8
		
		label ubnentry12
		menu label (zh_TW) Chinese
		kernel /CDlinux/bzImage
		append initrd=/CDlinux/initrd quiet CDL_LANG=zh_TW.UTF-8
		
		label ubnentry13
		menu label MemTest86+:  a thorough, stand alone memory tester for x86
		kernel /CDlinux/boot/memtest.bin.gz
		append initrd=/ubninit

4. 写入 MBR扇区((非必须))

	没有MBR扇区就无法启动。启动后黑屏，只有一个光标在最左上角一闪一闪

	UltraISO V9.2起包含制作启动U盘的功能

	1. 打开ULtraISO软件
	2. 点击“启动”菜单，选择“写入硬盘镜像...”
	3. 硬盘驱动器选择U盘的盘符
	4. 点击便捷启动-->写入新的硬盘主引导记录(MBR)-->USB-HDD+

5.重启电脑，选择USB启动

# 隐藏U盘的CDLinux系统 #

## 文件属性设置为隐藏 ##

制作完启动盘后,把所有的CDLinux文件属性设置为隐藏掉

## 制作一个隐藏分区，把CDLinux装在隐藏分区中 ##

想法是这样的：

- 用ULtraISO制作U盘启动CDLinux，ULtraISO只是机械的把CDlinux0.9.7.1_SSE.iso中的文件拷贝到U盘里，并没有产生其他的文件
- 利用这个功能，把可以正常启动进入CDLinux的U盘，重新刻录到U盘

制作步骤：

- 使用ULtraISO把我们已经制作成功的启动CDLinuxU盘所有文件，制作成一个ISO文件
- 用ULtraISO把这个ISO文件写入到U盘的隐藏分区
	- 点击“启动”菜单，选择“写入硬盘镜像...”
	- 选择硬盘驱动器和映像文件
	- 在隐藏启动分区选择“隐藏”
	- 点击“格式化”选择格式化保证U盘比较干净
	- 点击“写入”按钮
	- 等待完成并退出。再次重启，可以正常启动进入CDLinux系统
