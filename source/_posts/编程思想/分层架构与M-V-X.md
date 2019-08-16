---
title: 分层架构与M-V-X
date: 2019-01-14 08:58:53
categories:
  - 编程思想
tags:
  - 编程思想
---
	
# 分层架构

分层架构是一种常见的软件应用架构

在 Java 程序中可以算是一种应用标准了，通常又叫 N 层架构
而最常见的是 3 层架构，它包含如下 3 层：

{% asset_img 分层架构.png %}

## 展示层（Presentation Layer）

也称为 UI 层，也就是程序的界面部分。

也就是 **MVX结构** 所对应的地方（MVC、MVP等），这里不处理UI以外的任何逻辑。

## Domain Layer

又称 Bussiness Logic Layer， 业务层，是最为核心的一层。

纯java模块，不包含任何的平台(Android,Web)依赖

包含 业务实体(Entities)和具体业务逻辑(Interactor,又称Use Cases)

{% asset_img DomainLayer.png %}

## Data Layer

数据持久层。

应用的数据都是由这层提供

这层通常是 Repository Pattern 实现 Domain层 接口

数据流向：

{% asset_img DataLayer.png %}

# 分层架构依赖关系

3 层架构是存在物理上分层概念的，
从上往下即展示层、业务层、持久层，也从上往下由上一层依赖下一层。
不同层之间也是 高内聚低耦合 的体现，层内高内聚，层间低耦合，
层 是层内具体工作的高度抽象。
低耦合则是依赖倒转原则体现出来，高层依赖于下层的抽象而不是具体。

# M-V-X

在分层架构中 M-V-X 是在展示层（Presentation Layer）的应用