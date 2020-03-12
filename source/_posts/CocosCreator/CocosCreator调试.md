---
title: CocosCreator调试
date: 2019-11-21 14:00:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 背景

游戏发布后，由于运行环境不同，可能出现在浏览器浏览时无法重现的bug，特别是原生平台，这时我们就必须直接在相应平台下进行调试。

CocosCreator 从1.7版本开始引入JSB 2.0，可以很方便的对原生平台中的JavaScript进行远程调试

# 远程调试

默认远程调试和 Profile 是在 debug 模式中生效的，如果需要在 release 模式下也启用，需要手动修改 `cocos/scripting/js-bindings/jswrapper/config.hpp` 中的宏开关。

```
#if defined(COCOS2D_DEBUG) && COCOS2D_DEBUG > 0 // 这里改为 1，强制启用调试
#define SE_ENABLE_INSPECTOR 1
#define SE_DEBUG 2
#else
#define SE_ENABLE_INSPECTOR 0
#define SE_DEBUG 0
#endif
```

# 模拟器调试和真机调试

## 模拟器调试

一般来说，原生平台的大部分问题都能在模拟器中重现，可以先在模拟器中测试，复现问题的话直接在模拟器中调试即可。

### 选择模拟器预览运行游戏

{% asset_img 模拟器.png %}

在编辑器工具栏上方，选择`模拟器`作为预览平台（默认是浏览器），然后点击编辑器的`运行预览`在模拟器中运行游戏

## 真机调试

构建 -- 编译 相应平台的工程项目（编译可以选择Cocos Creator或者相应平台IDE），安装运行

# Chrome 远程调试 V8

## 模拟器

选择模拟器预览运行游戏

用 Chrome 浏览器打开 [chrome-devtools://devtools/bundled/inspector.html?v8only=true&ws=127.0.0.1:5086/00010002-0003-4004-8005-000600070008](chrome-devtools://devtools/bundled/inspector.html?v8only=true&ws=127.0.0.1:5086/00010002-0003-4004-8005-000600070008)

## 安卓真机

编译，运行游戏

保证 Android 设备与 PC 或者 Mac 在同一个局域网中

用 Chrome 浏览器打开 [chrome-devtools://devtools/bundled/inspector.html?v8only=true&ws=xxx.xxx.xxx.xxx: 6086/00010002-0003-4004-8005-000600070008](chrome-devtools://devtools/bundled/inspector.html?v8only=true&ws=xxx.xxx.xxx.xxx: 6086/00010002-0003-4004-8005-000600070008), 其中 xxx.xxx.xxx.xxx 为局域网中 Android 设备的 IP 地址。（从 v2.0.7 开始，端口由5086 改为 6086）

# 调试技巧

## 启动即等待调试器连接

有时候我们需要调试游戏的初始化逻辑，是需要游戏启动后等待调试器连接，然后继续执行

只需要在打开调试开关时 `jsb_enable_debugger` 第三个参数 `isWaitForConnect` 设置为true

```cpp
//AppDelegate.cpp
bool AppDelegate::applicationDidFinishLaunching()
{
    // Enable debugger here
    jsb_enable_debugger("0.0.0.0", 6086, true);
    
bool jsb_enable_debugger(const std::string& debuggerServerAddr, uint32_t port, bool isWaitForConnect)    
```

## 快速修改调试js

正常的IDE调试流程：修改js逻辑，构建，拷贝构建生成的资源到工程项目，编译，运行，调试。

即使只是修改一行代码，上面的流程下来也要两分钟，严重降低生产效率

其实我们可以直接修改构建后的js文件。即直接修改生成的工程项目 `assets\src`  目录下的相关js文件，然后运行项目即可调试，非常的方便。

这个方法仅限未加密js的情况下（一般只有构建release的时候我们才会选择加密js选项）

# 参考&扩展

- [Chrome 远程调试 V8](https://docs.cocos2d-x.org/creator/manual/zh/advanced-topics/jsb/JSB2.0-learning.html#chrome-%E8%BF%9C%E7%A8%8B%E8%B0%83%E8%AF%95-v8)
- [远程调试与 Profile](https://docs.cocos2d-x.org/creator/manual/zh/advanced-topics/jsb/JSB2.0-learning.html#%E8%BF%9C%E7%A8%8B%E8%B0%83%E8%AF%95%E4%B8%8E-profile)
