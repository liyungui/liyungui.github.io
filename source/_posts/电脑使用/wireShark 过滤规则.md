---
title: wireShark 过滤规则
date: 2018-12-20 08:56:53
categories:
  - 电脑使用
tags:
  - wireShark
  - 抓包
---

ip
	ip.dst==192.168.101.8
	ip.src==1.1.1.1
	
port
	tcp.port==80
	tcp.dstport==80
	tcp.srcport==80
	
protocol
	直接在Filter框中直接输入协议名即可
	
http模式过滤
	如过滤get包，http.request.method=="GET",
	过滤post包，http.request.method=="POST"；
	
连接符and的使用
	过滤两种条件时，使用and连接
	如过滤ip为192.168.101.8并且为http协议的，ip.src==192.168.101.8 and http。