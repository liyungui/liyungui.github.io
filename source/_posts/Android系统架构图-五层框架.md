---
title: Android系统架构图(五层框架)
date: 2018-05-07 14:15:53
tags:
---

{% asset_img Android架构图(五层框架).png %}

- 蓝色：java程序
- 黄色：运行JAVA程序而实现的虚拟机
- 绿色：C/C++语言编写的程序库
- 红色：内核(linux内核+drvier)

Android系统架构(Android-System-Architecture)组成：

 - Linux内核层（Linux kernel）
 - 硬件抽象层（HAL, Hardware Abstraction Layer）
 - 运行时库层（Runtime）
 - 应用程序框架层（Application Framework）
 - 应用程序层（Application）
 
 # Linux内核层（Linux kernel） #
 
 Android基于Linux 2.6内核
 
 但是它与Linux之间还是有很大的差别，比如Android在Linux内核的基础上添加了自己所特有的驱动程序。
 
 Linux内核层提供核心系统服务，例如：安全、内存管理、进程管理、网络堆栈、驱动模型。
 
 # 硬件抽象层（HAL, Hardware Abstraction Layer） #
 
 为了保护一些硬件提供商的知识产权而提出的，是为了避开linux的GPL束缚。
 
 由于Linux遵循的是GPL协议，而Android开源项目基于Apache协议，意味着其下的所有驱动都应该开源，这一点对于部分厂商来说无法接受；
 
 思路是把控制硬件的动作都放到了Android HAL中，新架构、调整为 HAL stub 的观念 
 
 主要包含以下一些模块：Gps、Vibrator、Wifi、Copybit、Audio、Camera、Lights、Ril、Overlay等。 
 
 {% asset_img hal.png %}
 
 # 运行时库层（Android Runtime、Libraries） #
 
 Android Runtime主要提供了核心类库Libraries包含SQLite 库、C/C++库的集合等…… 还有Dalvik虚拟机。
 
 # 应用程序框架层（Application Framework） #
 
 应用程序框架层提供开发Android应用程序所需的一系列API；
 
 我们在开发应用时都是通过框架来与Android底层进行交互，接触最多的就是应用框架层了
 
 # 应用程序层（Application） #
 
 系统自带的应用程序集合，包括电子邮件客户端、SMS程序、日历、地图、浏览器、联系人和其他设置。
 
