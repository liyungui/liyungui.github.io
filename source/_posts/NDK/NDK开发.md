---
title: NDK开发
date: 2019-10-24 11:08:53
tags: 
	- NDK
categories:
	- Android
---

# 背景

android的ndk开发一直被认为是很痛苦的一件事情，除了android程序员对c++的陌生外，还有一个主要原因是Android开发IDE对NDK开发支持度不如c++的IDE完善（代码提示补全，断点调试）。

# 开发环境

AS 2.2 开始支持NDK开发与断点调试

下载并安装 LLDB、Cmake、NDK三个工具

- 打开"SDK Manager"
- 右边选项卡选择"SDK Tools"
- 勾选 "CMake"、"LLDB"、"NDK"这3项，下载安装

# 创建项目

## 新建项目

AS 3.3之前，新建一个Android项目，勾选"Include C++ support”

AS 3.3及以上，新建项目时选择 "Native C++" 模板即可创建NDK项目

## 旧项目增加JNI

Android结构下，直接在项目右键，选择 New - Folder - JNI Folder ，对话框直接点击 Finish 即可方便地在默认位置(`app/src/main/jni`)创建 jni 文件夹

# javah生成jni头文件

## 手动

java文件路径：

`/Users/xuye/StudioProjects/ChatUI/app/src/main/java/com/im/MessageClient.java`

进入路径：

`cd /Users/xuye/StudioProjects/ChatUI/app/src/main/java/`

运行如下命令生成jni头文件

```
javac com/im/MessageClient.java
javah com.im.MessageClient
```

## External Tools

### 配置扩展工具

设置页面 - Tools - External Tools 打开外部工具配置页，点击 + 新建一个工具，命名为javah

配置，然后保存

```
Program: $JDKPath$\bin\javah
Arguments: -classpath . -jni -d $ModuleFileDir$\src\main\jni $FileClass$
Working directory: $ModuleFileDir$\src\main\Java
```

右击 java文件，在菜单中选择 External Tools - javah，快速生成头文件并放到 jni 目录

# 构建方式

AS 其实是支持 `ndk-build`（Android老构建方式） 和 `cmake`（官方推荐，通用跨平台编译方案） 两种构建方式的

## 产物不同

两种构建方式的产物路径不同

以release为例；release也带符号表和调试信息的

带符号表和调试信息的so又称为debug so

### `ndk-build`

`/项目/module/build/intermediates/ndkBuild/release/obj/local/armeabi-v7a`

`/项目/module/src/main/obj/local/armeabi-v7a`高版本as在这个目录

### cmake

`/项目/module/build/intermediates/cmake/release/obj/arm64-v7a` 

## 调试信息和符号表

gcc编译器带 `-g` 编译就会有调试信息，所以android编译(包括release)默认就是带符号表和调试信息的，strip后就不带符号表和调试信息了

elf文件的strip只是删除了symbol和debug的section，其他section段的内容没有变化。所以发布版本使用strip后的elf文件，调试时使用strip前有符号表的elf文件，不会出问题，因为他们的代码和数据部分相同。

`/项目/module/build/intermediates/stripped_native_libs/release/out/lib/arm64-v7a`

so是否含有符号表和调试信息，可以通过 ndk的`objdump` 或者 Linux `readelf` 查看

# `ndk-build`

 jni 目录下创建 Android.mk：
 
```
LOCAL_PATH := $(call my-dir)
include $(CLEAR_VARS)
LOCAL_LDLIBS += -llog
LOCAL_LDLIBS +=-lm
LOCAL_MODULE := JniLib
LOCAL_SRC_FILES =: JniLib.c
include $(BUILD_SHARED_LIBRARY)
```

jni 目录下创建 Application.mk：

```
APP_MODULES := JniLib
APP_ABI := all
```

module 的 build.gradle 里，amndroid.defaultConfig 下加入下面配置：

```
ndk{
    moduleName "JniLib"
    //abiFilters \"armeabi-v7a", "x86" //输出指定abi下的so库
}
sourceSets.main{
    jni.srcDirs = []
    jniLibs.srcDir "src/main/libs"
}
```

编译。为了方便添加一个外部工具，任意找个第地方右击，选择 External Tools - ndk-build 即可编译。成功后会创建 main/libs 目录，里面包含了不同平台下的 so。`ndk-build 位于ndk根目录`

# 隐藏内部符号表

win32通过 `.def` 文件或者 `__declspec(dllexport)` 来指定dll导出的函数名；android默认导出所有的符号表(函数名、全局变量名)

gcc新引进选项 `-fvisibility=hidden` 把所有的符号名（函数名和全局变量名）都强制标记成隐藏属性。

还可以通过调用 `strip -x` 隐藏局部符号名

`Android.mk`

```
cmd-strip = $(TOOLCHAIN_PREFIX)strip --strip-debug -x $1
LOCAL_CFLAGS := -DANDROID_NDK \
                -DDISABLE_IMPORTGL \
                -fvisibility=hidden
```

# 调试

两种调试方式

- debug模式运行
- 运行，attach进程，选 "auto"，即可支持NDK断点调试

**特别注意**：部分华为手机无法支持NDK断点调试，错误如下

`failed to set breakpoint site at 0x759cbac688 for breakpoint 2.1: error: 0 sending the breakpoint request`

# NDK和JNI

JNI：java native interface Java本地接口

JNI 是Java语言提供的Java和C/C++相互沟通的机制/接口

ABI: application binary interface 应用程序二进制接口

## NDK和JNI的区别

NDK：native develop kits 本地开发工具集

NDK是Google公司推出的帮助Android开发者通过C/C++语言编写应用的开发包，包含了C/C++的头文件、库文件、说明文档和示例代码

- JNI 是Java语言特性，和Android没有关系
- NDK 是Google推出的Android平台通过C/C++语言编写应用的开发包

## 为什么用JNI

- c更加高效。java不能直接操作底层硬件
- 复用优秀的c代码库。sqlite, webkit, opencore, 7zip, opencv, ffmepg
-  复用优秀的c代码
- 保护业务逻辑。java反编译很容易，c代码反编译比较困难

## java和C/C++交互

### JavaVM与JNIEnv对象

在标准Java平台，每个进程可以产生很多JavaVM对象，但在Android平台，每个进程只能产生一个DalvikVM对象，也就是说在一个Android进程中是通过有且只有一个DalvikVM对象来同时运行所有Java和C++代码的。

### 交互过程

- 在DalvikVM虚拟机中加载动态链接库
- 调用`JNI_Onload()`函数
- C层存储javaVM对象的指针存
- Android中每当一个Java线程第一次要调用本地C/C++代码时，Dalvik虚拟机实例会为该Java线程产生一个`JNIEnv *`指针。
	1. Java每条线程的JNIEnv是相互独立的，互不干扰
	2. C/C++使用DalvikVM对象的JavaVM `jvm->getEnv()`方法返回当前线程的 `JNIEnv*`
	3. JNIEnv 内部包含一个Pointer，Pointer指向Dalvik的JavaVM对象的Function Table

# 数据类型

## 基本类型

java的八种基本数据类型可以直接与jni基本数据类型映射：

{% asset_img 基本类型.png %}

## 引用类型

{% asset_img 引用类型.png %}

## c语言的输出函数
%d  -  int
%ld ¨ long int
%c  - char
%f -  float
%u ¨  无符号
%hd ¨ 短整型
%lf   double类型
%#x ¨ 十六进制显示数据
%o -  8进制显示数据
%s -  字符串

## c语言的输入函数

## 什么是指针
>指针就是一个内存地址
>在数据类型的后面加上一个*代表的是当前数据类型的指针变量。
>在一个指针变量的前面写*号 代表把这个地址的数据取出来。


## 指针和指针变量的概念
>指针是地址
>指针变量存放地址
>指针是地址，传递地址其实就是传递变量的引用



## 指针和数组的关系
>数组的名称，代表的是数组的首地址，其实我们可以把数组名，理解成指针变量。
>数组是连续的内存空间，数组名就是数组的首地址


## *号的含义
- \*号 乘法标示符  3\*5 = 15；
- \* 号放在一个数据类型的后面 
> int* int数据类型的指针变量
> double* double数据类型的指针变量
> float* float数据类型的指针变量
> int**  int*指针变量数据类型的指针变量

- \*号 放在一个指针变量的前面
> int* p;
> *p  把p变量里面存放的地址里面的数据取出来。


## 内存空间分为两种：
* 静态内存
>程序执行操作系统分配的内存。
>int i; int j; double d;
>在栈内存里面：连续的内存空间
>大小有限制 2M一下

* 动态内存
>一般程序员主动申请的内存。
>java --->new  
>c    ---> malloc
>在堆内存里面（heap) 不连续的内存空间。
>大小一般没有限制 在pcwindow系统上可以是全部的电脑内存。

# 参考&扩展

- [Android NDK隐藏jni动态库的内部符号表](https://blog.csdn.net/earbao/article/details/51453986)
- [Android Studio 3.5 JNI (ndk-build)](https://blog.csdn.net/weixin_43214827/article/details/103163776)