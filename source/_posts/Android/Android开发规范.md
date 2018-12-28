---
title: Android开发规范
date: 2018-11-20 11:12:53
tags: 
	- Android
---

主要来自于平时开发过程的总结

# 不是所有错误都能追溯到用户代码

默认的堆栈打印，并不是所有错误都能追溯到用户代码

所以有必要通过一些规范，帮助我们定位bug

	java.lang.IndexOutOfBoundsException
	Inconsistency detected. Invalid view holder adapter positionViewHolder{47a36d8 position=18 id=-1, oldPos=-1, pLpos:-1 no parent} 
	android.support.v7.widget.RecyclerView{fb87ab4 VFED..... .......D 0,0-1080,1433 #7f0e00cd app:id/recycler_view}, 
	adapter:com.shensz.common.component.multitype.MultiTypeAdapter@22746dd, 
	layout:android.support.v7.widget.LinearLayoutManager@e3eb252, 
	context:com.shensz.course.module.main.activity.MainActivity@46fd75b
	
	1 android.support.v7.widget.RecyclerView$Recycler.validateViewHolderForOffsetPosition(ProGuard:5447)
	2 android.support.v7.widget.RecyclerView$Recycler.tryGetViewHolderForPositionByDeadline(ProGuard:5629)
	3 android.support.v7.widget.GapWorker.prefetchPositionWithDeadline(ProGuard:285)
	4 android.support.v7.widget.GapWorker.flushTaskWithDeadline(ProGuard:342)
	5 android.support.v7.widget.GapWorker.flushTasksWithDeadline(ProGuard:358)
	6 android.support.v7.widget.GapWorker.prefetch(ProGuard:365)
	7 android.support.v7.widget.GapWorker.run(ProGuard:396)
	8 android.os.Handler.handleCallback(Handler.java:743)
	9 android.os.Handler.dispatchMessage(Handler.java:95)
	10 android.os.Looper.loop(Looper.java:150)
	11 android.app.ActivityThread.main(ActivityThread.java:5546)
	12 java.lang.reflect.Method.invoke(Native Method)
	13 com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:794)
	14 com.android.internal.os.ZygoteInit.main(ZygoteInit.java:684)
	
	
## 保证工程内view的id独一无二

## 保证工程内RecyclerView的adapter类独一无二

## 保证工程内RecyclerView的LayoutManager类独一无二

	

