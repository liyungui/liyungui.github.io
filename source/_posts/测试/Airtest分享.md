---
title: Airtest分享
date: 2020-06-03 10:25:42
categories: 测试
tags: 测试
---

# Airtest概述

## 关键词

- 完整名称：Airtest Project
- 2018 GDC 开幕第一天
- 谷歌发布
- 网易研发
- **游戏**UI自动化测试框架
	- 谷歌方面表示 Airtest 是**安卓游戏**开发最强大、最全面的自动测试方案之一
- 网易多游戏验证：
	- 《梦幻西游》、《荒野行动》、《阴阳师》等数十个游戏项目中

## 框架结构

{% asset_img 架构.png %}


# 快速上手

## 配置环境

## 录制脚本

## 执行脚本

## 查看测试报告


# `.air`脚本

{% asset_img air.png %}

# Airtest还是Poco

**结论：Poco优先，Airtest辅助(比如游戏暂时没有集成SDK)。**

因为poco性能和兼容性更强，而且Poco能获取属性值，测试更加灵活

图像识别在更换一台不同分辨率的手机/更换一个环境之后，基本失败

# 图片类Template

`class Template(filename, threshold=None, target_pos=5, record_pos=None, resolution=(), rgb=False)`

- **filename**。图片名。
- **record_pos**。截图位置。
	- 优先在录制时的位置附近查找
	- 如果找不到符合条件的图片，再扩大寻找范围到整个画面。
	- 这样能够提升查找图片的速度和精确度
- **resolution**。截图屏幕分辨率。跨分辨率匹配
- **threshold**。图像识别阈值。默认值是0.7
- **rgb**。是否灰度识别还是彩色识别
- **target_pos**。点击位置
	- 将图片划分为三横三列[1, 9]，默认值是5(图片正中间)

# Poco选择UI

- 只能选择可见UI。即使设置visible=False也无法返回不可见UI
- 查找UI是懒执行(只有使用该UI时才查找)
- 返回值是 UI对象的代理 UIObjectProxy
	- 可迭代对象
	- 记录着所有符合条件的UI列表

## 基本选择器(Basic Selector)

通过**属性**来选择 **可见UI**

### `__call__`

```python
class Poco(agent, **options):
	def __call__(name=None, **kw)
```

### Poco UI属性

UI对象常见的属性值

```
Path from root node: [0, 0, 0, 0, 0, 0, 5, 2, 3, 1, 1]
Payload details:
	type :  android.widget.TextView 
	name :  com.zy.course.dev:id/tv_title 
	text :  关于我们 
	enabled :  True 
	visible :  True 
	resourceId :  b'com.zy.course.dev:id/tv_title' 
	zOrders :  {'global': 0, 'local': 2} 
	package :  b'com.zy.course.dev' 
	anchorPoint :  [0.5, 0.5] 
	dismissable :  False 
	checkable :  False 
	scale :  [1, 1] 
	boundsInParent :  [0.17777777777777778, 0.02850877192982456] 
	focusable :  False 
	touchable :  False 
	longClickable :  False 
	size :  [0.17777777777777778, 0.02850877192982456] 
	pos :  [0.2388888888888889, 0.48333333333333334] 
	focused :  False 
	checked :  False 
	editalbe :  False 
	selected :  False 
	scrollable :  False 
```

## 相对选择器(Relative Selector)

直接用节点属性没法选出你所想要的UI时，还可以通过UI之间的渲染**层级关系**进行选择

### 子类`child`

```python
class UIObjectProxy(poco, name=None, **attrs):
	def child(name=None, **attrs)
```

### 后代`offspring`

```python
class UIObjectProxy(poco, name=None, **attrs):
	def offspring(name=None, **attrs)
```

### 所有子类`children()`

## 空间顺序选择器(Sequence Selector)

按照空间排布顺序来选择

- 从上到下，从左往右，索引从0开始
- 一旦选择，UI位置发生变化，索引值不变，消失(移除或者隐藏)的UI不能再访问


## 实例

{% asset_img poco.png %}

```python
poco(text="小班正确率").parent().parent().child("com.zy.course.dev:id/rv_rank").offspring("com.zy.course.dev:id/text_name")[0]
```

# Poco等待

```python
class UIObjectProxy(poco, name=None, **attrs):
	def wait(timeout=3) 等待UI出现，单位秒。
		返回UI对象的代理 UIObjectProxy
	wait_for_appearance(timeout=120)等待UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
	wait_for_disappearance(timeout=120)等待UI消失，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
```

```python
class UIObjectProxy(poco, name=None, **attrs):
	wait_for_all(objects, timeout=120)等待所有UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
	wait_for_any(objects, timeout=120)等待任一UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		返回第一个出现的UI对象的代理 UIObjectProxy
```

# Poco操作UI

```
exists 验证UI可见
focus 设置焦点的局部坐标(0到1)
click/long_click 默认点击UI正中，也可以指定局部坐标(0到1)
	click()
	click('center')
	click([0.5,0.5])
	focus([0.5,0.5]).click()
swipe 滑动
	swipe('up')
	swipe([0.2, -0.2])
	swipe([0.2, -0.2], duration=0.5)
drag_to 拖拽UI到UI
	drag_to(poco(text='岩石司康饼'))	
```

# Poco操作UI属性

- 直接访问属性名
- get方法。`get_text()`
- set方法。`set_text('hello')`

# Poco对WebView的支持

Poco对WebView的检视的支持程度，主要取决于WebView本身的兼容性情况，目前兼容性最好的WebView方案是Android系统自带内核 `Google-WebView`

Android设备设置可以设置浏览器使用系统内核自带的WebView
