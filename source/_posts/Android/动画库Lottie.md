---
title: 动画库Lottie
date: 2018-09-06 16:18:53
tags: 
	- Android
	- 动画
---

Lottie 是一个可以解析AE( Adobe After Effects )上的插件Bodymovin导出的json文件(依赖png文件)实现在移动设备上渲染的动画库。

**高效，文件体积小，展示效果好**。比gif体积小，效果好(AE导出gif有白边)

支持 Android（Jellybean/API16 及以上）和 ios

[github](https://github.com/airbnb/lottie-android)

[官方文档](http://airbnb.io/lottie/android/android.html)

# 基本使用 #

## 添加依赖 ##

	compile 'com.airbnb.android:lottie:2.6.0'

## xml ##
	
	<com.airbnb.lottie.LottieAnimationView
     android:id="@+id/animation_view"
     android:layout_width="wrap_content"
     android:layout_height="wrap_content"
     app:lottie_fileName="hello-world.json"
     app:lottie_loop="true"
     app:lottie_autoPlay="true" />
    
## 资源目录 ##
 
 Lottie animations can load animations from:

- A json animation in src/main/res/raw.
- A json file in src/main/assets.
- A zip file in src/main/assets. See images docs for more info.
- A url to a json or zip file.
- A json string. The source can be from anything including your own network stack.
- An InputStream to either a json file or a zip file.

依赖图片存放目录

- src/main/assets/image. image可以是其他名字

示例json文件放于 raw 目录，图片放于 assets/image

## 设置依赖图片目录 ##

**必须设置**，否则报错

	LottieAnimationView.setImageAssetsFolder("image/");

至此，动画**成功显示**在界面上了

## API控制 ##

	LottieAnimationView.setMinAndMaxFrame(0, 34);
	
	LottieAnimationView.setRepeatCount(0);
		0，表示不重复
		LottieDrawable.INFINITE，无限重复
		
	
	LottieAnimationView.playAnimation();//播放动画
	LottieAnimationView.addAnimatorListener(Animator.AnimatorListener）//监听动画状态



