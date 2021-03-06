---
title: PlantUML使用
date: 2018-05-08 17:56:13
tags: UML
---

# 为什么选择 PlantUML #

画 UML 的工具真的很多


从安装成本上，rose、startUML、visio、md 需要下载软件安装，而 webChart 和 ProcessOn 用浏览器访问即可使用。

从学习成本上，rose、startUML、visio、ProcessOn 都是图形化操作界面，而 md、webChart、PlantUML 需要学习专门的语法。

PlantUML 不仅可以嵌套到各种文本编辑器，IDE，也提供在线版。

# PlantUML 是什么 #

PlantUML 是基于 Java 语言的开源 UML 图形绘制工具，是创建UML图形的组件，它通过简单直观的脚本来定义和创建 UML 图形。

# AndroidStudio 中使用 PlantUML #

- AndroidStudio 安装 PlantUML 插件
- 系统 安装 Graphviz 工具包
- 设置 PlantUML
		
		File->Settings->Other Settings ->PlantUML，选中 Graphvizbin目录中dot.exe

至此，就可以正确 open 或者 new UML图了

# 注释

- 单行注释: 单引号 '
- 多行注释：/ /

# 长字符串，特殊符号字符串

可以使用双引号引起来

# 别名

通过 `as` 关键字来为对象赋予一个简单的别名

	participant "我是很长的一段话，如果要用我来表达的话，就太长了吧！" as par
	"Tom()" -> "牛儿还在山上吃草，放牛的却不知道哪里去了的王二小" as wang : Hi

# 类图

## 关系

{% asset_img 类图-关系.png %}

使用`..` 来代替 `--` 可以得到点 线

```
Class01 <|-- Class02 扩展 泛化 extends 实线三角形
Class11 <|.. Class12 实现 implements 虚线三角形

Class13 --> Class14 关联 成员变量 实线箭头
Class15 ..> Class16 依赖 虚线箭头

Class03 *-- Class04 组合 contains-a 整体与部分不可分 实线实心菱形
Class05 o-- Class06 聚合 has-a 整体与部分可分离 实线空心菱形

Class07 .. Class08 虚线
Class09 -- Class10 实线
```

## 关系上的标识

使用 :后接 标签文字，来说明 关系之间的标签

在标签的开始或结束位置添加< 或 >以表明是哪个对象作用到哪个对象上。

对关系数量的说明，可以在每一边使用 "数字" 来说明.

## 定义类

```
class Dummy {
  String data
  void methods()
}
```

### 可访问性

{% asset_img 类图-可访问性.png %}

### 抽象与静态

{static}

{abstract}

### 分割符

PlantUML默认自动将方法和属性重新分组，可以定义分隔符来重排方法和属性

可用的分隔符：

- `..` ；虚线
- `__` 下划线 ；细实线
- `--` 中划线 ；粗实线（默认的方法和属性分割线）
- `==` ；双实线

### 抽象类和接口

abstract class来定义抽象类。抽象类用斜体显示

也可以使用interface, annotation 和 enum关键字

### 指定标记（Spot）

默认通用标记字符 (C, I, E, A) 用于标记 类(classes), 接口（interface）, 枚举（enum）和 抽象类（abstract classes）

自定义标记：定义原型时，可以增加对应的单个字符及颜色

```
class System << (S,#FF7700) Singleton >>
class Date << (D,red) >>
```

### 泛型

你可以用 < 和 > 来定义类的泛型。

`class Foo<? extends Element>`

## 包

package 声明包，同时可选的来声明对应的背景色（通过使用html色彩代码或名称）

包可以被定义为嵌套。

package "Classic Collections" #DDDDDD {
  Object <|-- ArrayList
}

# 时序图

	张三 -> 李四 : 我要借钱

- 用箭头连接两个对象
- 对象可以不声明

## 样式

### 去掉底部的重复参与者对象

时序图默认顶部和底部都对称地显示了相同的参与者对象。为了图标更为简洁，我们可以去掉底部重复的对象

`hide footbox`

## 基本实例

```
@startuml

张三 -> 李四 : 我要借钱
李四 --> 张三 : 借给你
张三 -> 李四 : 我要还钱
李四 --> 张三 : 收到欠款

@enduml
```

{% asset_img 时序图-基本实例.png %}

## 参与者对象


### 声明参与者对象

可以通过事先声明的方式，使参与者在时序图中保持**确定的顺序**

### 图案样式

通过不同关键词声明，图案稍有不同，含义相同

- participant 默认
- actor
- boundary
- control
- entity
- database

{% asset_img 时序图-声明对象.png %}

### 指定背景颜色

	actor act #FF0000
	actor act #red

## 箭头类型

- **实线实心箭头**，最常见，**同步消息**。`->`
- **实线细箭头**，**异步消息**，使用两个箭头符号（\\、//或者>>、<<），使箭头变为。
- **虚线箭头**，**返回消息**，使用--代替-。
- 箭头末端为一把叉。表示**消息丢失**。
- 在箭头末尾增加一个o，可以在箭头末尾增加一个O。
- 使用\或者/来代替<和>,可以得到只有上半部或者下半部的箭头。
- 可以使用双向箭头。

## 消息注释	

紧跟消息箭头语句之后，使用`note left`或者`note right`关键字来添加注释。

如果注释有多行，可以在多行注释后，通过`end note`来结束注释

```
张三 -> 李四 : 我要借钱
note left: 我借钱肯定会还你的！

张三 -> 李四 : 我要还钱
note left
有借有还，
再借不难！
end note
```

## 消息分组

为了让时序图消息更有逻辑性，我们常需要对消息进行分组框起来

分组之间可以嵌套

### 关键字

- alt/else
- opt
- loop
- par
- break
- critical
- group

除了group以外，其他关键词都会显示在分组框的上方位置

出了alt以外，其他关键词都要end表示结束

## 参与者对象组合

有时候多个参与者对象构成了一个更大的逻辑对象。这时，我们可以将这多个参与者对象用一个框框起来，表达它们逻辑上的关联

### 关键字

box和end box

box关键字后面，可以接一个方框的标题，和指定方框的背景色

`box "解放军部队" #LightBlue`

## 分割线

可以将时序图按照逻辑步骤，使用分割线，将时序图分割为多个不同的步骤阶段。分割线是需要使用 `==` 关键字

```
@startuml

== 借钱阶段 ==

张三 -> 李四 : 我要借钱
李四 --> 张三 : 借给你

== 还钱阶段 ==

张三 -> 李四 : 我要还钱
李四 --> 张三 : 收到欠款

== 再次借钱阶段 ==

张三 -> 李四 : 我还要借钱
李四 --> 张三 : 不借了

@enduml
```

## 进出消息

当我们需要将注意力放在一个参与者对象时，我们只关心它的消息进出情况。因此，这样的时序图只需要一个参与对象，然后通过[和]配合箭头来表示进出消息

```
张三 ->] : 我要借钱
[--> 张三 : 风险有点大，有担保吗？
```



# 参考&扩展

- [官网](http://plantuml.com/zh/)
- [官网类图](https://plantuml.com/zh/class-diagram)
- [捣鼓PlantUML（三、时序图）](https://blog.csdn.net/zh_weir/article/details/72675013)
