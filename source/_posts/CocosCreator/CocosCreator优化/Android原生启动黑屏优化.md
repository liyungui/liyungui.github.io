---
title: Android原生启动黑屏优化
date: 2019-11-01 11:30:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 背景

Cocos Creator 的打包出来的原生项目（即便是一个空白项目），打开应用后，「黑屏」一段时间才能进入到场景

视乎机型与Android系统版本，这个「黑屏」时长可能会持续不同时间，但是实际测试这个持续最短可能也要1秒，需要优化改进

# 黑屏原因

分析 `Cocos2dxActivity.onCreate` 启动流程

## Activity.setContentView前

引擎启动耗时长

## Activity.setContentView后

setContentView并没有设置任何有颜色的组件，还是黑屏状态

## 加载场景

加载场景（main.js）需要一定时间

## 总结

{% asset_img CocosCreator启动黑屏优化.png %}

主场景JS的优化方案，在 一定程度上 都是属于弱优化，因为黑屏大头在前面两个阶段，场景JS优化只能优化第三阶段的黑屏。这也是为什么空白项目打包也会出现黑屏的原因，问题不在于场景大小，js脚本复杂度，而在于 原生启动阶段

因此为了减少可变因子，我们直接以一个简单场景作为第三阶段要加载的场景

还特别需要注意一点：因为我们是探索测试，所以强烈建议采用基于 default 模板去进行操作

default 和 link 的区别：

- default，使用默认的 cocos2d-x 源码版引擎构建项目
- link，不会拷贝 cocos2d-x 源码到构建目录下，而是使用共享的 cocos2d-x 源码。这样可以有效减少构建目录占用空间，以及对 cocos2d-x 源码的修改可以得到共享。

# 优化

## 流程

### 设置Activity背景

解决第一阶段的黑屏，进入第二个阶段(setContentView)后回再次触发黑屏

通过给Activity设置主题样式，可以在样式中 `android:windowBackground`属性指定背景（纯色或者图片）

### 添加背景到contentView

解决第二阶段的黑屏

## 源码

```java
private static ImageView sSplashBgImageView = null;

/**
 * oncreate 调用 显示原生开屏背景的方法
 */
private static void showSplash() {
    sSplashBgImageView = new ImageView(sCocos2dxActivity);
    sSplashBgImageView.setImageResource(R.drawable.splash);
    sSplashBgImageView.setScaleType(ImageView.ScaleType.FIT_XY);
    sCocos2dxActivity.addContentView(sSplashBgImageView,
            new WindowManager.LayoutParams(
                    FrameLayout.LayoutParams.MATCH_PARENT,
                    FrameLayout.LayoutParams.MATCH_PARENT
            )
    );
}
    
/**
 * 这是给 JS 调用的隐藏原生开屏背景的方法
 */
public static void hideSplash() {
    sCocos2dxActivity.runOnUiThread(new Runnable() {
        @Override
        public void run() {
            if (sSplashBgImageView != null) {
                sSplashBgImageView.setVisibility(View.GONE);
            }
        }
    });
}
```

```js
@ccclass
export default class MainSceneCtrl extends cc.Component {

    start() {
        // 场景加载之后，隐藏原生纯色背景View
        // 这里延迟1秒是为了更好的体验，实际可以不用
        this.scheduleOnce(() => {
            this._hideNativeSplash();
        }, 1);
    }

    private _hideNativeSplash() {
        if (CC_JSB) {
            if (cc.sys.os == cc.sys.OS_ANDROID) {
                // 反射调用原生的隐藏方法
                jsb.reflection.callStaticMethod(
                    "org/cocos2dx/javascript/AppActivity",
                    "hideSplash",
                    "()V"
                );
            }
        }
    }
}
```

## 图片的屏幕适配问题

上面两个阶段都是设置了一张图片作为背景

Activity主题背景是通过拉升图片的方式去屏幕适配，第二阶段我们可以自定义 `ImageView.ScaleType` 来屏幕适配

然后Activity启动后进入游戏一般就会隐藏底部虚拟按键，屏幕宽高比会发生变化，只用一张固定尺寸的图片，肯定会出现适配问题

这或许就是大部分游戏开屏不设置图片的原因，而是设置 Slogan图片 + 背景色 作为启动页

## Slogan图片 + 背景色

创建一个DrawableXML文件 `app/res/drawable/splash_slogan_with_bg.xml`

使用 Android 的图层列表 LayerList生成一个 Drawable：一个纯色的矩形，在这之上放置一个 Slogan 的 Bitmap 图片

```xml
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android" >
    <!--矩形 黄色作为背景色-->
    <item >
        <shape android:shape="rectangle" >
            <solid android:color="@color/splash_slogan_bg" />
        </shape >
    </item >
    
    <!--单独的slogan图片居中显示-->
    <item >
        <bitmap
            android:gravity="center"
            android:src="@drawable/splash_slogan_small" />
    </item >
</layer-list >
```

# 参考&扩展

- [Cocos Creator Android 原生启动优化系列 1 —— 黑屏原因分析](https://www.jianshu.com/p/2df139d48539)
- [Cocos Creator Android 原生启动优化系列 2 —— 自定义启动页](https://www.jianshu.com/p/21d269c8ef09)
- [Splash适配解决启动图拉伸的问题](https://blog.csdn.net/aa464971/article/details/86692198
)
- [Android启动页优化，去黑屏实现秒启动](https://www.jianshu.com/p/662274d5d637)
- [Android性能优化之启动优化](https://juejin.im/post/5ce8daa95188250ae716e1c2)
- [Android 性能优化—— 启动优化提升60%](https://mp.weixin.qq.com/s/OWImTj_4Ml1nmpN2v9mRAw)