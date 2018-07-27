---
title: RN工程结构
date: 2018-07-26 15:35:14
tags:
	- RN
---

- android/: 
	- Android 原生代码目录，主要用于原生库、原生View的编写桥接、以及 ReactNative 第三方库的 link。
- ios/: 
	- iOS 原生代码目录，主要用于原生库、原生View的编写桥接、以及 ReactNative 第三方库的 link。
- index.js: 
	- RN项目的**入口**文件。
- package.json: 
	- npm 的包管理文件
	- 功能类似 Android 的 gradle，iOS 的 cocoaPods。
	- 说明了RN项目的名称，版本号，依赖等
	- NodeJS相关的目录
- node_modules/: 
	- npm install 命令node解析package.json **下载生成**的相关依赖
	- NodeJS相关的目录

如果搭建了 typescript 开发环境：

- tsconfig.json: 
	- typescript 环境配置文件。
- src/: 
	- typescript 搭建环境时新建目录，用于存放编写的 ts 代码。
- lib/: 
	- 执行 tsc 脚本后，根据已有 ts 代码，编译成的 js 代码目录，也是代码运行时的目录，即运行时代码都指向 lib 文件夹。
