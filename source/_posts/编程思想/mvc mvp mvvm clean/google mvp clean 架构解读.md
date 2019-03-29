---
title: google mvp clean 架构解读
date: 2019-01-14 09:07:56
categories:
  - 编程思想
tags:
  - 编程思想
---

[学习 CleanArchitecture 心得体会](http://www.jianshu.com/p/cba6663435c7) 

[google mvp clean architecture sample](https://github.com/googlesamples/android-architecture/tree/todo-mvp-clean/)

[uncle-bob Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)

# Summary #

google samples
![](https://upload-images.jianshu.io/upload_images/1019822-cda363d399934d04.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/700)

uncle-bob
![](http://upload-images.jianshu.io/upload_images/1019822-b2acfd9ed6182541.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**两个图其实是一个意思。都是三层结构**

It's based on the MVP sample, adding a `domain` layer between the `presentation` layer and `data` layar, splitting the app in three layers:

- PresentationLayer。 展示层，原来的MVP
- DomainLayer。 新加的层
- DataLayer。原来的数据层。

	最底层，完全不知道 DomainLayer 和PresentationLayer 的存在。这是保证 `可测试性` `低耦合度` 的关键所在 



