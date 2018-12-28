---
title: BadTokenException异常修复
date: 2018-11-20 15:12:53
tags: 
	- Android
---

	android.view.WindowManager$BadTokenException
	
	解决方案
	该异常表示不能添加窗口，通常是所要依附的view已经不存在导致的。
	[解决方案]：Dialog&AlertDialog，WindowManager不能正确使用时，经常会报出该异常，原因比较多，几个常见的场景如下：
	1.上一个页面没有destroy的时候，之前的Activity已经接收到了广播。如果此时之前的Activity进行UI层面的操作处理，就会造成crash。UI层面的刷新，一定要注意时机，建议使用set_result来代替广播的形式进行刷新操作，避免使用广播的方式，代码不直观且容易出错。
	2.Dialog在Actitivty退出后弹出。在Dialog调用show方法进行显示时，必须要有一个Activity作为窗口的载体，如果Activity被销毁，那么导致Dialog的窗口载体找不到。建议在Dialog调用show方法之前先判断Activity是否已经被销毁。
	3.Service&Application弹出对话框或WindowManager添加view时，没有设置window type为TYPE_SYSTEM_ALERT。需要在调用dialog.show()方法前添加dialog.getWindow().SetType(WindowManager.LayoutParams.TYPE_SYSTEM_ALERT)。
	4.6.0的系统上, (非定制 rom 行为)若没有给予悬浮窗权限, 会弹出该问题, 可以通过Settings.canDrawOverlays来判断是否有该权限.
	5.某些不稳定的MIUI系统bug引起的权限问题，系统把Toast也当成了系统级弹窗，android6.0的系统Dialog弹窗需要用户手动授权，若果app没有加入SYSTEM_ALERT_WINDOW权限就会报这个错。需要加入给app加系统Dialog弹窗权限，并动态申请权限，不满足第一条会出现没权限闪退，不满足第二条会出现没有Toast的情况。
	

