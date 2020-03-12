---
title: ANR定位分析
date: 2020-01-07 15:08:53
categories:
  - Android
tags:
  - 性能优化
---

ANR问题很难定位

ANR是耗时操作造成

# ANR类型

## KeyDispatchTimeout

主要类型

按键或触摸事件在特定时间(5s)内无响应

## BroadcastTimeout

BroadcastReceiver在特定时间((10s)内无法处理完成

## ServiceTimeout

小概率类型

Service在特定时间((20s)内无法处理完成

# ANR基本定位--trace文件，定位不准 #

根据trace文件定位ANR未必能准确，trace只能够确定发生ANR的位置，但只是压死骆驼的最后一根稻草。

若有A/B/C事件串行执行于UI线程，当C事件发生ANR时，说明A->B->C太耗时了，并不能确定耗时操作在哪个具体事件上。

trace文件路径：data\anr\traces_packageName.txt

下面的"main"指的是主线程，我们分析"main"所在的片段即可定位ANR。

	"main" prio=5 tid=1 SUSPENDED
	  | group="main" sCount=2 dsCount=1 obj=0x94c48bd8 self=0xb79a2500
	  | sysTid=3319 nice=0 sched=0/0 cgrp=[fopen-error:2] handle=-1217108224
	  | state=S schedstat=( 0 0 0 ) utm=238 stm=2439 core=1
	  at com.xuehu365.xuehu.utils.XueHuVideoView.setVideoPlayRecord(XueHuVideoView.java:~244)
	  at com.xuehu365.xuehu.utils.XueHuVideoView.videoStart(XueHuVideoView.java:184)
	  at com.xuehu365.xuehu.utils.XueHuVideoView.onClick(XueHuVideoView.java:264)
	  at com.xuehu365.xuehu.utils.XueHuVideoView$$ViewBinder$1.doClick(XueHuVideoView$$ViewBinder.java:26)
	  at butterknife.internal.DebouncingOnClickListener.onClick(DebouncingOnClickListener.java:22)

# ANR辅助定位——BlockCanary #

BlockCanary工具却能**统计过程中所有耗时操作**(耗时阈值由自己设置)。

**原理**比较简单，通过**替换Looper的Printer达到计算msg处理的耗时**。

同时也提供了一些很有帮助的参数，譬如总耗时与线程耗时，可用内存等。

# ANR辅助定位——埋点 #

方法内多次调用同一耗时操作，那么就果断埋点吧！确定是哪次操作真正耗时

通过埋点统计操作用时，即可更准确定位耗时操作。

# 多次采样确定ANR耗时操作 #

ANR不好复现，耗时操作的耗时也不稳定，通过多次采样来确定耗时操作已经是通用方案了。

若是层级较深或复杂操作才能触发耗时操作的，推荐使用iTestin工具进行自动化测试。

# 参考&扩展

- [Android ANR 分析解决方法](https://www.cnblogs.com/purediy/p/3225060.html)