---
title: gradle导入依赖
date: 2020-02-03 14:13:53
categories:
  - Android
tags:
	- Android
---

[Gradle for Android-第三篇、依赖管理](https://segmentfault.com/a/1190000004237922)

[Android Studio 打包及引用 aar](http://www.androidchina.net/2467.html) 

# 依赖配置API #

## compile -- api/implementation
(Gradle plugin 3.0.0)

	依赖参与编译并且打包到最终的apk文件中。
		api
			外部依赖，等同于compile
		implementation
			内部依赖：编译期依赖隔离。将该依赖隐藏在内部，而不对外部公开(外部无法访问)
			提高编译速度：不会编译内部依赖
		
实例：A依赖B，B依赖C

依赖路径：

- compile/api：无法直观知道A所有的依赖，也无法直观知道传递依赖的具体版本
- implementation：规范直观。虽然需要多写依赖

编译期：C修改重新编译

- compile/api：AB都需要重新编译(即使A没有用到C的接口)
- implementation：编译期隔离，只重新编译B

打包运行：

- 都会打包进apk。如果某依赖有多个版本，打包最高版本

### 编译期和运行期版本冲突

	'com.facebook.fresco:fresco' has different version for the compile (1.3.0) and runtime (1.11.0) classpath. You should manually set the same version via DependencyResolution
	
统一版本即可

	configurations.all {
        resolutionStrategy.eachDependency { DependencyResolveDetails details ->
            def requested = details.requested
            if (requested.group == 'com.facebook.fresco'){
                details.useVersion '1.3.0'
            }
        }
    }

## Provided -- compileOnly

	依赖只在编译时使用，只参与编译，不打包到最终apk。类似eclipse中的external-libs,
		
	注：使用Provided必须删除compile fileTree(include: ['*.jar'], dir: 'libs') 
	不然lib下的jar均按照compile方式引入到Module
	
## apk -- runtimeOnly

	依赖只会打包到apk文件中，而不参与编译，所以不能在代码中直接调用jar中的类或方法，否则在编译时会报错

以上三个 对所有的build type以及favlors 有效

## testCompile

	仅单元测试apk时有效，而对正常的debug或者release apk包不起作用。

## debug compile

	仅debug模式的编译和最终的debug apk打包

## release compile

	仅Release 模式的编译和最终的Release apk打包。

## Gradle plugin 3.0.0依赖使用api和implementation，废弃compile

compile 兼容支持一段时间。即已废弃，还会保留一段时间，直到下个比较大的gradle tools版本发布

	



	compile fileTree(dir: 'xxx', include: ['*.jar', "*.xxx"])：将某个目录下所有符合扩展名的文件作为依赖；
	compile 'com.xx.xx:ProjectName:Version'：配置Maven 库作为依赖；在 Maven 库中心 可以搜索自己想用的库进行依赖；
	compile project(':AnotherModule')：配置另一个 Module 作为本 Module 的依赖，被依赖的 Module 必须被导入到当前工程中；
	compile files('xxx.jar')：配置某个 jar 包作为依赖。
	compile(name: 'xxx', ext: 'aar') //配置某个 aar 包作为依赖。xxx.aar是文件名

	compile fileTree(include: ['*.jar'], dir: 'libs')
    testCompile 'junit:junit:4.12'
    apt 'com.jakewharton:butterknife-compiler:8.0.1'
    compile 'com.android.support:appcompat-v7:23.3.0'
    compile 'com.squareup.retrofit2:retrofit:2.0.2'
    compile(name: 'Yrecycleview', ext: 'aar')
    compile project(path: ':easeui')
    compile files('libs/hyphenatechat_3.1.3.jar')

# library module

直接引入lib工程

	dependencies {
		compile project(':library名字')
		compile project(':libraries:library名字')//多个library，libraries是文件夹名字
	}

# jar包依赖 #

module目录下新建libs文件夹，放置jar

右键 Add As Library，选择相应module即可。

上面第二部的操作其实是配置了相应module的 `build.gradle`

	dependencies {
	       compile fileTree(dir: 'libs', include: ['*.jar'])//即添加所有在libs文件夹中的jar
	       compile fileTree('libs/WuXiaolong.jar')
	}


## 添加jar包 Choose the appropriate categories from the list.错误
	
	Android Studio cannot determine what kind of files the chosen items contain.
	Choose the appropriate categories from the list.
	- classes
	- external annotations
	- jar directory
	- JavaDocs
	- source archive directory
	- sources

不用考虑，jar出错了！！！
	
	http://ask.android-studio.org/?/question/188

# so库依赖 #

app/src/main/目录下新建jniLibs目录，so库需要放入对应的cpu下（如armeabi）


	sourceSets{
        main.jniLibs.srcDir 'src/main/libs' //设置自定义so库目录
    }
    
.so文件放在对应的文件夹中

	app
	   ├── AndroidManifest.xml
	   └── jniLibs
	       ├── armeabi
	       │   └── libiconv.so
	       ├── armeabi-v7a
	       │   └── libiconv.so
	       ├── mips
	       │   └── libiconv.so
	       └── x86
	           └── libiconv.so    

## 暂时不提供64位的so文件 ##

解决方案：强制APP使用32位so

- 指定只保留32位so库

		android{
			defaultConfig{
				ndk{abiFilters "armeabi"}
			}
		}
		
		如果配置后编译报错，在gradle.properties文件中加上 Android.useDeprecatedNdk=true； 

- 指定目录下必须有so文件(否则打包无该目录)

		build.gradle中配置的so加载目录:jniLibs.srcDir:customerDir

		如果没有该项配置则so加载目录默认为：src/main/jniLibs

		将.so文件放置该目录的armeabi文件夹下
			没有该目录则新建一个
			APP中没有使用到.so文件则需要拷贝任意一个32位的so文件到该目录下
				如果没有合适的so可以到官网http://x5.tencent.com/tbs/sdk.html下载官网“SDK接入示例“,拷贝对应目录下的liblbs.so文件

[与 so 有关的一个长年大坑](https://zhuanlan.zhihu.com/p/21359984)   
[ABI 管理](https://developer.android.com/ndk/guides/abis.html?hl=is#sa) 

### ABI ###

	mips / mips64: 极少用于手机可以忽略
	x86 / x86_64: x86 架构的手机都会包含由 Intel 提供的称为 Houdini 的指令集动态转码工具，实现 对 arm .so 的兼容，再考虑 x86 1% 以下的市场占有率，x86 相关的两个 .so 也是可以忽略的
	armeabi: 支持ARMV5TE和更高版本 相当老旧的版本 无硬浮点，在需要大量计算时有性能瓶颈
	armeabi-v7a: 支持armeabi等 目前主流版本（与 ARMv5、v6 设备不兼容）
	arm64-v8a: 支持AArch-64 64位支持

现在armeabi v5基本都淘汰了，**建议保留armeabi-v7a就可以兼容到市面上的绝大多数手机**

选择保留armeabi(微信保留了) ，并保证armeabi 和 armeabi-v7a这两个文件夹中 so 数量一致

**对只提供 armeabi 版本的第三方 so，原样复制一份到 armeabi-v7a 文件夹（armeabi-v7a: 支持armeabi）。**

[Android ABI想到的](http://www.jianshu.com/p/a8433f053248)

### ABI ###

应用程序二进制接口ABI（Application Binary Interface）

### .so文件 ###

Native Libs Monitor 这个app可以帮助我们理解手机上安装的APK用到了哪些.so文件，以及.so文件来源于哪些函数库或者框架

### ABI和CPU的关系 ###

很多设备都支持多于一种的ABI

但最好是针对特 定平台提供相应平台的二进制包，这种情况下运行时就少了一个模拟层（例如x86设备上模拟arm的虚拟层），从而得到更好的性能

可以通过 `Build.SUPPORTED_ABIS` 得到根据偏好排序的设备支持的ABI列表。但你不应该从你的应用程序中读取它，因为 Android包管理器安装APK时，会自动选择APK包中为对应系统ABI预编译好的.so文件，如果在对应的lib／ABI目录中存在.so文件的话。

对应关系如下图：
![](http://upload-images.jianshu.io/upload_images/2226246-efd370c8c43bd35f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**不同CPU架构的Android手机加载时会在libs下找自己对应的目录，从对应的目录下寻找需要的.so文件；如果没有对应的目录，就会去armeabi下去寻找，如果已经有对应的目录，但是没有找到对应的.so文件，也不会去armeabi下去寻找了。**

**微信就是只有armeabi一个目录**

当引入一个新的预编译.so文件，而且项目中还存在其他的.so文件时，需要首先确认新引入的.so文件使用的C++运行时是否和已经存在的.so文件一致。

### xx.so is 32-bit instead of 64-bit ###

这是因为module下有64位的so库目录，而某个so库却没有提供64位的

**解决方案：**

- 只保留armeabi，删除其他以”armeabi“开头的文件夹
- module的build.gradle

		android {
		    defaultConfig {
		        ndk {
		            abiFilters "armeabi"
		        }
		    }
		}
- gradle.properties

		Android.useDeprecatedNdk=true


### [Android 6.0 + .so 动态库的适配](http://www.cnblogs.com/linguanh/p/6137641.html) ###

#### 问题描述 ####

同一个 APP 在 api <=22 的 sdk 情况下编译，可以运行正常，不存在闪退或者 .so 库加载失败的情况

当你采用 api >=23 的sdk 编译的时候，安装到 Android 6.0 及其以上的手机的时候，大范围出现崩溃 或者 .so 库加载失败，而在 6.0 以下的手机却正常；

Catch的信息：`dlopen failed: cannot locate symbol "XXXX" xxxx.so`

#### 问题原因 ####

不同链接方式，决定dlopen是否会打开指定的系统中(手机中)提供的动态库，并使用 dlsym 获取符号地址

在此时的手机中如果找不到，那么就会出问题，一般和 API 有关系。

`Application.mk`，里面有一行 `APP_STL := XXX` 指明`库的链接方式`

**STL的取值：**

	1）system，默认的值，最危险方式，直接和手机系统版本挂钩，采用手机最小版本的.so库链接
	
	2）gabi++_static
	
	3）gabi++_shared
	
	4）stlport_static
	
	5）stlport_shared
	
	6）gnustl_static
	
	7）gnustl_shared

	主要是两种，静态链接，动态链接：

	动态链接，是指在生成可执行文件时不将所有程序用到的函数链接到一个文件，因为有许多函数在操作系统带的dll文件中，当程序运行时直接从操作系统中找。

	静态链接，是把所有用到的函数全部链接到 .so 文件中；

#### 目前存在该问题的知名SDK ####

百度地图、环信、高德地图、语音库 speex

不知道修复没有

这些 SDK 一但在你的 APK 编译版中中设置 API >=23 就会出现各种问题，闪退或者抛出异常。

#### 解决方案 ####

主要有两种：

1. 委曲求全，指标不治本，把你的 APK 编译时 API 降低到 23 以下，还出问题就继续降低

	这意味着，你很多 Android Sdk 的新控件用不了；

2. 在 Application.mk 中修改 APP_STL，重新编译 .so 。

如果没有源码，要么等他们解决，要么采用第一种，建议尝试 APP_STL := gnustl_shared 这种方式，对于所需要的外部动态链接函数、符号，在 NDK 13b 中都会独立生成一份，全部引用就解决此类问题，例如

	private void load() {
	      try {
	          System.loadLibrary("gnustl_shared");
	          System.loadLibrary("speex");
	      } catch (Throwable e) {
	          Log.d("zzzzz","加载语音库异常 ："+e.toString());
	      }
	}

# aar文件

- Android Library项目导出的**jar文件不能包含资源文件**，
	- 比如一些drawable文件、xml资源文件之类的，
	- 在gradle之前我们要引用带资源文件的Android Library必须要把整个library导入进来进行引用
- Android Library项目导出的**aar（包含资源文件、第三方库文件、so、manifest ）**
	- gradle最普遍的方法是把aar上传到mavenCentral或者jcenter

## 导出aar

	apply plugin: 'com.android.library' //输出 aar。 
	apply plugin: 'com.android.application' //输出 apk

	gradle aR 生成 aar

library库输出的.aar文件，目录为 [ModuleName]/build/outputs/aar

## 依赖aar 两种方式

1. 直接导入。不推荐
	
		File -- Project Structure，添加一个新 Module，选择 Import *.JAR or *.AAR Package
		导入后，在你的工程下面，会生成一个文件夹，里面是 aar 文件以及 Android Studio 的配置文件。
		接着在 gradle 中配置依赖，依赖方式使用 compile project 的方式
	`缺点`：被依赖的 aar 无法 F3 跟进去，无法看到资源文件内容以及目录层级等
2. 依赖配置。**推荐使用**
		 
	- module目录下新建aars文件夹，放置aar

			repositories {
				flatDir {
					dirs 'aars' //添加该文件夹作为依赖库
				}
			}
		
			dependencies {
				compile(name:'libraryname', ext:'aar')
			}

lib module 依赖了aar库，failed to resolve aar

在app module 的build.gradle中加入下面代码：

```
repositories {  
    flatDir {  
        dirs project(':taesdk').file('libs')  
    }  
}  
```

# 手动下载远程aar

有时gradle构建下载依赖包出现错误(timeout)，可以手动去仓库下载，放到gradle的cache目录(`~/.gradle/caches/modules-2/files-2.1`)

```
> Could not download codeview-android.aar (com.github.softwee:codeview-android:1.2.0)
  > Could not get resource 'https://jitpack.io/com/github/softwee/codeview-android/1.2.0/codeview-android-1.2.0.aar'.
     > Read timed out
```

最终目录 `/Users/liyungui/.gradle/caches/modules-2/files-2.1/com.github.softwee/codeview-android/1.2.0/83787aabb0260a92ae7c9632e56995a38395560d/codeview-android-1.2.0.aar`

关于文件父目录，网上资料很少，其实是文件SHA1码

mac的话可以用 `shasum` 命令查看，win的话是 `certutil -hashfile`

一般情况，jar、aar、pom、source、doc等文件，都是一个SHA1目录对应一个文件。

有时jar和pom会下载到同一个目录下面，这其实还是用的是jar的SHA1

# 依赖module和主module 资源id 冲突 #

android studio 并不会对依赖module和主module 资源id 在编译时时报错（eclipse会）

如 依赖和主module 都有 activity_main.xml 布局文件，在运行时，依赖module 中activity_main中的id就会找不到，因为首先是在主module中的activity_main文件中查找，就会报错 `ava.lang.NoSuchFieldError: No static field rl_dd of type I in class Lcom/xuehu365/videoviewmediacontroller/R$id;`

确保依赖工程和主module 资源文件名 不重复即可。

**每个资源文件名中的控件id可以重复，不影响查找（只要控件id不在同一个资源文件中）**

# [远程依赖包重复问题](https://juejin.im/post/591a5084128fe1005cda382d) #

错误 `com.android.dex.DexException: Multiple dex files define XXXX`

或 `java.util.zip.ZipException: duplicate entry: uk/co/senab/photoview/BuildConfig.class`

引用了重复的库或者jar包引起的

两个库同时引用了同一个第三方库，最坑人的是都是直接引用，而不是使用 Provided 的方式

**解决思路**：找到重复删掉一个

	gradlew -q app:dependencies 命令，输出树状依赖
	
	星号后缀标记 (*)，意思是忽略该依赖(不下载)
	
	
- 删掉远程依赖库的依赖

		compile('com.loonggg.saoyisao.lib:1.1.0')
		compile('com.timmy.qrcode.lib:1.4.1') {
		        exclude group: 'com.google.zxing'
		}
		编译时将group为com.google.zxing的所有library都去除在外，com.timmy.qrcode.lib:1.4.1就会自动去引用com.loonggg.saoyisao.lib:1.1.0项目里的zxing依赖

- 删掉本地依赖库的依赖

		下载修改后重修打jar包，蛋疼

`java.util.zip.ZipException: duplicate entry: tv/danmaku/ijk/media/player/AbstractMediaPlayer.class`

**完美解决方式** `resolutionStrategy.force`

	configurations.all {
	    resolutionStrategy {
	        force 'com.android.support:support-v4:27.0.1'
	        force 'com.android.support:design:27.0.1'
	        force 'com.android.support:appcompat-v7:27.0.1'
	    }
	}

# v4包重复 #

v7包已经包含了v4包。

所以如果主module已有v7包依赖，lib module有v4包依赖，就会v4包重复。这时需要把v7包中的v4 exclude

	compile('com.airbnb.android:lottie:2.5.4') { exclude group: 'com.android.support.v4' }
		lottie依赖v7包

# v4 v7包在线依赖失败 #

	//将maven.googlecom
	//maven { url 'https://maven.google.com/' }
	//替换为
	maven { url 'https://dl.google.com/dl/android/maven2/' }
	
	