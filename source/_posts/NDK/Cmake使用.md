---
title: Cmake使用
date: 2020-11-25 21:23:53
tags: 
	- NDK
categories:
	- Android
---

# 概述

cmake命令不区分大小写，但是变量区分大小写

## 变量

`set(Hello "hello")` 定义一个字符串

## 字符串

CMake中基础的数据形式是字符串。

原义字符串用双引号括起来。字符串可以是多行字符串

```
set(MY_STRING "this is a string with a

 newline in

it")
```

也可以在一个字符串中转义字符和使用变量

`message("\n\thello world")` 输出`hello world`

`message("\${VAR}= ${VAR}")` 输出 `${VAR}= hello`

## 字符串列表

也支持字符串列表

```
# 将 变量 Foo 设为 a b c
set(Foo a b c)
# set(Foo a b c) 等价

# Foo变量 传递给command方法
command(${Foo})
# command(a b c) 等价

command("${Foo}")
# command("a b c") 等价
```

## 控制流

条件

`if(var) some_command(...) endif(var)`

循环

`foreach(f ${VAR}) message(${f}) endforeach(f)`

`while(var) some_command(...)`

定义宏

`macro(hello MESSAGE) message(${MESSAGE}) endmacro(hello)`

`hello("hello world")` 使用宏

定义函数

`function(hello MESSAGE) message(${MESSAGE}) endfunction(hello)`

# 常用命令

## set

```
# Set Normal Variable
set(<variable> <value>... [PARENT_SCOPE])

# Set Environment Variable
# 这个环境变量只对当前cmake工程有效，对外界是无效的。
set(ENV{<variable>} [<value>])
```

## message

`message([<mode>] "message to display" ...)`

### mode

- **FATAL_ERROR** stop processing and generation
- **SEND_ERROR** continue processing, but skip generation
- **WARNING**
- **NOTICE**
- **STATUS**
- **VERBOSE**
- **DEBUG**

## `add_library`

将指定的源文件（CPP文件）生成目标文件，然后添加到工程中去。

```
add_library(<name> [STATIC | SHARED | MODULE]
	[EXCLUDE_FROM_ALL]
	[source1] [source2 ...])
            
<name>表示生成的库文件的名字。

STATIC、SHARED和MODULE的作用是指定生成的库文件的类型。
	STATIC库是归档文件(.a)，在链接其它目标的时候使用。默认
	SHARED库是动态链接库(.so)，在运行时会被加载。
	MODULE库是一种不会被链接到其它目标中的插件，但是可能会在运行时使用dlopen-系列的函数。    
```

### `set_target_properties`

设置属性

实例：导入三方so库

```
add_library(ijkffmpeg SHARED IMPORTED)
# 设置 ijkffmpeg 导入路径
set_target_properties(ijkffmpeg PROPERTIES IMPORTED_LOCATION
        ${CMAKE_CURRENT_SOURCE_DIR}/../../jniLibs/${ANDROID_ABI}/libijkffmpeg.so)
```


## `add_executable`

将指定的源文件（CPP文件）生成目标文件，然后添加到工程中去。

```
add_executable(<name> [WIN32] [MACOSX_BUNDLE]
	[EXCLUDE_FROM_ALL]
	source1 [source2 ...])
```

## `add_subdirectory`

`add_library` 或 `add_executable`之后

需要 `add_subdirectory` 使用之前add进来的文件

## `include_directories`

添加头文件目录

相当于g++选项中的`-I`参数的作用，也相当于环境变量中增加路径到`CPLUS_INCLUDE_PATH`变量的作用。

`include_directories([AFTER|BEFORE] [SYSTEM] dir1 [dir2 ...])`

## `link_directories`

添加需要链接的库文件目录

相当于g++命令的`-L`选项的作用，也相当于环境变量中增加`LD_LIBRARY_PATH`变量的作用

`link_directories(directory1 directory2 ...)`

## `find_library` 

查找库所在目录

`find_library (<VAR> name1 [path1 path2 ...])`

如果所有目录中都没有找到，变量VAR就会被赋为NO_DEFAULT_PATH

## `link_libraries` 

添加需要链接的库文件路径

`link_libraries(library1 <debug | optimized> library2 ...)`

```
# 直接是全路径
link_libraries(“/home/server/third/lib/libcommon.a”)
# 下面的例子，只有库名，cmake会自动去所包含的目录搜索
link_libraries(iconv)
```

## `target_link_libraries` 

设置要链接的库文件的名称

```
target_link_libraries(<target> [item1 [item2 [...]]]
	[[debug|optimized|general] <item>] ...)

# 以下写法都可以：
target_link_libraries(myProject comm)       # 链接libhello.so库，默认优先链接动态库
target_link_libraries(myProject libcomm.a)  # 显式指定链接静态库
target_link_libraries(myProject libcomm.so) # 显式指定链接动态库
```

## `configure_file`

复制文件

```
configure_file(<input> <output>
	[COPYONLY] [ESCAPE_QUOTES] [@ONLY]
	[NEWLINE_STYLE [UNIX|DOS|WIN32|LF|CRLF] ])
	
<input> 源文件
<output> 目标文件
COPYONLY 仅拷贝
ESCAPE_QUOTES 使用反斜杠（C语言风格）来进行转义；
@ONLY 限制替换， 仅仅替换 @VAR@ 变量， 不替换 ${VAR} 变量
NEWLINE_STYLE 指定输入文件的新行格式， 例如：Unix 中使用的是 \n, windows 中使用的 \r\n
```

## file

文件操作

`file(MAKE_DIRECTORY ${lib_build_DIR})` 创建目录

## include

载入并运行来自于文件或模块的CMake代码

实例场景：多C++标准版本指定。

在使用同一个外层 CMakeLists.txt 的前提下，每个源码子目录中要求使用的C++标准版本不同（有的要求使用c++98、有的要求使用c++11）




# 实例

编译ijkplay

## 源码

```
|- cpp
	|- android-ndk-profiler-dummy 自定义，用来dump ndk错误信息
	|- ffmpeg a
	|- ijkj4a
	|- ijkmedia a
	|- ijkplayer
	|- ijksdl
	|- ijksoundtouch
	|- ijkyuv
	|- CMakeLists.txt
```

## cmake

`cpp/CMakeLists.txt`内容如下：

```
# 设置CMake最低版本；必备
cmake_minimum_required(VERSION 3.4.1)

# 设置项目名称
project(ijkplayer)

# 显示执行构建过程中详细的信息
set(CMAKE_VERBOSE_MAKEFILE on)

# C和C++ 的编译参数
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99")
set(CMAKE_CXX_FLAGS "-Wno-error=format-security -Wno-error=pointer-sign")

# 设置静态库和动态库的输出路径
# PROJECT_SOURCE_DIR 是当前cmake文件目录
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../../../ss/${ANDROID_ABI})
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/../../../ss/${ANDROID_ABI})

# 设置变量
set(lib_src_DIR ${CMAKE_CURRENT_SOURCE_DIR})

# 设置变量，并创建对应文件夹
set(lib_build_DIR $ENV{HOME}/tmp)
file(MAKE_DIRECTORY ${lib_build_DIR})

#引入头文件
include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}/android-ndk-profiler/
)


add_library(
	android-ndk-profiler
	STATIC
	${CMAKE_CURRENT_SOURCE_DIR}/android-ndk-profiler-dummy/prof.c
)

# 导入CPU检测支持库
include(AndroidNdkModules)
android_ndk_import_module_cpufeatures()

add_subdirectory(ijkyuv)
add_subdirectory(ijksoundtouch)
add_subdirectory(ijkj4a)
add_subdirectory(ijksdl)
add_subdirectory(ijkplayer)
```

`ijkj4a等5个的CMakeLists.txt`类似，内容如下：

```
# 将指定的源文件（CPP文件）生成目标文件，然后添加到工程中去。
add_library(
	ijkj4a
	STATIC
	${ijkj4a_sources}
)

# 添加头文件目录
include_directories(
	${CMAKE_CURRENT_SOURCE_DIR}
)
```

# 参考&扩展

- [HelloWorld CMake](https://www.cnblogs.com/zhoug2020/p/5904206.html) CMake中构建静态库与动态库及其使用
- [cmake使用方法（详细）](https://zhuanlan.zhihu.com/p/93895403)