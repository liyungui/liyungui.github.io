---
title: Android动态运行时权限
date: 2019-01-30 10:53:53
categories:
  - Android
tags: 
	- Android
---

# 运行时申请权限

## 新权限模型

权限分为：

- 普通权限 `AndroidManifest.xml`文件中直接添加权限即可
- 危险权限 动态获取权限

**危险权限分为9组24种**

{% asset_img 危险权限.png %}

## 两个条件

- 项目TargetSDKVersion >=23
- 手机系统 Android 6.0 以上

直接访问权接导致app崩溃

### targetSdkVersion 说明

1. targetSdkVersion版本号<= 22时，不需要动态处理权限 。但有时应用程序会打不开。
2. 如果是之前的老版本升级上来的，系统会默认开启之前所有的权限。

	比如之前的targetSdkVersion是21，后来升级之后变成了25，这个时候系统会自动授权。
	
	一定要是升级变成的25，否则还是需要授权。

## 申请流程

- 检测是否有权限 `ContextCompat.checkSelfPermission()`
- 有权限，直接使用
- 无权限，请求权限 `ActivityCompat.requestPermissions()`
	- 根据需要设置权限说明

		`ActivityCompat.shouldShowRequestPermissionRationale()`
	- Activity中获取回调结果 
	
		重写 `onRequestPermissionsResult()` 
		
# 需求

1. 运行时申请
2. 支持单个权限、多个权限申请
3. 无侵入式申请，无需关注权限申请的逻辑
4. 除了Activity、Fragment之外，还需要支持Service中申请
5. 对国产手机做兼容处理

1和2，Google都有对应的API

3 可以通过自定义注解+AOP切面方式来解决

4 通过一个透明的Activity去申请权限，并且把申请结果返回来。Google提供的API只支持在Activity和Fragment中去申请权限

5 国产安卓手机碎片化比较严重，特殊处理


# 流行的三方库

|权限库|	是否使用注解|	是否支持链式调用|	是否支持Service|是否适配国产机|
|---|---|---|---|---|
|RxPermissions|	No|	Yes 基于RX的思想	|No |	No|
|PermissionsDispatcher|	Yes 编译时注解|	No|	No	|适配了小米|

# 设计

## 概念定义

- **申请权限**：弹出系统权限弹窗 `@NeedPermission`
- **权限被拒绝**：用户没有给权限，并且选中不再提示 `@PermissionCanceled`
- **权限被取消**：用户没有给权限，但是没有选中不再提示 `@PermissionDenied` 

注解都是声明在Method级别上的。

## 整体思路

在我们的Activity、Fragment及Service中声明注解，然后在AOP中解析我们的注解，并把申请的权限传递给一个透明的Activity去处理，并把处理结果返回来。

{% asset_img 整体思路.png %}

## 可能会遇到的问题

1. 不同型号的手机兼容问题（申请权限、跳设置界面）
2. AOP解析注解以及传值问题

# 国产手机兼容

## 兼容问题

1. 无法弹出权限申请对话框 `ActivityCompat.shouldShowRequestPermissionRationale(Activity, String)` 
2. 用户点击拒绝授权，却回调权限申请成功方法
3. 只能弹出一次权限申请，拒绝后就无法再弹出权限申请对话框

## 跳转到系统设置页面或者手机管家界面

权限申请对话框不再弹出时，跳转到系统设置页面或者手机管家界面

国产手机各个设置界面不一样，用通用的API跳转不到相应的APP设置界面，Aopermission采用了策略模式

{% asset_img 跳转到设置页.png %}

如需做兼容，只需要在库里修改，调用方是不需要处理的。

跳转到设置界面调用如下

```java
SettingUtil.go2Setting(this);
```

[Aopermission](https://github.com/crazyqiang/Aopermission) AOP方式封装的6.0运行时申请权限库

[permissions4m](https://github.com/jokermonn/permissions4m) 国产 Android 权限申请最佳适配方案。支持国产手机 5.0 权限申请。年久失修