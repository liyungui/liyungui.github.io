---
title: Android ProGuard 混淆
date: 2019-07-10 18:36:53
categories: 
	- Android
tags: 
	- Android
---	

# ProGuard作用

**压缩**（Shrinking）：默认开启，用以减小应用体积，移除未被使用的类和成员，并且会在优化动作执行之后再次执行（因为优化后可能会再次暴露一些未被使用的类和成员）。

	-dontshrink 关闭压缩

**优化**（Optimization）：默认开启，在字节码级别执行优化，让应用运行的更快。

	-dontoptimize  关闭优化
	-optimizationpasses n 表示proguard对代码进行迭代优化的次数，Android一般为5

**混淆**（Obfuscation）：默认开启，增大反编译难度，类和类成员会被随机命名，除非用keep保护。

	-dontobfuscate 关闭混淆

# 开启混淆

app module 的 build.gradle中minifyEnabled设置为true

# 混淆规则文件

app module
	
`proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'`

lib module

`consumerProguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'`

特别注意：lib module 一定要使用 consumerProguardFiles；否则混淆规则是不生效的

以`consumerProguardFiles`方式加入的混淆具有以下特性：

- *.pro文件会包含在aar文件中（aar混淆规则，对应用程序无效）
- 这些pro配置会在应用程序开启混淆的时候被使用
- 混淆配置对使用者透明，特别方便

# stacktrace的恢复

retrace脚本 `./tools/proguard/bin/retrace.sh`

mapping映射表 `./app/build/outputs/mapping/release/mapping.txt`

# 哪些不应该混淆

## 反射中使用的元素 

属性,方法,类,包名等

## 序列化与反序列化 

解决方案：

	1. 将序列化和反序列化的类排除混淆
	2. 使用@SerializedName注解字段

## 枚举 

## 泛型 

## 注解 

## 四大组件 

## jni调用的java方法 
## java的native方法 
## js调用java的方法 

## 第三方库不建议混淆 

# dontwarn指令

关闭警告。

引入的library可能存在一些无法找到的引用和其他问题,在build时可能会发出警告,如果我们不进行处理,通常会导致build中止.因此为了保证build继续,我们需要使用dontwarn处理这些我们无法解决的library的警告.

`-dontwarn com.twitter.sdk.** # 关闭Twitter sdk的警告`

# keep指令

|保留内容/作用域|	防止被移除或者被重命名|	防止被重命名(后缀names)|
| --- | --- | --- |
|类和类成员|	-keep|	-keepnames|
|仅类成员|	-keepclassmembers|	-keepclassmembernames|
|如果拥有某成员，保留类和类成员|	-keepclasseswithmembers|	-keepclasseswithmembernames|

移除是指在压缩(Shrinking)时是否会被删除。

# 指令对象

## `class`

# 指令对象属性

## `包名.*`

本包下的，不包括子包下

`-keep class cn.hadcn.test.*   `

## `包名.**`

本包和所含子包下的

`-keep class cn.hadcn.test.**  `

## `* extend` `* implement`

子类/实现类

`-keep public class * extends android.app.Activity  `

## `{*;}`

类的所有内容

`-keep class cn.hadcn.test.* {*;}  `

## 类的部分内容

保护类的特定内容不被混淆

	<init>;     //匹配所有构造器
	<fields>;   //匹配所有域
	<methods>;  //匹配所有方法方法

	还可以在<fields>或<methods>前面加上private 、public、native、注解 等来进一步指定不被混淆的内容

	-keep class cn.hadcn.test.One {
	    public <methods>;
	} One类下的所有public方法都不会被混淆

	-keep class cn.hadcn.test.One {
	   public <init>(org.json.JSONObject);
	} 参数为JSONObject的构造函数不会被混淆

	-keepclasseswithmembernames class * { # 保持native方法不被混淆    
	    native <methods>;
	}

	-keep class * implements Android.os.Parcelable { # Parcelable的子类和Creator静态成员变量不混淆       
	    public static final Android.os.Parcelable$Creator *;
	}

	-keepclassmembers enum * {  # 以下两个方法会被反射调用
	    public static **[] values();  
	    public static ** valueOf(java.lang.String);  
	}

	-keepclassmembers class cc.ninty.chat.ui.fragment.ScriptFragment$JavaScriptInterface {
		public *;
	}  # 保持ScriptFragment内部类JavaScriptInterface中的所有public内容不被混淆
	
	-keepclassmembers class ** {
	    @com.squareup.otto.Subscribe public *;
	    @com.squareup.otto.Produce public *;
	} # 保留使用了注解的成员


# 混淆配置模板

混淆分为2个主要部分

**定制化区域**。这里边的内容是我们主要需要补充的部分，大致分为4个小部分，主要是补充这4个部分的东西。

**基本不用动区域**。顾名思义，除非有特殊的需求，基本不用改动。

	#-------------------------------------------定制化区域----------------------------------------------
	#---------------------------------1.实体类---------------------------------
	
	
	
	#-------------------------------------------------------------------------
	
	#---------------------------------2.第三方包-------------------------------
	
	
	
	#-------------------------------------------------------------------------
	
	#---------------------------------3.与js互相调用的类------------------------
	
	
	
	#-------------------------------------------------------------------------
	
	#---------------------------------4.反射相关的类和方法-----------------------
	
	
	
	#----------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------
	
	#-------------------------------------------基本不用动区域--------------------------------------------
	#---------------------------------基本指令区----------------------------------
	-optimizationpasses 5 # 代码混淆的压缩比例，值在0-7之间
	-dontusemixedcaseclassnames # 混淆后类名不区分大小写（即只用小写）
	-dontskipnonpubliclibraryclassmembers # 不忽略非公共的库的类
	-dontskipnonpubliclibraryclassmembers # 不忽略非公共的库的类的成员
	-dontpreverify # 不做预校验的操作
	-printmapping proguardMapping.txt # 生成映射文件
	-optimizations !code/simplification/cast,!field/*,!class/merging/* # 指定混淆是采用的算法
	-keepattributes *Annotation*,InnerClasses # 不混淆Annotation
	-keepattributes Signature # 不混淆泛型
	-keepattributes SourceFile,LineNumberTable # 保留代码文件名和行号
	#----------------------------------------------------------------------------
	
	#---------------------------------默认保留区---------------------------------
	-keep public class * extends android.app.Activity
	-keep public class * extends android.app.Application
	-keep public class * extends android.app.Service
	-keep public class * extends android.content.BroadcastReceiver
	-keep public class * extends android.content.ContentProvider
	-keep public class * extends android.app.backup.BackupAgentHelper
	-keep public class * extends android.preference.Preference
	-keep public class * extends android.view.View
	-keep public class com.android.vending.licensing.ILicensingService
	-keep class android.support.** {*;}
	
	-keep public class * extends android.view.View{
	    *** get*();
	    void set*(***);
	    public <init>(android.content.Context);
	    public <init>(android.content.Context, android.util.AttributeSet);
	    public <init>(android.content.Context, android.util.AttributeSet, int);
	}
	-keepclasseswithmembers class * {
	    public <init>(android.content.Context, android.util.AttributeSet);
	    public <init>(android.content.Context, android.util.AttributeSet, int);
	}
	-keepclassmembers class * implements java.io.Serializable {
	    static final long serialVersionUID;
	    private static final java.io.ObjectStreamField[] serialPersistentFields;
	    private void writeObject(java.io.ObjectOutputStream);
	    private void readObject(java.io.ObjectInputStream);
	    java.lang.Object writeReplace();
	    java.lang.Object readResolve();
	}
	-keep class **.R$* {
	 *;
	}
	-keepclassmembers class * {
	    void *(**On*Event);
	}
	#----------------------------------------------------------------------------
	
	#---------------------------------webview------------------------------------
	-keepclassmembers class fqcn.of.javascript.interface.for.Webview {
	   public *;
	}
	-keepclassmembers class * extends android.webkit.WebViewClient {
	    public void *(android.webkit.WebView, java.lang.String, android.graphics.Bitmap);
	    public boolean *(android.webkit.WebView, java.lang.String);
	}
	-keepclassmembers class * extends android.webkit.WebViewClient {
	    public void *(android.webkit.WebView, jav.lang.String);
	}
	#----------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------------------