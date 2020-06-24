---
title: 我不使用Android Data Binding的四个理由
date: 2019-01-14 09:04:53
categories:
  - 编程思想
tags:
  - 编程思想
---

	我不使用Android Data Binding的四个理由  http://mafei.me/2016/08/14/%E8%AF%91%E6%96%87-%E6%88%91%E4%B8%8D%E4%BD%BF%E7%94%A8Android-Data-Binding%E7%9A%84%E5%9B%9B%E4%B8%AA%E7%90%86%E7%94%B1/

## 1、专家不建议这么做 ##

ButterKnife的作者Jake在下面这个github issue中直指要点。

	data binding在最简单的场景下是比较有用的。
	但它并没有什么创新，所以在复杂度增加的情况下还是会像其他平台上的解决方案一样用起来非常痛苦（例如：XAML）。
	当这个库扩展到高级的情况下，将会迫使你把绑定的逻辑写到代码中，那里才是它真正该在的地方。

事实上，我同意其中的两点：

	1、它的扩展性并不好。
	2、业务逻辑应该在代码中。

## 2、它让你写出意大利面式的代码 ##

一旦我们开始实现复杂的布局，将会使我们的Data Binding解决方案越来越复杂。

首先我们将会面临下面的问题：

	1、Layout 要求你给他们分别传递数据。
	
	2、你也可能想为你的布局创建不同的数据源。
	
	3、同样的问题也会在ViewStubs中发生。
	
	4、当你使用Picasso加载图片的时候，你需要为他实现一个自定义的data binding adapter，那样的话你就不能作为依赖mock和注入了。

## 3、单元测试也不能用了 ##

我非常喜欢Robolectric和Mockito，他们节约了我很多时间在创建和运行测试实例的时候，没有了他们我将无法工作。

Data Binding的一个特性对于我来说是一个bug：如果layout发生了异步更新，那就意味着在我设置了绑定之后单元测试中我无法确定view上的数据是否正确。

## 4、它比ButterKnife提供的功能少很多 ##

# 总结一下放弃的理由

最后总结一下经过这些使用后让我放弃Data Binding的理由。

一、xml代码耦合度增加，业务逻辑内聚性降低。 不利于项目质量的持续发展。

二、经常需要手动点击编译，影响开发体验。 在布局里新增的Data Binding变量，在Java/Kotlin中要使用的时候需要先点击编译等待完成，否则可能引用不到对应的BR类或该类里的变量。另外，已经删除的变量，如果不执行清理，在BR类里也依然存在，无法如R类一样更新及时。

三、失去了Kotlin语法糖的优势。 Kotlin扩展函数的特点可以使得代码尽可能的简洁直观易于阅读，而在xml中目前只支持Java语法而不支持Kotlin，所以也失去了使用Kotlin作为开发语言所带来的优势。


# 参考&扩展

- [我为什么放弃在项目中使用Data Binding](https://blog.csdn.net/maosidiaoxian/article/details/85560206)