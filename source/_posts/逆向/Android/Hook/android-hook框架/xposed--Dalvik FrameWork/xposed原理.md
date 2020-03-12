---
title: xposed原理
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[Android Hook框架Xposed原理与源代码分析](http://www.xuebuyuan.com/2141468.html) 

# xposed #

Cydia Substrate可以修改任何主进程的代码，不管是用Java还是C/C++（native代码）编写的。

而Xposed（开源）只支持 HOOK app_process中的java函数

Xposed框架是一款可以在不修改APK的情况下影响程序运行（修改系统）的框架服务，
通过替换/system/bin/app_process程序控制zygote进程，使得app_process在启动过程中会加载XposedBridge.jar这个jar包，从而完成对Zygote进程及其创建的Dalvik虚拟机的劫持。

基于Xposed框架可以制作出许多功能强大的模块，且在功能不冲突的情况下同时运作。
此外，Xposed框架中的每一个库还可以单独下载使用，

	如Per APP Setting（为每个应用设置单独的dpi或修改权限）、
		Cydia、XPrivacy（防止隐私泄露）、
		BootManager（开启自启动程序管理应用）对原生Launcher替换图标等应用或功能均基于此框架。
	
Xposed框架是基于一个Android的本地服务应用XposedInstaller，与一个提供API 的jar文件来完成的。

# xposed安装 #

安装使用Xposed框架我们需要完成以下几个步骤：

## 安装本地服务XposedInstalle(需要root权限) ##

### [下载](http://repo.xposed.info/module/de.robv.android.xposed.installer) 安装。 ###
		
### 激活框架。 ###

点击“安装/更新”就能完成框架的激活了。

部分设备如果不支持直接写入的话，选择“安装方式”为在Recovery模式下自动安装即可

由于国内的部分ROM对Xposed不兼容，Recovery模式可能会造成设备反复重启而无法正常启动
			
安装后会启动Xposed的app_process，所以安装过程中会存在设备多次重新启动

# xposed项目编码 #

## jar包依赖 ##

- 下载API库 XposedBridgeApi-.jar。

- 复制到lib目录（注意是lib目录，不是Android提供的libs目录）
		
如果直接将jar包放置到了libs目录下，很可能会产生[错误](http://forum.xda-developers.com/xposed/xposed-api-changelog-developer-news-t2714067)： 

	“IllegalAccessError: Class ref in pre-verified class resolved to unexpected  implementation” 

估计Xposed作者在其框架内部也引用了BridgeApi，这样操作避免重复引用。
	
## Manifest设置 ##

在AndroidManifest.xml文件中meta-data配置 插件名称与Api版本号

	application  下
	<meta-data  
        android:name="xposedmodule"  
        android:value="true" />  
    
	<!-- 模块描述 载入model之后显示的描述信息-->
    <meta-data  
        android:name="xposeddescription"  
        android:value="一个登陆劫持的样例" />  
    
	<!-- 最低版本号 -->
    <meta-data  
        android:name="xposedminversion"  
        android:value="30" />  
	
## 自定义hook类 ##

	package com.example.loginhook
	public class Main implements IXposedHookLoadPackage { //加载包的时候回调  
		public void handleLoadPackage(final LoadPackageParam lpparam) throws Throwable {  
			
			// 包名不是 com.example.login 的应用 不hook
			if (!lpparam.packageName.equals("com.example.login")) return;  
			
			 // Hook MainActivity中的isCorrectInfo(String,String)方法  
			XposedHelpers.findAndHookMethod("com.example.login.MainActivity", lpparam.classLoader, "isCorrectInfo", String.class,  
            String.class, new XC_MethodHook() {  

                @Override  
                protected void beforeHookedMethod(MethodHookParam param) throws Throwable {  
                    XposedBridge.log("开始劫持了~");  
                    XposedBridge.log("参数1 = " + param.args[0]);  
                    XposedBridge.log("参数2 = " + param.args[1]);  
                }  

                @Override  
                protected void afterHookedMethod(MethodHookParam param) throws Throwable {  
                    XposedBridge.log("劫持结束了~");  
                    XposedBridge.log("参数1 = " + param.args[0]);  
                    XposedBridge.log("参数2 = " + param.args[1]);  

                }  
            });    
		}  
	}
		
## assets/xposed_init 声明主入口类. ##

这里我们的主入口类为 com.example.loginhook.Main

## 编译，安装xposed模块 ##
		
XpasedInstaller--模块选项中勾选待启用的模块让其正常的生效

重启Android设备，进入XposedInstaller查看日志模块

# 关键api #

hook主类入口接口

	void handleLoadPackage(final LoadPackageParam lpparam) hook包加载 IXposedHookLoadPackage
	void initCmdApp(StartupParam startupParam) hook java程序初始化 IXposedHookCmdInit
	void handleInitPackageResources(InitPackageResourcesParam resparam) hook包资源初始化 IXposedHookInitPackageResources
	void initZygote(StartupParam startupParam) hook Zygote初始化 IXposedHookZygoteInit

XposedHelpers hook方法等操作api

	Unhook findAndHookMethod(String className, ClassLoader classLoader, String methodName, Object... parameterTypesAndCallback)
 
		
# xposed模块模块检测

## /proc/<pid>/smaps 文件分析

进程 加载 dex，so文件 占用的内存

```
app dex maps
Pss		Rss		Size		name	other
2269 kB		11284 kB		11536 kB		/data/dalvik-cache/arm/system@framework@boot.art	
42 kB		72 kB		88 kB		/data/app/com.zy.course.dev-1/oat/arm/base.odex	
0 kB		28 kB		15556 kB		/data/app/cn.cyt.cracker007-1/oat/arm/base.odex
```	
