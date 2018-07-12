---
title: 获取View坐标
date: 2018-07-11 16:17:40
tags:
	- View
---

# Android坐标系：坐标原点在屏幕左上角 #

{% asset_image 1.jpg %}

**public void getLocationOnScreen(int[] location)**

Computes the coordinates of this view on the screen.

# 视图坐标系：原点在父视图左上角 #

{% asset_image 2.jpg %}

{% asset_image 3.jpg %}

## View提供的获取坐标的方法：到父布局的距离 ##

getTop()

getLeft()

getRight()

getBottom()

## MotionEvent提供的方法 ##

getX()：点击事件到控件自身左边的距离

getY()：点击事件到控件自身顶边的

getRawX()：点击事件到屏幕左边的

getRawY()：点击事件到屏幕顶边的