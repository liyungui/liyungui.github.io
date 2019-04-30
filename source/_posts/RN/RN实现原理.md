---
title: RN实现原理
date: 2018-07-26 15:35:14
tags:
	- RN
---

RN版本 `0.48.4`

# 原理概览

## RN源码目录结构

{% asset_img RN源码目录结构.png %}

## RN框架

{% asset_img RN框架.png %}

## 重要角色类

- **ReactContext**：ReactContext继承于ContextWrapper，是ReactNative应用的上下文，通过getContext()去获得，通过它可以访问ReactNative核心类的实现。
- **ReactInstanceManager**：ReactInstanceManager是ReactNative应用总的管理类，**创建ReactContext、CatalystInstance等**类，解析ReactPackage生成映射表，并且配合ReactRootView管理View的创建与生命周期等功能。
- **CatalystInstance**：CatalystInstance是ReactNative应用Java层、C++层、JS层**通信**总管理类，总管Java层、JS层核心Module映射表与回调，三端通信的入口与桥梁。
- **NativeToJsBridge**：NativeToJsBridge是Java调用JS的桥梁，用来调用JS Module，回调Java。
- **JsToNativeBridge**：JsToNativeBridge是JS调用Java的桥梁，用来调用Java Module。
- **JavaScriptModule**：JavaScriptModule是JS Module，负责JS到Java的映射调用格式声明，由CatalystInstance统一管理。
- **NativeModule**：NativeModule是ava Module，负责Java到Js的映射调用格式声明，由CatalystInstance统一管理。
- **JavascriptModuleRegistry**：JS Module映射表
- **NativeModuleRegistry**：Java Module映射表

页面真正渲染出来以后，它实际上还是Native代码，React Native的作用就是把JavaScript代码映射成Native代码以及实现两端
的通信

所以我们在React Native基础框架搭建的过程中，指导思路之一就是弱化Native与RN的边界与区别，让业务开发组感受不到两者的区别，从而简化开发流程。

有了对React Native框架的整体理解，我们来继续分析一个RN页面是如何启动并渲染出来的，这也是我们关心的主要问题。后续的基础框架的搭建、JS Bundle分包加载、渲染性能优化
等都会围绕着着一块做文章。

ReactActivity的ReactRootView调用自己的startReactApplication()方法启动了整个RN页面，在启动的过程
中先去创建页面上下文ReactContext，然后再去加载、执行并将JavaScript映射成Native Widget，最终一个RN页面就显示在了用户面前

# 启动流程

主要关注以下五个问题

## 用户创建ReactNativeHost

使用RN页面，需要用户先创建一个ReactNativeHost

```java
  new ReactNativeHost(this) {
    @Override
    public boolean getUseDeveloperSupport() {//是否使用开发模式
      return BuildConfig.DEBUG;
    }

    @Override
    protected List<ReactPackage> getPackages() {//Package List
      return Arrays.<ReactPackage>asList(
              new MainReactPackage()
      );
    }
  };
```

## 创建ReactInstanceManager

从序列图可以发现，最终创建ReactInstanceManager是ReactNativeHost.createReactInstanceManager()方法

{% asset_img 创建ReactInstanceManager.png %}

### ReactActivity

构造函数中调用createReactActivityDelegate()生成 ReactActivityDelegate 实例对象 mDelegate，使用**委托模式**将 Activity 的生命周期及事件传递委托给 mDelegate 进行处理，之所以使用这种形式是为了让 ReactFragmentActivity 也能**复用**该处理逻辑。 

可以覆写 createReactActivityDelegate() 实现自定义的委托。

```java
public abstract class ReactActivity extends Activity
    implements DefaultHardwareBackBtnHandler, PermissionAwareActivity {
  private final ReactActivityDelegate mDelegate;

  protected ReactActivity() {
    mDelegate = createReactActivityDelegate();
  }
```
```java
public interface DefaultHardwareBackBtnHandler {

  /**
   * By default, all onBackPress() calls should not execute the default backpress handler and should
   * instead propagate it to the JS instance. If JS doesn't want to handle the back press itself,
   * it shall call back into native to invoke this function which should execute the default handler
   */
  void invokeDefaultOnBackPressed();
}
默认，所有的 onBackPress() 不应该执行默认的按下处理，
而是应该把按下事件传递给JS，
如果JS不想处理，JS将回调这个函数
```
```java
/**
 * Interface used to denote activities that can forward permission requests and call
 * {@link PermissionListener}s with the permission request results.
 */
public interface PermissionAwareActivity {}
标记接口，标记该Activity可以请求权限及监听请求权限结果
```

### ReactActivityDelegate

```java 
protected void onCreate(Bundle savedInstanceState) {
	boolean needsOverlayPermission = false;
   
   // Get DrawOverlay permission to show redbox in dev builds. 
	if (getReactNativeHost().getUseDeveloperSupport() && Build.VERSION.SDK_INT >= 23) {
    	if (!Settings.canDrawOverlays(getContext())) {
    		needsOverlayPermission = true;
    		// 弹窗动态获取权限
    	}
    }
    
    // 组件加载逻辑
    if (mMainComponentName != null&& !needsOverlayPermission) {
      loadApp(mMainComponentName);
    }
    
    // 双击判断工具类 DoubleTapReloadRecognizer
    mDoubleTapReloadRecognizer = new DoubleTapReloadRecognizer();
  }
}
```
```java	
protected void loadApp(String appKey) {
	if (mReactRootView != null) {
	  	throw new IllegalStateException("Cannot loadApp while app is already running.");
	}
	
    mReactRootView = createRootView();// 创建 RN 容器根视图，父类为 FrameLayout
    mReactRootView.startReactApplication(
      getReactNativeHost().getReactInstanceManager(),
      appKey,
      getLaunchOptions());
	getPlainActivity().setContentView(mReactRootView);// 将 RN 视图放入 Activity
}
```
**loadApp()**两个调用时机

- onCreate() 不需要动态获取DrawOverlay权限，或已获取权限
- onActivityResult 动态获取DrawOverlay权限成功

### ReactInstanceManager

```java
public class ReactInstanceManager {
```

### ReactNativeHost

```java
/**
 * 创建并持有/管理 ReactInstanceManager 实例
 * 一般将 ReactNativeHost实例 存在Application或者静态变量中，以便全局使用
 */
public abstract class ReactNativeHost {
  private final Application mApplication;
  private @Nullable ReactInstanceManager mReactInstanceManager;

  //构造函数
  protected ReactNativeHost(Application application) {
    mApplication = application;
  }

  //获取 ReactInstanceManager
  public ReactInstanceManager getReactInstanceManager() {
    if (mReactInstanceManager == null) {
      mReactInstanceManager = createReactInstanceManager();
    }
    return mReactInstanceManager;
  }
}
```
  
### 创建 ReactInstanceManager

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

### 获取JSMainModuleName/JS入口文件名

```java
 /**
   * 获取 main module 名字. 
   * dev模式支持从packager server获取js bundle.
   *  ReactInstanceManager创建后执行的第一个文件. 
   *  默认是 index.android. RN工程默认的Android js入口文件名 index.android.js
   */
  protected String getJSMainModuleName() {
    return "index.android";
  }
```

## 创建ReactContext

从序列图可以发现，最终创建ReactContext是ReactInstanceManager.createReactContext()方法

{% asset_img 创建ReactContext.png %}

### ReactRootView

因此可以认为 **RN 其实就是一个特殊的“自定义 View ”**-- `ReactRootView`

{% asset_img ReactRootView.png %}

- Default root view for catalyst apps. 
- Provides the ability to **listen for size changes** so that a UI manager can **re-layout** its elements.
- It delegates handling **touch events** for itself and child views and **sending** those events **to JS** by using **JSTouchDispatcher**.

```java
  /**
   * Schedule rendering of the react component rendered by the JS application from the given JS
   * module (@{param moduleName}) using provided {@param reactInstanceManager} to attach to the
   * JS context of that manager. Extra parameter {@param launchOptions} can be used to pass initial
   * properties for the react component.
   */
  public void startReactApplication(
      ReactInstanceManager reactInstanceManager,
      String moduleName,
      @Nullable Bundle initialProperties) {
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "startReactApplication");
    try {
      UiThreadUtil.assertOnUiThread();// 确保在 UI 线程执行

      // 确保 mReactInstanceManager 没有初始化过
      Assertions.assertCondition(
        mReactInstanceManager == null,
        "This root view has already been attached to a catalyst instance manager");

      mReactInstanceManager = reactInstanceManager;
      mJSModuleName = moduleName;
      mAppProperties = initialProperties;

		// ReactContext 没有初始化，异步在后台线程创建
      if (!mReactInstanceManager.hasStartedCreatingInitialContext()) {
        mReactInstanceManager.createReactContextInBackground();
      }

      attachToReactInstanceManager();
    } finally {
      Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
    }
  }
```
```java  
  /**
   * 绑定 mReactInstanceManager 和 rootview
   * 添加布局监听
   */
  private void attachToReactInstanceManager() {
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "attachToReactInstanceManager");
    try {
      if (mIsAttachedToInstance) {
        return;
      }

      mIsAttachedToInstance = true;
      Assertions.assertNotNull(mReactInstanceManager).attachRootView(this);
      getViewTreeObserver().addOnGlobalLayoutListener(getCustomGlobalLayoutListener());
    } finally {
      Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
    }
  }
```

### ReactContext 和 ReactApplicationContext

ReactApplicationContext 和 ReactContext 的关系，就如 ApplicationContext 和 Context

```java
public class ReactContext extends ContextWrapper {}
```
```java
public class ReactApplicationContext extends ReactContext {
  public ReactApplicationContext(Context context) {
    super(context.getApplicationContext());
  }
}
```

### 创建ReactContext

#### createReactContextInBackground

```java
  /**
   * 在后台线程异步初始化ReactContext，这个方法只会在 Application 创建时调用一次，
   * 重新加载 JS 时将会调用 recreateReactContextInBackground 方法
  */
  public void createReactContextInBackground() {  
    // 断言：已经开始创建Context，返回
    mHasStartedCreatingInitialContext = true;
    recreateReactContextInBackgroundInner();
  }
```

#### recreateReactContextInBackgroundInner

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

#### recreateReactContextInBackgroundFromBundleLoader

```java
  private void recreateReactContextInBackgroundFromBundleLoader() {
    recreateReactContextInBackground(
        new JSCJavaScriptExecutor.Factory(mJSCConfig.getConfigMap()),
        mBundleLoader);
  }
```

#### recreateReactContextInBackground

```java
  private void recreateReactContextInBackground(
    JavaScriptExecutor.Factory jsExecutorFactory,
    JSBundleLoader jsBundleLoader) {
    //确保UI线程运行

    final ReactContextInitParams initParams = new ReactContextInitParams(
      jsExecutorFactory,
      jsBundleLoader);
    if (mCreateReactContextThread == null) {
      //新线程初始化ReactContext
      runCreateReactContextOnNewThread(initParams);
    } else {
      mPendingReactContextInitParams = initParams;
    }
  }	
```

#### runCreateReactContextOnNewThread

```java
/**
 * 新线程初始化 ReactContext
 * /
private void runCreateReactContextOnNewThread(final ReactContextInitParams initParams) {
  mCreateReactContextThread = new Thread(new Runnable() {
	  @Override
	  public void run() {
	    try {
	      Process.setThreadPriority(Process.THREAD_PRIORITY_DISPLAY);
	      //创建 ReactApplicationContext
	      final ReactApplicationContext reactApplicationContext = createReactContext(
	          initParams.getJsExecutorFactory().create(),
	          initParams.getJsBundleLoader());
		
	      mCreateReactContextThread = null;
	      ReactMarker.logMarker(PRE_SETUP_REACT_CONTEXT_START);
	      
	      //需要的话，子线程 Recreate ReactContex
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
	      
	      //这里能保证是先 createReactContex 后 setupReactContext。
	      //因为setupReactContext中ReactContext为空则返回，
	      //maybeRecreateReactContextRunnable 中递归调用了runCreateReactContextOnNewThread
	      reactApplicationContext.runOnNativeModulesQueueThread(setupReactContextRunnable);
	      UiThreadUtil.runOnUiThread(maybeRecreateReactContextRunnable);
	    } catch (Exception e) {
	      mDevSupportManager.handleException(e);
	    }
	  }
	});
	mCreateReactContextThread.start();
```

#### 创建ReactContext - createReactContext

```java
  /**
   * @return instance of {@link ReactContext} configured a {@link CatalystInstance} set
   */
  private ReactApplicationContext createReactContext(
      JavaScriptExecutor jsExecutor,
      JSBundleLoader jsBundleLoader) {
    Log.d(ReactConstants.TAG, "ReactInstanceManager.createReactContext()");
    ReactMarker.logMarker(CREATE_REACT_CONTEXT_START);
    
    // 包装 ApplicationContext 为 ReactApplicationContext
    final ReactApplicationContext reactContext = new ReactApplicationContext(mApplicationContext);

	 // 调试模式下 ReactApplicationContext 中崩溃信息由 mDevSupportManager 进行拦截处理（红色背景的错误页）
    if (mUseDeveloperSupport) {
      reactContext.setNativeModuleCallExceptionHandler(mDevSupportManager);
    }

	// 创建JavaModule注册表，把所有的 NativeModule 注册到 CatalystInstance ，将 Java 的可调用 API 暴露给 JS。
    NativeModuleRegistry nativeModuleRegistry = processPackages(reactContext, mPackages, false);

	// 异常处理器选择逻辑
    NativeModuleCallExceptionHandler exceptionHandler = mNativeModuleCallExceptionHandler != null
      ? mNativeModuleCallExceptionHandler
      : mDevSupportManager;
      
    // 核心逻辑， Builder 模式创建 CatalystInstance 实例，它是三端通信的管理类
    CatalystInstanceImpl.Builder catalystInstanceBuilder = new CatalystInstanceImpl.Builder()
      .setReactQueueConfigurationSpec(mUseSeparateUIBackgroundThread ?
        ReactQueueConfigurationSpec.createWithSeparateUIBackgroundThread() :
        ReactQueueConfigurationSpec.createDefault())
      .setJSExecutor(jsExecutor)// JS执行器
      .setRegistry(nativeModuleRegistry)// Java Module注册表
      .setJSBundleLoader(jsBundleLoader)// JS Bundle加载器
      .setNativeModuleCallExceptionHandler(exceptionHandler);// Java Exception处理器

    ReactMarker.logMarker(CREATE_CATALYST_INSTANCE_START);
    // CREATE_CATALYST_INSTANCE_END is in JSCExecutor.cpp
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "createCatalystInstance");
    
    final CatalystInstance catalystInstance;
    //构建CatalystInstance实例
    try {
      catalystInstance = catalystInstanceBuilder.build();
    } finally {
      Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
      ReactMarker.logMarker(CREATE_CATALYST_INSTANCE_END);
    }

    if (mBridgeIdleDebugListener != null) {
      catalystInstance.addBridgeIdleDebugListener(mBridgeIdleDebugListener);
    }
    if (Systrace.isTracing(TRACE_TAG_REACT_APPS | TRACE_TAG_REACT_JSC_CALLS)) {
      catalystInstance.setGlobalVariable("__RCTProfileIsProfiling", "true");
    }

	// 关联catalystInstance与reactContext
    reactContext.initializeWithInstance(catalystInstance);
    ReactMarker.logMarker(ReactMarkerConstants.PRE_RUN_JS_BUNDLE_START);
    
    // 加载执行JS Bundle
    catalystInstance.runJSBundle();

    return reactContext;
  }
```
**方法的两个入参**

在 recreateReactContextInBackgroundFromBundleLoader()传入

- **JavaScriptExecutor.Factory**：管理Webkit 的 JavaScriptCore，JS与C++的双向通信在这里中转
	- **JSCJavaScriptExecutor**，继承于JavaScriptExecutor。该类被加载时，它会自动去加载"reactnativejnifb.so"库，并会调用Native方 法initHybrid()初始化C++层RN与JSC**通信的框架**
- **JSBundleLoader**：bundle加载器，根据ReactNativeHost中的配置决定从哪里加载bundle文件，不同的场景会创建 不同的加载器，具体可以查看类JSBundleLoader
 - 缓存了JSBundle的信息，封装了上层加载JSBundle的相关接口，CatalystInstance通过其间接调用**ReactBridge**去加载JS文件。 

ReactContext**创建过程**中，主要做了以下3件事情：

- **构建ReactApplicationContext**对象(ReactContext的包装类)。
- **构建CatalystInstance**实例，作为以为三端通信的中枢。需要使用jsExecutor、nativeModuleRegistry、jsBundleLoader、exceptionHandler等参数。
- 调用CatalystInstance的runJSBundle()开始**加载执行JS**。

另一个重要的角色CatalystInstance出现了，它是三端通信的中枢。关于通信的具体实现我们会在接下来的通信机制小节来讲述，我们先来接着看JS的加载过程。

#### 创建NativeModuleRegistry

```java
  private NativeModuleRegistry processPackages(
    ReactApplicationContext reactContext,
    List<ReactPackage> packages,
    boolean checkAndUpdatePackageMembership) {
    NativeModuleRegistryBuilder nativeModuleRegistryBuilder = new NativeModuleRegistryBuilder(
      reactContext,
      this,
      mLazyNativeModulesEnabled);

    ReactMarker.logMarker(PROCESS_PACKAGES_START);

    // TODO(6818138): Solve use-case of native modules overriding
    for (ReactPackage reactPackage : packages) {
      if (checkAndUpdatePackageMembership && mPackages.contains(reactPackage)) {
        continue;
      }
      Systrace.beginSection(
        TRACE_TAG_REACT_JAVA_BRIDGE,
        "createAndProcessCustomReactPackage");
      try {
        if (checkAndUpdatePackageMembership) {
          mPackages.add(reactPackage);
        }
        processPackage(reactPackage, nativeModuleRegistryBuilder);
      } finally {
        Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
      }
    }
    ReactMarker.logMarker(PROCESS_PACKAGES_END);

    ReactMarker.logMarker(BUILD_NATIVE_MODULE_REGISTRY_START);
    Systrace.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "buildNativeModuleRegistry");
    NativeModuleRegistry nativeModuleRegistry;
    try {
      nativeModuleRegistry = nativeModuleRegistryBuilder.build();
    } finally {
      Systrace.endSection(TRACE_TAG_REACT_JAVA_BRIDGE);
      ReactMarker.logMarker(BUILD_NATIVE_MODULE_REGISTRY_END);
    }

    return nativeModuleRegistry;
  }

```
```java
  private void processPackage(
    ReactPackage reactPackage,
    NativeModuleRegistryBuilder nativeModuleRegistryBuilder) {
    SystraceMessage.beginSection(TRACE_TAG_REACT_JAVA_BRIDGE, "processPackage")
      .arg("className", reactPackage.getClass().getSimpleName())
      .flush();
    if (reactPackage instanceof ReactPackageLogger) {
      ((ReactPackageLogger) reactPackage).startProcessPackage();
    }
    nativeModuleRegistryBuilder.processPackage(reactPackage);

    if (reactPackage instanceof ReactPackageLogger) {
      ((ReactPackageLogger) reactPackage).endProcessPackage();
    }
    SystraceMessage.endSection(TRACE_TAG_REACT_JAVA_BRIDGE).flush();
  }
```
## 加载JS Bundle

### 创建CatalystInstance

#### CatalystInstance接口

```java
/**
 * A higher level API on top of the asynchronous JSC bridge. This provides an
 * environment allowing the invocation of JavaScript methods and lets a set of
 * Java APIs be invokable from JavaScript as well.
 */
@DoNotStrip
public interface CatalystInstance{}
异步JSC bridge 更高一层的API。提供JavaScript方法调用的环境，同时也使得一系列Java APIs可以被JavaScript调用
```
#### CatalystInstanceImpl

```java
/**
 * This provides an implementation of the public CatalystInstance instance.  It is public because
 * it is built by XReactInstanceManager which is in a different package.
 */
@DoNotStrip
public class CatalystInstanceImpl implements CatalystInstance {}
该类为public是因为它的实例是被另一个包的XReactInstanceManager类所创建
```

#### CatalystInstanceImpl类的构造函数

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
    mBridgeIdleListeners = new CopyOnWriteArrayList<>();
    mNativeModuleRegistry = nativeModuleRegistry;
    mJSModuleRegistry = new JavaScriptModuleRegistry();//创建JS Module注册表实例，老版本是在上面的createReactContext()方法中创建的
    mJSBundleLoader = jsBundleLoader;
    mNativeModuleCallExceptionHandler = nativeModuleCallExceptionHandler;
    mNativeModulesQueueThread = mReactQueueConfiguration.getNativeModulesQueueThread();
    mUIBackgroundQueueThread = mReactQueueConfiguration.getUIBackgroundQueueThread();
    mTraceListener = new JSProfilerTraceListener(this);

    Log.d(ReactConstants.TAG, "Initializing React Xplat Bridge before initializeBridge");
    //在C++层初始化通信桥
    initializeBridge(
      new BridgeCallback(this),
      jsExecutor,
      mReactQueueConfiguration.getJSQueueThread(),
      mNativeModulesQueueThread,
      mUIBackgroundQueueThread,
      mNativeModuleRegistry.getJavaModules(this),
      mNativeModuleRegistry.getCxxModules());
    Log.d(ReactConstants.TAG, "Initializing React Xplat Bridge after initializeBridge");
  }
```
构造函数的入参除了 ReactQueueConfigurationSpec，我们都已经了解过，我们来了解一下它

#### ReactQueueConfigurationSpec

```java
/**
 * Spec for creating a ReactQueueConfiguration. This exists so that CatalystInstance is able to
 * set Exception handlers on the MessageQueueThreads it uses and it would not be super clean if the
 * threads were configured, then passed to CatalystInstance where they are configured more. These
 * specs allows the Threads to be created fully configured.
 */
public class ReactQueueConfigurationSpec {
  private final @Nullable MessageQueueThreadSpec mUIBackgroundQueueThreadSpec;
  private final MessageQueueThreadSpec mNativeModulesQueueThreadSpec;
  private final MessageQueueThreadSpec mJSQueueThreadSpec;
}
创建ReactQueueConfiguration实例的Spec
就因为有Spec，CatalystInstance可以完全配置线程创建参数，比如可以设置它所使用的MessageQueueThreads的Exception handlers
三个MessageQueueThreadSpec类型的成员变量，分别记录三大线程(UI线程、Native线程与JS线程)的Spec
```

#### ReactQueueConfiguration接口

```java
/**
 * Specifies which {@link MessageQueueThread}s must be used to run the various contexts of
 * execution within catalyst (Main UI thread, native modules, and JS). Some of these queues *may* be
 * the same but should be coded against as if they are different.
 *
 * UI Queue Thread: The standard Android main UI thread and Looper. Not configurable.
 * Native Modules Queue Thread: The thread and Looper that native modules are invoked on.
 * JS Queue Thread: The thread and Looper that JS is executed on.
 */
public interface ReactQueueConfiguration {
  MessageQueueThread getUIQueueThread();
  @Nullable
  MessageQueueThread getUIBackgroundQueueThread();
  MessageQueueThread getNativeModulesQueueThread();
  MessageQueueThread getJSQueueThread();
  void destroy();
}
```

创建catalyst**三大线程**（必须的三个带消息队列的线程）：

- UI线程：Android的UI线程，处理和UI相关的事情。
- Native线程：主要是完成通信的工作。
- JS线程：主要完成JS的执行和渲染工作。

### 创建CatalystInstance总结

创建CatalystInstance对象时，主要做了两件事情：

- 创建三大线程：UI线程、Native线程与JS线程。
- 在C++层初始化通信桥。

### 加载 JS Bundle

加载 JS Bundle实际上是在C++层完成的，序列图如下(接 创建ReactContext序列图)

{% asset_img 加载JSBundle.png %}

注：JS Bundle有三种加载方式：

- setSourceURLs(String deviceURL, String remoteURL) ：从远程服务器加载。
- loadScriptFromAssets(AssetManager assetManager, String assetURL, boolean loadSynchronously)：从Assets文件夹加载。
- loadScriptFromFile(String fileName, String sourceURL, boolean loadSynchronously)：从文件路径加载。

从序列图上可以看出，真正加载执行JS的地方就是JSCExector.cpp的loadApplicationScript()方法。

至此，JS Bundle已经加载解析完成，进入MessageQueue.js开始执行。

## 绑定ReactContext与ReactRootView

JS Bundle加载完成以后，前面说的createReactContext()就执行完成了，然后开始执行setupReacContext()方法，绑定ReactContext与ReactRootView

### setupReactContext

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

	//将所有的ReactRootView与catalystInstance进行绑定
    ReactMarker.logMarker(ATTACH_MEASURED_ROOT_VIEWS_START);
    synchronized (mAttachedRootViews) {
      for (ReactRootView rootView : mAttachedRootViews) {
        attachRootViewToInstance(rootView, catalystInstance);
      }
    }
    ReactMarker.logMarker(ATTACH_MEASURED_ROOT_VIEWS_END);

    ReactInstanceEventListener[] listeners =
      new ReactInstanceEventListener[mReactInstanceEventListeners.size()];
    listeners = mReactInstanceEventListeners.toArray(listeners);
	//省略代码
  }
```

```java
  private void attachRootViewToInstance(
      final ReactRootView rootView,
      CatalystInstance catalystInstance) {
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

### setupReactContext总结

setupReactContext()主要完成每个ReactRootView与catalystInstance的绑定

绑定的过程主要做两件事情:

- 将ReactRootView作为根布局.
- 执行JS的页面入口.

### ReactRootView.runApplication

```java
  /**
   * Calls into JS to start the React application. Can be called multiple times with the
   * same rootTag, which will re-render the application from the root.
   * 调用JS开启application。使用同样的rootTag可以重复调用，每次调用都会从root重新渲染application
   */
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