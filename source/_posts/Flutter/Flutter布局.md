---
title: Flutter布局
date: 2018-07-03 17:00:29
tags:
	- Flutter
---

[Flutter中文文档](https://docs.flutter.kim/) 

# Flutter内置控件

## 分类

- **可视控件**(visible widget)。

	如text、Icon、Button
	
- **布局控件**(layout widget)。

	承载可视控件的容器。如Row、Column、Container。布局控件是为了实现可视控件的各种视觉效果而做的包装

	child可承载单个子控件，children可承载多个子控件。

	布局控件提供了各种样式的参数，可实现子控件的对齐(align)、缩放(size)、包装(pack)和嵌套(Nest)。

## 调试布局样式

通常用到 网格线、标尺、动画帧 等

开启布局调试

main.dart中

```dart
import 'package:flutter/rendering.dart' show debugPaintSizeEnabled;

void main() {
  debugPaintSizeEnabled = true;      //打开视觉调试开关
  runApp(new MyApp());
}
```

# Padding

给子节点设置 内边距 属性

从继承关系可以看出，Padding控件是一个基础控件，Container是组合控件。Container中的margin以及padding属性都是利用Padding控件去实现的。使用Padding比Container的成本要小

Flutter中没有单独的Margin控件，在Container中有margin属性，看源码关于margin的实现可以看出，**Flutter中margin实质上也是由Padding实现的**(淡化了margin以及padding的区别)。

```dart
if (margin != null)
  current = new Padding(padding: margin, child: current);
```

## 布局行为

- child为空, 产生一个宽为left+right，高为top+bottom的区域；
- child不为空，Padding会将布局约束传递给child，根据设置的padding属性，缩小child的布局尺寸。然后Padding将自己调整到child设置了padding属性的尺寸，在child周围创建空白区域。

# Align

设置child的对齐方式，例如居中、居左居右等，并根据child尺寸调节自身尺寸

基础组件，Container中的align属性，是使用Align实现的


## 属性

### alignment

系统默认提供9种对齐方式。

```dart
/// The top left corner.
static const Alignment topLeft = const Alignment(-1.0, -1.0);
```

Alignment包含两个参数。第一个参数，-1.0是左边对齐，1.0是右边对齐；第二个参数，-1.0是顶部对齐，1.0是底部对齐。根据这个规则，我们可以自定义我们需要的对齐方式

```dart
/// 居右高于底部1/4处.
static const Alignment rightHalfBottom = alignment: const Alignment(1.0, 0.5),
```

## 布局行为

- widthFactor和heightFactor为null
	- 有限制条件
		
		根据限制条件尽量的扩展自己的尺寸
		
	- 没有限制条件

		调整到child的尺寸

- widthFactor或者heightFactor不为null

	根据factor属性，扩展自己的尺寸。例如widthFactor为2.0，Align的宽度将会是child的两倍。

Align为什么会有这样的布局行为呢？原因很简单，外层元素尺寸不确定的话，内部的对齐就无法确定。因此，会有宽高因子、根据外层限制扩大到最大尺寸、外层不确定时调整到child尺寸这些行为。

# Center

Center继承自Align，Align的默认实现

# Container #

组合控件，内部有 绘制widget、定位widget、尺寸widget

## 属性

```dart
Container({
    Key key, //唯一标识符，用于查找更新
    this.alignment,
    this.padding,
    Color color, //背景色
    Decoration decoration, //child后面的装饰。设置了这个就不要设置color，否则报错
    this.foregroundDecoration, //前景装饰
    double width, //double.infinity可以强制在宽度上撑满
    double height,
    BoxConstraints constraints, //child上额外的约束
    this.margin,
    this.transform, //变换矩阵，类型为Matrix4
    this.child,
  })
```
 
## 组成

- padding及里层的child
- 额外的constraints限制
- margin

绘制过程如下：

- 首先绘制transform；
- 接着绘制decoration；
- 然后绘制child；
- 最后绘制foregroundDecoration。

## 布局行为

Container组合了一系列的widget，这些widget都有自己的布局行为，因此Container的布局行为有时候是比较复杂的。

### 遵循如下顺序去尝试布局：

- 对齐（alignment）；
	- 父节点提供了unbounded限制，Container调节自身尺寸来包住child；
 	- 父节点提供了bounded限制，Container会将自身调整的足够大（在父节点的范围内），然后将child根据alignment调整位置；
- 调节自身尺寸适合子节点；
- 采用width、height以及constraints布局；
- 扩展自身去适应父节点；
- 调节自身到足够小。

进一步说：

- 如果没有子节点、没有设置width、height以及constraints，并且父节点没有设置unbounded的限制，Container会将自身调整到足够小。
- 如果没有子节点、对齐方式（alignment），但是提供了width、height或者constraints，那么Container会根据自身以及父节点的限制，将自身调节到足够小。
- 如果没有子节点、width、height、constraints以及alignment，但是父节点提供了bounded限制，那么Container会按照父节点的限制，将自身调整到足够大。

- 如果有alignment，父节点提供了unbounded限制，那么Container将会调节自身尺寸来包住child；
- 如果有alignment，并且父节点提供了bounded限制，那么Container会将自身调整的足够大（在父节点的范围内），然后将child根据alignment调整位置；

- 含有child，但是没有width、height、constraints以及alignment，Container会将父节点的constraints传递给child，并且根据child调整自身。

另外，margin以及padding属性也会影响到布局。

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
- spaceAround 剩余空间均匀的分布在children**周围**(两边)。
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

# TextField

```dart
TextField(
      controller: TextEditingController(),
      maxLength: 30,//最大长度，设置此项会让TextField右下角有一个输入数量的统计字符串
      maxLines: 1,//最大行数
      autocorrect: true,//是否自动更正
      autofocus: true,//是否自动对焦
      obscureText: true,//是否是密码
      textAlign: TextAlign.center,//文本对齐方式
      style: TextStyle(fontSize: 30.0, color: Colors.blue),//输入文本的样式
      keyboardType: TextInputType.phone,//键盘类型
      inputFormatters: [WhitelistingTextInputFormatter.digitsOnly],//允许的输入格式
      onChanged: (text) {//内容改变的回调
        print('change $text');
      },
      onSubmitted: (text) {//内容提交(按回车)的回调
        print('submit $text');
        FocusScope.of(context).reparentIfNeeded(FocusNode());
      },
      enabled: true,//是否禁用
    );
```

**decoration**

一般使用InputDecoration

```dart
TextField(
  decoration:
      InputDecoration(fillColor: Colors.blue.shade100, filled: true, labelText: 'Hello'),
);
```

contentPadding 内容padding

fillColor设置填充颜色

labelText设置标签文字，这个标签在没有输入的时候是占满输入框的，当获取聚焦以后，就会缩小到输入框左上角，变为主题色。

hintText设置输入提示，有输入内容后就不显示了

errorText设置错误提示，输入框左下角，红色

helperText设置帮助提示，输入框左下角，黑色

prefixIcon前缀图标，获取焦点后变为主题色

suffixText后缀文本，获取焦点后展示

{% asset_img textField-1.png %}
{% asset_img textField-2.png %}
{% asset_img textField-3.png %}
{% asset_img textField-4.png %}
{% asset_img textField-5.png %}
{% asset_img textField-6.png %}

border 边框，默认为下划线边框。一般使用 OutlineInputBorder

```dart
TextField(
  decoration: InputDecoration(
    border: OutlineInputBorder(
      borderRadius: BorderRadius.circular(15.0),
    )),
);
```
{% asset_img textField-border-1.png %}
{% asset_img textField-border-2.png %}

设置边框颜色。装饰线默认对焦后是主题颜色primaryColor，失去焦点以后是黑色

```dart
Theme(
	data: new ThemeData(primaryColor: Colors.red, hintColor: Colors.blue),
	child: TextField(
	  decoration: InputDecoration(
	      contentPadding: EdgeInsets.all(10.0),
	      border: OutlineInputBorder(
	        borderRadius: BorderRadius.circular(15.0),
	      )),
	),
)
```

设置边框的粗细。需要禁用装饰线，而是使用外面包围的Container的装饰线

```dart
Container(
	padding: const EdgeInsets.all(8.0),
	alignment: Alignment.center,
	height: 60.0,
	decoration: new BoxDecoration(
	    color: Colors.blueGrey,
	    border: new Border.all(color: Colors.black54, width: 4.0),
	    borderRadius: new BorderRadius.circular(12.0)),
	child: new TextFormField(
	  decoration: InputDecoration.collapsed(hintText: 'hello'),
	),
),
```

{% asset_img textField-border-3.png %}

# 布局技巧

## 键盘弹出超出屏幕问题

```dart
return Scaffold(
	resizeToAvoidBottomPadding: false, //输入框抵住键盘
}	
```


