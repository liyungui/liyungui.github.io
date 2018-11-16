---
title: Android Support Library详细介绍
date: 2018-11-15 10:48:25
tags: Android
---

[参考](https://www.jianshu.com/p/a5aa5f209895)

	com.android.support:support-v4 v4包
	com.android.support:support-compat v4 compat包
	com.android.support:appcompat-v7 v7 compat包
# 为什么提供

- 向后兼容
- 提供不适合打包进framework的功能
	- Android官方对App开发提供了推荐设计，希望Android应用都有相对一致的交互设计来减少用户的使用成本，希望三方App类似系统应用从而完美融入到Android生态系统中。但是这都仅仅是推荐，不要求开发者一定要这样，如果有这种需求就可以使用官方支持包提供的这些功能，避免重复造轮子。如支持包中的DrawerLayout、Snackbar等类都是这种情况。
- 支持不同形态的设备
	- 通过使用支持包来在不同形态设备上提供功能，如手机、电视、可穿戴设备等。

各个依赖包可以在 `<sdk>/extras/android/support/`文件夹下查看，如果该路径下没有，打开SDK Tools更新SDK即可。

# V4 Support Libraries


## 引入整个v4包

	com.android.support:support-v4

Android Support Library **24.2.0**及之后的版本中，为了增强效率和减小APK的大小起见，Android将V4包**拆分成5个包**

- v4 compat library `compile 'com.android.support:support-compat:24.2.1'`
- v4 core-utils library `compile 'com.android.support:support-core-utils:24.2.1'`
- v4 core-ui library `compile 'com.android.support:support-core-ui:24.2.1'`
- v4 media-compat library `compile 'com.android.support:support-media-compat:24.2.1'`
- v4 fragment library `compile 'com.android.support:support-fragment:24.2.1'`
	跟fragment相关部分，V4这个子库依赖了其他4个子库，所以我们一旦依赖这个库就会自动导入其他4个子库

考虑到V4的向后兼容，工程中依赖V4这个依赖包时默认是包含拆分后的5个包的

为了节省APK大小，建议在开发过程中根据实际情况依赖对应的V4包，移除不必要的V4包。

拆包并不一定代表能够真的解决问题，V4各子包的依赖关系如下，可见即使拆包之后，要用到V4中的某个API时，依赖包并没有减小多少：

{% asset_img v4包依赖关系.png %}

# V7 Support Libraries

最初发布时就以各个独立库的形式发布的。

## v7 appcompat library
这个包支持对Action Bar接口的设计模式、Material Design接口的实现等，核心类有ActionBar、AppCompatActivity、AppCompatDialog、ShareActionProvider等，在AS中的依赖方式如下：

    compile 'com.android.support:appcompat-v7:24.2.1'
注意：这个包需要依赖android-support-v4。

## v7 cardview library
支持cardview控件，使用Material Design语言设计，卡片式的信息展示，在电视App中有广泛的使用，在AS中的依赖方式如下：

    compile 'com.android.support:cardview-v7:24.2.1'
## v7 gridlayout library
一个支持GridLayout布局的support包，在AS中的依赖方式如下：

    com.android.support:gridlayout-v7:24.2.1
## v7 mediarouter library
一个用于设备间音频、视频交换显示的support包，在AS中的依赖方式如下：

    com.android.support:mediarouter-v7:24.2.1
## v7 palette library
该库提供了palette类，使用这个类可以很方便提取出图片中主题色。比如在音乐App中，从音乐专辑封面图片中提取出专辑封面图片的主题色，然后将播放界面的背景色设置为封面的主题色，随着播放音乐的改变，播放界面的背景色也会巧妙的跟着改变，从而提供更好的用户体验。，在AS中的依赖方式如下：

    com.android.support:palette-v7:24.2.1
## v7 recyclerview library
核心类是RecyclerView，用于替换ListView、GridView，具体可以查阅RecyclerView方面的资料，在AS中的依赖方式如下：

    com.android.support:recyclerview-v7:24.2.1
## v7 Preference Support Library
一个用于支持各种控件存储配置数据的support包，比如CheckBoxPreference和ListPreference，在AS中的依赖方式如下：

    com.android.support:preference-v7:24.2.1

# V8 Support Library
V8 Support Library支持的最低SDK版本是Android 2.3即API Level 9。

## v8 renderscript library
一个用于渲染脚本的support包，在AS中按照如下方式配置即可正常使用：

    defaultConfig {
        renderscriptTargetApi 18
        renderscriptSupportModeEnabled true
    }
# V13 Support Library
这个包的作用主要是为Android3.2（API Level 13）及以上的系统提供更多地Framgnet特性支持，使用它的原因在于，android-support-v4中虽然也对Fragment做了支持，由于要兼容低版本，导致他是自行实现的 Fragment 效果，在高版本的 Fragment 的一些特性丢失了，而对于 v13以上的 sdk 版本，我们可以使用更加有效，特性更多的代码，在AS中的依赖方式如下：

    com.android.support:support-v13:24.2.1
# Multidex Support Library
该support包用于使用多dex技术编译APP，当一个应用的方法数超过65536个时需要使用multidex配置，关于multidex的更多信息，可以参见如何编译超过65K方法数的应用，在AS中的依赖方式如下：

    compile 'com.android.support:multidex:1.0.0'
# Annotations Support Library
一个支持注解的support包，在AS中的依赖方式如下：

    compile 'com.android.support:support-annotations:24.2.1'
# Design Support Library
一个用于支持Design Patterns的support包，它提供了Material Desgin设计风格的控件，在AS中的依赖方式如下：

    com.android.support:design:24.2.1
# Custom Tabs Support Library
一个提供了在应用中添加和管理custom tabs的support包，在Google IO 2015中有介绍，在AS中的依赖方式如下：

    compile 'com.android.support:customtabs:24.2.1'
# Percent Support Library
一个提供了百分比布局的support包，通过这个包可以实现百分比布局，在AS中的依赖方式如下：

    com.android.support:percent:24.2.1

# AndroidX

如果使用support为27.1.1的相关依赖库时。可能需要所有相关的support 库都为27.1.1。如果其中有bug的话，可能需要所有的都去升级，存在一个绑定关系，而且正式版的发布周期也很长。

通过AndroidX，可以**实时**实现特性和修复bug，升级**个别**依赖，不需要对使用的所有其他库进行更新。

为了给开发者一定迁移的时间，所以28.0.0的稳定版本还是采用android.support。但是所有后续的功能版本都将采用androidx。

## 迁移

Android Studio 3.2 Canary中添加了一键迁移的功能 `Refactor -> Migrate to AndroidX`

首先你的gradle版本至少为3.2.0以上，以及compileSdkVersion为28以上。

	classpath 'com.android.tools.build:gradle:3.2.0+'

如果你是一个新项目，如果使用AndroidX相关依赖，需要在gradle.properties文件里添加配置：

	android.useAndroidX=true
	android.enableJetifier=true

如果你想使用AndroidX，但是之前的不迁移，可以这样配置：

	android.useAndroidX=true
	android.enableJetifier=false

# 常见问题
## 找不到 android.support.v4.util.ArraySet

指定v7版本为27。24版本是的v7包中的v4是没有该类的

## 找不到 android.support.v4.animation.AnimatorCompatHelper

在support包 24,25都有

在support包26的时候这个类没有了。

网上的修复方案：

	configurations.all {
	    resolutionStrategy.eachDependency { DependencyResolveDetails details ->
	        def requested = details.requested
	        if (requested.group == 'com.android.support') {
	            if (!requested.name.startsWith("multidex")) {
	                details.useVersion '24.1.0'
	            }
	        }
	    }
	}
	
由于项目需要27的一些类，不能改低版本

**解决方案：复制相关类**

建包 android.support.v4.animation（在目录 main->java 文件夹下开始建包名）

在电脑中安装的sdk的目录下搜索 AnimatorCompatHelper，右键，跳转到所在文件夹，复制所有相关java文件到刚刚新建的文件包下即可

