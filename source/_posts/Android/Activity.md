---
title: Activity
date: 2019-10-16 14:13:53
categories:
  - Android
tags:
	- Android
---

# 全屏

设置在setContentView()方法之前

```java
//无title    
requestWindowFeature(Window.FEATURE_NO_TITLE);    
//全屏    
getWindow().setFlags(WindowManager.LayoutParams. FLAG_FULLSCREEN , WindowManager.LayoutParams. FLAG_FULLSCREEN);
```

# 背景透明

- Activity使用自定义透明背景style
- Activity布局根view使用默认(不要设置)

```xml
android:theme="@style/activity_Transparent"
```

```xml
<style name="activity_Transparent" >
    <item name="android:windowBackground">@color/translucent</item>
    <item name="android:windowNoTitle">true</item>
    <item name="android:windowFullscreen">true</item>
    <item name="android:windowIsTranslucent">true</item>
    <item name="android:windowCloseOnTouchOutside">false</item>
    <item name="android:colorBackgroundCacheHint">@null</item>
    <item name="android:windowAnimationStyle">@android:style/Animation.Translucent</item>
</style>
```

```xml
<color name="translucent">#00000000</color>
```





