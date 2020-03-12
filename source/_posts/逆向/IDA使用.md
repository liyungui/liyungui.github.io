---
title: IDA使用
date: 2019-11-23 16:40:53
categories:
  - 逆向
tags:
	- 逆向
---

# 32位和64位

根据逆向的目标文件选择对应版本。

比如：32位的so对应使用32位ida打开；64位的so使用64位的ida打开

# 主要窗口

通过 `View-Open subviews-窗口名字(Disassembly等)` 打开窗口

各窗口支持搜索 `ctr + f`

## IDA View

汇编代码窗口

按 空格键 切换代码视图和流程图视图

## Functions window

函数窗口

## Functions calls

当前函数调用的函数

## Strings

字符串

## Imports

导入函数

## Exports

导出函数

## Hex View

十六进制编辑器窗口

## Structures

## Enumes

## Segmentation


# 汇编指令转C

在 汇编代码 窗口 ，选中 需要转换的函数名，按 F5 即可

## F5无效

无效可能有两个原因：

- 使用的是 ida 版本错误；32位的so对应使用32位ida打开；64位的so使用64位的ida打开
- 没有 [HexRaysCodeXplorer](https://github.com/REhints/HexRaysCodeXplorer) 插件。

## 无法还原JNI函数名

### 手动修改

`(*(_DWORD *)v5 + 676))(v5, a5, &v11);`

一般JNI函数方法名首先是一个指针加上一个数字，比如v5+676。然后将这个地址作为一个方法指针进行方法调用，并且第一个参数就是指针自己。这实际上就是我们在JNI里经常用到的JNIEnv方法。Ida并不会自动的对这些方法进行识别。解决方法非常简单，只需要对JNIEnv指针做一个类型转换即可。

我们可以选中v5变量，然后按一下y键，然后输入： JNIEnv*

类似的地址有：672，676，680，684，688

### 手动导入`jni.h`

1. 点击 IDAPro 菜单项“File->Load file->Parse c header file ” 选择jni.h（`ndk/platforms/andoid-21/arch-arm/usr/include/jni.h`）
2. 简单修改jni.h ,注释第27行的 `#include<stdarg.h>` ,将1122行的`#define JNIEXPORT_attribute_((visibility("default")))` 改成 `#define JNIEXPORT`（文件保存在 IDA tools 目录），修改完后可以成功导入    
3. 导入成功后把jni.h修改的地方  改回来 防止编译NDK出错。
4. 点击IDAPro 主界面上的“Structures”选项卡 然后按下Insert键打开“Create structure/union”对话框，点击界面上的"Add standard structure"按钮，在打开的结构体选择对话框中选择JNINativeInterface并点击OK返回，同理JNIInvokeInterface结构体也导入进来；（如果有报错，逐个按照错误信息修改）
5. 鼠标点击参数(v5)，然后右键选中 Convert to Struct * ，选择 `_JNIEnv`

### 脚本导入`jni.h`

script file 导入 飞虫提供的 `jni.idc` 脚本（书籍源码包里面有）来完成 `jni.h` 的导入

然后执行上面的步骤4和5





