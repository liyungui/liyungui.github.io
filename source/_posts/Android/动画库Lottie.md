---
title: 动画库Lottie
date: 2018-09-06 16:18:53
tags: 
	- Android
	- 动画
---

Lottie 是一个可以解析AE( Adobe After Effects )上的插件Bodymovin导出的json文件(依赖png文件)实现在移动设备上渲染的动画库。

优点：

**开发高效，文件体积小，展示效果好，性能消耗小，控制灵活，服务器更新动画，跨平台**。比gif体积小，效果好(AE导出gif有白边)，可以重复播放指定帧指定次数

缺陷：

系统版本有要求。支持 Android(Jellybean/API16 及以上)，ios(8.0)，RN

不支持交互动画。只能播放类型动画

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

```java
LottieAnimationView.setMinAndMaxFrame(0, 34);

LottieAnimationView.setRepeatMode(LottieDrawable.RESTART);
LottieAnimationView.setRepeatCount(0);
	//0，表示不重复
	//LottieDrawable.INFINITE，无限重复
	
	
LottieAnimationView.playAnimation();//播放动画

LottieAnimationView.addAnimatorListener(Animator.AnimatorListener）//监听动画状态
LottieAnimationView.removeAllAnimatorListeners();

LottieAnimationView.addAnimatorUpdateListener(ValueAnimator.AnimatorUpdateListener)//监听播放进度
LottieAnimationView.removeAllUpdateListeners() //慎用，会导致动画无法播放
LottieAnimationView.removeUpdateListener(ValueAnimator.AnimatorUpdateListener)

//播放进度回调中
animation.getAnimatedValue() 返回进度[0,1]
animation.getAnimatedFraction() 返回进度[minFrame,maxFrame]。如果没设置，也是返回[0,1]
```
# 注意事项

- 可能会v4包冲突
		
	移除lottie的v4包
		
			compile ("com.airbnb.android:lottie:2.6.1"){exclude group: "com.android.support.v4"}
			
- 保持v7依赖的版本为27

	v7的24版本带的v4包，找不到 android.support.v4.util.ArraySet

# 缩放

会自动将AE中的px转为dp，大部分都能保持一致

如果尺寸不是很合适，有两个解决方案

## scaleType

`LottieAnimationView ` 继承了ImageView scaleType

## Scaling Up/Down

`LottieAnimationView` 和 `LottieDrawable` 支持`setScale(float)` 按比例缩放

**注意：不要重复调用**

```java
lottieAnimationView.setScale(1 / mContext.getResources().getDisplayMetrics().density);
```

# 卡顿问题

全屏动画卡顿问题特别严重

```java
//硬件加速，开启之后瞬间丝滑
animationView.useHardwareAcceleration(true);

//合并路径 默认是关闭的，根据自己需求调整
animationView.enableMergePathsForKitKatAndAbove(true);
```

# 回收图片资源的时机

- 设置图片资源
- onDetachedFromWindow；即设置可见性为gone，且把view remove

```java
---LottieAnimationView---
@Override protected void onDetachedFromWindow() {
  if (isAnimating()) {
    cancelAnimation();
    wasAnimatingWhenDetached = true;
  }
  recycleBitmaps();
  super.onDetachedFromWindow();
}
  
@Override public void setImageResource(int resId) {
  recycleBitmaps();
  cancelLoaderTask();
  super.setImageResource(resId);
}
  
@VisibleForTesting void recycleBitmaps() {
  // AppCompatImageView constructor will set the image when set from xml
  // before LottieDrawable has been initialized
  if (lottieDrawable != null) {
    lottieDrawable.recycleBitmaps();
  }
}
---LottieDrawable---
public void recycleBitmaps() {
  if (imageAssetManager != null) {
    imageAssetManager.recycleBitmaps();
  }
}
--ImageAssetManager
public void recycleBitmaps() {
  synchronized (bitmapHashLock) {
    for (Map.Entry<String, LottieImageAsset> entry : imageAssets.entrySet()) {
      LottieImageAsset asset = entry.getValue();
      Bitmap bitmap = asset.getBitmap();
      if (bitmap != null) {
        bitmap.recycle();
        asset.setBitmap(null);
      }
    }
  }
}
```