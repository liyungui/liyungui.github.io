	---
title: VO DTO DO PO 概念
date: 2019-01-14 08:56:53
categories:
  - 编程思想
tags:
  - 编程思想
---
	
	浅析VO、DTO、DO、PO的概念、区别和用处 http://blog.csdn.net/zjrbiancheng/article/details/6253232

## 概念 ##

	VO（View Object）：视图对象，用于展示层，它的作用是把某个指定页面（或组件）的所有数据封装起来。 展示User 可能是包含昵称头像
	DTO（Data Transfer Object）：数据传输对象，服务层返回的数据传输对象。 服务器返回的User不包含密码
	DO（Domain Object）：领域对象，就是从现实世界中抽象出来的有形或无形的业务实体。 抽象User可能包含密码和登录方法
	PO（Persistent Object）：持久化（通常是关系型数据库）对象。 存储User可能不包含密码