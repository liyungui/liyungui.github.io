---
title: Flutter环境配置
date: 2018-12-15 15:33:29
tags:
	- Flutter
---

环境：mac

# Flutter概述

## Flutter channels

four release channels: 

- stable
- beta
- dev
- master

## Web支持

2019年9月,谷歌开发者大会正式发布了`Flutter 1.9`版本,正式将`flutter_web` 合并到了 flutter `master`

`1.12`版本beta分支开始支持Web，但官方不建议用于生产环境 

目前，hot reload 还不支持web

# 使用镜像

Flutter官方为中国开发者搭建了临时镜像

可以参考 [Using Flutter in China](https://flutter.dev/community/china) 以获得有关镜像服务器的最新动态

将如下环境变量加入到用户环境变量中：

```
export PUB_HOSTED_URL=https://pub.flutter-io.cn
export FLUTTER_STORAGE_BASE_URL=https://storage.flutter-io.cn
```

# 安装Flutter SDK

## 下载SDK zip

## 解压zip

## 添加flutter的bin目录到环境变量

## 检查安装依赖项

运行 `flutter doctor` 

该命令检查您的环境并在终端窗口中显示报告。Dart SDK已经在捆绑在Flutter里了，没有必要单独安装Dart。 仔细检查命令行输出以获取可能需要安装的其他软件或进一步需要执行的任务（以粗体显示）

一旦你安装了任何缺失的依赖，再次运行`flutter doctor`命令来验证你是否已经正确地设置了

# 配置Android Studio

## 安装Android Studio

3.0版本以上

## 安装插件

- Flutter插件： 支持Flutter开发工作流 (运行、调试、热重载等).
- Dart插件： 提供代码分析 (输入代码时进行验证、代码补全等).

# 配置VS Code

如果想进行web应用开发，需要配置vs code

## 安装VS Code

最新版本

## 安装插件

- Flutter插件

# Android体验Flutter

## AS创建新应用

```
1. 选择 File>New Flutter Project
2. 选择 Flutter application 作为 project 类型, 然后点击 Next
3. 输入项目名称 (如 myapp), 然后点击 Next
4. 点击 Finish
5. 等待Android Studio安装SDK并创建项目.

在项目目录中，您应用程序的代码位于 lib/main.dart.
```

## AS运行应用程序

```
在工具栏中点击 Run图标, 或者调用菜单项 Run > Run.
如果一切正常, 您应该在您的设备或模拟器上会看到启动的应用程序
```

# Web体验Flutter

## 开启web support

`1.12`版本beta分支开始支持Web，但官方不建议用于生产环境

```
 flutter channel beta
 flutter upgrade
 flutter config --enable-web
```

输出 `Setting "enable-web" value to "true".`表示成功开启web支持

运行 `flutter devices` 发现设备列表多了 `Chrome和Web Server`

```
3 connected devices:

LLD AL20   • 37KRX18A25012338 • android-arm64  • Android 8.0.0 (API 26)
Chrome     • chrome           • web-javascript • Google Chrome 80.0.3987.163
Web Server • web-server       • web-javascript • Flutter Tools
```

## 创建项目

用IDE或者命令创建 全新项目

## 运行项目

`flutter run -d chrome`

会自动在Chrome打开页面

## 老项目 增加web support

如果是老项目，需要 `flutter create .`

```
运行老项目，报错如下
This application is not configured to build on the web.
To add web support to a project, run `flutter create .`.
```

## 如何刷新

- 浏览器按刷新按钮。【实践发现不生效】
- 控制台输入 r。

# 常用Flutter命令

```
帮助：
	flutter -h 或 flutter --help

检查Flutter版本
	flutter --version 
诊断flutter：
	flutter doctor
flutter升级：升级Flutter SDK 和 packages(`pubspec.yaml`配置的，默认是flutter SDK目录下，app目录下运行则是app的)
	flutter upgrade
查看flutter分支/channel：
	flutter channel
切换flutter分支：
	flutter channel master
查看配置：
	flutter config	
配置flutter：
	flutter config --enable-web 开启web支持
获取flutter packages包：
	flutter packages get
json序列化，自动监听命令（使用json_annotation、build_runner、json_serializable库的执行命令）：
	flutter packages pub run build_runner watch
设备列表：
	flutter devices
创建项目：
	flutter create myapp 	
运行：
	flutter run （默认为debug环境）
	flutter run --release (以release模式运行)
	flutter run -d chrome 指定运行设备为Chrome。如果只有一个设备，不需要指定
打包apk包：
	64位-release：
		flutter build apk --release --target-platform android-arm64
	32位-release：
		flutter build apk --release --target-platform android-arm
打包web发布：
	flutter build web	
```



