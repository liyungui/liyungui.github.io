---
title: 分层架构与 M-V-X
date: 2019-01-14 08:58:53
categories:
  - 编程思想
tags:
  - 编程思想
---
	
分层架构与 M-V-X

分层架构是一种常见的软件应用架构
在 Java 程序中可以算是一种应用标准了，通常又叫 N 层架构
而最常见的是 3 层架构，它包含如下 3 层：
	展示层（Presentation tier），也称为 UI 层，也就是程序的界面部分。

	业务层（business logic(domain) tier）， 业务层，是最为核心的一层。

	持久层（Data tier），数据持久层。

3 层架构是存在物理上分层概念的，
从上往下即展示层、业务层、持久层，也从上往下由上一层依赖下一层。
不同层之间也是 高内聚低耦合 的体现，层内高内聚，层间低耦合，
层 是层内具体工作的高度抽象。
低耦合则是依赖倒转原则体现出来，高层依赖于下层的抽象而不是具体。

在分层架构中 M-V-X 是在展示层（Presentation tier）的应用

M-V-X 的鼻祖 MVC
Model–View–Controller (MVC) is a software architectural pattern for implementing user interfaces.
Model，domain model（领域模型）是数据层代表的数据模型，
	也可以理解为用户界面需要显示数据的抽象（数据）