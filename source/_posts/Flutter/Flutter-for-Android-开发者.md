---
title: Flutter for Android 开发者
date: 2018-07-04 15:42:04
tags:
	- Flutter
---

本文档适用于Android开发人员，可以将您现有的Android知识应用于使用Flutter构建移动应用程序。您可以将此文档用作Flutter开发的一个开端

# View #

## Widget = Android中的View ##

在Flutter中，Widget相当于Android的View。

### Widget与View不同之处 ###

- 绘制
	- Widget仅支持一帧，并且每一帧上Flutter框架都会创建一个Widget实例树(每一帧它们都会重新构建)。
	- View绘制结束后，就不会重绘，直到调用invalidate时才会重绘
- 更新
	- widget是不可变的，不会直接更新，而必须使用Widget的状态。这允许widget变得超级轻量
	- 直接对view进行改变来更新视图（在framework改变View视图）

**Widget特性**

- 每一帧都会重新构建
- 不可变(不能直接更新)
- 通过Widget的状态(State对象)更新

## 如何布局 ##

Android中，通过XML编写布局

但在Flutter中，使用widget树来编写布局

## 如何更新widget ##

Android中，通过方法直接更新View

但在Flutter中，使用Widget的状态更新Widget

这是Stateful和Stateless widget的概念的来源。

StatefulWidget有一个State对象，它可以跨帧存储状态数据并恢复它(更新)。

可以将StatelessWidget包装在StatefulWidget中实现更新

### Widget如何创建子Widget ###

StatelessWidget实现 `Widget build(BuildContext context)` 创建 Widget

StatefulWidget实现 `State createState();` 创建 自定义State --> 自定义State实现 `Widget build(BuildContext context)` 创建 Widget

示例：**点击按钮更新Text(StatelessWidget的子类)**

	class SampleApp extends StatelessWidget {
	  @override
	  Widget build(BuildContext context) {
	    return new MaterialApp(
	      title: 'Sample App',
	      theme: new ThemeData(primarySwatch: Colors.blue),
	      home: new SampleAppHomePage(),
	    );
	  }
	}
	
	class SampleAppHomePage extends StatefulWidget {
	  SampleAppPage({Key key}) : super(key: key);//官方文档源码有定义该构造函数。但是不写测试没发现问题
	  @override
	  State createState() {
	    return new SampleAppHomeState();
	  }
	}
	
	class SampleAppHomeState extends State<SampleAppHomePage> {
	  String textToShow = 'I Like Flutter';
	
	  void updateText() {
	    setState(() {//匿名函数。void setState(VoidCallback fn)，typedef void VoidCallback();
	      textToShow = 'Flutter is Awesome';
	    });
	  }
	
	  @override
	  Widget build(BuildContext context) {
	    return new Scaffold(
	      appBar: new AppBar(
	        title: new Text('HomePage'),
	      ),
	      body: new Center(
	        child: new Text(textToShow),
	      ),
	      floatingActionButton: new FloatingActionButton(
	        onPressed: updateText,//很奇怪
	        tooltip: 'Update Text',//长按会展示action的描述
	        child: new Icon(Icons.update),
	      ),
	    );
	  }
	}

## 如何在布局中添加或删除组件Widget ##

Android中，可以从父级控件调用addChild或removeChild以动态添加或删除View。 

在Flutter中，在返回widget给父项的函数中通过值(一般是布尔值)控制widget的创建

示例：**点击按钮切换widget**

	class SampleAppHomeState extends State<SampleAppHomePage> {
	  @override
	  Widget build(BuildContext context) {
	    return new Scaffold(
	      appBar: new AppBar(
	        title: new Text('HomePage'),
	      ),
	      body: new Center(
	        child: getBodyChild(),
	      ),
	      floatingActionButton: new FloatingActionButton(
	        onPressed: onPress,
	        child: new Icon(Icons.update),
	      ),
	    );
	  }
	
	  getBodyChild() {
	    if (toggle) {
	      return new Text('Toggle One');
	    } else {
	      return new MaterialButton(
	        onPressed: () {},
	        child: new Text('Toggle Two'),
	      );
	    }
	  }
	
	  bool toggle = true;
	  void onPress() {
	    setState(() {
	      toggle = !toggle;
	    });
	  }
	}

## 动画 ##

Android中，可以通过XML创建动画或在视图上调用.animate()

Flutter中，将widget包装到Animation中，告诉**控制器**(`AnimationController`和`Interpolator`)启动**动画**

示例：**FadeTransition淡入**

	class SampleAppHomeState extends State<SampleAppHomePage> with TickerProviderStateMixin {
	  AnimationController animationController;
	  CurvedAnimation curvedAnimation;
	
	  @override
	  void initState() {
	    super.initState();
	    animationController = new AnimationController(duration: new Duration(microseconds: 2000), vsync: this);
	    curvedAnimation = new CurvedAnimation(parent: animationController, curve: Curves.easeIn);
	  }
	
	  @override
	  Widget build(BuildContext context) {
	    return new Scaffold(
	      appBar: new AppBar(
	        title: new Text('HomePage'),
	      ),
	      body: new Center(
	        child: getBodyChild(),
	      ),
	      floatingActionButton: new FloatingActionButton(
	        onPressed: onPress,
	        child: new Icon(Icons.update),
	      ),
	    );
	  }
	
	  getBodyChild() {
	    return new Container(
	      child: new FadeTransition(
	        opacity: curvedAnimation,
	        child: new FlutterLogo(
	          size: 100.0,
	        ),
	      ),
	    );
	  }
	
	  void onPress() {
	    animationController.forward();
	  }
	}

## Canvas draw/paint ##

CustomPaint和CustomPainter，Canvas

示例使用了手势，先跳过

## 自定义 Widget ##

在Android中，通过**继承**View(覆盖其方法)和**组合**View来实现自定义View

在Flutter中，自定义widget通常是通过**组合**其它widget来实现的，而不是继承。

# Intent #

Intent主要有两种使用场景：在Activity之间切换，以及调用外部组件(如Camera或File picker)

**Flutter没有Intent**

如果需要的话，Flutter可以通过**Native**集成来触发Intent


## Flutter中切换屏幕 ##

两个核心概念和类：

- **Route**是应用程序的“屏幕”或“页面”的抽象（可以认为是Activity）
- **Navigator**是管理Route的Widget。Navigator可以通过push和pop route以实现页面切换

声明页面：

- Android，您可以在**AndroidManifest.xml**中声明您的Activities
- Flutter中，您可以将具有指定Route的Map传递到**顶层MaterialApp**实例

		new MaterialApp(
		    home: new MyAppHome(), // becomes the route named '/'
		    routes: <String, WidgetBuilder> {
		      '/a': (BuildContext context) => new MyPage(title: 'page A'),
		      '/b': (BuildContext context) => new MyPage(title: 'page B'),
		      '/c': (BuildContext context) => new MyPage(title: 'page C'),
		    },
		  )

通过Navigator来切换到命名路由的页面

	Navigator.of(context).pushNamed('/b');

## 处理Android传入的Intent ##

示例：**其他应用程序共享文本到Flutter应用程序**

基本流程：首先处理Android端的共享文本数据，然后等待Flutter请求数据，然后通过MethodChannel发送

## Flutter实现startActivityForResult ##

Navigator.push()返回结果就是新route页面pop的数据

示例：**选择定位位置**

	Map coordinates = await Navigator.of(context).pushNamed('/location');
	Navigator.of(context).pop({"lat":43.821757,"long":-79.226392});//位置路由中，用户选择位置，将结果”pop”出栈

# Activity 和 Fragment #

在Flutter中，这两个概念都等同于Widget

## 生命周期 ##

Android中，可以复写Activity/Fragment的生命周期回调函数

Flutter中，通过添加`WidgetsBindingObserver`监听生命周期事件

	WidgetsBinding.instance.addObserver.(WidgetsBindingObserver)
	
WidgetsBindingObserver

	abstract class WidgetsBindingObserver {
		void didChangeAppLifecycleState(AppLifecycleState state) { }//前后台切换回调
	}

AppLifecycleState

- resumed
	- 可见有焦点。
	- 类似Android的onResume
- inactive
	- 可见，无焦点
	- 随时可能转为 paused
- paused
	- 不可见
	- 随时可能转为 suspending
- suspending
	- 暂时中止
	- iOS暂时不可用

# 资源 #

## 图片 ##

Flutter遵循类似iOS简单的3种分辨率格式: 1x, 2x, 3x.

- 项目根创建images文件夹，子文件夹2x和3x，放入对应图片

		…/my_icon.png
		…/2.0x/my_icon.png
		…/3.0x/my_icon.png
- pubspec.yaml文件中声明这些图片

		assets:
		 - images/my_icon.png
- 使用AssetImage访问图片

		return new AssetImage("images/my_icon.png");

## 依赖：Android Gradle vs Flutter pubspec.yaml ##

在Android中，您可以在Gradle文件来添加依赖项。

在Flutter中，虽然在Flutter项目中的Android文件夹下有Gradle文件，但只有在添加平台相关所需的依赖关系时才使用这些文件。 否则，应该使用pubspec.yaml声明用于Flutter的外部依赖项。

# 触摸事件处理 #

## Widget支持事件监听 ##

将一个函数传递给它并进行处理

	return new RaisedButton(
      onPressed: () {
        print("click");
      },
      child: new Text("Button"));

## Widget不支持事件监听 -- GestureDetector ##

将该Widget包装到GestureDetector中

GestureDetector，可以监听多种手势

- Tap
	- onTapDown
	- onTapUp
	- onTapCancel
	- onTap
- Double tap 用户快速连续两次在同一位置轻敲屏幕.
	- onDoubleTap 
- 长按
	- onLongPress
- 垂直拖动
	- onVerticalDragStart
	- onVerticalDragUpdate
	- onVerticalDragEnd
- 水平拖拽
	- onHorizontalDragStart
	- onHorizontalDragUpdate
	- onHorizontalDragEnd

示例：双击旋转FlutterLogo

	class SampleAppHomeState extends State<SampleAppHomePage>  with TickerProviderStateMixin {
	  @override
	  Widget build(BuildContext context) {
	    return new Scaffold(
	      appBar: new AppBar(
	        title: new Text('HomePage'),
	      ),
	      body: new Center(
	        child: getBodyChild(),
	      ),
	      floatingActionButton: new FloatingActionButton(
	        onPressed: onPress,
	        child: new Icon(Icons.update),
	      ),
	    );
	  }
	
	  AnimationController controller;
	  CurvedAnimation curve;
	
	  @override
	  void initState() {
	    super.initState();
	    controller = new AnimationController(duration: const Duration(milliseconds: 2000), vsync: this);
	    curve = new CurvedAnimation(parent: controller, curve: Curves.easeIn);
	  }
	
	  getBodyChild() {
	    return new GestureDetector(
	      child: new RotationTransition(
	          turns: curve,
	          child: new FlutterLogo(
	            size: 200.0,
	          )),
	      onDoubleTap: () {
	        if (controller.isCompleted) {
	          controller.reverse();
	        } else {
	          controller.forward();
	        }
	      },
	    );
	  }
	
	  void onPress() {
	  }
	}

# Listview & Adapter #

必须确保在合适的时机回收行，否则，你会得到各种疯狂的视觉和内存问题。

	class SampleAppHomeState extends State<SampleAppHomePage>  with TickerProviderStateMixin {
	  @override
	  Widget build(BuildContext context) {
	    return new Scaffold(
	      appBar: new AppBar(
	        title: new Text('HomePage'),
	      ),
	      body: new Center(
	        child: getBodyChild(),
	      ),
	      floatingActionButton: new FloatingActionButton(
	        onPressed: onPress,
	        child: new Icon(Icons.update),
	      ),
	    );
	  }
	
	  void onPress() {
	  }
	
	  getBodyChild() {
	    return new ListView(children: getListData());
	  }
	
	  getListData() {
	    List<Widget> widgets = [];
	    for (int i = 0; i < 100; i++) {
	      widgets.add(new GestureDetector(
	        child: new Padding(
	            padding: new EdgeInsets.all(10.0),
	            child: new Text("Row $i")),
	        onTap: () {//点击item事件
	          print('row $i tapped');
	        },
	      ));
	    }
	    return widgets;
	  }
	
	}

	logcat输出： 07-05 06:21:57.034 1997-2032/com.lyg.flutterapp I/flutter: row 0 tapped

## 动态更新ListView ##

示例：点击item，在列表末尾add一个item

### 新建ListView：setState中创建一个新的List ###

setState被调用时，Flutter渲染引擎会遍历所有的widget以查看它们是否已经改变。 当遍历到ListView时，它会做一个==运算，以查看两个ListView是否相同，因为没有任何改变，因此没有更新数据。

	  List<Widget> widgets = [];
	
	  @override
	  void initState() {
	    super.initState();
	    for (int i = 0; i < 100; i++) {
	      widgets.add(getRow(i));
	    }
	  }
	
	  getBodyChild() {
	    return new ListView(children: widgets);
	  }
	
	  Widget getRow(int i) {
	    return new GestureDetector(
	      child: new Padding(
	          padding: new EdgeInsets.all(10.0),
	          child: new Text("Row $i")),
	      onTap: () {
	        print('row $i tapped');
	        setState(() {
	          widgets = new List.from(widgets);//创建新列表
	          widgets.add(getRow(widgets.length));
	        });
	      },
	    );
	  }

### 新建ListView.Builder：推荐使用 ###

**动态列表或包含大量数据的列表**时，ListView.Builder非常有用。

实际上相当于在Android上使用RecyclerView，会**自动回收列表元素**

	  getBodyChild() {
	    return new ListView.builder(
	        itemCount: widgets.length,
	        itemBuilder: (BuildContext context, int position) {//非常类似Android适配器中的getView()
	          return getRow(position);
	        });
	  }
	
	  Widget getRow(int i) {
	    return new GestureDetector(
	      child: new Padding(
	          padding: new EdgeInsets.all(10.0),
	          child: new Text("Row $i")),
	      onTap: () {
	        print('row $i tapped');
	        setState(() {
	          widgets.add(getRow(widgets.length));//不创建新列表，只添加新元素到列表
	        });
	      },
	    );
	  }

# 异步UI #

Dart是单线程执行模型(默认在主UI线程中运行)，并由事件循环驱动

支持Isolates、事件循环和异步编程。 

## 异步函数 ##

将函数声明为异步函数 `async`，并在该函数中等待 `await` 这个耗时任务返回即可。Dart的事件循环将负责其余的事情

声明异步函数的方式需要注意，是将  `async` 放在 函数体{} 前面

示例：**异步加载数据并将其显示在ListView中**

	import 'package:flutter/material.dart';
	import 'dart:convert';
	import 'package:http/http.dart' as http;

	  List widgets = [];
	
	  @override
	  void initState() {
	    super.initState();
	    loadData();
	  }
	
	  getBodyChild() {
	    return new ListView.builder(
	        itemCount: widgets.length,
	        itemBuilder: (BuildContext context, int position) {
	          return getRow(position);
	        });
	  }
	
	  Widget getRow(int i) {
	    return new Padding(
	        padding: new EdgeInsets.all(10.0),
	        child: new Text("Row ${widgets[i]["title"]}")
	    );
	  }
	
	  loadData() async {
	    String dataURL = "https://jsonplaceholder.typicode.com/posts";
	    http.Response response = await http.get(dataURL);
	    setState(() {
	      widgets = JSON.decode(response.body);
	    });
	  }

## Isolates ##

isolates	英['aɪsəleɪts]	使隔离;使分离;

有时您可能需要处理大量数据，导致UI可能会挂起。

在这种情况下，通过使用Isolates，可以利用多个CPU内核来执行耗时或计算密集型任务。

Isolates是一个独立的执行线程，它运行时不会与主线程共享任何内存。这意味着你不能从该线程访问变量或通过调用setState来更新你的UI。

示例：**Isolate与主线程通信和共享数据以更新UI**

	import 'package:flutter/material.dart';
	import 'dart:convert';
	import 'package:http/http.dart' as http;
	import 'dart:async';
	import 'dart:isolate';

	  getBodyChild() {
	    if (widgets.length == 0) {
	      return new Center(child: new CircularProgressIndicator());//LoadingDialog
	    } else {
	      return new ListView.builder(
	          itemCount: widgets.length,
	          itemBuilder: (BuildContext context, int position) {
	            return getRow(position);
	          });
	    }
	  }
	
	  Widget getRow(int i) {
	    return new Padding(
	        padding: new EdgeInsets.all(10.0),
	        child: new Text("Row ${widgets[i]["title"]}")
	    );
	  }
	
	  loadData() async {
	    ReceivePort receivePort = new ReceivePort();
	    await Isolate.spawn(dataLoader, receivePort.sendPort);
	
	    // The 'echo' isolate sends it's SendPort as the first message
	    SendPort sendPort = await receivePort.first;
	
	    List msg = await sendReceive(sendPort, "https://jsonplaceholder.typicode.com/posts");
	
	    setState(() {
	      widgets = msg;
	    });
	  }
	
	// the entry point for the isolate
	  static dataLoader(SendPort sendPort) async {
	    // Open the ReceivePort for incoming messages.
	    ReceivePort port = new ReceivePort();
	
	    // Notify any other isolates what port this isolate listens to.
	    sendPort.send(port.sendPort);
	
	    await for (var msg in port) {
	      String data = msg[0];
	      SendPort replyTo = msg[1];
	
	      String dataURL = data;
	      http.Response response = await http.get(dataURL);
	      // Lots of JSON to parse
	      replyTo.send(JSON.decode(response.body));
	    }
	  }
	
	  Future sendReceive(SendPort port, msg) {
	    ReceivePort response = new ReceivePort();
	    port.send([msg, response.sendPort]);
	    return response.first;
	  }