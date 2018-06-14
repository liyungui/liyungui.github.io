---
title: VirtualApp
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[VirtualHook: 基于VirtualApp的Java代码hook工具](http://bbs.pediy.com/thread-216786.htm)

在ART模式下安装Xposed，不仅要求root权限，而且需要替换大量的系统库，因此其使用门槛大幅提高。

# 基本原理 #

[VirtualHook](https://github.com/rk700/VirtualHook)是基于以下两个框架实现的：

1. **VirtualApp**，这是一套插件框架，允许应用以插件的方式运行在其构造的虚拟空间中，而无需实际安装应用。**通过VirtualApp实现非root环境下注入窗口的添加**
2. **YAHFA**，这是一套hook框架，实现了ART环境下的Java方法hook

## [VirtualApp](https://github.com/asLody/VirtualApp) ##

hook就是在应用运行过程中，注入外部的代码，从而改变原有的执行流程。

因此，应用中必须存在注入代码的窗口。

Xposed便是这样做的：它修改了系统库，对所有应用在启动时添加了注入窗口。但是，这就需要具有root权限。

[VirtualApp的工作原理](http://rk700.github.io/2017/03/15/virtualapp-basic/)简而言之，它通过代理常用系统服务的方式，在系统服务层与应用层之间添加了一层虚拟空间，从而允许在不安装应用的情况下运行应用。特别地，VirtualApp本身并不需要root权限。

利用VirtualApp提供的虚拟空间，我们就可以实现很多事情了。应用启动时，会初始化Application，此时会在应用所在的进程中调用bindApplication()。而VirtualApp重写了相关代码，那么我们就可以在把注入代码的窗口放在这里，从而实现应用启动时，加载外部的hook代码。

所以，本文所说的非root权限hook应用，更准确来说，hook的是在VirtualApp中运行的应用。

## [YAHFA (Yet Another Hook Framework for ART)](https://github.com/rk700/YAHFA) ##

我们调研了几款hook框架，包括Xposed, AndFix和Legend，但发现如果在这里使用的话，多少都存在一定的问题：

1. Xposed需要进行大量的代码变更，过于复杂，而且方法执行的额外开销会增多
2. [AndFix](https://github.com/alibaba/AndFix)的代码量相对较小，但其进行了方法的全部替换，不支持原方法的调用；对于热修复来说也许影响不大，但对于逆向分析来说，很多时候我们是通过hook来插桩，所以原方法必须要备份以执行
3. [Legend](https://github.com/asLody/legend)与AndFix的实现方式基本一致，但试用后发现存在某些方法解析失败的问题

于是，我们重新设计实现了一套hook框架YAHFA，专门用于这里的代码hook。[关于YAHFA的具体工作原理，可见这篇介绍](http://rk700.github.io/2017/03/30/YAHFA-introduction/)。

至此，我们有了插件框架和hook框架，将其简单地集成，便得到了最终的hook工具，VirtualHook。其具有如下优点：

1. 支持ART模式，事实上也只支持ART，因为这就是其设计的出发点，DVM模式下用Xposed就OK了。
2. 无需root权限。由于我们是通过VirtualApp为应用添加代码注入窗口，所以不需要修改系统本身的库，因此不需要root权限，安装难度降低。
3. 轻量。YAHFA的工作目标，就是高效地运行hook。hook方法执行所带来的额外开销仅有2、3条机器指令，执行原方法时甚至没有额外的开销。
4. 方便。由于是在VirtualApp中完成hook，因此添加或删除hook插件后，不需要像Xposed那样重启设备，只需要退出目标应用再重新进入即可。
5. 精细。理论上来说，可以加载多个hook插件，甚至对不同应用使用不同hook插件。配合VirtualApp应用多开，能够更精细地控制hook的行为。

# 使用 #

将hook apk保存到设备SD卡的指定位置 `/sdcard/io.virtualhook/patch.apk` 以待加载。

随后启动VirutalHook，在VirutalHook中 添加并运行应用。

# 其他说明 #

由于VirtualHook是VirtualApp与YAHFA的集成，因此其适用范围就是两者的交集：目前支持的系统是**Android 5.1和6.0**，支持的架构是**armeabi和x86**。由于VirtualHook的**出发点是便于安全研究**，因此适配度不是其考虑的主要问题

特别地，对于加固应用的hook，目前使用上述的demoHookPlugin试验了360，腾讯，梆梆和爱加密。除了梆梆之外，其他加固的应用均可被hook（爱加密把非错误的日志打印全部重定向了，所以必须通过Log.e()打印日志）。**梆梆加固的应用，在VirtualApp上无法运行**，因此作为其下游的VirtualHook，目前对梆梆加固的应用也无法使用。希望能够有人研究解决这一问题。

VirtualApp中自带了对native方法进行hook的功能，看雪上已经有利用该功能进行应用脱壳的实践了。后续可以将native hook一并整合起来，使VirtualHook的功能更强大