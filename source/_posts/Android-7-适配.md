---
title: Android 7 适配
date: 2018-05-24 18:40:36
tags: Android
---

# FileProvider替代file://Uri #

不再允许在app中把file://Uri暴露给其他app，包括但不局限于通过Intent或ClipData 等方法

提供了FileProvider，使用它生成content://Uri来替代file://Uri。

## 原因 ##

使用file://Uri会有一些风险，比如：

- 文件是私有的，接收file://Uri的app无法访问该文件。
- Android6.0引入运行时权限，如果接收file://Uri的app没有申请READ_EXTERNAL_STORAGE权限，在读取文件时会引发崩溃。

## FileProvider ##

manifest application节点下

	<provider
		android:authorities="${applicationId}.fileProvider"
		android:exported="false"
		android:grantUriPermissions="true">
		<meta-data
            android:name="android.support.FILE_PROVIDER_PATHS"
			android:resource="@xml/provider_paths"/>
    </provider>

res/xml/provider_paths.xml 指定路径和转换规则

	<?xml version="1.0" encoding="utf-8"?>
	<paths xmlns:android="http://schemas.android.com/apk/res/android">
	    <files-path name="cache_pdf" path="cache/pdf/"/>
	    <external-files-path name="external_cache_pdf" path="cache/pdf/"/>
	    <external-path name="external_image" path="zywx/image/"/>
	</paths>

代码

	//Uri photoOutputUri = Uri.fromFile(photoOutputFile);
	Uri photoOutputUri = FileProvider.getUriForFile(
	                    mContext,
	                    mActivity.getPackageName() + ".fileprovider",
	                    photoOutputFile);
	            intent.putExtra(MediaStore.EXTRA_OUTPUT, photoOutputUri);

## 注意 ##

android.support.v4.content.FileProvider 类只可以在manifest中注册一次。就如同一个Activity只可以注册一次一样

	Error:
		Element provider#android.support.v4.content.FileProvider at AndroidManifest.xml:119:9-131:20 duplicated with element declared at AndroidManifest.xml:105:9-117:20

一些第三方sdk为了适配android 7 也添加了这个节点

解决方案：

- 自定义类 继承自FileProvider
- 使用合并规则替换resource为我们的xml，然后把第三方sdk中的路径配置copy到provider_paths.xml
	- 如果 authorities 不一致，就是利用合并规则替换了，也会报错。因为第三方库java代码大概率写死了 authorities。
		- 代码不要写死 authorities，从manifest动态获取

## 异常处理 ##

- FileUriExposedException

		android.os.FileUriExposedException: file:///storage/emulated/0/Android/data/com.zy.course.dev/1467180514061025%23kefuchannelapp54752/test_22616/video/1527152182117.mp4 exposed beyond app through Intent.getData()
			at android.os.StrictMode.onFileUriExposed(StrictMode.java:1799)
			at android.net.Uri.checkFileUriExposed(Uri.java:2346)

	- 解决方案：使用FileProvider代替Uri.fromFile


- java.lang.SecurityException: Provider must not be exported
	- 解决方案：android:exported必须设置成false


- Attempt to invoke virtual method 'android.content.res.XmlResourceParser android.content.pm.PackageItemInfo.loadXmlMetaData(android.content.pm.PackageManager, java.lang.String)' on a null object reference
	- 解决方案：AndroidManifest.xml处的android:authorities必须跟 mActivity.getPackageName() + ".fileProvider" 一样





