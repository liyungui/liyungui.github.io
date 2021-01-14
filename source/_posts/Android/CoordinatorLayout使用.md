---
title: CoordinatorLayout使用
date: 2019-12-12 17:00:53
categories: 
	- Android
tags: 
	- Android
---

# CoordinatorLayout

协调者布局

协调child之间的联动

## 原理

主要依靠一个插件--Behavior。

Behavior不仅仅协助联动，而且还接管了child的三大流程

CoordinatorLayout就根据每个希望被协调的child所携带的Behavior信息进行协调。

## 使用

CoordinatorLayout 一般和 AppbarLayout 以及实现了NestedScrollView控件(RecyclerView) 配合使用

与AppbarLayout组合的滚动布局需要设置 `app:layout_behavior = "@string/appbar_scrolling_view_behavior"`，AppbarLayout才能响应滚动布局的滚动事件。


# AppBarLayout

本身自带Behavior

LinearLayout了类，默认方向 Vertical

在CoordinatorLayout中实现折叠ActionBar效果的首选控件。

AppBarLayout必须作为CoordinatorLayout的直接子View，否则它的大部分功能将不会生效，如`layout_scrollFlags`等

## `app:layout_scrollFlags`属性

```
noScroll 不可滚动，默认
scroll 可滚动出屏幕

exitUntilCollapsed 
当标题栏向上逐渐“消逝”时，会一直往上滑动，
直到剩下的的高度达到它的最小高度后，再响应滑动组件的内部滑动事件。

enterAlways
当滑动组件向下滚动时，标题栏会直接往下滚动。

enterAlwaysCollapsed
视图以最小高度进入，只有当滚动视图到达顶部时才扩大到完整高度。
```

## 监听

```
mAppBar.addOnOffsetChangedListener(new AppBarLayout.OnOffsetChangedListener() {
    @Override
    public void onOffsetChanged(AppBarLayout appBarLayout, int verticalOffset) {
        int scrollRange = appBarLayout.getTotalScrollRange();//最大可滚动距离
```

# CollapsingToolbarLayout

工具栏的包装器,它通常作为AppBarLayout的孩子。

主要实现以下功能

- title（展开时的标题，titleEnable设置为true才生效）
	- 文本
	- setTitle(CharSequence)
- expandedTitleGravity 展开时title对齐方式
	- expandedTitleMargin
	- expandedTitleTextAppearance 
	- setExpandedTitleColor();
- collapsedTitleGravity 折叠时title对齐方式
	- collapsedTitleTextAppearance
	- setCollapsedTitleTextColor():
- contentScrim（内容装饰），当我们滑动的位置 到达一定阀值的时候，内容 装饰将会被显示或者隐藏
	- Drawable。默认是colorPrimary的色值
	- setContentScrim(Drawable)
	- scrimAnimationDuration 设置颜色动画时间
- statusBarScrim（状态栏装饰）
	- Drawable。默认是colorPrimaryDark的色值
	- setStatusBarScrim(Drawable) 
- Parallax scrolling children，- Pinned position children，固定位置的 孩子

## `app:layout_collapseMode`

- parallax 滑动的时候孩子呈现视觉差效果(滚动速度慢一些)
	- layout_collapseParallaxMultiplier 视差因子，值为：0~1
- pin 固定位置


# 参考&扩展

- [CoordinatorLayout使用详解: 打造折叠悬浮效果](https://blog.csdn.net/jxf_access/article/details/79564669)
- [AppbarLayout的简单用法](https://www.jianshu.com/p/bbc703a0015e) 折叠属性详细展示
- [CollapsingToolbarLayout使用](https://www.jianshu.com/p/564a0c56022b) 折叠属性详细展示；折叠状态监听