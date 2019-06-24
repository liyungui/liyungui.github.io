---
title: 串口、COM口、TTL、RS-232
date: 2017-07-22 14:39:23
tags:
	- RFID
---

# 概念

- 电平标准（电信号）
	- TTL
		- 低电平为0，高电平为1（+5V电平）
	- RS-232
		- 正电平为0，负电平为1（±15V电平）
	- RS-485
		- 与RS-232类似，但是采用差分信号负逻辑
- 物理接口形式（硬件）
	- **COM口**(cluster communication port)即串行通讯端口，简称**串口**。
		- 9针(D型9针串口)
			- 协议只有两种：RS-232和RS-485。不会是TTL电平的（除非特殊应用）
			- 一般只接出
				- RXD
					- Receive Data指示灯
				- TXD
					- Transmit Data指示灯
				- GND
					- (Ground)代表地线或0线
					- 直流电源的负极
			- 不会接Vcc或者+3.3v的电源线，避免与目标设备上的供电冲突
				- Volt Current Condenser伏特电源电容器;
				- 直流电源的正极 
		- 4针杜邦头
			- 协议是ttl
			- 电路板上常见
			- 经常还带有杜邦插针
			- 有时候有第五根针，3.3V电源端。
	- **USB**(Universal Serial Bus)即“通用串行总线”
	- **SATA**(Serial Advanced Technology Attachment)
		- SATA（Serial ATA）口的硬盘又叫串口硬盘

# 实物图

4针杜邦头

{% asset_image dubangtou.jpg %}

D型9针串口

{% asset_image d9comkou.jpg %}

转TTL串口的小板。芯片为PL2303HX

{% asset_image usb2ttl.jpg %}

USB转TTL串口的小板。芯片为CP2102,多了+3.3V电源端，以适应不同的目标电路。

{% asset_image usb2ttl2.jpg %}

USB转 RS-232串口（D型9针接口）和 TTL串口

{% asset_image usb2rs232.jpg %}
{% asset_image usb2rs232b.jpg %}

- 电平转换用的是MAX232
- TTL电平与RS232电平的专用**双向转换**芯片

USB转RS-232串口（D型9针接口）

{% asset_image usb2rs232c.jpg %}

参考&扩展

- [串口、COM口、TTL、RS-232的区别详解](http://www.dzsc.com/data/2016-10-19/110834.html)


