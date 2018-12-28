---
title: PageView-BottomNavigationBar实现首页页面切换
date: 2018-12-15 16:10:29
tags:
	- Flutter
---

{% asset_img PageView.png %}

`lib/main.dart`

```dart
import 'package:flutter/material.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _currentPageIndex = 0;
  var _pageController = new PageController(initialPage: 0);

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar:
      new AppBar(
        title: new Text("我是AppBar"),
        centerTitle: true,
      ),
      body: new PageView.builder(
        onPageChanged: _pageChange,
        controller: _pageController,
        itemBuilder: (BuildContext context, int index) {
          return index == 0 ? new Text("我是第一页") : new Text("我是第二页");
        },
        itemCount: 2,
      ),
      bottomNavigationBar: new BottomNavigationBar(items: [
        BottomNavigationBarItem(
            icon: new Icon(Icons.category), title: new Text("首页")),
        BottomNavigationBarItem(
            icon: new Icon(Icons.message), title: new Text("我的")),
      ],
        currentIndex: _currentPageIndex,
        onTap: onTap,
      ),
    );
  }

  // bottomnaviagtionbar 和 pageview 的联动
  void onTap(int index) {
    // 通过pageview的pagecontroller的animateToPage方法可以跳转
    _pageController.animateToPage(index,
        duration: const Duration(milliseconds: 300), curve: Curves.ease);
  }

  void _pageChange(int index) {
    setState(() {
      if (_currentPageIndex != index) {
        _currentPageIndex = index;
      }
    });
  }
}
```