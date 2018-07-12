---
title: Flutter布局
date: 2018-07-03 17:00:29
tags:
	- Flutter
---

[Flutter中文文档](https://docs.flutter.kim/) 

# Row 和 Column #

行。水平方向上排列子widget

列。垂直方向上排列子widget

## 对齐 ##

### 对齐方向 ###

- mainAxisAlignment **主轴**
- crossAxisAlignment **垂直轴**

对于行，主轴水平，垂直轴垂直。对于列，主轴垂直，垂直轴水平。

### 属性 ###

- start
- end
- center
- spaceBetween  剩余空间均匀的分布在children**之间**
- spaceAround 剩余空间均匀的分布在children**周围**(两边)
- spaceEvenly  剩余空间均匀的分布在children**之间和周围**

{% asset_img space.png %}

	body: new Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        new Image.asset(
          'images/lake.jpg',
          width: 100.0,
          height: 100.0,
          fit: BoxFit.cover,
        ),
        new Image.asset(
          'images/lake.jpg',
          width: 100.0,
          height: 100.0,
          fit: BoxFit.cover,
        ), new Image.asset(
          'images/lake.jpg',
          width: 100.0,
          height: 100.0,
          fit: BoxFit.cover,
        ),
      ])),


# Expanded #

只可用于Row、Column、Flex内，会被Expanded撑开，充满主轴可用空间

如果多个子组件展开，可用空间会被其伸缩因子(可理解为比例,每个控件默认为1) `flex` 分割

Row、Column、Flex到Expanded的路径必须只包括StatelessWidgets或StatefulWidgets组件

	body: new Row(
      children: [
        new Image.asset('images/lake.jpg'),
        new Image.asset('images/lake.jpg'),
        new Image.asset('images/lake.jpg'),
      ])),

当布局太大而不适合设备时，沿着受影响的边缘会出现黄黑条纹。例如，示例中的行对于设备的屏幕来说太宽了

{% asset_img out-width.png %}

	body: new Row(children: [
        new Expanded(
          child: new Image.asset('images/lake.jpg'),
        ),
        new Expanded(
          child: new Image.asset('images/lake.jpg'),
        ),
        new Expanded(
          child: new Image.asset('images/lake.jpg'),
        ),
      ])),

{% asset_img Expanded.png %}

# Container #

绘制、定位、调整大小

- constraints : Additional constraints to apply to the child。 类型是 BoxConstraints
- decoration ： The decoration to paint behind the child。类型是Decoration
- foregroundDecoration ： The decoration to paint in front of the child
- transform ：The transformation matrix to apply before painting the container. 类型是 Matrix4

示例

	body: new Container(
      constraints: new BoxConstraints.expand(
        height:
            Theme.of(context).textTheme.display1.fontSize * 1.1 + 200.0,
      ),
      padding: const EdgeInsets.all(8.0),
      color: Colors.teal.shade700,
      alignment: Alignment.center,
      child: new Text('Hello World',
          style: Theme
              .of(context)
              .textTheme
              .display1
              .copyWith(color: Colors.white)),
      foregroundDecoration: new BoxDecoration(
        image: new DecorationImage(
          image: new NetworkImage(
              'http://img.zcool.cn/community/0142135541fe180000019ae9b8cf86.jpg@1280w_1l_2o_100sh.png'),
          centerSlice: new Rect.fromLTRB(270.0, 180.0, 1360.0, 730.0),
        ),
      ),
      transform: new Matrix4.rotationZ(0.1),
    ))

# Scaffold #

属性有：

- appBar 顶部bar
- body 中间内容
- bottomNavigationBar 底部导航
- persistentFooterButtons 底部按钮
- floatingActionButton 右下角悬浮按钮
- drawer 抽屉。 Swipes in from either left-to-right (TextDirection.ltr) or right-to-left (TextDirection.rtl) 
- endDrawer 抽屉

# MaterialApp #

- title ： 任务管理窗口(历史堆栈)中所显示的应用名字
- theme ： 主题颜色
- color ： 主要颜色值（primary color），也就是安卓任务管理窗口中所显示的应用颜色
- home ： 默认显示的界面 Widget
- builder ： 
	- 类型是TransitionBuilder。
		- Widget TransitionBuilder(BuildContext context, Widget child)
- routes ： 多页面路由(跳转)规则。 
	- 类型是 Map<String, WidgetBuilder>。
		- Widget WidgetBuilder(BuildContext context)
	- 当使用 Navigator.pushNamed 来路由的时候
		- 会在 routes 查找路由名字
		- 然后使用 对应的 WidgetBuilder 来构造一个带有页面切换动画的 MaterialPageRoute。
	- 只有routes时，必须有Navigator.defaultRouteName(`/`)的入口。
	- 有 home，又有Navigator.defaultRouteName(`/`)的入口，就会出错，home冲突
	- 查找的路由在 routes 中不存在，则会通过 onGenerateRoute 来查找
- initialRoute ：默认显示的路由名字，默认值为 Window.defaultRouteName。
- onGenerateRoute ： 生成路由的回调函数
- onLocaleChanged ： 系统修改语言的回调
- navigatorObservers ： 应用 Navigator 的监听器
- debugShowMaterialGrid ： 是否显示基础布局网格(调试 UI 的工具)
- showPerformanceOverlay ： 显示性能标签
- checkerboardRasterCacheImages 、showSemanticsDebugger、debugShowCheckedModeBanner 调试开关

示例，注释掉home,使用routes

	routes: <String, WidgetBuilder>{
	    Navigator.defaultRouteName: (context) => Scaffold(
	        appBar: AppBar(
	          title: Text('Flutter Title'),
	        ),
	        body: new Container(
	          constraints: new BoxConstraints.expand(
	            height:
	                Theme.of(context).textTheme.display1.fontSize * 1.1 + 200.0,
	          ),
	          padding: const EdgeInsets.all(8.0),
	          color: Colors.teal.shade700,
	          alignment: Alignment.center,
	          child: new Text('Hello World',
	              style: Theme
	                  .of(context)
	                  .textTheme
	                  .display1
	                  .copyWith(color: Colors.white)),
	          foregroundDecoration: new BoxDecoration(
	            image: new DecorationImage(
	              image: new NetworkImage(
	                  'http://img.zcool.cn/community/0142135541fe180000019ae9b8cf86.jpg@1280w_1l_2o_100sh.png'),
	              centerSlice: new Rect.fromLTRB(270.0, 180.0, 1360.0, 730.0),
	            ),
	          ),
	          transform: new Matrix4.rotationZ(0.1),
	        ))
	  },




