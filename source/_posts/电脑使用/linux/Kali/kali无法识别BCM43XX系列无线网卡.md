---
title: kali无法识别BCM43XX系列无线网卡
date: 2018-12-20 09:13:53
categories:
  - 电脑使用
tags:
  - Linux
---


打开终端，输入
cat /etc/apt/sources.list

看看里面有没有一下三行kali官方源的地址（如果是断网安装，kali的默认源可能不会写入到这个文件里），
如果没有，请在/etc/apt/sources.list中入这三行。
deb http://http.kali.org/kali kali main non-free contrib
deb-src http://http.kali.org/kali kali main non-free contrib
deb http://security.kali.org/kali-security kali/updates main contrib non-free
 
加入之后就可以对整个系统进行更新了，终端中输入：
apt-get update && apt-get dist-upgrade
 
解决kali无法识别BCM43XX系列无线网卡问题（我的博通 BCM 4312）
安装BCM43XX系列无线网卡驱动：
aptitude update && aptitude install wireless-toolsaptitude install firmware-b43-lpphy-installer
完成之后注销或者重启电脑，
在终端中输入 iwconfig 即可看到无线网卡已经识别

关于BCM43XX系列的无线网卡驱动请参考Debian官方文档：
http://wiki.debian.org/bcm43xx
老的博通系列网卡可能需要 firmware-b43legacy-installer 安装包
