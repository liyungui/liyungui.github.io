---
title: 自定义Activity背景-奇葩的启动页实现方式
date: 2019-01-17 19:27:53
categories:
  - Android
tags: 
	- Android
---

接受一个单Activity多View栈架构的APP，需要修改splash启动页。找了很久的代码，没有定位到关键实现。最后用笨方法，找对启动页图片的引用，发现是通过自定义Activity背景的方法实现。

一般APP的Activity很快就会展示出来，很难展示出背景图片

该APP有三个特性：

- 使用RN混合开发
- RN热更新
- 首页就是RN页面

所以首页出来时间较久，跟常规启动页效果一样

`splash.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">

    <item
        android:drawable="@color/white"/>

    <item>
        <bitmap
            android:gravity="center|fill_vertical|fill_horizontal"
            android:src="@mipmap/ic_splash"/>
    </item>

</layer-list>
```

无法设置宽高，通过 `center|fill_vertical|fill_horizontal` 实现图片居中完全展示

`styles.xml`

```xml
<style name="Default" parent="AppTheme.NoActionBar">
    <item name="android:windowBackground">@drawable/splash</item>
</style>
``` 

`AndroidManifest.xml`

```xml
<activity
	android:name="com.shensz.course.module.main.activity.MainActivity"
    android:configChanges="keyboardHidden|orientation|screenSize"
    android:launchMode="singleTask"
    android:screenOrientation="portrait"
    android:theme="@style/Default"
    android:windowSoftInputMode="adjustPan">