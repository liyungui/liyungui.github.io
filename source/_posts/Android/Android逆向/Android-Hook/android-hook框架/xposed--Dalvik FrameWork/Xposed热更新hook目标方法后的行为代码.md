---
title: Xposed热更新hook目标方法后的行为代码
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[Xposed热更新 hook目标方法后的行为代码](https://github.com/githubwing/HotXposed)

无法更新hook的目标，但可以更新hook目标后的行为。

比如 hook Activity的onCreate方法，toast Activity名称改为 logcat 打印Activity名称

# 原理 #

参考android里classloader实现，发现findClass()最后都是调用了DexFile来loadClass。把需要写的逻辑代码单独放到一个dex里，然后使用DexFile加载

读取/sdcard/classes.dex文件，直接导入Hotfix类，调用他的invoke方法

{% asset_img DexFile-loadClass.jpg %}

{% asset_img DexFile-loadClass-2.jpg %}
