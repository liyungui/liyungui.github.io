---
title: ImageView使用
date: 2019-04-30 18:02:53
tags: 
	- Android
---

# adjustViewBounds

## 作用

调整ImageView的界限来**保持图片的宽高比例**

设置adjustViewBounds="ture"的时候，会将这个ImageView的scaleType属性设置为**fitCenter**

## 优先级

android:scaleType的优先级会更高，两个属性同时设置，adjustViewBounds="ture"中对scaleType属性设置将会失效。

这种情况，只有在Java代码中设置setAdjustViewBounds（true）的时候，才会生效

## 起效条件

- ImageView宽高都是固定值，adjustViewBounds无效
- ImageView宽高只有一个固定值/match_parent，比较两者的宽高
	- 图片宽/高比ImageView小，图片不缩放，ImageView的非固定值变成和图片一致
	- 图片宽高比大于等于，图片等比放大至填满ImageView
- ImageView宽高都是wrap_content，adjustViewBounds无意义，因为ImageView将始终与图片拥有相同的宽高比（但是并不是相同的宽高值，通常都会放大一些

实例：

	<ImageView
		layout_ width="100dp"，
		layout_ height="wrap_ content"/>
		
图片的宽度将会与100dp进行对比（抛开单位换算）。

- 图片的宽度小于100dp
	- ImageView的layout_height将与图片的高相同
	- 即图片不会缩放，完整显示在ImageView中，ImageView高度与图片实际高度相同。
	- 图片没有占满ImageView，ImageView中有空白。
- 图片的宽度大于或等于100dp
	- 图片将保持自身宽高比缩放，完整显示在ImageView中，
	- 图片完全占满ImageView


## 最大宽高

m在Android机制中，只用当设置adjustViewBounds="ture"的时候，maxWidth/maxHeight设置效果才能有效
