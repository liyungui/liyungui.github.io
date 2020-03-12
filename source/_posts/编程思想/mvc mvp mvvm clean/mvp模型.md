---
title: MVP模型
date: 2019-01-14 09:08:56
categories:
  - 编程思想
tags:
  - 编程思想
---

本文所采用的架构是单Activity多View栈模式，跟常见的Activity架构不同

# 基础架构

{% asset_img 基础架构.jpg %}

**Contract**：协议层，负责定义MVP三层所有对外的接口。

**Model**：数据业务层，负责数据获取、处理等逻辑，其通过回调接口将数据返回给Presenter层(可以不通过接口回调，持有Presenter返回数据)。

**Presenter**：中间层，Model层与View层的中间枢纽，负责表现层逻辑以及提供模块对外的方法，其持有Model层与View层的引用（对View层的引用为弱引用，以防出现内存泄漏）。

**View**：视图层，只负责UI更新和交互相关的逻辑，持有Presenter的引用，用以响应控件的交互事件。


## View层

{% asset_img view.png %}

一般一个交互模块(比如直播投票)需要多个视图组件协同工作，因此设置ViewManager类统一管理模块内部的所有组件。ViewManager作为View层的黑盒入口，起到隔离Presenter与View层的作用（Presenter无需知道View层内部的具体实现）。那么对于Presenter来说，它就只需要在特定时机下，调用IView.showVote()方法即可。
     
关于ViewManager还有以下几点说明：

- ViewManager对象的初始化是在主模块ScreenLiveRoom中完成的，在初始化的时候会注入模块相关的父容器和控件
- 需要动态加载的子View会在ViewManager中完成初始化
- ViewManager负责子View生命周期的管理（动态添加到相关区域的父容器、互动结束时清除View对象等）
- 在ViewManager的构造方法中会初始化此模块的Presenter对象

## Presenter层

{% asset_img presenter.png %}

Presenter的职责如下：

- 初始化Model对象，接收Model层数据，实现表现层逻辑
- 在构造方法中注入持有ViewManager的引用，控制View层更新UI
- 作为互动模块的黑盒入口对外提供接口方法

## Model层

{% asset_img model.png %}

持有Repository对象的引用。Model负责加工处理数据以及数据的映射工作，而Repository则为Model提供数据（数据可以是从网络也可以是从本地获取）。

# 模块通信

{% asset_img 基础架构-模块.jpg %}

模块之间将处于各自独立的状态，无法直接通信

通过路由的方式解决模块间通信的问题

路由内部维护着一份路由表（通过Map实现），路由表保存着所有直播间模块（包括主模块）的Presenter对象，其索引为对象的类型。

```java
public class LiveRouter {
    public static Map<Class, Object> mPresenterMap = new HashMap<>();// 互动模块Presenter路由表
 
    public static void savePresenter(Object presenter) {
        mPresenterMap.put(presenter.getClass(), presenter);
    }
 
    public static  <T> T findPresenter(Class<T> clazz) {
        if (mPresenterMap.containsKey(clazz)) {
            return (T) mPresenterMap.get(clazz);
        } else {
            return null;
        }
    }
 
    public static void clearCache() {
        mPresenterMap.clear();
    }
}
```

在Presenter基类的构造方法中调用LiveRouter.savePresenter()方法将本类对象存入路由表中，然后在其他模块里就可以通过LiveRouter.findPresenter()方法查找到目标对象。这样，通过路由器LiveRouter的中转作用，模块之间就可以以间接调用的方式访问对方的外部方法了。

当前LiveRouter的实现方式成本极低（只有十几行代码），但有不足的地方。LiveRouter.findPresenter()方法需要显式地传入Presenter的类型来查找对应的对象，这会造成一定程度上的耦合，当需要移除某个模块所有代码时，就要去到其他模块删除其Presenter类型的引用。但这种代价是可以接受的，因为这样的引用并不会太多，而且清理起来非常方便，此外，对比其他实现方案（事件总线、apt实现的路由），这种方式性价比是最高的，因此直播间模块通信暂定为这种方法。

{% asset_img 整体架构.jpg %}

# mvp接口迷局

MVP的问题在于，使用接口去连接view层和presenter层，这就导致一个逻辑复杂的页面，接口会有很多，十几二十个都不足为奇。维护接口的成本就会非常的大。

这个问题的解决方案就是你得根据自己的业务逻辑去斟酌着写接口。你可以定义一些基类接口，把一些公共的逻辑，比如网络请求成功失败，toast等等放在里面，之后你再定义新的接口的时候可以继承自那些基类，这样会好不少。

# mvp开源库

[A Model-View-Presenter library for modern Android apps](https://github.com/sockeqwe/mosby)

# 参考&扩展

- [mvp in android](http://blog.csdn.net/lmj623565791/article/details/46596109)

