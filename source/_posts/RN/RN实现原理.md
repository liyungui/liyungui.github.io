---
title: RN实现原理
date: 2018-07-26 15:35:14
tags:
	- RN
---

RN版本 `0.48.4`，后期更新了部分 `0.61.2`

# 原理概览

## RN源码目录结构

{% asset_img RN源码目录结构.png %}

## RN框架

{% asset_img RN框架.png %}

## 重要角色类

{% asset_img 重要角色.png %}

- **ReactNativeHost**：ReactInstanceManager 管理者(创建，持有，销毁)

	```java
	Application mApplication;
	ReactInstanceManager mReactInstanceManager;
	getReactInstanceManager()
	hasInstance()
	clear()
	```

- **ReactRootView**：RN的根View
- **ReactInstanceManager**：ReactNative应用管理类(持有ReactContext和JSBundleLoader)
	- **创建ReactContext、CatalystInstance等**类，解析ReactPackage生成映射表，并且配合ReactRootView管理View的创建与生命周期等功能。
- **ReactContext**：持有CatalystInstance
	- **ReactApplicationContext**：ReactContext的子类 
- **CatalystInstance**：Java层、C++层、JS层**通信**总管理类，总管Java层、JS层核心Module映射表与回调，三端通信的入口与桥梁。
	- **CatalystInstanceImpl**：CatalystInstance 实现类
- **NativeToJsBridge**：NativeToJsBridge是Java调用JS的桥梁，用来调用JS Module，回调Java。
- **JsToNativeBridge**：JsToNativeBridge是JS调用Java的桥梁，用来调用Java Module。
- **JavaScriptModule**：JavaScriptModule是JS Module，负责JS到Java的映射调用格式声明，由CatalystInstance统一管理。
- **NativeModule**：NativeModule是ava Module，负责Java到Js的映射调用格式声明，由CatalystInstance统一管理。
- **JavascriptModuleRegistry**：JS Module映射表
- **NativeModuleRegistry**：Java Module映射表
- **JavaScriptExecutor**：JS执行通信类。管理Webkit 的 JavaScriptCore，JS与C++的双向通信在这里中转
	- **JSCJavaScriptExecutor**，继承于JavaScriptExecutor。该类被加载时，它会自动去加载"reactnativejnifb.so"库，并会调用Native方 法initHybrid()初始化C++层RN与JSC**通信的框架**
- **JSBundleLoader**：bundle加载器，根据ReactNativeHost中的配置决定从哪里加载bundle文件，不同的场景会创建 不同的加载器
	- 缓存了JSBundle的信息，封装了上层加载JSBundle的相关接口，CatalystInstance通过其间接调用**ReactBridge**去加载JS文件。 
 
页面真正渲染出来以后，它实际上还是Native代码，React Native的作用就是把JavaScript代码映射成Native代码以及实现两端的通信

所以我们在React Native基础框架搭建的过程中，指导思路之一就是弱化Native与RN的边界与区别，让业务开发组感受不到两者的区别，从而简化开发流程。

有了对React Native框架的整体理解，我们来继续分析一个RN页面是如何启动并渲染出来的，这也是我们关心的主要问题。后续的基础框架的搭建、JS Bundle分包加载、渲染性能优化
等都会围绕着着一块做文章。

# 启动流程

ReactActivity的ReactRootView调用自己的startReactApplication()方法启动了整个RN页面

## 流程概览

### 加载so库

调用SoLoader的init方法，启动C++层逻辑代码的初始化加载

`SoLoader.init(Context context, int flags)`

### 创建 ReactInstanceManager

需要传入 根据场景创建的 **JSBundleLoader**

直接使用 `ReactInstanceManagerBuilder` 

或者使用封装的 `ReactNativeHost` ReactInstanceManager 管理者(创建，持有，销毁) 

### 创建 ReactRootView

`mReactRootView = createRootView();`

### 调用 ReactRootView.startReactApplication()

需要传入 ReactInstanceManager

`mReactRootView.startReactApplication(mReactInstanceManager,moduleName,initialBundle)`

具体工作：

- mReactInstanceManager.createReactContextInBackground()
	- 子线程创建 ReactContext
		- 构建ReactApplicationContext
		- 创建NativeModuleRegistry
		- 构建CatalystInstance
			- 创建JavaScriptModuleRegistry
			- 创建三大线程：UI线程、Native线程与JS线程。
			- 传入C++层初始化通信桥。
		- 关联catalystInstance(赋值成员变量)
		- CatalystInstance.runJSBundle()
			- JSBundleLoader.loadScript()
			- 遍历执行JS
	- 子线程 setupReactContext(reactApplicationContext)
		- 遍历 attachRootViewToInstance(reactRoot)。即绑定ReactRootView到CatalystInstance
			- 将ReactRootView作为根布局.
			- 执行JS页面入口.
				- 即 AppRegistry.js(RN应用的JS层入口)的runApplication 方法
- mReactInstanceManager.attachRootView(this)
	- 添加记录到容器。
		- 之后 setupReactContext 中 会遍历它
	- attachRootViewToInstance(reactRoot)

### 将 ReactRootView 添加到 Activity 布局视图

`setContentView(mReactRootView)`

## 代码流程跟踪

{% asset_img 创建ReactInstanceManager.png %}

Activity.onCreate() 创建ReactRootView，调用RootView.startReactApplication()

```java
public abstract class ReactActivity extends Activity
    implements DefaultHardwareBackBtnHandler, PermissionAwareActivity {
  private final ReactActivityDelegate mDelegate;

  protected ReactActivity() {
    //构造函数中调用createReactActivityDelegate()生成 ReactActivityDelegate 实例对象 mDelegate，
    //使用**委托模式**将 Activity 的生命周期及事件传递委托给 mDelegate 进行处理，
    //之所以使用这种形式是为了让 ReactFragmentActivity 也能**复用**该处理逻辑。
    //可以覆写 createReactActivityDelegate() 实现自定义的委托。
    mDelegate = createReactActivityDelegate();
  }
  
  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    mDelegate.onCreate(savedInstanceState);
  }  
}  

--------------------------------------
//返回键默认处理，所有的按下事件传递给JS，如果JS不想处理，JS将回调这个函数
public interface DefaultHardwareBackBtnHandler {
  void invokeDefaultOnBackPressed();
}

//标记接口，标记该Activity可以请求权限及监听请求权限结果
public interface PermissionAwareActivity {}
```

```java
public class ReactActivityDelegate { 
   protected void onCreate(Bundle savedInstanceState) {
      //动态获取悬浮窗权限，如果是开发者欧式，且在23版本及以上
      ...代码省略   
      // 核心代码：RN加载
      loadApp(mMainComponentName);   
   }
	
   protected void loadApp(String appKey) {
      mReactRootView = createRootView();// 创建 RN 容器根视图，父类为 FrameLayout
      mReactRootView.startReactApplication(
      getReactNativeHost().getReactInstanceManager(), appKey, getLaunchOptions());
      getPlainActivity().setContentView(mReactRootView);// 将 RN 视图放入 Activity
   }
```

## 创建 ReactInstanceManager

RootView.startReactApplication()参数需要ReactInstanceManager实例

从序列图可以发现，最终创建ReactInstanceManager是ReactNativeHost.createReactInstanceManager()方法

```java
protected ReactInstanceManager createReactInstanceManager() {
ReactInstanceManagerBuilder builder = ReactInstanceManager.builder()
  .setApplication(mApplication)//应用上下文
  .setJSMainModuleName(getJSMainModuleName())//首页js文件名，dev模式支持从packager server拉取
  .setUseDeveloperSupport(getUseDeveloperSupport())//是否开启dev模式；创建ReactNativeHost实例时需实现getUseDeveloperSupport()
  .setRedBoxHandler(getRedBoxHandler())//红盒回调
  .setUIImplementationProvider(getUIImplementationProvider())//自定义UI实现机制，一般用不到
  .setInitialLifecycleState(LifecycleState.BEFORE_CREATE);

//添加package；创建ReactNativeHost实例时需实现getPackages()
for (ReactPackage reactPackage : getPackages()) {
  builder.addPackage(reactPackage);
}
	
 //添加js Bundle的加载路径
String jsBundleFile = getJSBundleFile();
if (jsBundleFile != null) {
  builder.setJSBundleFile(jsBundleFile);
} else {
  builder.setBundleAssetName(Assertions.assertNotNull(getBundleAssetName()));
}
return builder.build();
}
```

### 创建 JSBundleLoader

在 ReactInstanceManagerBuilder 中根据设置的场景 完成 JSBundleLoader 初始化

不同的场景会创建不同的加载器

有三种加载场景：

- **从远程服务器加载** setSourceURLs(String deviceURL, String remoteURL) 
- **从Assets文件夹加载** loadScriptFromAssets(AssetManager assetManager, String assetURL, boolean loadSynchronously)
- **从文件路径加载** loadScriptFromFile(String fileName, String sourceURL, boolean loadSynchronously)

## RootView.startReactApplication()

```java
//子线程创建ReactContext
mReactInstanceManager.createReactContextInBackground();

//attachToReactInstanceManager
mReactInstanceManager.attachRootView(this)
```

```java
  public void attachRootView(ReactRoot reactRoot) {
    UiThreadUtil.assertOnUiThread();
    
    //添加记录到容器；
    //js加载后，将所有的ReactRootView与catalystInstance进行绑定
    mAttachedReactRoots.add(reactRoot);

    ReactContext currentContext = getCurrentReactContext();
    if (mCreateReactContextThread == null && currentContext != null) {
      attachRootViewToInstance(reactRoot);
    }
  }
```
  
## 创建ReactContext

在启动的过程中先去创建页面上下文ReactContext，然后再去加载、执行并将JavaScript映射成Native Widget，最终一个RN页面就显示在了用户面前

从序列图可以发现，最终创建ReactContext是ReactInstanceManager.createReactContext()方法

{% asset_img 创建ReactContext.png %}

### ReactContext 和 ReactApplicationContext

ReactApplicationContext 和 ReactContext 的关系，就如 ApplicationContext 和 Context

```java
public class ReactContext extends ContextWrapper {}
public class ReactApplicationContext extends ReactContext {}
```

### createReactContextInBackground

**public; 初始化/重新初始化 ReactContext；这个方法可以预加载JS**


```java
  public void createReactContextInBackground() {
    //只能调用一次
    //public 方法只有destroy()才能置标识为false
    if (!mHasStartedCreatingInitialContext) {
      mHasStartedCreatingInitialContext = true;
      recreateReactContextInBackgroundInner();
    }
  }
```

RN 提供了另一个public API `recreateReactContextInBackground()`

**可以无限次重新创建 ReactContext**，前提是之前调用过 `createReactContextInBackground `

```java
  public void recreateReactContextInBackground() {
    Assertions.assertCondition(
        //mHasStartedCreatingInitialContext为false，抛出异常
        mHasStartedCreatingInitialContext,
        "recreateReactContextInBackground should only be called after the initial "
            + "createReactContextInBackground call.");
    recreateReactContextInBackgroundInner();
  }
```
  
### recreateReactContextInBackgroundInner

根据是否是调试模式，初始化ReactContext

```java
  private void recreateReactContextInBackgroundInner() {  
    // 确保在UI线程执行

    // 调试模式，从服务器加载 bundle
    if (mUseDeveloperSupport && mJSMainModuleName != null) {
      // 省略代码
      return;
    }

    // 正式环境，从本地加载 bundle
    recreateReactContextInBackgroundFromBundleLoader();
  }
```

### recreateReactContextInBackgroundFromBundleLoader

```java
  private void recreateReactContextInBackgroundFromBundleLoader() {
    recreateReactContextInBackground(
        new JSCJavaScriptExecutor.Factory(mJSCConfig.getConfigMap()),
        mBundleLoader);
  }
```

### recreateReactContextInBackground

根据负责创建ReactContext的线程是否运行中，不在运行中马上起新线程，否则延时创建

```java
  private void recreateReactContextInBackground(
    JavaScriptExecutor.Factory jsExecutorFactory,
    JSBundleLoader jsBundleLoader) {
    //确保UI线程运行

    final ReactContextInitParams initParams = new ReactContextInitParams(
      jsExecutorFactory,
      jsBundleLoader);
    if (mCreateReactContextThread == null) {//线程不在运行
      //启动新线程初始化ReactContext
      runCreateReactContextOnNewThread(initParams);
    } else {
      //延时初始化ReactContext
      //因为runCreateReactContextOnNewThread检测到延迟参数非空，会递归调用自身
      mPendingReactContextInitParams = initParams;
    }
  }	
```

### runCreateReactContextOnNewThread

启动新线程初始化 ReactContext

```java
private void runCreateReactContextOnNewThread(final ReactContextInitParams initParams) {
  mCreateReactContextThread = new Thread(new Runnable() {
	  @Override
	  public void run() {
	    try {
	      //创建 ReactApplicationContext(ReactContext的子类)
	      final ReactApplicationContext reactApplicationContext = createReactContext(
	          initParams.getJsExecutorFactory().create(),
	          initParams.getJsBundleLoader());
		
	      mCreateReactContextThread = null;
	      
	      //需要的话，子线程 重建 ReactContex
	      //延时参数非空，递归调用runCreateReactContextOnNewThread自身
	      final Runnable maybeRecreateReactContextRunnable = new Runnable() {
	        @Override
	        public void run() {
	          if (mPendingReactContextInitParams != null) {
	            runCreateReactContextOnNewThread(mPendingReactContextInitParams);
	            mPendingReactContextInitParams = null;
	          }
	        }
	      };
	      //子线程 设置 ReactContex
	      //这里能保证是先 createReactContex 后 setupReactContext。
	      //因为setupReactContext中ReactContext为空则返回，
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
	      reactApplicationContext.runOnNativeModulesQueueThread(setupReactContextRunnable);
	      UiThreadUtil.runOnUiThread(maybeRecreateReactContextRunnable);
	    } catch (Exception e) {
	      mDevSupportManager.handleException(e);
	    }
	  }
	});
	mCreateReactContextThread.start();
```

### createReactContext

主要做了以下5件事情：

- **构建ReactApplicationContext**对象(ReactContext的子类)。
- 创建NativeModuleRegistry
- **构建CatalystInstance**实例，作为以为三端通信的中枢。需要使用jsExecutor、nativeModuleRegistry、jsBundleLoader、exceptionHandler等参数。
- 关联catalystInstance(赋值成员变量)
- 调用CatalystInstance的**runJSBundle()**开始**加载执行JS**。

```java
  private ReactApplicationContext createReactContext(
      JavaScriptExecutor jsExecutor,
      JSBundleLoader jsBundleLoader) {
      
    // 创建 ReactApplicationContext 实例
    final ReactApplicationContext reactContext = new ReactApplicationContext(mApplicationContext);

	 // 创建JavaModule注册表，把所有的 NativeModule 注册到 CatalystInstance ，将 Java 的可调用 API 暴露给 JS。
    NativeModuleRegistry nativeModuleRegistry = processPackages(reactContext, mPackages, false);

	// 异常处理器选择逻辑
    NativeModuleCallExceptionHandler exceptionHandler = mNativeModuleCallExceptionHandler != null
      ? mNativeModuleCallExceptionHandler
      : mDevSupportManager;
      
    // 创建 CatalystInstance 实例，它是三端通信的管理类
    CatalystInstanceImpl.Builder catalystInstanceBuilder = new CatalystInstanceImpl.Builder()
      .setReactQueueConfigurationSpec(mUseSeparateUIBackgroundThread ?
        ReactQueueConfigurationSpec.createWithSeparateUIBackgroundThread() :
        ReactQueueConfigurationSpec.createDefault())
      .setJSExecutor(jsExecutor)// JS执行通信类
      .setRegistry(nativeModuleRegistry)// Java Module注册
      .setJSBundleLoader(jsBundleLoader)// JS Bundle加载器
      .setNativeModuleCallExceptionHandler(exceptionHandler);// Java Exception处理器

    catalystInstance = catalystInstanceBuilder.build();

    if (mBridgeIdleDebugListener != null) {
      catalystInstance.addBridgeIdleDebugListener(mBridgeIdleDebugListener);
    }
    
    // 调用 C++ 层代码，把 Java Registry 转换为Json，再由 C++ 层传送到 JS 层
    if (Systrace.isTracing(TRACE_TAG_REACT_APPS | TRACE_TAG_REACT_JSC_CALLS)) {
      catalystInstance.setGlobalVariable("__RCTProfileIsProfiling", "true");
    }

	// 关联catalystInstance与reactContext
    reactContext.initializeWithInstance(catalystInstance);
    
    // 加载执行JS Bundle
    catalystInstance.runJSBundle();

    return reactContext;
  }
```

## 创建CatalystInstance

创建CatalystInstance对象时，主要做了两件事情：

- 创建JavaScriptModuleRegistry
- 创建三大线程：UI线程、Native线程与JS线程。
- 传入C++层初始化通信桥。

创建catalyst**三大线程**（必须的三个带消息队列的线程）：

- UI线程：Android的UI线程，处理和UI相关的事情。
- Native线程：主要是完成通信的工作。
- JS线程：主要完成JS的执行和渲染工作。

```java
  private CatalystInstanceImpl(
      final ReactQueueConfigurationSpec reactQueueConfigurationSpec,
      final JavaScriptExecutor jsExecutor,
      final NativeModuleRegistry nativeModuleRegistry,
      final JSBundleLoader jsBundleLoader,
      NativeModuleCallExceptionHandler nativeModuleCallExceptionHandler) {
    //创建JS Module注册表实例
    mJSModuleRegistry = new JavaScriptModuleRegistry();
    
    mReactQueueConfiguration = ReactQueueConfigurationImpl.create(
        reactQueueConfigurationSpec,
        new NativeExceptionHandler());
    
    //创建三大线程：UI线程、Native线程与JS线程
    //传入C++层初始化通信桥
    initializeBridge(
      new BridgeCallback(this),
      jsExecutor,
      mReactQueueConfiguration.getJSQueueThread(),
      mReactQueueConfiguration.getNativeModulesQueueThread(),
      mReactQueueConfiguration.getUIBackgroundQueueThread(),
      mNativeModuleRegistry.getJavaModules(this),
      mNativeModuleRegistry.getCxxModules());
  }
```

### ReactQueueConfigurationSpec

创建ReactQueueConfiguration实例的Spec。就因为有Spec，可以完全配置CatalystInstance线程创建参数，比如可以设置它所使用的MessageQueueThreads的Exception handlers

三个MessageQueueThreadSpec类型的成员变量，分别记录三大线程的Spec


```java
public class ReactQueueConfigurationSpec {
  private final MessageQueueThreadSpec mUIBackgroundQueueThreadSpec;
  private final MessageQueueThreadSpec mNativeModulesQueueThreadSpec;
  private final MessageQueueThreadSpec mJSQueueThreadSpec;
}

public class MessageQueueThreadSpec {
  private final ThreadType mThreadType;
  private final String mName;
  private final long mStackSize;
}
```

### ReactQueueConfiguration

```java
public interface ReactQueueConfiguration {
  MessageQueueThread getUIQueueThread();
  MessageQueueThread getUIBackgroundQueueThread();
  MessageQueueThread getNativeModulesQueueThread();
  MessageQueueThread getJSQueueThread();
  void destroy();
}
```

## catalystInstance.runJSBundle()

- JSBundleLoader.loadScript()
- 遍历执行JS

```java
  public void runJSBundle() {
    // 通过 JSBundleLoader 去执行加载
    mJSBundleLoader.loadScript(CatalystInstanceImpl.this);

    synchronized (mJSCallsPendingInitLock) {

      // 遍历执行JS
      for (PendingJSCall function : mJSCallsPendingInit) {
        function.call(this);
      }
      mJSCallsPendingInit.clear();
      mJSBundleHasLoaded = true;
    }
  }
```

### loadScript

```java
public abstract String loadScript(JSBundleLoaderDelegate delegate);

public interface JSBundleLoaderDelegate {
  void loadScriptFromAssets(AssetManager assetManager, String assetURL, boolean loadSynchronously);
  void loadScriptFromFile(String fileName, String sourceURL, boolean loadSynchronously);
  void loadScriptFromDeltaBundle(String sourceURL, NativeDeltaClient deltaClient, boolean loadSynchronously);
  void setSourceURLs(String deviceURL, String remoteURL);     
}
```

通过 `CatalystInstanceImpl` 实现 `JSBundleLoaderDelegate`接口 来加载 js

加载 JS Bundle实际上是在C++层完成的，序列图如下(接 创建ReactContext序列图)

{% asset_img 加载JSBundle.png %}

从序列图上可以看出，真正加载执行JS的地方就是JSCExector.cpp的loadApplicationScript()方法。

至此，JS Bundle已经加载解析完成，进入MessageQueue.js开始执行。
  
## setupReactContext

JS Bundle加载完成以后，前面说的createReactContext()就执行完成了，然后开始执行setupReacContext()方法，将所有的ReactRootView与catalystInstance进行绑定

- 遍历 attachRootViewToInstance(reactRoot)
	- 将ReactRootView作为根布局.
	- 执行JS页面入口.
		- 即 AppRegistry.js(RN应用的JS层入口)的runApplication 方法
		
```java
  private void setupReactContext(ReactApplicationContext reactContext) {
    mCurrentReactContext = Assertions.assertNotNull(reactContext);
    CatalystInstance catalystInstance =
      Assertions.assertNotNull(reactContext.getCatalystInstance());

    catalystInstance.initialize();// 初始化所有 Native Module
    //通知ReactContext已经被创建
    mDevSupportManager.onNewReactContextCreated(reactContext);
    // 添加内存警告的回调
    mMemoryPressureRouter.addMemoryPressureListener(catalystInstance);
    //复位生命周期
    moveReactContextToCurrentLifecycleState();
    
    ReactMarker.logMarker(ATTACH_MEASURED_ROOT_VIEWS_START);
    
    //将所有的ReactRootView与catalystInstance进行绑定
    // mAttachedRootViews 保存的是ReactRootView
    synchronized (mAttachedRootViews) {
      for (ReactRootView rootView : mAttachedRootViews) {
        attachRootViewToInstance(reactRoot);
      }
    }
    ReactMarker.logMarker(ATTACH_MEASURED_ROOT_VIEWS_END);

    //省略代码
  }
```

```java
  private void attachRootViewToInstance(final ReactRootView rootView) {
    Log.d(ReactConstants.TAG, "ReactInstanceManager.attachRootViewToInstance()");
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "attachRootViewToInstance");
    
    UIManagerModule uiManagerModule = catalystInstance.getNativeModule(UIManagerModule.class);
    //将ReactRootView作为根布局
    final int rootTag = uiManagerModule.addRootView(rootView);
    rootView.setRootViewTag(rootTag);
    //调用rootView.runApplication()
    rootView.runApplication();
    
    UiThreadUtil.runOnUiThread(new Runnable() {
      @Override
      public void run() {
        rootView.onAttachedToReactInstance();
      }
    });
  }
```

```java
  void runApplication() {
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "ReactRootView.runApplication");
    try {
      if (mReactInstanceManager == null || !mIsAttachedToInstance) {
        return;
      }

      ReactContext reactContext = mReactInstanceManager.getCurrentReactContext();
      if (reactContext == null) {
        return;
      }

      CatalystInstance catalystInstance = reactContext.getCatalystInstance();

      WritableNativeMap appParams = new WritableNativeMap();
      appParams.putDouble("rootTag", getRootViewTag());
      @Nullable Bundle appProperties = getAppProperties();
      if (appProperties != null) {
        appParams.putMap("initialProps", Arguments.fromBundle(appProperties));
      }

      String jsAppModuleName = getJSModuleName();
      
      //调用 AppRegistry.js(RN应用的JS层入口)的runApplication 方法
      catalystInstance.getJSModule(AppRegistry.class).runApplication(jsAppModuleName, appParams);// AppRegistry 是 JS 暴露给 Java 层的 API
    } finally {
      Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
    }
  }
```

这里的调用方式实际上就是**原生调用JS方法**，它默认调用AppRegistry.js 的runApplication()开始执行JS页面的渲染，最终转换为
Native UI显示在手机上。

到此，RN页面的启动流程就分析完了

我们接着来看看RN的通信机制，以理解原生调用JS方法的实现，即Java是如何调用到AppRegisty.js的runApplication()的。

# 通信机制

Java层与JavaScript层的相互调用都不是直接完成的，而是间接通过C++层来完成的。

## 基本概念

### JavaScript Module注册表

#### JavaScriptModule 接口

JS Module都会继承此接口，实现该接口即可被Java调用

它表示在JS层会有一个相同名字的js文件，该js文件实现了该接口定义的方法

```java
/**
 * Interface denoting that a class is the interface to a module with the same name in JS. Calling
 * functions on this interface will result in corresponding methods in JS being called.
 *
 * When extending JavaScriptModule and registering it with a CatalystInstance, all public methods
 * are assumed to be implemented on a JS module with the same name as this class. Calling methods
 * on the object returned from {@link ReactContext#getJSModule} or
 * {@link CatalystInstance#getJSModule} will result in the methods with those names exported by
 * that module being called in JS.
 *
 * NB: JavaScriptModule does not allow method name overloading because JS does not allow method name
 * overloading.
 */
@DoNotStrip
public interface JavaScriptModule {
}
标记接口，标记该类是定义JS接口(就如native关键字表明该方法是so中的native方法)
调用该类的方法，最终调用的是JS中的同名方法
一个类继承该标记接口并在CatalystInstance中注册，意味着该类的所有public方法都在JS中有同名实现方法
ReactContext.getJSModule()和CatalystInstance.getJSModule()返回的都是JavaScriptModule对象
注意：JavaScriptModule标记接口的子类，不允许方法名重载，因为JS不支持方法名重载
```

##### AppRegistry接口

```java
/**
 * JS module interface - main entry point for launching React application for a given key.
 */
public interface AppRegistry extends JavaScriptModule {  
  void runApplication(String appKey, WritableMap appParameters);
  void unmountApplicationComponentAtRootTag(int rootNodeTag);
  void startHeadlessTask(int taskId, String taskKey, WritableMap data);
}
```

`runApplication()` 是加载 `index.android.js` 的主**入口**

#### JavaScriptModuleInvocationHandler

所有的 **JS 方法调用**都会经过 JavaScriptModuleInvocationHandler

```java
@Override
public @Nullable Object invoke(Object proxy, Method method, @Nullable Object[] args) throws Throwable {  
  NativeArray jsArgs = args != null ? Arguments.fromJavaArgs(args) : new WritableNativeArray();
  // 调用 C++ 层的 callFunction
  mCatalystInstance.callFunction(getJSModuleName(), method.getName(), jsArgs);
      return null;
}
```

#### JavaScriptModuleRegistry

JS Module注册表

内部维护了一个HashMap：HashMap<Class<? extends JavaScriptModule>, JavaScriptModule> mModuleInstances;

利用动态代理生成接口JavaScriptModule对应的代理类，再通过C++传递到JS层，从而调用JS层的方法。

### Java Module注册表

#### NativeModule 接口

Native Module都会继承此接口，实现了该接口则可以被JS层调用

在为JS层提供Java API时通常会继承BaseJavaModule/ReactContextBaseJavaModule，这两个类就
实现了NativeModule接口。

#### ModuleHolder

NativeModule的一个Holder类，可以实现NativeModule的懒加载。

#### NativeModuleRegistry

Java Module注册表

内部持有Map：Map<Class<? extends NativeModule>, ModuleHolder> mModules

NativeModuleRegistry可以遍历
并返回Java Module供调用者使用。

## 创建注册表

注册表的创建，我们前面都已经提到

- NativeModuleRegistry是在createReactContext()方法里构建的。
- JavaScriptModuleRegistry是在CatalystInstanceImpl的构建方法里构建的。

最后都是在CatalystInstanceImpl的构建方法里通过native方法CatalystInstanceImpl::initializeBridge()传入了C++层，打包好的ModuleRegistry通过Instance::initializeBridge()传入到NativeToJsBridge.cpp中，并在NativeToJsBridge的构造方法中传给JsToNativeBridge，以后JS如果调用Java就可以通过
ModuleRegistry来进行调用。
这里的NativeToJsBridge.cpp与JsToNativeBridge.cpp就是Java与JS相互调用的通信桥，我们来看看它们的通信方式。

## 创建通信桥

关于整个RN的通信机制，可以用一句话来概括：

```
JNI作为C++与Java的桥梁，JSC作为C++与JavaScript的桥梁，
C++最终连接了Java与JavaScript。
``` 

# 渲染原理

上面说了，RN页面的入口默认是AppRegistry.js 的runApplication()

我们接着来看看RN页面是如何渲染最终显示在手机上的。

RN页面渲染流程序列图 如下

{% asset_img RN页面渲染流程序列图.png %}

流程比较长(方法调用链多)，原理很简单，概括性的总结一下：

- React Native将代码由JSX转化为JS组件，启动过程中利用instantiateReactComponent将ReactElement转化为复合组件ReactCompositeComponent与元组件ReactNativeBaseComponent，利用
ReactReconciler对他们进行渲染。
- UIManager.js利用C++层的Instance.cpp将UI信息传递给UIManagerModule.java，并利用UIManagerModule.java构建UI。
- UIManagerModule.java接收到UI信息后，将UI的操作封装成对应的Action，放在队列中等待执行。各种UI的操作，例如创建、销毁、更新等便在队列里完成，UI最终
得以渲染在屏幕上。

# 参考&扩展

- [React Native for Android 原理分析与实践：实现原理](https://juejin.im/post/5a6460f8f265da3e4f0a446d#heading-11) 条理清晰而详实
- [20 分钟理解 React Native For Android 原理](https://juejin.im/entry/58d4770544d9040069295eaa) [原文链接-大搜车](https://blog.souche.com/react-native-source-code-analysis/)
- [React Native Android Gradle 编译流程浅析](https://blog.csdn.net/yanbober/article/details/53105728)
- [React Native JSBundle拆包之原理篇](https://www.epubit.com/articleDetails?id=N430cc4fa-4b89-4d26-9ae8-d2791ac23416)