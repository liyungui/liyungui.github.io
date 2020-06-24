---
title: Jetpack MVVM
date: 2020-05-27 14:50:56
categories:
  - 编程思想
tags:
  - 编程思想
---

# Lifecycle

## 目的

解决 **生命周期管理 的一致性问题**

## Lifecycle 前的混沌世界

Lifecycle 前，生命周期管理 纯靠手工维持，这样就容易滋生大量的一致性问题。

例如跨页面共享的 GpsManager 组件，在每个依赖它的 Activity 的 onResume 和 onPause 中都需要 手工 激活、解绑 和 叫停。

那么 随着 Activity 的增多，这种手工操作 埋下的一致性隐患 就会指数级增长：

- 凡是手工维持的，开发者容易**疏忽**，特别是**协作开发**中，其他同事并不能及时注意到这些细节。
- 分散的代码**不利于维护**，日后若有其他操作需要补充（例如状态监听），那么每个 Activity 都需要额外书写一遍。

## Lifecycle 如何解决上述问题

Lifecycle 通过 模板方法模式 和 观察者模式，将生命周期管理的复杂操作，全部封装在LifecycleOwner中，而**视图控制器**(Activity和Fragment)的基类已实现该接口，开发者在视图控制器子类中只需一句 `getLifecycle().addObserver(GpsManager.getInstance)` 就能增加一个生命周期观察者(一般继承DefaultLifecycleObserver)，第三方组件 优雅地完成 对 LifecycleOwner 生命周期的感知。

# LiveData

## 目的

解决 **状态 的一致性问题**

具有生命周期感知的被观察者(RxJava Observable)，可以确保只有处于 active 状态的组件才能收到 LiveData 的更新

## LiveData 前的混沌世界

LiveData 前，分发状态(网络请求回调，跨页面通信) 多是通过 EventBus 或 Java Interface 来完成的。

EventBus 因 去中心化 地滥用，而容易造成 诸如 毫无防备地收到 预期外的 不明来源的推送、拿到过时的数据 及 事件源追溯复杂度 为 n² 的局面。

并且，EventBus 本身缺乏 Lifecycle 的加持，存在生命周期管理的一致性问题

## LiveData 如何解决上述问题

**LiveData 职责十分克制**：仅支持状态的输入和监听

开发者不得不 在单例的配合下，**由 唯一可信源 一对多地 分发状态**。即所有视图控制器发起的 对某个共享状态改变的请求，都由 唯一可信源 来一对多地通知改变

这使得任何一次状态推送，都可预期、都能方便地追溯来源

**唯一可信源**是指 生命周期独立于 视图控制器的 数据组件，通常是 单例 或SharedViewModel(姑且也算是工厂模式实现的伪单例)。

```java
MutableLiveData<Integer> mNumberLiveData = new MutableLiveData<>();
//增加一个观察者。
//生命周期感知的来源，this为 AppCompatActivity,实现了 LifecycleOwner 接口
mNumberLiveData.observe(this, new Observer<Integer>() {
	@Override
	public void onChanged(@Nullable Integer integer) {
		mTvNumber.setText("" + integer);
		Log.d(TAG, "onChanged: " + integer);
	}
}

//点击按钮，每隔一秒发送递增的计数
mNumberLiveData.postValue(number);
}
//运行APP，按Home键进入后台，过一会儿切回app
//日志如下：1，2，5，6...
```
	
## LiveData设计缺陷

为了在视图控制器发生重建后，能够 自动倒灌 所观察的 LiveData 的最后一次数据，**LiveData 被设计为粘性事件(未提供非粘性事件支持)**。

因为 Jetpack MVVM 是一个整体，既然 ViewModel 支持共享作用域(实现跨页面通信的需求)，那么基于 “开闭原则”，LiveData 理应提供一个与 MutableLiveData 平级的底层支持，专门用于非粘性的事件通信的情况，否则直接在跨页面通信中使用 MutableLiveData 必造成 **事件回调的一致性问题 及 难以预期的错误**。

# ViewModel

## 目的

解决 **状态管理 问题**。顺带也能实现作用域共享(跨页面通信)

## ViewModel 前的混沌世界

ViewModel 前，Presenter 和 Clean ViewModel 的生命周期都与视图控制器同生共死，无法实现状态的恢复。

视图控制器重建状态恢复，只能通过视图控制器基类的 onSaveInstanceState 序列化存储和恢复。这种方式只适用于轻量级的状态恢复

## ViewModel 如何解决上述问题

基于 工厂模式，使得 ViewModel 被 LifecycleOwner 所持有、通过 ViewModelProvider 来引用。

**特别注意：当 Activity 处于前台的时候被销毁了(横竖屏切换)，那么得到的 ViewModel 是之前实例过的 ViewModel；如果 Activity 处于后台时被销毁了，那么得到的 ViewModel 不是同一个。** 原因是把实例缓存在了一个空HolderFragment中，而 `setRetainInstance(true)` 表示Activity 被重建的时候该 Fragment(只适用于非后台Fragment) 会被保留，然后传递给新创建的 Activity

它**类似于单例**：当被作为 LifecycleOwner 的 Activity 持有时，能够脱离 Activity 下 Fragment 的生命周期，从而实现作用域共享。

**实际上不是单例**：生命周期跟随 作为 LifecycleOwner 的视图控制器，当 Owner（Activity 或 Fragment）被销毁时，它也被 clear。

对于重量级的状态，例如通过网络请求得到的 List，可以通过生命周期长于视图控制器的 ViewModel 持有，从而得以直接从 ViewModel 恢复，而不是以效率较低的序列化方式。

再者，由于能实现作用域共享，所以 ViewModel 本身也能承担跨页面通信（例如事件回调）的职责。

```java
public class MyViewModel extends ViewModel {
	private MutableLiveData<List<User>> users;
	public LiveData<List<User>> getUsers() {
	if (users == null) {
		users = new MutableLiveData<List<User>>();
	}
	return users;
}

//Activity onCreate()中获取MyViewModel实例
//生命周期绑定当前Activity
//Activity重建的时候，onCreate()会重新走一遍，但是返回的仍然是第一次创建的MyViewModel实例
//在ViewModelProviders.of(this).get(***.class)中的get方法中进行了缓存
MyViewModel model = ViewModelProviders.of(this).get(MyViewModel.class);
model.getUsers().observe(this, users -> {
	// update UI
});	
```

# DataBinding

## 被不假思索地抵制的 DataBinding

许多人对 DataBinding 的第一印象：

`android:visibility:"@{ age > 13 ? View.VISIBLE : View.GONE }"`

 xml 中居然还要写 三元表达式 “这样的逻辑”，便草草地断定：DataBinding 不是个好东西，在**声明式编程中书写 UI 逻辑，既不可调试，也不便于察觉和追踪**，万一出现问题就麻烦了。
 
## 目的

解决 **视图调用 的一致性问题**

通过 基于适配器模式 的 **“数据驱动”** 思想实现

数据驱动 顺带免去了 因调用视图对象 而存在的大量样板代码(绑定视图)和冗余的判空处理

## DataBinding 前的混沌世界

DataBinding 前，视图操作都是：绑定该视图，判空，改变视图的状态

这就导致存在存大量样板代码(绑定视图)和冗余的判空处理

这里解释一下**为什么要有判空，因为视图是动态的(视图一致性问题)**

比如页面横竖布局的控件一般都存在差异，例如横屏存在 textView 控件，而竖屏没有

再比如用户界面会因为用户角色不同存在差异

那么我们就不得不在视图控制器中为 textView 做判空处理

## DataBinding 如何解决上述问题

**在布局中绑定可观察的数据**，该数据被 set 新的内容时，控件也将得到通知和刷新。

**DataBinding 只负责绑定数据(UI跟随数据状态改变，即它是一个不可再分的原子操作，不需要调试)**

先前的 UI 逻辑没有任何改变，改变的只是UI状态的改变方式(之前是手动操作视图，现在是观察数据状态原子刷新)

此外，DataBinding 有个大杀器，**BindingAdapter 能为控件提供自定义属性**，它可以解决 圆角 Drawable 复用的问题，还可以实现 imageView 直接绑定 url 等需求


# 参考&扩展

- [Jetpack MVVM 精讲](https://juejin.im/post/5dafc49b6fb9a04e17209922#heading-14)
- [LiveData && ViewModel使用详解](https://juejin.im/post/5ca9f9156fb9a05e3d0a8aea#heading-8)
- [揭开 ViewModel 的生命周期控制的神秘面纱](https://juejin.im/post/5c3dacde518825247c723ab5)
- [Android官方架构组件DataBinding-Ex: 双向绑定篇](https://juejin.im/post/5c3e04b7f265da611b589574#heading-1)
