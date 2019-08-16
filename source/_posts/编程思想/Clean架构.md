---
title: Clean架构
date: 2019-01-14 09:06:53
categories:
  - 编程思想
tags:
  - 编程思想
---

作者尝试使用简单的观点将各种架构的共通之处和最终目标说清楚。

全文要说清楚的就是一件事“如何写出整洁的架构”。

作者希望在架构系统的时候只需要秉持最简单的两个观点（**分层和依赖规则**）开发，就能开发出干净整洁的系统架构。

# 好架构共性

{% asset_img Clean架构.png %}

过去几年间有许多关于系统架构的观点。虽然这些架构在细节处都有一些变化，但是实际上，它们是非常相似的。它们的目标是一样的，将各种实体间的关系进行分离。它们分离操作的方法也是一样的，采用软件分层的方式。它们分的层中至少有一个业务逻辑层，并且有其他的接口层。

每一种架构在写系统的**业务逻辑**的时候有以下特征：

1. 与框架的分离。
框架决不能依赖一些有限制特征的库。这样就能保证你能像使用手边的工具一样简单地使用这些框架，而不会让你的系统业务逻辑在使用前就有一些强制性的约束。

2. 可测试性。
业务逻辑必须能独立测试，不需要UI，数据库，Web服务器或者一些其他的外部条件。

3. 与UI的分离。
UI必须能非常容易独立地修改。而不能在改变UI的同时需要改变系统其他部分。比如当把系统的UI从Web UI改成控制台UI，你并不需要改变任何业务逻辑的代码。

4. 与数据库的分离。
能很方便地在Oracle，SQL Server，Mongo DB，BigTable，CouchDB或者其他数据库中进行切换和改变。业务逻辑决不能依赖这些数据库。

5. 与外部结构的分离。
系统的业务逻辑并不需要知道任何外部的结构。

文章最上面的图就是将所有这些架构进行统一概括，提取出统一的观点。

# Clean架构要点

## 依赖规则（The Dependency Rule）

**单向向内依赖**。内层完全不知道外层的存在；

## 分层

### 实体层（Entities）

业务逻辑对象，封装了最通用的规则。

外部环境变化的时候，这些实体是最不需要被变化的。即**用户实例层的任何改变都不会影响到实体层**

比如在增加翻页需求或者是安全需求的时候，这些实体是最不应该被改变的。

### 用户实例层（Use Cases）

具体的业务逻辑

由流入实体的数据流和流出实体的数据流实现，用户实例使得内层的实体能依靠实体内定义的业务逻辑规则来完成系统的用户需求。

能够引起用户实例层**改变的唯一原因是 用户需求改变**。外层，比如UI、数据库或者任何公共的框架，改变都不会影响到用户实例层

### 接口适配层（Interface Adapters）

目的就是进行**数据结构转换** DataMapper

按数据流向需要，转换 **用户实例层和实体层** 和 **外层(比如数据库或者Web)** 的数据结构。

接口适配层 并不需要知道任何数据库的信息。如果数据库是SQL数据库，那么，所有的SQL语言应当在这层被限制使用

这里可以是Presenters(MVP),ViewModel(MVVM),Controller(MVC)等MVX结构，X所在的地方

### 框架和驱动层（Frameworks and Drivers）

最外层是由**框架和工具**组成的

数据最终到达的地方(Web、数据库)

# Clean架构问题

## 只有四层？

答案是否定的。这个分层模型是纲要性的。

并没有任何规定说你必须只能实现这四个层级。但是，**依赖规则（The Dependency Rule）是必须遵守的**：代码依赖只能 **单向向内** 。越向内，抽象程度越高，需要设计越高层面的策略。

## 跨层调用/反向调用

图片的右下角是一个如何跨层调用的例子。准确的说是 反向调用

它演示了 控制器、表现器和 用户实例层 进行交互。

注意流向，从控制器开始，通过用户实例层，然后向上执行到表现器。

为了遵守向内依赖规则，通常使用 **依赖倒置原则**（Dependency Inversion Principle）来实现这种反向调用。

例子中，让 用户实例层 调用一个接口（Use Case Output Port），然后让表现层在外部实现这个接口。

实践中，一般都是通过 **依赖注入(DI)** 来实现依赖倒置。

## 数据跨层传递原则

保持简单的数据结构。原则是不要违背向内依赖规则

所以，没有必要在各层定义数据结构实体(比如 框架和驱动层、用户实例层、实体层)，外层是可以跨层依赖内层的(符合向内依赖规则)

# 三层与洋葱图的对应关系

Domain Layer 对应洋葱图最里面两层：Entities，Use Cases

Presentation Layer 和 Data Layer 对应洋葱图最外层：Frameworks and Drivers 即(UI Web Devices DB)

# 数据流向

{% asset_img 数据流向.png %}

实例：从Presenter层传递一个对象UserModel给Data层进行存储

## Presenter层

- 用户输入数据，并点击OK按钮(View)
- Presenter(ViewModel,Controller等)获取到数据，并构造一个UserModel
- 使用UserModelMapper（Presenter层的数据Mapper对象）将UserModel转换成User对象。
	- 这步可以省略，上一步直接构造User对象
- 调用UseCase.store(user)

## Domain层

唯一目:执行上面的业务逻辑(存储对象)

- StoreUseCase接受到User对象
- 调用UserRepository接口的方法，传入User

## Data层

- UserDataRepository(UserRepository接口的实现类)，接受到User对象
- 调用Mapper方法(Data层的)将User对象转换成UserEntity
- 存储UserEntity对象

这只是数据的流动过程，与依赖关系无关。Domain层实际上不持有任何依赖。

# 总结

Clean 架构是 **分层 和 单向内向依赖** 。即内层完全不知道外层的存在

# 参考&扩展

- [The Clean Code Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) by Robert C. Martin (Uncle Bob) - 原文
- [架构整洁之道](https://www.cnblogs.com/yjf512/archive/2012/09/10/2678313.html) - 译文
- [Clean架构探讨](https://www.jianshu.com/p/66e749e19f0d)