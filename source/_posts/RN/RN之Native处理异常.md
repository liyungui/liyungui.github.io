---
title: RN之Native处理异常
date: 2019-03-29 17:41:12
tags: 
	- RN
---

研究RN框架异常的动机在于，我们需要建立起一套针对性的容错机制，毕竟它还是一个不够成熟的框架。期望能够做到的效果就是，对于每一个RN页面的启动，我们能够在**进入页面至退出页面**期间侦测所有发生的**RN相关**的崩溃，然后根据崩溃来考虑该页面是否该有降级策略、判断框架是否真的能够支持稳定迭代。

并且，集中地处理崩溃，也有利于我们后续对框架稳定性进行针对性的统计与优化。即使最后还是最简单粗暴的try-catch，这个catch的位置也是一门艺术。

**异常种类**

- 产生位置
	- JS
	- Java 
	- C++
- 产生时期
	- 启动期
	- 运行期

# 启动期异常

## 框架启动流程

ReactActivity.onCreate 调用 ReactActivityDelegate.loadApp 开始核心启动流程

- **预初始化**：
	- 初始化ReactRootView与ReactInstanceManager实例
- **创建React上下文**：由ReactRootView.startReactApplication一路走下来，会用懒加载方式创建React上下文，通过进入ReactInstanceManager.ReactContextInitAsyncTask这个AsyncTask中执行上下文创建的工作，里面执行的东西可以说是所有的Java部分初始化内容（收集与注册提供的Native/JS/View模块、初始化CatalystInstance（负责核心Bridge相关）、运行JSBundle、将界面展示到ReactRootView上等）。

## 预初始化

涉及了so加载的操作，可以在 `ReactRootView.startReactApplication`
外部再加一层try-catch

## 创建React上下文阶段

{% asset_img 启动期异常.png %}

```java
  private void runCreateReactContextOnNewThread(final ReactContextInitParams initParams) {
    mCreateReactContextThread = new Thread(new Runnable() {
      @Override
      public void run() {
        try {
          final ReactApplicationContext reactApplicationContext = createReactContext(
              initParams.getJsExecutorFactory().create(),
              initParams.getJsBundleLoader());

          Runnable setupReactContextRunnable = new Runnable() {
            @Override
            public void run() {
              try {
                setupReactContext(reactApplicationContext);
              } catch (Exception e) {
                mDevSupportManager.handleException(e);
              }
            }
          };

        } catch (Exception e) {
          mDevSupportManager.handleException(e);
        }
      }
    });
  }
```

在框架启动的核心阶段，RN有捕获异常，但是仅仅只用 `DevSupportManager` 去处理，当不使用 `develop support` 时，会直接抛出异常。

这里我们可以做**第一个修改**，不使用dev support时

- 传入一个Handler去专门处理启动期的崩溃
- 用`ReactInstanceManagerBuilder.setNativeModuleCallExceptionHandler()` 传入的ExceptionHandler 统一去处理崩溃

## 运行期异常

1. JS调用Native产生异常
	- Native模块不存在
	- Native模块函数原型不一致
	- Native模块执行的异常
2. Native调用JS异常
	- JS模块不存在
	- JS模块函数原型不一致
	- JS模块执行的异常
3. JS本身代码执行的异常
4. UI操作的异常

### 运行线程

RN维护了三个线程的MessageQueue，所有的操作都会被push到上面运行

- **NativeQueue** 运行Native模块函数的线程（通常由JS发起），后台线程；
- **JSQueue** 运行JS的线程，后台线程。
- **UIQueue** 专门做UI操作，使用Android里面的**主线程**；

在CatalystInstance初始化的时候会初始化三个Queue，启动后台线程，并将他们的句柄传给C++层的Bridge。Queue里面调度使用的Handler，重写了dispatchMessage，并在外面包装了层try-catch，统统都会交到 `CatalystInstance.onNativeException` 中。而这其中使用的就是我们传入给ReactInstanceManager的ExceptionHandler。

```java
  private CatalystInstanceImpl(
     final ReactQueueConfigurationSpec reactQueueConfigurationSpec,
     final JavaScriptExecutor jsExecutor,
     final NativeModuleRegistry nativeModuleRegistry,
     final JSBundleLoader jsBundleLoader,
     NativeModuleCallExceptionHandler nativeModuleCallExceptionHandler) {
   Log.d(ReactConstants.TAG, "Initializing React Xplat Bridge.");
   mHybridData = initHybrid();

//创建三大线程：UI线程、Native线程与JS线程
   mReactQueueConfiguration = ReactQueueConfigurationImpl.create(
       reactQueueConfigurationSpec,
       new NativeExceptionHandler());
  }

  private void onNativeException(Exception e) {
    mNativeModuleCallExceptionHandler.handleException(e);
    mReactQueueConfiguration.getUIQueueThread().runOnQueue(
      new Runnable() {
        @Override
        public void run() {
          destroy();
        }
      });
  }

  private class NativeExceptionHandler implements QueueThreadExceptionHandler {
    @Override
    public void handleException(Exception e) {
      // Any Exception caught here is because of something in JS. Even if it's a bug in the
      // framework/native code, it was triggered by JS and theoretically since we were able
      // to set up the bridge, JS could change its logic, reload, and not trigger that crash.
      onNativeException(e);
    }
  }
```
初始化 `ReactInstanceManager` 时传的Handler 可以处理上面的前7种异常，我们需要单独处理UI操作异常

### UI操作的异常

UI操作，其实是调用的UIManagerModule这个Java模块进行的操作，但是实际上它不是马上被同步执行的，而是仅仅只有一个入队列的操作。所有的UI操作都通过Choreographer来驱动执行，那这个时候虽然是在主线程运行，但是不在上面任何一个MessageQueue里面了，于是上面的方式捕获不到。

以创建视图(`UIManagerModule.createView()`)为例，来追踪调用流程

```java
public abstract class GuardedFrameCallback extends ChoreographerCompat.FrameCallback {

  private final ReactContext mReactContext;

  protected GuardedFrameCallback(ReactContext reactContext) {
    mReactContext = reactContext;
  }

  @Override
  public final void doFrame(long frameTimeNanos) {
    try {
      doFrameGuarded(frameTimeNanos);
    } catch (RuntimeException e) {
      mReactContext.handleException(e);
    }
  }
}
```
UI操作的异常默认由 `ReactContext.handleException` 处理，追踪发现是 RN React上下文创建时设给它一个Handler，只在develop support时才起作用

```java
private ReactApplicationContext createReactContext(
      JavaScriptExecutor jsExecutor,
      JSBundleLoader jsBundleLoader) {
    Log.d(ReactConstants.TAG, "ReactInstanceManager.createReactContext()");
    ReactMarker.logMarker(CREATE_REACT_CONTEXT_START);
    final ReactApplicationContext reactContext = new ReactApplicationContext(mApplicationContext);

    if (mUseDeveloperSupport) {
      reactContext.setNativeModuleCallExceptionHandler(mDevSupportManager);
    }

    NativeModuleRegistry nativeModuleRegistry = processPackages(reactContext, mPackages, false);

    NativeModuleCallExceptionHandler exceptionHandler = mNativeModuleCallExceptionHandler != null
      ? mNativeModuleCallExceptionHandler
      : mDevSupportManager;
    CatalystInstanceImpl.Builder catalystInstanceBuilder = new CatalystInstanceImpl.Builder()
      .setReactQueueConfigurationSpec(mUseSeparateUIBackgroundThread ?
        ReactQueueConfigurationSpec.createWithSeparateUIBackgroundThread() :
        ReactQueueConfigurationSpec.createDefault())
      .setJSExecutor(jsExecutor)
      .setRegistry(nativeModuleRegistry)
      .setJSBundleLoader(jsBundleLoader)
      .setNativeModuleCallExceptionHandler(exceptionHan}ler);
}
```
这里我们可以做**第二个修改**，初始化ReactContext时，可以像设给CatalystInstance的一样

- 在使用develop support时设给它DevSupportManagerImpl
- 否则使用传入的NativeModuleExceptionHandler

# 参考&扩展

- 
[React Native for Android 异常处理概览](https://mp.weixin.qq.com/s/aWuenpGOKug4fovT5uKXTQ?)