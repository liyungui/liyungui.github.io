---
title: RN图片资源
date: 2018-08-06 17:21:21
tags:
	- RN
---
# 资源属性是一个对象 #

**图片的资源属性，不接受字符串，只接受带有uri属性的对象**

## 优势 ##

- **方便开发者在对象中添加一些元数据(metadata)**
	- 例如写入图片尺寸(而不必在样式中写死)
- 利于扩展
	- 未来可能加入精灵图（sprites）的支持。理论上可以无缝支持精灵图的切分
		- 进一步输出裁切信息{uri: ..., crop: {left: 10, top: 50, width: 20, height: 40}}

# 在主线程外解码图片 #

 React Native 中，图片解码则是在另一线程中完成的

# RN图片资源 #

**require("完整文件名，带路径")**

	<Image source={require("./logo.png")} />

require现在返回的对象包含**真实文件路径以及尺寸**等信息

	{
	  "__packager_asset":true,
	  "isStatic":true,
	  "path":"/Users/react/HelloWorld/iOS/Images.xcassets/react.imageset/logo.png",
	  "uri":"logo",
	  "width":591,
	  "height":573
	}

## 优势 ##

- Packager可以得知图片大小，在代码里**不需要再声明尺寸**
	- 也可通过style属性调整为新的大小
- iOS 和 Android 一致的文件系统
- 通过 npm 来分发组件或库可以包含图片

## 查找规则 ##

- 根据平台
	- `my-icon.ios.png` 和 `my-icon.android.png`
- 根据屏幕精度
	- `check@2x.png` 和 `check@3x.png`
	- 会打包所有**实际被用到(即require)**的图片并且依据屏幕精度提供对应的资源
		- require图片名字必须是**静态字符串(非变量)**
			- 因为**require是编译时期执行**
		- 如果没有图片恰好满足屏幕分辨率，则选中最接近的一个图片

注意：添加图片的时候 packager 正在运行，可能需要**重启 packager** 以便能正确引入新添加的图片

实例：require图片名字必须是静态字符串

	// 正确
	var icon = this.props.active
	  ? require("./my-icon-active.png")
	  : require("./my-icon-inactive.png");
	<Image source={icon} />;

# Native的图片资源 #

**注意：保证存在，指定尺寸**

## iOS的asset, Android的drawable ##

**uri: "只使用文件名，不带路径和后缀"**

	<Image source={{ uri: "app_icon" }} style={{ width: 40, height: 40 }} />

## Android的assets ##

**uri: "asset:/文件名，不带路径"**

	<Image
	  source={{ uri: "asset:/app_icon.png" }}
	  style={{ width: 40, height: 40 }}
	/>

# 网络图片 #

**注意：保证存在，指定尺寸**

## url图片 ##

**uri: "https://..."**

	<Image source={{uri: 'https://facebook.github.io/react/logo-og.png'}}
	       style={{width: 400, height: 400}} />

## 数据图片 ##

**uri: "data:image/png;base64,...**

建议仅对**非常小的图片**使用 base64 数据，比如一些小图标。

## 网络图片的请求参数 ##

**在 Image 组件的 source 属性中指定一些请求参数**

	<Image
	  source={{
	    uri: "https://facebook.github.io/react/logo-og.png",
	    method: "POST",
	    headers: {
	      Pragma: "no-cache"
	    },
	    body: "Your Body goes here"
	  }}
	  style={{
		width: 400, 
		height: 400,
		resizeMode: Image.resizeMode.contain
	  }}
	/>

# 本地文件系统中的图片 #

# 为什么不在所有情况下都自动指定尺寸 #

## 浏览器处理方式 ##

如果不给图片指定尺寸，那么浏览器会首先渲染一个 0x0 大小的元素占位，然后下载图片，在下载完成后再基于正确的尺寸来渲染图片

## 缺陷 ##

UI 会在图片加载的过程中上下跳动，使得用户体验非常糟糕

## RN处理方式 ##

**RN图片资源无需指定(加载时立刻知道尺寸)，其他的都需要手动指定**

