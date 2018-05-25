---
title: Android Studio 运行 Java代码
date: 2018-05-25 11:45:08
tags: 
	- Android Studio
	- Java
---

# 修改启动方式 #

目前有2种方法 :

## 右键运行方法 ##

在Java文件中添加main方法，  鼠标点击到main方法里任意地方，然后点击鼠标右键，选择Run 'MainActivity main()'或者Debug 'MainActivity main'就行了

### 异常 ###

	Error:Gradle: failed to create directory 'D:\AndroidProject\app\build\generated\source\r\debug\com\example\test'.

Android Studio 3.0，在项目的 gradle.properties 中添加 android.enableAapt2=false 即可

## Java Library ##

new Module -- Java Library

运行处有个下拉小箭头，点击Edit Configuration -- Add New Configuration -- Application

	Name 名字随便，这里取名Java
	Main class 填要运行的Java类路径
	Use class of Module 选择lib名字

运行处选择运行方式为Java， 然后点击绿色运行按钮就行了

# 直接创建JAVA文件 #

类文件上右键 ，`Run 'MainClass.mian()'`

# 使用Gradle编译和运行Java程序 #

build.gradle

	apply plugin: 'java'  
	apply plugin: 'application'  
	  
	mainClassName = 'com.binwin20.testjava.Main' // main() 的路径

运行java

	gradle -q run  