---
title: Android内嵌混合Flutter-跨平台的渐进式解决方案
date: 2018-09-27 11:00:04
tags:
	- Flutter
---

Flutter工程只作为一个module引入工程，代码入侵极小，Android工程和Flutter工程都可以独立运行。

可以只从一个view/一个页面开始来让Flutter参与到项目中去

写此文时，GDD 2018已经结束，使用的是会上发布的preview 2版本，即`Flutter 0.8.2 • channel beta •`

# 创建工程

## 目录结构

	项目根目录
		├── 原生安卓工程 (android) AS打开此工程，可独立运行
			├── app module
			├── 其他 module
		└── Flutter module (flutter_lib) AS打开此工程，可独立运行
			├── .android (纯Flutter工程flutter_app 没有.前缀)
				├── app 
				├── Flutter (纯Flutter工程flutter_app 没有该module)
			├── lib
				├── main.dart
			├── .ios (纯Flutter工程flutter_app 没有.前缀)

| 区别	| Flutter module工程中的Android工程 | 纯Flutter应用工程中的Android工程 |
| ------ | ------ | ------ |
|文件夹名称	| .android |	android |
|包含的module	| app和Flutter	| app |
|说明 | app只提供了入口Activity，Flutter包含了插件扩展及原生工程调用的接口 | app包含入口Activity及插件扩展 |
|说明 |app供Flutter自身开发调试，Flutter作为module供Android原生调用 | app作为Android工程运行及打包 |

## 创建Android工程

这里勾选上kotlin支持。准备用kotlin实现Android原生
			
## 创建Flutter module

flutter create -t module flutter_lib

## 引用Flutter module

android根目录 setting.gradle

 	//加入下面配置
	setBinding(new Binding([gradle: this]))
	evaluate(new File(
	        settingsDir.parentFile,
	        'flutter_lib/.android/include_flutter.groovy'
	))

app的 build.gradle

	...
	dependencies {
	    ...
	    // 加入下面配置
	    implementation project(':flutter')
	}	
	
AS打开android工程，重新构建项目，即可成功的将Flutter加入Android工程(即生成 `根目录/flutter_lib/.android/Flutter`)。	

# Android工程中使用Flutter组件

Flutter提供了两种方式让Android工程来引用组件

- 一种是View

	`FlutterView createView(Activity activity, final Lifecycle lifecycle, final String initialRoute)`
	
- 一种是Fragment

	`FlutterFragment createFragment(String initialRoute)`
	
## 实例：作为页面的根View

	class MainActivity : AppCompatActivity() {
	
	    override fun onCreate(savedInstanceState: Bundle?) {
	        super.onCreate(savedInstanceState)
	        setContentView(R.layout.activity_main)
	        val flutterView = Flutter.createView(this@MainActivity, lifecycle, "route1")
	        val layout = FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT)
	        val layout = FrameLayout.LayoutParams(600, 1200)
	        addContentView(flutterView, layout)
	    }
	}
	
### setContentView然后addContentView的原因--防止启动黑屏

**设置FlutterView加载完成之前展示给用户的界面。** 当然大部分情况下用户根本感知不到这个界面Flutter就已经加载完成了，但我们仍需要它

- 虽然FLutter的加载速度非常快，但是这个过程依然存在
- 如果没有这个界面的话在Activity的加载过程会出现一个黑色的闪屏，用户体验差
- debug模式下Flutter的加载速度并不是非常快，这个界面可以给开发人员看
	- 实际测试发现，即使这样处理，在测试机上debug有黑色闪屏，release正常
		- 可能测试机太渣，直接新建一个helloworld工程(kotlin)冷启动都会有明显白屏

# Flutter工程中根据route创建组件

可以通过window的全局变量中获取到当前的routeName，这个值正是上面通过原生工程传给Flutter的标识，有了这个标识就可以简单的做判断来进行不同的组件创建了：
import 'dart:ui';
import 'package:flutter/material.dart';

void main() => runApp(_widgetForRoute(window.defaultRouteName));

//根据不同的标识创建不同的组件给原生工程调用
Widget _widgetForRoute(String route) {
  switch (route) {
    case 'route1':
      return SomeWidget(...);
    case 'route2':
      return SomeOtherWidget(...);
    default:
      return Center(
        child: Text('Unknown route: $route', textDirection: TextDirection.ltr),
      );
  }
}

# 让Flutter模块支持热加载

项目根目录/flutter_lib下执行

	flutter attach
	
代码执行后，监听服务会等待并监听debug应用中flutter的状态

然后AS中以正常方式调试运行android，当flutter的view或Fragment激活时会触发文件同步。

终端输出如下

	Waiting for a connection from Flutter on Le X620...
	Done.
	Syncing files to device Le X620...                           2.3s
	🔥  To hot reload changes while running, press "r". To hot restart (and rebuild state), press "R".
	An Observatory debugger and profiler on Le X620 is available at: http://127.0.0.1:61500/
	For a more detailed help message, press "h". To detach, press "d"; to quit, press "q".
	
修改flutter工程中的dart代码文件，保存后在**终端中**点击r键即可进行热加载，R键进行热重启。

# 签名打包

常规打包操作即可

	

	

