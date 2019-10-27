---
title: CocosCreator跨平台原理
date: 2019-10-22 11:02:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 系统架构

{% asset_img CocosCreator架构.jpg %}

## native 层

最底层

Cocos2d-x 框架在这一层提供了对 JavaScriptCore、SpiderMonkey、V8、ChakraCore 等多种可选的 JS 执行引擎的封装。

右侧是我们在底层自定义封装的多种基础能力，包括支持直出的webview、自定义的视频播放器、音频播放器、支付、推送等。

## JSB 层 
 
桥接作用。

## JS 层

Cocos在这一层提供了丰富的开发组件和 API，即 Creator组件。

我们也扩展了多种组件，包括一些通用的UI组件、一个多端通用的音频播放器、一个带缓存和内存回收功能的图片加载器、常驻节点、上报、日志等组件。有些组件是依赖 native 层的。

## JS 层和 Native 层 交互

通过 `jsb.reflection.callStaticMethod` 和 `Cocos2dxJavascriptJavaBridge.evalString.evalString` 来完成互相调用。

## 场景开发

有了上面这些基础后，再往上则可以开展具体的场景开发了。

# 渲染原理

为了更好地理解 Cocos 的跨平台原理，我们可以拿 Cocos 的渲染原理和 React Native 做一个对比

## Cocos

{% asset_img Cocos渲染原理.jpg %}

在 UI 线程将场景文件理解成场景树，然后交给 GL 线程渲染。

也就是说，用户看到的大部分场景都是使用 OpenGL 或者 WebGL 绘制的，即使在不同的平台，也能够有完全相同的表现。

## React Native

{% asset_img React Native渲染原理.jpg %}

将 JS/JSX 理解成 Virtual DOM，然后调用各自平台的 Widget 。

由于不同的平台，底层的 Widget 表现是不同的，因此使用上可能会存在差异。

# 参考&扩展

- [腾讯用 Cocos Creator 改造教育 app，尽显高性能跨平台优势](https://zhuanlan.zhihu.com/p/39006183) ABCmouse；架构分析；自定义底层功能、增加通用UI、音频播放、视频播放；踩坑；性能优化；收益分析；