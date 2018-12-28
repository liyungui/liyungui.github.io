---
title: Android中View的绘制.md
date: 2018-11-14 17:54:53
tags:
	- View
	- Canvas
---

# View的绘制原理

View通过刷新来绘制视图，为了不让画面掉帧，Android系统4.1之后通过发出**VSYNC**(垂直同步)信号进行屏幕绘制，。为了不掉帧，View的绘制需要在**16ms**之内完成。如果执行耗时太长或者需要频繁刷新，那么View就不合适了，影响用户体验和性能。

# SurfaceView

 SurfaceView内部是在子线程进行页面刷新，使用了双缓冲机制，性能比View更好
 
 



