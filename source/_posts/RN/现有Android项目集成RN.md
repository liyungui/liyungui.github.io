---
title: 现有Android项目集成RN
date: 2018-07-25 15:23:51
tags:
	- RN
---

首先阅读官方文档 [集成到现有原生应用](https://reactnative.cn/docs/0.51/integration-with-existing-apps.html#content)

# 关于 #

## 加载RN资源包 ##

正常运行模式，优先加载 `assets/index.android.bundle`，加载失败加载 `packager`服务器的bundle到 `assets`

Live Reload 和 Debug JS模式下，每次都是加载  `packager`服务器的bundle到 `assets`

## 编译并运行RN应用到两种方法 ##

- 根目录 `react-native run-android`
- 根目录 `npm install` `yarn start` android目录 `./gradlew installDebug `

## 小技巧 ##

APP和调试服务器并没有绑定。即任一APP都可以读取本地调试服务器的bundle

如果某个工程无法运行调试，就可以直接开启 packager服务器，然后运行app，app会自动从packager服务器读取bundle，达到调试目的

# 初始化指定RN版本 #

历史原因。之前RN开发由IOS端同学负责，用的是 0.48.4

	react-native init rns --version 0.48.4

# 自定义js文件名和文件路径 #

实际开发几乎不会用官方文档中的 app.js，也不会直接就放根目录下

历史原因。 js文件放在 ssz_rn_project\js\pages_live 文件夹。 js下还有 pages_student, pages_teacher等

`index.android.js`

	require('js/pages_teacher/index.teacher.js');
	require('js/pages_student/index.student.js');
	require('js/pages_parent/index.parent.js');
	require('js/pages_live/index.liveplay.js');

`index.liveplay.js`

	import { AppRegistry } from 'react-native';
	import LivePlayCourseDetail from './LivePlayCourseDetail/index';
	
	// 课程详情页
	AppRegistry.registerComponent('LiveCourseDetail', () => LivePlayCourseDetail);


# 运行有坑 #

## 找不到AndroidManifest ##

	ENOENT: no such file or directory, open 'D:\rn_project\android\app\src\main\AndroidManifest.xml'

### 原因：RN默认的Android项目名称为app ###

实际开发都会修改默认的moudle名称

解决方案：指定module name

`node_modules\react-native\local-cli\runAndroid\runAndroid.js`
	
	module.exports = {
	  name: 'run-android',
	  description: 'builds your app and starts it on a connected Android emulator or device',
	  func: runAndroid,
	  options: [{
	    command: '--install-debug',
	  }, {
	    command: '--root [string]',
	    description: 'Override the root directory for the android build (which contains the android directory)',
	    default: '',
	  }, {
	    command: '--flavor [string]',
	    description: '--flavor has been deprecated. Use --variant instead',
	  }, {
	    command: '--variant [string]',
	  }, {
	    command: '--appFolder [string]',
	    description: 'Specify a different application folder name for the android source.',
	    default: 'app',
	  }, {
	    command: '--appIdSuffix [string]',
	    description: 'Specify an applicationIdSuffix to launch after build.',
	    default: '',
	  }, {
	    command: '--main-activity [string]',
	    description: 'Name of the activity to start',
	    default: 'MainActivity',
	  }, {
	    command: '--deviceId [string]',
	    description: 'builds your app and starts it on a specific device/simulator with the ' +
	      'given device id (listed by running "adb devices" on the command line).',
	  }, {
	    command: '--no-packager',
	    description: 'Do not launch packager while building',
	  }],
	};

## 找不到Activity ##

`react-native run-android --appFolder course`

	Error: Activity class {com.shensz.course/com.shensz.course.MainActivity} does not exist.

### 原因1：Mainactivity不在清单文件里package的直接目录下 ###

解决方案：指定Activity路径

`react-native run-android --appFolder course --main-activity module.main.activity.MainActivity`

	Error: Activity class {com.shensz.course/com.shensz.course.module.main.activity.MainActivity} does not exist.

### 原因2：清单文件里 `package` 和build.gradle里的 `applicationId` 不一致。 ###

RN运行时直接读取清单文件 `package` 作为 `applicationId`

查看APP当前Activity可以确认正确 `applicationId`

	mFocusedActivity: ActivityRecord{72be82 u0 com.zy.course.dev/com.shensz.course.module.main.activity.MainActivity t1446}

不一致是历史遗留问题，已经转让shensz所有权，所以需要改applicationId。新项目框架直接复用shensz，未修改包名

	package="com.shensz.course"

	defaultConfig {
        applicationId "com.zy.course"

解决方案：统一两者

	修改package略麻烦，会引起R文件找不到(import com.shensz.course.R;报错)，需要改动工程结构重编译才行

	这里修改applicationId，反正也只是为了本地调试RN
	
### 原因3：build.gradle 指定了 `applicationIdSuffix` ###

上面查看APP当前Activity确认正确 `applicationId` 发现 applicationId 有后缀

	buildTypes {
        debug {
            multiDexEnabled true
            minifyEnabled false
            applicationIdSuffix '.dev'

解决方案：指定 applicationId 后缀名

指定后缀名时，后缀名最前面的 `.` 不需要写，RN会自动添加

`react-native run-android --appFolder course  --appIdSuffix dev --main-activity module.main.activity.MainActivity`

运行成功

## 其他错误 ##

运行成功，但在显示RN页面时报错(只能显示原生页面)

	java.util.concurrent.ExecutionException:java.lang.RuntimeException:referenceError:can't find variable:_fbBatchedBridge

	或者
	
	Cannot find entry file index.android.js in any of the roots

### 原因1：没有连上开发服务器 ###

解决方案：打开RN调试菜单，设置IP和端口，Reload JS

### 原因2：RN没有自动生成打包文件 ###

解决方案：手动打包，然后运行

	React-native bundle --platform Android --dev false --entry-file index.android.js --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res

# 调试有坑 #

## 多个react-native node module ##

打开调试(使用开发服务器bundle)开关，红屏报错

	Bundling `index.android.js`  [development, non-minified, hmr disabled]  25.0% (1/2), failed.
	error: bundling failed: ambiguous resolution: module `D:\AndroidProject\rns\ssz_rn_project\js\pages\index.js` tries to require `react-native`, but there are several files providing this module. You can delete or fix them:
	
	  * `D:\AndroidProject\rns\ssz_rn_project\android\node_modules\react-native\package.json`
	  * `D:\AndroidProject\rns\ssz_rn_project\node_modules\react-native\package.json`

### 尝试删除 android\node_modules ###

android\node_modules 是原来Android项目就有的。

尝试删除，重新运行。发现还是提示同样错误，判断是nmp 缓存原因。清除缓存，重启大法都无法解决缓存问题，最后重命名工程文件夹名字解决缓存问题

**删除后会造成无法编译。**报错无法找到 react-native

	 A problem occurred configuring project ':react-native-svg'.
	   > Could not resolve all dependencies for configuration ':react-native-svg:_debugCompile'.
	      > Could not find com.facebook.react:react-native:0.48.4.
	        Searched in the following locations:
	 			https://dl.bintray.com/thelasterstar/maven/com/facebook/react/react-native/0.48.4/react-native-0.48.4.pom
	            https://dl.bintray.com/thelasterstar/maven/com/facebook/react/react-native/0.48.4/react-native-0.48.4.jar
	            https://jitpack.io/com/facebook/react/react-native/0.48.4/react-native-0.48.4.pom
	            https://jitpack.io/com/facebook/react/react-native/0.48.4/react-native-0.48.4.jar
	 			file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native/android/com/facebook/react/react-native/0.48.4/react-native-0.48.4.pom
	            file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native/android/com/facebook/react/react-native/0.48.4/react-native-0.48.4.jar
				file:/D:/AndroidProject/rns/ssz_rn_project/android/node_modules/react-native-svg/android/libs/react-native-0.48.4.jar



查看工程根目录build.gradle

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


**修改工程根目录build.gradle**

	url "$rootDir/../node_modules/react-native/android"


**修改settings.gradle**

	include ':react-native-svg', ':pay', ':base', ':common', ':downloader', ':camera', ':cropper', ':statistics', ':imsdk', ':ping', ':location', ':pdf-view', ':react-native-ssz-pdf', ':course', ':kefu-easeui'
	project(':react-native-svg').projectDir = new File(rootProject.projectDir, 'node_modules/react-native-svg/android')
	include ':react-native-fs'
	project(':react-native-fs').projectDir = new File(rootProject.projectDir, 'node_modules/react-native-fs/android')
	include ':react-native-fetch-blob'
	project(':react-native-fetch-blob').projectDir = new File(rootProject.projectDir, 'node_modules/react-native-fetch-blob/android')

	改后：

	include ':react-native-svg', ':pay', ':base', ':common', ':downloader', ':camera', ':cropper', ':statistics', ':imsdk', ':ping', ':location', ':pdf-view', ':react-native-ssz-pdf', ':course', ':kefu-easeui'
	project(':react-native-svg').projectDir = new File('../node_modules/react-native-svg/android')
	include ':react-native-fs'
	project(':react-native-fs').projectDir = new File('../node_modules/react-native-fs/android')
	include ':react-native-fetch-blob'
	project(':react-native-fetch-blob').projectDir = new File('../node_modules/react-native-fetch-blob/android')

重新运行，调试成功




	



