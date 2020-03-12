---
title: gradle构建最佳实践
date: 2020-02-03 14:13:53
categories:
  - Android
tags:
	- Android
---
	
	gradle构建最佳实践 https://www.figotan.org/2016/04/01/gradle-on-android-best-practise/
	Gradle构建编译速度太慢的解决方法 http://www.52codes.net/article/658.html
	加速Android Studio/Gradle构建 http://blog.isming.me/2015/03/18/android-build-speed-up/

# 加速篇 #

GRADLE的构建过程通常会比较漫长，一个中等项目，10M左右大小的app，一次完整构建大概在5分钟左右。

调试阶段，采用Android Studuo 2.0，默认提供的Instant Run方式，每次修改都不会重新构建项目，从而加快了构建过程。

GRADLE一次完整的构建过程通常分成三个部分，初始化，配置和执行任务，那么我们可以考虑从这三个部分分别尝试优化。

### 1. 开启daemon ###

构建初始化的很多工作是关于java虚拟机的启动，加载虚拟机环境，加载class文件等，这些动作交给一个单独的后台进程去做

	gradle.properties（全局起效是~/.gradle/gradle.properties，从工程目录拷贝过来）

	org.gradle.daemon=true

### 2. 并行构建模块化项目 ###

库工程(Library projects)，主工程(Application project)并行构建

	org.gradle.parallel=true

### 3. 按需配置 ###

	org.gradle.configureondemand=true

### 4. 增大gradle运行的java虚拟机的大小 ###

org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8

### 5. 依赖库使用固定版本 ###

	compile 'com.google.code.gson:gson:2.2.1'

	compile 'com.google.code.gson:gson:2.+'这种避免使用，每次都去repo拉取最新版本

### 6. 升级到最新的GRADLE、和android gradle plugin 和 JDK ###

最新版的GRADLE和JDK往往是性能最好

GRALDE采用了一种叫做wrapper的方式，可以做到每个项目独立使用其自己的GRADLE版本，这样做的好处是每个项目的构建环境独立，互不影响。GRADLE发展太快，新旧版本之间很难兼容。假设都用同一个全局的GRADLE，那么当这个GRADLE升级后，所有的项目可能都会编译失败，你得一个一个改配置

### 7. 命令行构建 ###

Android Studio中，点击运行是将当前的构建任务加入到队列中。如果你改过build.gradle的文件导致它在同步脚本时，就必须等到这个任务完成之后才会执行你刚才的构建任务

### 8. 屏蔽不必要的productFlavor ###

尽管只是要构建Develop版本，但还是会去解析每一个productFlavor的依赖，并且在依赖上卡很久。所以在构建时先注释掉其他pruductFlavor

### 9. 使用离线模式 ###

编译过一次，依赖应该都在本地中有缓存了。这时命令行构建可以使用--offline参数

### 10. 没必要 不要在构建时进行clean ###

### 11. 引入依赖库尽量使用aar ###

	maven http://gradleplease.appspot.com/
	githu https://github.com/Goddchen/mvn-repo。

自己的库模块也可以打包成aar

**以上功能其实可以通过修改android studio配置实现，区别是配置只会在ide构建的时候生效，命令行构建不会生效**

Gradle 和 Compiler 两个选项卡中配置

# gradle 把依赖缓存在哪 #

用户目录\ .gradle\caches\modules-2\files-2.1

# 使用Gradle Wrapper必要性 #

便于统一项目所使用的gradle版本。

GRALDE采用了一种叫做wrapper的方式，可以做到每个项目独立使用其自己的GRADLE版本，这样做的好处是每个项目的构建环境独立，互不影响。GRADLE发展太快，新旧版本之间很难兼容。假设都用同一个全局的GRADLE，那么当这个GRADLE升级后，所有的项目可能都会编译失败，你得一个一个改配置

使用Gradle Wrapper，自动下载二进制包的时间需要以分钟计算（毕竟服务器在国外），不过还好，这个过程只会出现一次

# 常见错误 #
## [Error:Configuration with name 'default' not found.](http://blog.csdn.net/luo451591667/article/details/50667549) ##

同事添加了某个module,自己同步代码后会出现Error:Configuration with name 'default' not found.的错误,

这是因为同步时不会自动把`远程仓库`下载下来，需要你自己初始化下载,这时只要执行:

	git submodule update --init --recursive 

**实例** 

https://github.com/eolwral/OSMonitor/

包含远程仓库

	colorpicker @ ec1d13e
	volley @ d20f9d3

下载回来发现 colorpicker 和volley文件夹为空

	$ git submodule update --init --recursive
	Submodule 'colorpicker' (https://github.com/eolwral/android-ColorPickerPreference.git) registered for path 'colorpicker'
	Submodule 'volley' (https://android.googlesource.com/platform/frameworks/volley/) registered for path 'volley'
	Cloning into 'colorpicker'...
	remote: Counting objects: 394, done.
	Receivin94 g objects:  77% (3(0d4/39e4lta 0), reused 0) ,(del 2ta 0), pa4ck4.00  394
	Receiving objects: 100% (394/394), 252.30 KiB | 83.00 KiB/s, done.
	Resolving deltas: 100% (164/164), done.
	Checking connectivity... done.
	Submodule path 'colorpicker': checked out 'ec1d13e450e65bbd086bd6094c5cd36a4da737fa'
	Cloning into 'volley'...
	fatal: unable to access 'https://android.googlesource.com/platform/frameworks/volley/': Failed to connect to android.googlesource.com port 443: Timed out
	fatal: clone of 'https://android.googlesource.com/platform/frameworks/volley/' into submodule path 'volley' failed

volley下载失败，点击发现volley远程仓库地址失效（无法跳转），手动搜索下载volley

## transformClassesWithDexForXuehuDebug UnsupportedOperationException ##

可能两种原因：

1. JDK1.8与gradle不兼容
2. 内存不足

	主module build.gradle

		dexOptions {
	        javaMaxHeapSize "4g"
	        preDexLibraries = false
	    }

		defaultConfig {
			multiDexEnabledtrue
		}
		
		dependencies {
			compile 'com.android.support:multidex:1.0.1'
		}

## Unsupported major.minor version 52.0 ##

	 java.lang.UnsupportedClassVersionError: com/android/build/gradle/LibraryPlugin : Unsupported major.minor version 52.0

可能两种原因：

1. JDK1.8与gradle不兼容
2. compileSdkVersion 和 buildToolsVersion 版本不一致。一个23，一个24

		android {
		    compileSdkVersion 23
		    buildToolsVersion "24.0.3"

    
# 指定cpu类型，减少apk体积 #

gradle.properties

	android.useDeprecatedNdk=true

主module 的 build.gradle

	android {
		defaultConfig {
			ndk {
	            abiFilters "armeabi", "armeabi-v7a", "armeabi-v8a", "x86"
	        }
		}
	}