---
title: Clean架构开发Android应用
date: 2019-01-14 10:06:53
categories:
  - 编程思想
tags:
  - 编程思想
---

# 测试方法

## 表现层

Espresso 2 + Instrumentation

测试 Android UI

## 领域层

JUnit + Mockito

是Java的标准模块。

## 数据层

Robolectric 3 + JUnit + Mockito

有部分Android模块

### Robolectric

在 PC上使用 JVM 模拟实现 Android SDK。

支持UI表现测试和网络请求测试

使Android模块的测试 更加高效

# 实例

Fernando 大神 对 Clean架构的解读及实践

[实例源码](https://github.com/android10/Android-CleanArchitecture)

## Clean在Android中如何表现 ##

一个应用可以有任意数目的层，但除非你的应用到处是企业级功能逻辑，一般需要这三层：

- 外层：接口实现层
- 中层：接口适配层
- 内层：逻辑层

**接口实现层是体现架构细节的地方**。实现架构的代码是所有不用来解决问题的代码，这包括所有与安卓相关的东西，比如创建Activity和Fragment，发送Intent以及其他联网与数据库的架构相关的代码。图片中UI、Web、Devices、DB、External Interfaces是和架构相关的（android还是ios或是web）

**接口适配层就是桥接逻辑层和架构层的代码，是胶水代码**。mvc中的c，mvp的p。

**逻辑层最重要，这里包含了真正解决问题的代码**。这一层不包含任何实现架构的代码， 不用模拟器也应能运行这里的代码 。这样一来你的逻辑代码就有了易于测试、开发和维护的优点。这就是Clean架构的一个主要的好处。

每一个位于核心层外部的层都应能将外部模型转成可以被内层处理的内部模型。内层不能持有属于外层的模型类的引用。

为什么要进行模型转换呢？举个例子，当逻辑层的模型不能直接很优雅地展现给用户，或是需要同时展示多个逻辑层的模型时，最好创建一个ViewModel类来更好的进行UI展示。这样一来，你就需要一个属于外层的Converter类来将逻辑层模型转换成合适的ViewModel。

再举一个例子：你从外部数据库层获得了ContentProvider的Cursor对象，外层首先要将这个对象转换成内层模型，再将它传给内层处理。

## 如何开始写Clean应用？ ##

**开始写用例**

一般来说一个安卓应用的结构如下：

- 外层项目包：UI，Storage，Network等等。

- 中层项目包：Presenter，Converter。

- 内层项目包：Interactor，Model，Repository，Executor。

**外层体现了框架的细节。**

UI– 包括所有的Activity，Fragment，Adapter和其他UI相关的Android代码。

Storage– 用于让交互类获取和存储数据的接口实现类，包含了数据库相关的代码。包括了如ContentProvider或DBFlow等组件。

Network– 网络操作。

**中层是桥接实现代码与逻辑代码的Glue Code。**

Presenter– presenter处理UI事件，如单击事件，通常包含内层Interactor的回调方法。这里需要注意不能持有外层UI的引用，所以通过持有接口而UI实现接口实现间接持有UI（mvp的做法）

Converter– 负责将内外层的模型互相转换。内层不能持有外层引用，所以转换成ViewModule传给内层

**内层真正解决问题的代码，这一层的类和对象不知道外层的任何信息，且应能在任何JVM下运行。**

Interactor– Interactor中包含了解决问题的逻辑代码。这里的代码在后台执行，并通过回调方法向外层传递事件。在其他项目中这个模块被称为用例Use Case。一个项目中可能有很多小Interactor，这符合单一职责原则，而且这样更容易让人接受。一般mvp是在这里直接调用mvp方法。clean不能持有相对外层的引用，所以需要在本层再增加一个回调接口，让present去实现。

Model– 在业务逻辑代码中操作的业务模型。

Repository– 包含接口让外层类实现，如操作数据(获取/保存)的类等。不能持有外层引用，Interactor持有这些接口来获取和存储数据,外层需要实现这些接口（DB/External Interfaces就是这些接口的实现）。这也叫资源库模式Repository Pattern。

Executor– 通过Worker Thread Executor让Interactor在后台执行。一般不需要修改这个包里的代码。

# 参考&扩展

- [Architecting Android...The clean way?](https://fernandocejas.com/2014/09/03/architecting-android-the-clean-way/) by Fernando Cejas (Fernando 大神) - 原文
- [一种更清晰的Android架构](https://zhuanlan.zhihu.com/p/20001838) - by 何红辉 - 译文
- [实例源码](https://github.com/android10/Android-CleanArchitecture)
- [Clean架构探讨](https://www.jianshu.com/p/66e749e19f0d)