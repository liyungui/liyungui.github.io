---
title: CocosCreator的JSB绑定
date: 2019-10-24 18:00:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 背景

尽管Cocos官方提供了接口实现 JS 层和 Native 层 交互

## callStaticMethod

 `jsb.reflection.callStaticMethod` 从JS端直接调用Native端（Android，iOS/Mac），但是经过大量实践发现此接口在大量频繁调用情况下性能很低下

实例：调用Native实现log打印

```js
if (cc.sys.isNative && cc.sys.os == cc.sys.OS_IOS) {
    msg = this.buffer_string + '\n[cclog][' + clock + '][' + tag + ']' + msg;
    jsb.reflection.callStaticMethod("ABCLogServuce", "log:module:level:", msg, 'cclog', level);
    return;
} else if (cc.sys.isNative && cc.sys.os == cc.sys.OS_ANDROID) {
    msg = this.buffer_string + '\n[cclog][' + clock + '][' + tag + ']' + msg;
    jsb.reflection.callStaticMethod("com/example/test/CommonUtils", "log", "(ILjava/lang/String;Ljava/lang/String;)V", level, 'cclog', msg);
    return;
}
```

在C++层Android端是通过jni的方式实现的，IOS端是通过运行时的方式动态调用

但是为了兼顾通用性和支持所有的方法，Android端没有对jni相关对象做缓存机制，就会导致短时间大量调用时出现很严重的性能问题，甚至 `local reference table overflow` 的 crash

修复此问题就需要针对log调用进行JSB的改造，同时还要加上jni的相关缓存机制，优化性能。

## evalString

`Cocos2dxJavascriptJavaBridge.evalString` 执行 JS 代码

Android开发实际场景中，我们会发现为了保证 JS 代码能够被正确执行，在拼接字符串时针对引号的控制格外重要，必须明确 '与 " 的使用，稍有不慎就会出现 evalString 失败的情况。在 Cocos 的官方论坛上，也有这个问题的大量反馈，的确是一个十分容易踩坑的地方

实例：

```java
Cocos2dxJavascriptJavaBridge.evalString("window.sample.testEval('" + param + "',JSON.stringify(" + jsonObj + "))");
```

因此，我们决定绕过 `evalString` ，直接基于 JSB 绑定的方式进行通信。

## 总结

Cocos官方提供的两个JS 层和 Native 层 交互接口，存在以下问题

- 执行效率问题
- 代码不够精简
- 大量字符串拼接，难以规范约束，维护成本高

所以需要 基于 JSB 绑定的方式进行通信

# 前置

## 抽象层架构

{% asset_img CocosCreator架构.png %}

从架构可知，JavaScript – C++绑定层的设计支持的JS引擎包括：

- Mozilla的Spider Monkey
- iOS的JavaScriptCore
- Google的v8
- 微软的ChakraCore

Cocos 团队设计之初 就将ScriptEngine定义为一个独立模块，完全不依赖 Cocos 引擎。完全可以把 `cocos/scripting/js-bindings/jswrapper` 下的所有抽象层源码移植到其他项目中直接使用。

## 宏

抽象层必然会比直接使用 JS引擎 的API 性能开销更大，而且不同多JS 引擎的关键方法的定义各不相同，如何做到抽象层开销最小而且暴露统一的 API 供上层使用，成为设计的第一目标。

JS 绑定的大部分工作其实就是设定 JS 相关操作的 CPP 回调，在回调函数中关联 CPP 对象。其实主要包含如下两种类型：

- 注册 JS 函数（包含全局函数，类构造函数、类析构函数、类成员函数，类静态成员函数），绑定一个 CPP 回调
- 注册 JS 对象的属性读写访问器，分别绑定读与写的 CPP 回调

Cocos 团队使用 **宏** 来抹平不同 JS 引擎回调函数定义与参数类型的差异，不管底层是使用什么引擎，开发者统一使用一种函数的定义。我们借鉴了 lua 的回调函数定义方式，抽象层所有的 JS 到 CPP 的回调函数的定义为：

```cpp
bool foo(se::State& s)
{
    ...
}
SE_BIND_FUNC(foo) // 此处以回调函数的定义为例
```

开发者编写完回调函数后，记住使用 `SE_BIND_XXX` 系列的宏对回调函数进行包装。目前提供了如下几个宏：

- `SE_BIND_PROP_GET`：包装一个 JS 对象属性读取的回调函数
- `SE_BIND_PROP_SET`：包装一个 JS 对象属性写入的回调函数
- `SE_BIND_FUNC`：包装一个 JS 函数，可用于全局函数、类成员函数、类静态函数
- `SE_DECLARE_FUNC`：声明一个 JS 函数，一般在 .h 头文件中使用
- `SE_BIND_CTOR`：包装一个 JS 构造函数
- `SE_BIND_SUB_CLS_CTOR`：包装一个 JS 子类的构造函数，此子类使用 cc.Class.extend 继承 Native 绑定类
- `SE_FINALIZE_FUNC`：包装一个 JS 对象被 GC 回收后的回调函数
- `SE_DECLARE_FINALIZE_FUNC`：声明一个 JS 对象被 GC 回收后的回调函数
- `_SE`：包装回调函数的名称，转义为每个 JS 引擎能够识别的回调函数的定义，注意，第一个字符为下划线，类似 Windows 下用的_T("xxx")来包装 Unicode 或者 MultiBytes 字符串

## SE 类型
## se::ScriptEngine 与 ScriptingCore 的区别

在1.7版本中，抽象层被设计为一个与引擎没有关系的独立模块，对 JS 引擎的管理从 `ScriptingCore` 被移动到了 `se::ScriptEngine` 类中，ScriptingCore 被保留下来是希望通过它把引擎的一些事件传递给封装层，充当适配器的角色。

`ScriptingCore` 只需要在 AppDelegate 中被使用一次即可，之后的所有操作都只需要用到 se::ScriptEngine。

```cpp
bool AppDelegate::applicationDidFinishLaunching()
{
    ...
    ...
    director->setAnimationInterval(1.0 / 60);

    // 这两行把 ScriptingCore 这个适配器设置给引擎，用于传递引擎的一些事件，
    // 比如 Node 的 onEnter, onExit, Action 的 update，JS 对象的持有与解除持有
    ScriptingCore* sc = ScriptingCore::getInstance();
    ScriptEngineManager::getInstance()->setScriptEngine(sc);

    se::ScriptEngine* se = se::ScriptEngine::getInstance();
    ...
    ...
}
```





# JSB 绑定

本质：C++ 和脚本层之间对象的转换，并转发脚本层函数调用到 C++ 层的过程

JSB绑定通常有两种方式：手动绑定和自动绑定

# 手动绑定

优点是灵活，可定制型强

缺点就是全部代码要自己书写，尤其是在js类型跟c++类型转换上，稍有不慎容易导致内存泄漏，某些指针或者对象没有释放。

虽然 Cocos 很人性化提供了自动绑定的配置文件，可以通过一些配置直接生成目标文件，减少了很多工作量。

但是亲手来完成一次手动绑定的流程会帮助更为全面地了解整个绑定的实现流程，有助于加深理解。另一方面，当存在特殊需要自动绑定无法满足时，手动绑定也往往会更为灵活

## 流程

- 确定方法接口与 JS/Native 公共字段
- 声明头文件，并分别实现 Android JNI 与 OC 具体业务代码
- 编写抽象层代码，将必要的类与对应方法注册到 JS 虚拟机中
- 将绑定的类挂载在 JS 中的指定对象（类似命名空间）中

## 实例

下载器 `FileDownloader`

- `download(url, path, callback)`
- `callback` 中是 `code，msg`
- `getInstance()`
- `destroyInstance()`
- `FileDownloader* s_sharedFileDownloader`
- `std::unordered_map<std::string, ResultCallback> reqCtx;`
	- map类型，存储回调对应关系 

为了方便使用，我们将它挂载在 `jsb` 对象下

这样我们便可以使用如下代码进行简单地调用:

```js
jsb.fileDownloader.download(url, path, (msg, code) => {
    // do whatever you want
});
```

### 定义接口

```cpp
class FileDownloader {
        public:
            typedef std::function<void(const std::string& msg, const int code)> ResultCallback;
            static FileDownloader* getInstance();
            static void destroyInstance();
            void download(const std::string& url,
                                         const std::string& savePath,
                                         const ResultCallback& callback);
            void onDownloadResult(const std::string msg, const int code);
            ... ...
        protected:
            static FileDownloader* s_sharedFileDownloader;
            std::unordered_map<std::string, ResultCallback> reqCtx;
};
```

### 绑定

下载器就功能上分类属于 network 模块，我们可以选择将我们的 FileDownloader 的绑定实现在 Cocos 源码中现有的 `jsb_cocos2dx_network_auto` 中。

在 `jsb_cocos2dx_network_auto.hpp` 中声明 JS调用 函数：

```cpp
SE_DECLARE_FUNC(js_cocos2dx_network_FileDownloader_download); // 声明成员函数，download，下载调用
SE_DECLARE_FUNC(js_cocos2dx_network_FileDownloader_getInstance); // 声明静态函数，getInstance，获取单例
```

在 `jsb_cocos2dx_network_auto.cpp` 中注册 上面声明的两个函数到 JS 虚拟机中。实现留空，等注册逻辑完成后再来补全

```cpp
static bool js_cocos2dx_network_FileDownloader_download(se::State &s) { // 方法名与声明时一致
    // TODO
}

SE_BIND_FUNC(js_cocos2dx_network_FileDownloader_download); // 包装该方法

static bool js_cocos2dx_network_FileDownloader_getInstance(se::State& s) { // 方法名与声明时一致
    // TODO
}

SE_BIND_FUNC(js_cocos2dx_network_FileDownloader_getInstance); // 包装该方法
```

### 注册

新增一个注册方法实现 FileDownloader 的全部注册逻辑

```cpp
bool js_register_cocos2dx_network_FileDownloader(se::Object* obj) {
    auto cls = se::Class::create("FileDownloader", obj, nullptr, nullptr);
    cls->defineFunction("download", _SE(js_cocos2dx_network_FileDownloader_download));
    cls->defineStaticFunction("getInstance", _SE(js_cocos2dx_network_FileDownloader_getInstance));
    cls->install();
    JSBClassType::registerClass<cocos2d::network::FileDownloader>(cls);
    se::ScriptEngine::getInstance()->clearException();
    return true;
}
```

1. 创建一个名为 `FileDownloader` 的 Class
	- 调用 `se::Class::create(className, obj, parentProto, ctor) `方法来创建
	- 注册成功后，在 JS 层中可以通过 `let xxx = new FileDownloader();`的方式创建实例。
2. 为Class定义了一个成员函数 `download`，并绑定其实现
	- 调用 `defineFunction(name, func)` 方法
		- 定义了一个成员函数 download
		- 并将其实现绑定到包装后的 `js_cocos2dx_network_FileDownloader_download` 上。
3. 为Class定义了一个静态成员函数 `getInstance`，并绑定其实现
	- 调用 `defineStaticFunction(name, func)` 方法
		- 定义了一个静态成员函数 getInstance
		- 并将其实现绑定到包装后的 `js_cocos2dx_network_FileDownloader_getInstance` 上。
4. 将Class注册到 JS 虚拟机中
	- 调用 `install()` 方法，
5. 注册Class 与 C++ 层的类对应关系
	- 调用 `JSBClassType::registerClass` 方法
		- 内部通过 `std::unordered_map<std::string, se::Class*>`实现

在 network 模块的注册入口调用 定义的Downloader注册逻辑`js_register_cocos2dx_network_FileDownloader`

```cpp
bool register_all_cocos2dx_network(se::Object* obj)
{
    // Get the ns
    se::Value nsVal;
    if (!obj->getProperty("jsb", &nsVal))
    {
        se::HandleObject jsobj(se::Object::createPlainObject());
        nsVal.setObject(jsobj);
        obj->setProperty("jsb", nsVal);
    }
    se::Object* ns = nsVal.toObject();

    ... ...
    // 将前面生成的 Class 注册 设置为 jsb对象 的一个属性，这样我们便能通过
    // let downloader = new jsb.FileDownloader();
    // 获取实例
    js_register_cocos2dx_network_FileDownloader(ns);
    return true;
}
```

到此，Class 已经成功绑定

# 自动绑定

python脚本一键生成相关的文件(`.cpp .h .js`)

## 环境配置

- python
	- PyYAML
	- Cheetah
- NDK

## 演示

演示的是cocos引擎下面 `⁨build/⁨jsb-default⁩/frameworks⁩/cocos2d-x/cocos⁩/scripting⁩/js-bindings/⁨auto`⁩目录下的文件是怎么自动生成的

- 打开终端
- cd到 `build/jsb-default/frameworks/cocos2d-x/tools/tojs`目录
- 运行./genbindings.py
- 大概运行一分钟左右后，会提示生成成功

如果出现 `stdint.h` 文件找不到，是因为配置的NDK版本太高导致，NDK14b就ok


# 参考&扩展

- [腾讯用 Cocos Creator 改造教育 app，尽显高性能跨平台优势](https://zhuanlan.zhihu.com/p/39006183) ABCmouse；架构分析；自定义底层功能、增加通用UI、音频播放、视频播放；踩坑；性能优化；收益分析；
- [Cocos Creater 中如何实现JSB的自动绑定](https://oedx.github.io/2019/07/03/cocos-creator-js-binding-auto/) --> [源md文件仓库](https://github.com/OEDx/OEDx)  --> 公众号：腾讯在线教育技术 --> ABCmouse
- [拒绝 evalString 进行回调，使用 JSB 进行手动绑定（流程篇）](https://oedx.github.io/2019/05/29/cocos-creator-js-binding-manual/)