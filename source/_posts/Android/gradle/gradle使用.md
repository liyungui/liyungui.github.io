---
title: gradle使用
date: 2020-02-03 14:13:53
categories:
  - Android
tags:
	- Android
---

[Gradle for Android 读书笔记](https://segmentfault.com/a/1190000004241503#articleHeader7)

# [Android Gradle plugin vs Gradle](https://developer.android.google.cn/studio/releases/gradle-plugin#updating-gradle)

Android Gradle plugin 增加了一些编译apk的特性，可以独立于Android Studio 升级和使用


## Android Gradle plugin 和 Gradle 版本兼容

|Plugin version|	Required Gradle version|
|----|----|
|1.0.0 - 1.1.3|	2.2.1 - 2.3|
|1.2.0 - 1.3.1 |	2.2.1 - 2.9|
|1.5.0	|2.2.1 - 2.13|
|2.0.0 - 2.1.2|	2.10 - 2.13|
|2.1.3 - 2.2.3|	2.14.1+|
|2.3.0+|	3.3+|
|3.0.0+|	4.1+|
|3.1.0+|	4.4+|

## 升级 Android Gradle plugin

工程根目录 build.gradle

	buildscript {
	    repositories {
	        // Gradle 4.1 and higher include support for Google's Maven repo using
	        // the google() method. And you need to include this repo to download
	        // Android Gradle plugin 3.0.0 or higher.
	        google()
	        ...
	    }
	    dependencies {
	        classpath 'com.android.tools.build:gradle:3.2.1'
	    }
	}

## 升级 Gradle

工程根目录 gradle/wrapper/gradle-wrapper.properties

	distributionUrl = https\://services.gradle.org/distributions/gradle-4.6-all.zip
	
[Gradle版本](https://services.gradle.org/distributions/)

## 选择那个Gradle plugin版本

旧版本的话，建议升级到3.0.0

因为有些特性虽然已声明废弃，但还暂时支持

比如 compile，注解

这样可以兼容很多第三方库，节省大量工作

## 升级到Gradle plugin 3.0.0遇到的坑

### 坑1

	Error:Cannot set the value of read-only property 'outputFile' for ApkVariantOutputImpl_Decorated{apkData=Main{type=MAIN, fullName=debug, filters=[]}} of type com.android.build.gradle.internal.api.ApkVariantOutputImpl.
	
代码如下

	// APK 文件名带上版本号
	android.applicationVariants.all { variant ->
	    variant.outputs.each { output ->
	        output.outputFile = new File(
	                output.outputFile.parent,
	                output.outputFile.name.replace(".apk", "-${variant.versionName}.apk"))
	    }
	}
	
解决方案：

	用 all() 代替 each() 
		新模式下，each只能遍历配置时存在的变量；all才能循环执行时生成的变量
	用 outputFileName 代替 output.outputFile ，如果只是修改文件名
	
修改后代码

	android.applicationVariants.all { variant ->
	    variant.outputs.all { output ->
	        outputFileName = output.outputFile.name.replace(".apk", "-${variant.versionName}.apk")
	    }
	}
	
### 坑2

	Error:Cannot choose between the following configurations of project :XXX:
	  - debugApiElements
	  - debugRuntimeElements
	  - releaseApiElements
	  - releaseRuntimeElements

解决方案

	annotationProcessor 替换 apt
	
详细步骤

1、项目根目录build.gradle文件，删除“apt”配置：

	classpath 'com.neenbedankt.gradle.plugins:android-apt:1.8' //删除

2、module的build.gradle文件，删除“android-apt” plugin引用：

	apply plugin: 'android-apt'  //删除
	
3、module的build.gradle文件，修改“dependencies”中的“apt”方式 为“annotationProcessor”方式：

	apt "引用项"  //老方式，删除
	annotationProcessor "引用项" //新方式
	
	比如
	apt 'com.jakewharton:butterknife-compiler:8.0.1'
	annotationProcessor 'com.jakewharton:butterknife-compiler:8.0.1'

### 坑3

	Error:All flavors must now belong to a named flavor dimension. Learn more at https://d.android.com/r/tools/flavorDimensions-missing-error-message.html

Plugin 3.0.0之后有一种自动匹配消耗库的机制，便于debug variant 自动消耗一个库，然后就是必须要所有的flavor 都属于同一个维度。 

在主 app 的 build.gradle 里面的

	defaultConfig {
		 targetSdkVersion：***
		 minSdkVersion ：***
		 versionCode：***
		 versionName ：***
			
		//意思是flavor dimension 它的维度就是该版本号，
		//这样维度就是都是统一的了
		 **flavorDimensions "versionCode"**

### 坑4

	Error:Execution failed for task ':youyoubao:javaPreCompileCommonDebug'.
	> Annotation processors must be explicitly declared now.  The following dependencies on the compile classpath are found to contain annotation processor.  Please add them to the annotationProcessor configuration.
	    - butterknife-compiler-8.6.0.jar (com.jakewharton:butterknife-compiler:8.6.0)
	  Alternatively, set android.defaultConfig.javaCompileOptions.annotationProcessorOptions.includeCompileClasspath = true to continue with previous behavior.  Note that this option is deprecated and will be removed in the future.
	  See https://developer.android.com/r/tools/annotation-processor-error-message.html for more details.

需要在 `app下的build.gradle的defaultConfig`下 显式声明annotation Processor库。

3.0.0之前的版本中，compile a ，不但会把lib a 放到compile classpath 路径下，还会自动放到processor classpath路径下。这会导致processor classpath路径下有大量不必要的依赖，这会更加编译时间。所以从gradle插件3.0.0以后，如果一个库是annotation processors库（如果库中还有META-INF/services/javax.annotation.processing.Processor，那么就认为这是一个annotation processors库），那么需要自己手动使用**annotationProcessor**关键字添加：

	 dependencies {
	      ...
	 annotationProcessor 'com.google.dagger:dagger-compiler:<version-number>'
	 }

如果annotation processors库也需要放到compile classpath 路径下，需要使用compile/api/implementation再声明依赖一次。

并且，新版本如果发现annotation processors库也存在于compile classpath路径下，就会报错。所以需要在android defaultConfig块中进行声明不进行错误检查。

	  android {
	     ...
	    defaultConfig {
	    ...
	      javaCompileOptions {
	         annotationProcessorOptions {
	           includeCompileClasspath false
	       }
	     }
	  }
	 }

如果不想那么麻烦，直接使用如下配置也可以，但是这样的配置在之后的gradle插件版本中并不支持，所以不推荐

	defaultConfig {
	   ...
	   javaCompileOptions { annotationProcessorOptions { includeCompileClasspath = true } }
	}

# [基本配置](http://www.cnblogs.com/xinmengwuheng/p/5797026.html) #

## gradle-wrapper.properties ##
 
- 声明gradle的目录。 一般不修改
- 声明项目使用的gradle版本及gradle的下载路径

		distributionBase=GRADLE_USER_HOME
		distributionPath=wrapper/dists
		zipStoreBase=GRADLE_USER_HOME
		zipStorePath=wrapper/dists
		distributionUrl=https\://services.gradle.org/distributions/gradle-2.14.1-all.zip //gradle 版本

## setting.gradle ##

声明工程包含的模块

	include ':app',':library'

## 根目录的build.gradle ##

声明工程所有模块的公共属性

	buildscript {
	    repositories {
	        jcenter()//使用jcenter库
	    }
	    dependencies {
	        classpath 'com.android.tools.build:gradle:1.5.0'// 依赖android提供的1.5.0的gradle build plugin Tools，一般跟AndroidStudio版本号一致
	
	        // NOTE: Do not place your application dependencies here; they belong
	        // in the individual module build.gradle files
	    }
	}
	//为所有的工程的repositories配置为jcenters
	allprojects {
	    repositories {
	        jcenter()
	    }
	}
	
	task clean(type: Delete) {
	    delete rootProject.buildDir
	}

### 使用技巧 ###

repositories 指定本地文件夹

	allprojects {
		    repositories {
		        maven { url "https://dl.bintray.com/thelasterstar/maven/" }
		        maven {
		            // 本地依赖。目录下所有lib都是通过npm安装的。All of React Native (JS, Obj-C sources, Android binaries) is installed from npm
		            url "$rootDir/node_modules/react-native/android"
		        }
				flatDir {
		            dirs 'libs'
		        }

	A problem occurred configuring project ':react-native-svg'.
	   > Could not resolve all dependencies for configuration ':react-native-svg:_debugCompile'.
	      > Could not find com.facebook.react:react-native:0.48.4.
	        Searched in the following locations:
	 			https://dl.bintray.com/thelasterstar/maven/com/facebook/react/react-native/0.48.4/react-native-0.48.4.pom
	            https://dl.bintray.com/thelasterstar/maven/com/facebook/react/react-native/0.48.4/react-native-0.48.4.jar
	 			file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native/android/com/facebook/react/react-native/0.48.4/react-native-0.48.4.pom
	            file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native/android/com/facebook/react/react-native/0.48.4/react-native-0.48.4.jar
				file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native-svg/android/libs/react-native-0.48.4.jar

## app/build.gradle ##

module的gradle配置

	#表示该module是一个app module,library module 写com.android.library
    apply plugin: 'com.android.application'

	#android专用配置
    android {
        compileSdkVersion 23
        buildToolsVersion "23.0.2" //构建工具的版本号,对应 AndroidSDK 中的 Android SDK Build-tools

		#默认配置，如果没有其他的配置覆盖，就会使用这里的
        defaultConfig {
            applicationId "com.wuxiaolong.gradle4android"
            minSdkVersion 15
            targetSdkVersion 23
            versionCode 1
            versionName "1.0"
        }
        buildTypes {
            release {
                minifyEnabled false
                proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
            }
        }
    }

	#依赖的jar，aar，jcenter库信息
    dependencies {
        compile fileTree(dir: 'libs', include: ['*.jar'])
        testCompile 'junit:junit:4.12'
        compile 'com.android.support:appcompat-v7:23.2.1'
        compile 'com.android.support:design:23.2.1'
    }

## gradle.properties ##

- 任何module的 build.gradle 都可以读取 gradle.properties 中的常量
- gradle.properties 中的数据类型都是 String 类型
	- 使用其他数据类型需要自行转换；

[利用本地化配置buildToolsVersion和gradleBuildTools](http://blog.csdn.net/guiying712/article/details/72629948) 

解决方案：

- gradle.properties 从版本控制工具中给忽略掉
gradle.properties

- 配置好的 gradle.properties 给每个开发人员发一份，供本地使用

代码：

gradle.properties 中

	# 为自动化出包配置(因为每个开发的电脑坏境不一致)
	localBuildToolsVersion=25.0.3
	# 这个值一般跟你的AndroidStudio版本号一致
	localGradlePluginVersion=2.2.3

根目录的build.gradle

	buildscript {
	    dependencies {
	        classpath "com.android.tools.build:gradle:$localGradlePluginVersion"

module的build.gradle

	android {
    	buildToolsVersion localBuildToolsVersion

## repositories节点

- buildScript块。根目录下build.gradle
	- Gradle脚本自身执行依赖插件 
- allprojects块。根目录下build.gradle
	- 所有项目共同所需依赖包
- 根级别。module目录下build.gradle
	- 当前项目所需依赖包

# [全局设置](http://www.cnblogs.com/xinmengwuheng/p/5797048.html) #

## 方式一 ##
根目录下build.gradle 定义全局设置

	ext {
		compileSdkVersion = 23
		buildToolsVersion = "23.0.2"
		minSdkVersion = 14
		targetSdkVersion = 23
	}

module下build.gradle 引用全局设置

	android {
	    compileSdkVersion rootProject.ext.compileSdkVersion
	    buildToolsVersion rootProject.ext.buildToolsVersion
	
	    defaultConfig {
	        applicationId "com.example.android"
	        minSdkVersion rootProject.ext.minSdkVersion
	        targetSdkVersion rootProject.ext.targetSdkVersion
	        versionCode 1
	        versionName "1.0"
	    }

## 方式二 ##
根目录下建config.gradle 定义全局变量设置

	ext {
	
	    android = [
	            compileSdkVersion: 23,
	            buildToolsVersion: "23.0.2",
	            minSdkVersion    : 14,
	            targetSdkVersion : 22,
	
	    ]
	
	    dependencies = [
	            appcompatV7': 'com.android.support:appcompat-v7:23.2.1',
	            design      : 'com.android.support:design:23.2.1'
	
	    ]
	}
 
根目录下build.gradle 最顶部

	apply from: "config.gradle"

module下build.gradle 引用全局设置

	android {
	    compileSdkVersion rootProject.ext.android.compileSdkVersion
	    buildToolsVersion rootProject.ext.buildToolsVersion
	
	    defaultConfig {
	        applicationId "com.example.android"
	        minSdkVersion rootProject.ext.android.minSdkVersion
	        targetSdkVersion rootProject.ext.android.targetSdkVersion
	        versionCode 1
	        versionName "1.0"
	    }
	
	...
	
	dependencies {
	    compile fileTree(dir: 'libs', include: ['*.jar'])
	    testCompile 'junit:junit:4.12'
	    compile rootProject.ext.dependencies.appcompatV7
	    compile rootProject.ext.dependencies.design
	}

# buildConfigField #

自动生成 BuildConfig 类。 每个字段都是 public static final，直接由BuildConfig类点出key名来取值

示例：服务器可能有正式环境和测试环境

	defaultConfig {
	    buildConfigField 'String','API_SERVER_URL','"http://url/"' //定义了String类型，名为API_SERVER_URL，值为http://url/
	}

	Log.d("wxl", "API_SERVER_URL=" + BuildConfig.API_SERVER_URL);

注意，字符串类型的值一定要用双引号包裹起来，否则生成的BuildConfig类中会值类型错误

	buildConfigField("String", "APP_URL", "https://test-app.xuehu365.com/")
	public static final String APP_URL = https://test-app.xuehu365.com/; //错误值类型，没有双引号
	
	buildConfigField("String", "APP_URL", '"https://test-app.xuehu365.com/"')
	public static final String APP_URL = "https://test-app.xuehu365.com/";

生成的完整的BuildConfig类

	public static final boolean DEBUG = Boolean.parseBoolean("true");
	public static final String APPLICATION_ID = "com.xuehu365.xuehu";
	public static final String BUILD_TYPE = "debug";
	public static final String FLAVOR = "xuehuDetect";
	public static final int VERSION_CODE = 280;
	public static final String VERSION_NAME = "2.8.0";
	public static final String FLAVOR_channel = "xuehu";
	public static final String FLAVOR_server = "detect";
	// Fields from build type: debug
	public static final boolean isDebug = true;
	// Fields from product flavor: detect 正式开始自定义的值。上面都是预定义的
	public static final String APP_URL = https://test-app.xuehu365.com/;

# [flavorDimensions 一套代码打包多个应用](https://juejin.im/post/59648441f265da6c415f3078) #

将某个应用更换 UI、文案或者某些界面布局和逻辑代码,换一套皮肤、第三方账号、后台服务器，改个名字上线，并且以后的新功能同步进行更新

总结一下技术点：

	manifestPlaceholders -> AndroidManifest.xml 占位符
	buildConfigField -> BuildConfig 动态配置常量值
	resValue -> String.xml 动态配置字符串
	signingConfigs -> 配置签名文件
	productFlavors -> 产品定制多版本
	flavorDimensions -> 为产品定制设置多个维度
	android.applicationVariants -> 操作 task

示例： 区分渠道(官方，应用宝)和服务器版本（开发，测试，生产），

根据 Product Flavors 的两个维度和 Build Type [debug, release]，最后会生成 `2渠道x3服务器版本x2打包类型=12` 12个 Build Variant

	android {

		//创建两个维度的 flavor
	    flavorDimensions "server", "channel"//定义顺序很重要。决定BuildVariant和productFlavors.all批量遍历的name值(最后一维的flavor为name值)
	
		productFlavors {
	        xuehu { dimension "channel" }
	        yybao { dimension "channel" }
	
	        dev {
	            dimension "server"
	            buildConfigField("String", "APP_URL", "https://dev.app.xuehu365.com/")
	        }
	        detect {
	            dimension "server"
	            buildConfigField("String", "APP_URL", "https://test-app.xuehu365.com/")
	        }
	        prod {
	            dimension "server"
	            buildConfigField("String", "APP_URL", "https://app.xuehu365.com/")
	        }

	        productFlavors.all {
	            flavor -> flavor.manifestPlaceholders = [UMENG_CHANNEL_VALUE: name]//取值为最后一维的值(xuehu,yybao等)
	        }
	    }

# [android.applicationVariants](http://www.jianshu.com/p/25b385afd8b7) #

Android工程相对Java工程来说，要复杂的多，因为通过Build Types和Product Flavors动态的创建很多任务。

- applicationVariants (仅仅适用于Android应用Gradle插件)
- libraryVariants (仅仅适用于Android库Gradle插件)
- testVariants (以上两种Gradle插件都使用)

以上三个属性返回的都是**DomainObjectSet对象集合**，里面元素分别是ApplicationVariant、LibraryVariant和TestVariant

applicationVariants是Android动态构建的产物，可以代表google渠道正式服务器的release包，也可以代表baidu渠道dev开发服务器的debug包

**特别注意**，访问以上这三种集合都会触发动态创建所有的任务。也就是说假如我们通过访问这些集合，修改生成Apk的输出文件名，那么就会自动的触发创建所有任务，此时我们修改后的新的Apk文件名就会在所有任务中起作用（如果我们在多个product flavor中都访问这些集合，就以最后一次访问结果为最终结果，而不是每个flavor有不同结果）。

applicationVariants是一个DomainObjectCollection集合，可以通过all方法进行遍历，遍历的每一个variant都是一个ApplicationVariant

ApplicationVariant，通过查看源代码看到它有一个outputs List集合 作为它的输出，我们再遍历它，如果它的名字是以.apk结尾的话那么就是我们要修改的apk名字了

	android.applicationVariants.all { variant ->
        variant.outputs.each { output ->
            if (output.outputFile != null && output.outputFile.name.endsWith('.apk')) {
                def file = output.outputFile
                output.outputFile = new File(file.parent, file.name.replace(file.name,
                        variant.productFlavors[0].name + "_" +
                                variant.versionName
                                + "_${variant.productFlavors[1].name}.apk"))
            }
        }
    }

## 修改apk文件名

```
//自定义获取时间戳函数
import java.text.DateFormat
import java.text.SimpleDateFormat
def getDateTime() {
    DateFormat df = new SimpleDateFormat("yyyy_MM_dd_HH_mm");
    return df.format(new Date());
}
// APK 文件名带上版本号和时间戳
android.applicationVariants.all { variant ->
    variant.outputs.all { output ->
        outputFileName = output.outputFile.name.replace(".apk", "-${variant.versionName}-" + getDateTime() + ".apk")
    }
}
```
# library 构建 #

**library module 默认是输出 release 包的**。所以默认情况下载library module 设置debug字段(如高德debug key)是浪费表情

## library 支持 debug 设置 ##

- library的gradle中加入以下配置 `publishNonDefault true` 意思是 library在打包的时候不只是打release包
- 主module的gradle中添加如下配置

		debugCompile project(path: ':library', configuration: 'debug')
		releaseCompile project(path: ':library', configuration: 'release')

	这样项目就会根据不同的编译环境依赖对应的包。

# compileSdkVersion与buildToolsVersion引起的问题 #

	No resource found that matches the given name: attr 'android:keyboardNavigationCluster'.

一般都是compileSdkVersion低于依赖的sdk版本，升级版本即可

	例如compileSdkVersion是25，依赖了v7:27。就会报错
	
	
# 删除重复文件#

有时候依赖三方库会造成文件重复。比如腾讯im包含部分bugly的文件


	// 解决IM SDK与RN依赖和bugly冲突【libgnustl_shared.so】
	import com.android.build.gradle.internal.pipeline.TransformTask
	
	def deleteDuplicateJniFiles() {
	    def files = fileTree("${buildDir}/intermediates/exploded-aar/shensz_android/imsdk/unspecified/jni/") {
	        include "**/libgnustl_shared.so"
	    }
	    files.each { it.delete() }
	    def buglyFiles = fileTree("${buildDir}/intermediates/exploded-aar/com.tencent.bugly/nativecrashreport/3.0/jni/") {
	        include "**/libBugly.so"
	    }
	    buglyFiles.each { it.delete() }
	
	    def sharedFiles = fileTree("${buildDir}/intermediates/exploded-aar/com.tencent.ilivesdk/ilivesdk/1.7.0/jni/") {
	        include "**/libstlport_shared.so"
	    }
	    sharedFiles.each { it.delete() }
	}
	
	tasks.withType(TransformTask) { pkgTask ->
	    pkgTask.doFirst { deleteDuplicateJniFiles() }
	}
# ResolutionStrategy

support包冲突,无法编译

最深的坑是：force强制使用某个版本，编译通过。然后在某些系统，ClassNotFoundException

	java.lang.ClassNotFoundException:Didn't find class "android.support.v4.animation.AnimatorCompatHelper" on path: DexPathList[[zip file "/data/app/com.zy.course-1/base.apk"],nativeLibraryDirectories=[/data/app/com.zy.course-1/lib/arm, /data/app/com.zy.course-1/base.apk!/lib/armeabi-v7a, /vendor/lib, /system/lib]]
		dalvik.system.BaseDexClassLoader.findClass(BaseDexClassLoader.java:56)
		java.lang.ClassLoader.loadClass(ClassLoader.java:511)
		java.lang.ClassLoader.loadClass(ClassLoader.java:469)
		android.support.v7.widget.DefaultItemAnimator.resetAnimation(ProGuard:515)
		android.support.v7.widget.DefaultItemAnimator.animateChange(ProGuard:322)
		android.support.v7.widget.SimpleItemAnimator.animateChange(ProGuard:149)
		android.support.v7.widget.RecyclerView.animateChange(ProGuard:3624)

原来方案：

	configurations.all {
        resolutionStrategy {
            force 'com.android.support:support-v4:27.0.1'
            force 'com.android.support:design:27.0.1'
            force 'com.android.support:appcompat-v7:27.0.1'
        }
    }
    	
解决方案

	android {
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
	}
	
# Walle 渠道包打包神器

Android Signature V2 Scheme签名下的新一代渠道包打包神器

[github](https://github.com/Meituan-Dianping/walle)

## 未开启V2签名错误

`Plugin requires 'APK Signature Scheme v2 Enabled' for Release.`

官方教程要求 在 app 的 `build.gradle` 配置

```
android {
  signingConfigs {
      sign {
          storeFile file("../sjd.jks")
          storePassword "sjd123"
          keyAlias "sjd"
          keyPassword "sjd123"
          v2SigningEnabled true//v2签名
      }
  }
   buildTypes {
      release {
          minifyEnabled false
          proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
          signingConfig signingConfigs.sign
      }
      debug {
          minifyEnabled false
          proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
          signingConfig signingConfigs.sign
      }
  }
}
```

配置上还是提示未开启V2签名；排查gradle脚本好久，才发现项目未把 keystore文件和sign.properties文件加入git管理，然后ci工作空间这个两个文件被清理掉了。加入这个两个文件，打包成功。

所以，缺少签名配置也会报 未开启V2签名 这个错误

# 设置代理

配置文件 `gradle.properties`

作用域：

- 全局。配置文件在 ~/.gradle目录下
- 当前项目。配置文件在当前项目根目录下

配置内容(Host和Port是必须)

```
systemProp.http.proxyHost=xx.xx.xx.xx
systemProp.http.proxyPort=xxxx
# systemProp.http.proxyUser=userid
# systemProp.http.proxyPassword=password
# systemProp.http.nonProxyHosts=*.nonproxydomains.com|localhost

systemProp.https.proxyHost=xx.xx.xx.xx
systemProp.https.proxyPort=xxxx
```

# 替换仓库地址

## 阿里云

打开 [阿里云源](https://maven.aliyun.com)
，会转到https://maven.aliyun.com/mvn/view。跟Android相关的有以下四个

```
maven { url 'https://maven.aliyun.com/repository/jcenter' }
maven { url 'https://maven.aliyun.com/repository/google' }
maven { url 'https://maven.aliyun.com/repository/central' }
maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
```

## 初始化

gradle 生命周期中有一个初始化(Initialization)的过程，初始化之后才会运行 build script。我们可以在初始化中定制一些全局设置，比如配置仓库地址。

可以使用初始化脚本的位置：

- 命令行
- 放一个`init.gradle` 文件到`USER_HOME/.gradle/`目录下
- 放一个`xx.gradle`的文件到 `USER_HOME/.gradle/init.d/` 目录下.
- 放一个`xx.gradle`的文件到 `GRADLE_HOME/init.d/` 目录下.

## 文件内容

### 在最前面插入仓库

```
allprojects {
    repositories {
        mavenLocal()
        maven { url 'http://maven.aliyun.com/nexus/content/repositories/central/' }
    }
}
```

这样就会优先搜索本地和阿里云，找不到才会使用项目配置的仓库

### 移除国外仓库

```
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public/' }
        maven { url 'https://maven.aliyun.com/nexus/content/repositories/google' }
        maven { url 'https://maven.aliyun.com/nexus/content/groups/public/' }
        maven { url 'https://maven.aliyun.com/nexus/content/repositories/jcenter'}

        all { ArtifactRepository repo ->
            if (repo instanceof MavenArtifactRepository) {
                def url = repo.url.toString()

                if (url.startsWith('https://repo.maven.apache.org/maven2/') || url.startsWith('https://repo.maven.org/maven2') || url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
                    //project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
                    remove repo
                }
            }
        }
    }

    buildscript {

        repositories {

            maven { url 'https://maven.aliyun.com/repository/public/'}
            maven { url 'https://maven.aliyun.com/nexus/content/repositories/google' }
            maven { url 'https://maven.aliyun.com/nexus/content/groups/public/' }
            maven { url 'https://maven.aliyun.com/nexus/content/repositories/jcenter'}
            all { ArtifactRepository repo ->
                if (repo instanceof MavenArtifactRepository) {
                    def url = repo.url.toString()
                    if (url.startsWith('https://repo1.maven.org/maven2') || url.startsWith('https://jcenter.bintray.com/')) {
                        //project.logger.lifecycle "Repository ${repo.url} replaced by $REPOSITORY_URL."
                        remove repo
                    }
                }
            }
        }
    }

}
```

# 依赖本地模块

`settings.gradle`中引入

```
// 本工程目录下的子模块
include  ':pay', ':base'

// 非工程目录下的子模块
include ':video'
project(':video').projectDir = new File('/Users/liyungui/StudioProjects/grmeeting_android/lib_video')
```

主模块下`build.gradle`中使用

```
dependencies {
	api project(':pay')
	api project(':common')
	api project(':video')    
```

 	