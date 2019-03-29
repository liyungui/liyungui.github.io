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

StatefulWidget有一个State对象，它可以跨帧存储状态数据并恢复它(更新)。**State对象有个`widget`变量持有它的widget**

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
- **Navigator**是通过堆栈管理Route的Widget。Navigator可以通过push和pop route以实现页面切换

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

通过Navigator切换到MaterialPageRoute实例页面

	Navigator.push(context, new MaterialPageRoute<void>(
	  builder: (BuildContext context) {//通过build创建widget展示到屏幕，从而绑定context实现push和pop
	    return new Scaffold(
	      appBar: new AppBar(title: new Text('My Page')),
	      body: new Center(
	        child: new FlatButton(
	          child: new Text('POP'),
	          onPressed: () {
	            Navigator.pop(context);//退出页面
	          },
	        ),
	      ),
	    );
	  },
	));

### 路由带参和返回参数

必须使用 MaterialPageRoute 进行路由。

使用命名路由报错如下

```
type 'MaterialPageRoute<dynamic>' is not a subtype of type 'Route<String>'
```

实例：跳转登录页面，返回用户信息刷新页面

```dart
String string = await Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => Login()));
        
login.dart页面
Navigator.pop(context, "");
```
## 处理Android传入的Intent ##

**Flutter通过自定义MethodChannel和原生交互**

示例：**其他应用程序共享文本到Flutter应用程序**

基本流程：首先处理Android端的共享文本数据，然后等待Flutter请求数据，然后通过MethodChannel发送

manifest中为MainActivity添加 intent-filter
	
	<intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>

MainActivity中 注册MethodChannel

	public class MainActivity extends FlutterActivity {//继承FlutterActivity
	  String sharedText;
	  @Override
	  protected void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    GeneratedPluginRegistrant.registerWith(this);//生成Flutter工程默认实现

	    Intent intent = getIntent();
	    String action = intent.getAction();
	    String type = intent.getType();
	
	    if (Intent.ACTION_SEND.equals(action) && type != null) {
	      if ("text/plain".equals(type)) {
	        sharedText = intent.getStringExtra(Intent.EXTRA_TEXT); // Handle text being sent
	      }
	    }
	
	    new MethodChannel(getFlutterView(), "app.channel.shared.data").setMethodCallHandler(new MethodChannel.MethodCallHandler() {
	      @Override
	      public void onMethodCall(MethodCall methodCall, MethodChannel.Result result) {
	        if (methodCall.method.contentEquals("getSharedText")) {
	          result.success(sharedText);
	          sharedText = null;
	        }
	      }
	    });
	  }
	
	}

Flutter中 使用MethodChannel

	import 'package:flutter/material.dart';
	import 'package:flutter/services.dart';
	
	  static const platform = const MethodChannel('app.channel.shared.data');
	  String dataShared = "No data";
	
	  @override
	  void initState() {
	    super.initState();
	    getSharedText();
	  }
	
	  getBodyChild() {
	    return new Text(dataShared);
	  }
	
	  getSharedText() async {
	    var sharedData = await platform.invokeMethod("getSharedText");
	    if (sharedData != null) {
	      setState(() {
	        dataShared = sharedData;
	      });
	    }
	  }

在系统浏览器中选中一段文本，右键分享，选择APP，发现APP内容刷新为分享的文本

## Flutter实现startActivityForResult ##

Navigator.push()返回结果就是新route页面pop的数据

示例：**选择定位位置**

	Map coordinates = await Navigator.of(context).pushNamed('/location');
	Navigator.of(context).pop({"lat":43.821757,"long":-79.226392});//位置路由中，用户选择位置，将结果”pop”出栈

## PopupRoute ##

半透明模态页面(阻断下面的页面获取焦点)，直接覆盖在当前route上面

创建和显示PopupRoute的函数有：`showDialog`, `showMenu`, `showModalBottomSheet`

PopupRoute类Widget有：`PopupMenuButton`, `DropdownButton`。原理是创建 PopupRoute的内部子类，通过Navigator来显示隐藏

## Custom routes ##

`PageRouteBuilder`自定义页面，包括页面动画，样式，行为等

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

## 异步函数--async和await ##

将函数声明为异步函数 `async`，并在该函数中等待 `await` 这个耗时任务返回即可。Dart的事件循环将负责其余的事情

声明异步函数的方式需要注意，是将  `async` 放在 函数体{} 前面

- await关键字可以获取async函数返回值
- await关键字必须在async函数内部使用
			
### 示例：**异步加载数据并将其显示在ListView中**

添加http依赖

	pubspec.yaml文件
		dependencies:
			http: '>=0.11.3+12'
			
代码

```dart
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
```

HTTP的get请求返回值为`Future<String>`类型

## Dart进程/线程机制--Isolates ##

isolates	英['aɪsəleɪts]	使隔离;使分离;

Dart进程/线程机制，名叫isolate。

APP的启动入口main函数就是一个isolate

Isolates是一个独立的执行线程，线程之间无法直接共享内存，只能通过isolate API进行通信。所以子线程不能访问类变量或通过调用setState来更新UI。

示例：**Isolate与主线程通信共享数据更新UI(带进度指示器)**

```dart
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
```

## Future

### 线程消息循环机制

{% asset_img event-loop.png %}

Dart线程中消息循环机制（event loop）有两个队列（event queue和microtask queue）

- **event queue**
	- 所有外来的事件都会先放入event queue中排队等待执行。
		- 事件：I/O，mouse events，drawing events，timers，isolate之间的message等 
	- 好比机场的公共排队大厅。
- **microtask queue**
	- 只在当前isolate的任务队列中排队
	- 优先级高于event queue
	- 好比机场里的某个VIP候机室，总是VIP用户先登机了，才开放公共排队入口。
	- 实际提供了一种插队机制
	- 当事件循环正在处理microtask的时候，event queue会被堵塞。这时候app就无法进行UI绘制，响应鼠标事件和I/O等事件
	
当main方法执行完毕退出后，event loop就会以FIFO(先进先出)的顺序执行microtask，当所有microtask执行完后它会从event queue中取事件并执行。如此反复，直到两个队列都为空

### Future是event

每创建一个Future就会把这个Future扔进event queue中排队等候安检~

Http的get函数、RefreshIndicator的onRefresh函数是event。

被await标记的句柄也是一个event


### 为什么要用Future

用async和await组合，即可向event queue中插入event实现异步操作

为什么还要用Future呢？

- 定义Flutter函数时，可以指定其运行结果**返回值类型**，以提高代码的**可读性**
- 最主要的功能就是提供了**链式调用**
	- 链式调用解决两大问题：明确代码执行的依赖关系和实现异常捕获

实例代码

```dart
new Future.then(funA()).then(funB());   // 明确表现出了后者依赖前者设置的变量值
 
  new Future.then(funA()).then((_) {new Future(funB())});    //还可以这样用

  //链式调用，捕获异常
  new Future.then(funA(),onError: (e) { handleError(e); }).then(funB(),onError: (e) { handleError(e); }) 
```

# Flutter packages #

## 使用 packages ##


[GPS插件](https://pub.dartlang.org/packages/location)

[相机插件](https://pub.dartlang.org/packages/image_picker)

Packages会被发布到了 [Pub](https://pub.dartlang.org/) 包仓库.

### 使用步骤 ###

- 添加包依赖
	- `pubspec.yaml`文件`dependencies`下添加
- 安装包依赖
	- terminal中: 运行 flutter packages get
	- 或者IntelliJ中: 点击pubspec.yaml文件顶部的’Packages Get’
- 导入包依赖
	- 在Dart代码中添加相应的import语句.

### 管理包依赖和版本 ###

#### Package versions ####

	dependencies:
	  css_colors: //被解释为 css_colors: any可以使用任何版本的包。为了稳定性，建议指定版本范围
	  url_launcher: '>=0.1.2 <0.2.0'  //指定一个最小和最大的版本号
	  collection: '^0.1.2' //caret 语法

#### 更新依赖包 ####

添加一个包后首次运行（IntelliJ中的’Packages Get’）flutter packages get，Flutter将找到包的版本保存在 `pubspec.lock`。这确保了团队中的其他开发人员运行flutter packages get后回获取相同版本的包

升级到软件包的新版本，请运行flutter packages upgrade（在IntelliJ中点击Upgrade dependencies）。 这将根据您在pubspec.yaml中指定的版本约束下载所允许的最高可用版本

#### 管理包依赖 ####

- 发布到 **Pub**
- **路径** 支持相对路径和绝对路径

		dependencies:
	  	  plugin1:
	        path: ../plugin1/
- **Git**

		dependencies:
		  plugin1:
		    git:
		      url: git://github.com/flutter/plugin1.git //包位于Git存储库的根目录中
			  //还可以通过path指定非根目录包，ref指定commit，branch或tag
			  path: packages/package1    

## 开发Packages ##

### Package 介绍 ###

创建可轻松共享的模块化代码

#### Package 结构 ####

一个最小的package包括

- 一个 `pubspec.yaml` 文件：声明了package的名称、版本、作者等的元数据文件。

- 一个 `lib` 文件夹：包括包中公开的(public)代码，最少应有一个 `<package-name>.dart` 文件

#### Package 类型 ####

- Dart包：
	- 可能依赖Flutter框架
- 插件包：
	- 包含针对Android（使用Java或Kotlin）和/或针对iOS（使用ObjC或Swift）平台的特定实现。一个具体的例子是`battery`插件包。

### 开发Dart包 ###
