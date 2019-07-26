---
title: setVisibility不起作用
date: 2019-07-04 17:40:53
categories: 
	- Android
tags: 
	- Android
---

# 控件本身正在执行动画

解决方案：view.clearAnimation()

# 控件还在使用当中

比如设置点击某个ViewGroup的子View后，让改ViewGroup 消失。就极有可能导致setVisibility 无效

解决方案：利用Handler.post()发送 setVisibility任务

# 设备性能问题

方案一：

利用Handler.post()发送 setVisibility任务

这个方法同样适用于**动画不生效等其他UI异常**

方案二：重新加载，即重新构造。

setVisibility 后 调用view.invalidate()或者view.postinvalidate()；

如果也不行，直接调用自身的requestLayout或者其父容器的requestLayout()进行强制的界面即时刷新重构;



