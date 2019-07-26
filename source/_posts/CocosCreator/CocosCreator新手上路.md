---
title: CocosCreator新手上路
date: 2019-07-24 18:30:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 关于 Cocos Creator

是一个完整的游戏开发解决方案

包括了

-  cocos2d-x 引擎的 JavaScript 实现（不需要学习一个新的引擎）
- 快速开发游戏所需要的各种图形界面工具

# 安装 Cocos Creator

## 下载

访问 [Cocos Creator 产品首页](https://www.cocos.com/creator/) 上的下载链接获得 Cocos Creator 的安装包

兼容已有旧项目，选择 [2.1.0版本](http://cocos2d-x.org/filedown/CocosCreator_v2.1.0_mac)

## 安装

### Mac安装

操作系统要求：最低版本是 OS X 10.9

双击 DMG 文件，然后将 `CocosCreator.app` 拖拽到 `应用程序` 文件夹快捷方式

# 安装配置原生开发环境

如果只想开发 Web 平台的游戏，完成上面的步骤就足够了。

如果希望发布游戏到原生平台，就需要安装配置原生开发环境。

Cocos Creator 使用基于 cocos2d-x 引擎的 JSB 技术实现跨平台发布原生应用。

在使用 Cocos Creator 打包发布到原生平台之前，我们需要先配置好 cocos2d-x 相关的开发环境

## Android 平台相关依赖

### JDK

### Android Studio

### SDK

### NDK

## C++ 编译环境

Cocos2d-x 自带的编译工具 Cocos Console 需要以下运行环境：

- Python 2.7.5+，[下载页](https://www.python.org/downloads/)，注意不要下载 Python 3.x 版本。

- Windows 下需要安装 Visual Studio 2015 或 2017 社区版，[下载页](https://www.visualstudio.com/downloads/download-visual-studio-vs)
- Mac 下需要安装 Xcode 和命令行工具，[下载页](https://developer.apple.com/xcode/download/)


## 配置原生发布环境路径

CocosCreator -> `设置`，打开设置窗口

我们在这里需要配置以下两个路径：

`NDK` 路径，选择 Android SDK Location 路径下的 ndk-bundle 文件夹（NDK 是其根目录），不需要编译 Android 平台的话这里可以跳过。

`Android SDK` 路径，选择刚才在 SDK Manager 中记下的 Android SDK Location 路径（Android SDK 的目录下应该包含 build-tools、platforms 等文件夹），不需要编译 Android 平台的话这里可以跳过。
配置完成后点击 保存 按钮，保存并关闭窗口。

注意：这里的配置会在编译 原生工程 的时候生效。如果没有生效（一些 Mac 机器有可能出现这个情况），可能需要您尝试到 系统环境变量 设置这些值：COCOS_CONSOLE_ROOT, NDK_ROOT, ANDROID_SDK_ROOT。

# Hello World

## 创建项目

在 `Dashboard` 中，打开 `新建项目` 选项卡，选中 `Hello World` 项目模板。

## 打开场景，开始工作

Cocos Creator 的工作流程是以数据驱动和场景为核心的，初次打开一个项目时，默认不会打开任何场景，要看到 Hello World 模板中的内容，我们需要先打开场景资源文件。

{% asset_img open_scene.png %}

在 `资源管理器` 中双击箭头所指的 `helloworld` 场景文件

## 预览场景

点击编辑器窗口正上方的 `预览游戏` 按钮。

{% asset_img preview_button.png %}

Cocos Creator 会使用您的默认浏览器运行当前游戏场景。点击预览窗口左上角的下拉菜单，可以选择不同设备屏幕的预览效果。

{% asset_img preview.png %}

## 修改欢迎文字

首先在 `层级管理器` 中选中 `Canvas` 节点，我们的 HelloWorld 组件脚本就挂在这个节点上。

接下来在 `属性检查器` 面板下方找到 `HelloWorld `组件属性，然后将 `Text` 属性里的文本改成 你好，世界！

{% asset_img change_text.png %}

再次运行预览，可以看到欢迎文字已经更新了

# 项目结构

```
ProjectName（项目文件夹）
	├──assets 
		├──Scene		├──Scene.meta		├──Script		├──Script.meta		├──Texture		├──Texture.meta
	├──build
	├──library
	├──local
	├──settings
	├──temp
	└──project.json
```

## assets 资源文件夹

游戏中所有本地资源、脚本和第三方库文件 

显示在 **资源管理器** 中

每个文件在导入后都会生成一个同名 `.meta` 文件，用于存储该文件作为资源导入后的信息和与其他资源的**关联**。

## library 资源库

`assets` 中的资源导入后**自动生成**的。将文件结构和资源格式处理成最终游戏发布时需要的形式。

不需要进入版本控制的

丢失或损坏的时候，删除整个 `library` 文件夹再打开项目，就会重新生成资源库

## local 本地设置

该项目的本地设置：包括编辑器面板布局，窗口大小，位置等信息。

按照您的习惯设置编辑器布局，这些就会自动保存在这个文件夹

不需要进入版本控制

## settings 项目设置

项目相关的设置：`构建发布` 菜单里的包名、场景和平台选择等。

需要进行版本控制

## project.json

`project.json` 文件和 `assets` 文件夹一起，作为验证 Cocos Creator 项目合法性的标志。只有包括了这两个内容的文件夹才能作为 Cocos Creator 项目打开。

目前只用来规定当前使用的引擎类型和插件存储位置，不需要用户关心其内容。

需要进行版本控制

## build 构建目标

在使用主菜单中的 `项目` -> `构建发布...` 使用**默认发布路径**发布项目后，编辑器会在项目路径下创建 build 目录，并存放所有目标平台的构建工程。

不进入版本控制

- 每次构建项目后资源 id 可能会变化
- 体积很大

# 打包发布原生平台

点击菜单栏的 `项目` -> `构建发布`，打开构建发布面板。

## 构建原生工程

选择发布平台，设置初始场景，点击右下角的 `构建` 按钮，开始构建流程。

{% asset_img build.png %}

进度条到达 100% 后请继续等待 **控制台** 面板(在主面板底部)中的工程构建结束

编译成功

控制台面板日志：

```
Building /Users/liyungui/StudioProjects/cocos_helloworld
Destination /Users/liyungui/StudioProjects/cocos_helloworld/build/jsb-link
Delete /Users/liyungui/StudioProjects/cocos_helloworld/build/jsb-link/res/**/*,/Users/liyungui/StudioProjects/cocos_helloworld/build/jsb-link/src/*/
Checked Python Version [2.7.10]
Creating native cocos project to /Users/liyungui/StudioProjects/cocos_helloworld/build/jsb-link
Start building assets
Finish building assets
Start building plugin scripts
Checked Python Version [2.7.10]
Built to "/Users/liyungui/StudioProjects/cocos_helloworld/build/jsb-link" successfully
```

构建结束后，我们得到的是一个标准的 cocos2d-x 工程

接下来我们可以选择通过 Cocos Creator 编辑器的进程进行编译，以及运行桌面预览，或手动在相应平台的 IDE 中打开构建好的原生工程，进行进一步的预览、调试和发布。

## 编译原生工程

### 通过编辑器编译

点击下方的 `编译` 按钮，进入编译流程，如果模板选择了 default 的源码版引擎，这个编译的过程将会花费比较久的时间。

编译成功

控制台面板日志：

```
Checked Python Version [2.7.10]
Start to compile native project. Please wait...
The log file path [ /Users/liyungui/.CocosCreator/logs/native.log ]
Compile native project successfully.
```

注意：首次编译 Android 平台，建议通过 Android Studio 打开工程，根据提示下载缺失的工具，再进行编译运行。

## 运行预览原生工程

### 通过编辑器运行预览

点击右下角的 `运行` 按钮，通过默认方式预览原生平台的游戏。

点击运行后，视平台不同可能还会继续进行一部分编译工作，请耐心等待或通过日志文件查看进展。

其中 Mac/Windows 平台直接在桌面运行预览，iOS 平台会调用模拟器运行预览，Android 平台必须通过 USB 连接真机，并且在真机上开启 USB 调试后才可以运行预览。

运行成功后，logcat日志 过滤 tag: jswrapper

```
2019-07-24 19:02:18.986 6156-6195/? D/jswrapper: Initializing V8, version: 6.0.286.52
2019-07-24 19:02:20.081 6156-6195/? D/jswrapper: JS: Enable batch GL commands optimization!
2019-07-24 19:02:20.960 6156-6195/? D/jswrapper: glGetIntegerv: pname: 0x8b4c
2019-07-24 19:02:21.004 6156-6195/? D/jswrapper: JS: Cocos Creator v2.1.0
2019-07-24 19:02:21.078 6156-6195/? D/jswrapper: JS: LoadScene 2dL3kvpAxJu6GJ7RdqJG5J: 70.58299999999986ms
2019-07-24 19:02:21.082 6156-6195/? D/jswrapper: JS: Success to load scene: db://assets/Scene/helloworld.fire
```
## 使用原生工程

点击发布路径旁边的 `打开 `按钮，就会在操作系统的文件管理器中打开构建发布路径。

{% asset_img open_project.png %}

这个路径中的 `jsb-default` 或 `jsb-link` （根据选择模板不同）里就包含了所有原生构建工程。

{% asset_img native_projects.jpg %}

接下来您只要使用原生平台对应的 IDE （如 Xcode、Android Studio、Visual Studio）打开这些工程，就可以进行进一步的编译、预览、发布操作了。

注意：在 MIUI 10 系统上运行 debug 模式构建的工程可能会弹出 “Detected problems with API compatibility” 的提示框，这是 MIUI 10 系统自身引入的问题，使用 release 模式构建即可。