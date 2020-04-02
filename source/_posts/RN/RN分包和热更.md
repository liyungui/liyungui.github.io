---
title: RN分包和热更
date: 2020-03-20 17:41:12
tags: 
	- RN
---

# 官方metro分包方案

本文RN版本是 `0.61.2`，使用基于metro分包的三方框架 `react-native-multibundler`

优势：

- 稳定
- 灵活
	- 支持debug
	- 支持远程加载
	- 可以每个页面作为一个业务包
	- 可选模块路径或者递增id作为模块id

# 加载bundle

## 基础包

```java
ReactInstanceManagerBuilder builder = ReactInstanceManager.builder()
if (jsBundleFile != null) {//本地文件存在
	builder.setJSBundleFile(jsBundleFile);
} else {
	builder.setBundleAssetName(getBundleAssetName());
}
```

## 业务包

```java
private void loadScriptAsync(final ReactRootView reactRootView, final String moduleName) {
	String moduleFileName = getModuleFileNameByModuleName(moduleName);
	if (sd卡的版本最新) {
	    String rnBundleFilePath = getRNBundleFilePath(moduleFileName);
	    loadScriptFromFile(mReactInstanceManager, rnBundleFilePath, rnBundleFilePath);
	} else {
	    String moduleBundleAssertsPath = getRNBundleAssertsPath(moduleFileName);
	    loadScriptFromAssets(mReactInstanceManager, getAssetManager(), moduleBundleAssertsPath);
	}
                        
	//切换到UI线程，展示业务页面
	reactRootView.startReactApplication(mReactInstanceManager, moduleName, null);                      
}

@WorkerThread
public static void loadScriptFromFile(ReactInstanceManager reactInstanceManager, String fileName, String sourceURL) {
    CatalystInstance catalystInstance = reactInstanceManager.getCurrentReactContext().getCatalystInstance();
    try {
        Method method = CatalystInstanceImpl.class.getDeclaredMethod("loadScriptFromFile",
            String.class,
            String.class, boolean.class);
        method.setAccessible(true);
        method.invoke(catalystInstance, fileName, sourceURL, false);
    } catch (Exception e) {
        e.printStackTrace();
    }
}

@WorkerThread
public static void loadScriptFromAssets(ReactInstanceManager reactInstanceManager, AssetManager assetManager, String assetName) {
    CatalystInstance catalystInstance = reactInstanceManager.getCurrentReactContext().getCatalystInstance();
    try {
        String source = "assets://" + assetName;
        Method method = CatalystInstanceImpl.class.getDeclaredMethod("loadScriptFromAssets",
            AssetManager.class,
            String.class, boolean.class);
        method.setAccessible(true);
        method.invoke(catalystInstance, assetManager, source, false);
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```
    
# 代码bundle热更

有两种方案：

- 重启
	- 重新初始化ReactInstanceManager 
- 反射修改ReactInstanceManager的JSBundleLoader，然后重建ReactContext
	- recreateReactContextInBackground不行
		- 因为里面的JSBundleLoader已经初始化好了
		- 没有开放更新的方法，所以只能用反射了

```java
//反射重新设置BundleLoader
try {
    JSBundleLoader jSBundleLoader;
    if (jSBundleFile.toLowerCase().startsWith("assets://")) {
        jSBundleLoader = JSBundleLoader.createAssetLoader(getReactApplicationContext(), jSBundleFile, false);
    } else {
        jSBundleLoader = JSBundleLoader.createFileLoader(jSBundleFile);
    }
    Field bundleLoaderField = instanceManager.getClass().getDeclaredField("mBundleLoader");
    bundleLoaderField.setAccessible(true);
    bundleLoaderField.set(instanceManager, jSBundleLoader);
} catch (Exception e) {
    Log.i("lyg", "Could not setJSBundle");
}

//重新创建
try {
	instanceManager.recreateReactContextInBackground();
} catch (Exception e) {
    // 重新创建失败；尝试重启Activity
    currentActivity.runOnUiThread(new Runnable() {
	    @Override
	    public void run() {
	        currentActivity.recreate();
	    }
	});
}
```

```java
//或者直接反射调用带参的recreateReactContextInBackground
try {
    Class<?> RIManagerClazz = mReactInstanceManager.getClass();
    Method method = RIManagerClazz.getDeclaredMethod("recreateReactContextInBackground",
            JavaScriptExecutorFactory.class,
            JSBundleLoader.class);
    method.setAccessible(true);
    method.invoke(mReactInstanceManager,
            new JSCJavaScriptExecutorFactory("", ""),
            JSBundleLoader.createFileLoader(JS_BUNDLE_LOCAL_PATH));
} catch (Exception e) {
    e.printStackTrace();
}
```

# 图片资源热更

RN热更必不可少的要面对RN中图片的热更新

先探究一下React-Native中图片是如何加载的，搞懂了这个问题，图片的热更新问题也就迎刃而解

## Image设置图片

RN中图片一般是这样使用的

`<Image source={require('js/assets/common/ic_phone_kefu.png');} />`

重点关注Image控件属性source，所谓的图片热更新也就是更换source的地址

## 图片资源打包

```js
react-native/Libraries/Image/assetPathUtils.js

function getAndroidResourceIdentifier(asset: PackagerAsset): string {
  var folderPath = getBasePath(asset); //去掉/(如果以/打头)
  return (folderPath + '/' + asset.name)
    .toLowerCase()
    .replace(/\//g, '_') // Encode folder structure in file name
    .replace(/([^a-z0-9_])/g, '') // Remove illegal chars
    .replace(/^assets_/, ''); // Remove "assets_" prefix
}
```

打包处理：转小写，文件路径用 `_`连接，去除非法字符，去除开头 `assets_`(如果是这个开头)

图片被处理成了 `js_assets_common_ic_phone_kefu.png`

## 加载过程分析

### Image.android.js

```js
react-native/Libraries/Image/Image.android.js

let Image = (
  props: ImagePropsType,
  forwardedRef: ?React.Ref<'RCTTextInlineImage' | 'ImageViewNativeComponent'>,
) => {
  //设置source；重点关注，图片路径处理逻辑在里面完成
  let source = resolveAssetSource(props.source);
  const defaultSource = resolveAssetSource(props.defaultSource);
  const loadingIndicatorSource = resolveAssetSource(
    props.loadingIndicatorSource,
  );
  ...检查source、props.src属性...
  if (source && !source.uri && !Array.isArray(source)) {
    source = null;
  }

  //根据source.uri 设置sources
  let style;
  let sources;
  if (source?.uri != null) {
    sources = [{uri: source.uri}];
  } else {
    style = flattenStyle([styles.base, props.style]);
    sources = source;
  }

  //合并属性
  const {onLoadStart, onLoad, onLoadEnd, onError} = props;
  const nativeProps = merge(props, {
    style,
    shouldNotifyLoadEvents: !!(onLoadStart || onLoad || onLoadEnd || onError),
    src: sources,
    headers: source?.headers,
    defaultSrc: defaultSource ? defaultSource.uri : null,
    loadingIndicatorSrc: loadingIndicatorSource
      ? loadingIndicatorSource.uri
      : null,
    ref: forwardedRef,
  });

  //返回真正的图片实现类
  return (
    <TextAncestor.Consumer>
      {hasTextAncestor =>
        hasTextAncestor ? (
          <TextInlineImageNativeComponent {...nativeProps} />
        ) : (
          <ImageViewNativeComponent {...nativeProps} />
        )
      }
    </TextAncestor.Consumer>
  );
};
```

### ImageViewNativeComponent.js

通过上面的分析可知，如果父路径没有文本，Image真正的图片实现类是 ImageViewNativeComponent 

合并属性后生成nativeProps对象，传递给了 ImageViewNativeComponent

```js
react-native/Libraries/Image/ImageViewNativeComponent.js

const ImageViewNativeComponent: string = requireNativeComponent('RCTImageView');
```

### ReactImageManager.java

继续跟踪，通过 `ReactImageManager.java`，可知 `RCTImageView` 对应的是 `ReactImageView`

```java
ReactImageView.java

  @Override
  public ReactImageView createViewInstance(ThemedReactContext context) {
    return new ReactImageView(
        context, getDraweeControllerBuilder(), mGlobalImageLoadListener, getCallerContext());
  }
  
  // In JS this is Image.props.source
  @ReactProp(name = "src")
  public void setSource(ReactImageView view, @Nullable ReadableArray sources) {
    view.setSource(sources);
  }
```

setSource的文档说明，这里是原封不动的传递了JS中`Image.props.source` 属性，我们**需要回头到JS代码中去分析图片路径的处理逻辑**

### resolveAssetSource.js

现在我们回头分析 resolveAssetSource

```js
react-native/Libraries/Image/resolveAssetSource.js

function resolveAssetSource(source: any): ?ResolvedAssetSource {
  //已经处理成对象了，直接返回
  if (typeof source === 'object') {
    return source;
  }
 
  //获取图片id，rn会对所有图片编码索引
  const asset = AssetRegistry.getAssetByID(source);
  if (!asset) {
    return null;
  }
  
  //关注核心代码
  const resolver = new AssetSourceResolver(
    getDevServerURL(),
    getScriptURL(),
    asset,
  );
  if (_customSourceTransformer) {
    return _customSourceTransformer(resolver);
  }
  return resolver.defaultAsset();
}
```

#### 获取当前js源码路径地址

```js
let _sourceCodeScriptURL: ?string;
function getSourceCodeScriptURL(): ?string {
  if (_sourceCodeScriptURL) {
    return _sourceCodeScriptURL;
  }

  let sourceCode =
    global.nativeExtensions && global.nativeExtensions.SourceCode;
  if (!sourceCode) {
    sourceCode = require('../NativeModules/specs/NativeSourceCode').default;
  }
  _sourceCodeScriptURL = sourceCode.getConstants().scriptURL;
  return _sourceCodeScriptURL;
}
```

通过 `NativeSourceCode.js` 获取到当前js源码路径地址

#### 服务器地址父路径

```js
function getDevServerURL(): ?string {
  if (_serverURL === undefined) {
    const sourceCodeScriptURL = getSourceCodeScriptURL();
    const match =
      sourceCodeScriptURL && sourceCodeScriptURL.match(/^https?:\/\/.*?\//);
    if (match) {
      // jsBundle was loaded from network
      _serverURL = match[0];
    } else {
      // jsBundle was loaded from file
      _serverURL = null;
    }
  }
  return _serverURL;
}
```

通过js源码路径地址判断js是来自网络还是本地，网络返回网络地址父路径，本地返回null

#### js脚本地址父路径

```js
function _coerceLocalScriptURL(scriptURL: ?string): ?string {
  if (scriptURL) {
    if (scriptURL.startsWith('assets://')) {
      // android: running from within assets, no offline path to use
      return null;
    }
    scriptURL = scriptURL.substring(0, scriptURL.lastIndexOf('/') + 1);
    if (!scriptURL.includes('://')) {
      // Add file protocol in case we have an absolute file path and not a URL.
      // This shouldn't really be necessary. scriptURL should be a URL.
      scriptURL = 'file://' + scriptURL;
    }
  }
  return scriptURL;
}

function getScriptURL(): ?string {
  if (_scriptURL === undefined) {
    _scriptURL = _coerceLocalScriptURL(getSourceCodeScriptURL());
  }
  return _scriptURL;
}
```

通过js源码路径地址判断js是否来自assets目录，是返回null，否返回js上级目录地址（没有`file://`前缀，代码会补上）

### AssetSourceResolver.js

真正处理图片地址 

```js
react-native/Libraries/Image/AssetSourceResolver.js

  defaultAsset(): ResolvedAssetSource {
    if (this.isLoadedFromServer()) {//服务器地址不为空
      return this.assetServerURL();
    }

    //Android，js从assets加载，返回R文件中图片
    //js从本地加载，使用drawableFolderInBundle从bundle目录下获取图片
    if (Platform.OS === 'android') {
      return this.isLoadedFromFileSystem()
        ? this.drawableFolderInBundle()
        : this.resourceIdentifierWithoutScale();
    } else {
      return this.scaledAssetURLNearBundle();
    }
  }
  
  //从本地bundle目录下获取图片
  drawableFolderInBundle(): ResolvedAssetSource {
    const path = this.jsbundleUrl || 'file://';
    return this.fromSource(path + getAssetPathInDrawableFolder(this.asset));
  }
```

### 总结

如果是从本地文件加载的js代码(例如 `/sdcard/rn/LiveShoppingMall.js`)，那么加载图片的地址就是 **js文件同级目录下** `/sdcard/rn/drawable-xhpi/js_assets_common_ic_phone_kefu.png`

## SmartAssets对图片路径的hook

`react-native-smartassets`

### 缺陷

上面的图片处理过程有个缺陷（不够**高效和灵活**），就是如果js代码同级目录下找不到目标图片，是展示不出来的。这就意味着，一个页面如果热更，需要把这个页面所有图片都拷贝js文件同级目录下。如果每个业务包都有独立文件夹（方便配置版本控制和安全策略），这个重复拷贝工作量很恐怖的

### 解决方案

通过hook上面的 `AssetSourceResolver.js` 获取图片路径的方法，判断js代码父路径下是否存在目标图片，不存在(表示图片不需要更新)则使用R文件中的图片，完美

```js
react-native-smartassets/index.js

	var SmartAssets= {
	initSmartAssets(){
		var initialize = _.once(this.initSmartAssetsInner);
		initialize();
	},
	initSmartAssetsInner() {
		let drawablePathInfos = [];
		//getSourceCodeScriptURL()获取js文件地址
		//完全复制resolveAssetSource.js. 
		//调用Java方法遍历js文件同级的图片文件，存入数组
		Smartassets.travelDrawable(getSourceCodeScriptURL(),
			(retArray)=>{
				drawablePathInfos = drawablePathInfos.concat(retArray);
			});
		
		//核心，hook AssetSourceResolver.defaultAsset方法
		AssetSourceResolver.prototype.defaultAsset=_.wrap(AssetSourceResolver.prototype.defaultAsset, function (func, ...args) {
			if (this.isLoadedFromServer()) {
				return this.assetServerURL();
			}
			if (Platform.OS === 'android') {
				if(this.isLoadedFromFileSystem()||bundlePath!=null){//begin assets ios begin drawable android
					this.jsbundleUrl = bundlePath;
					let resolvedAssetSource = this.drawableFolderInBundle();
					let resPath = resolvedAssetSource.uri;
					if(drawablePathInfos.includes(resPath)){//已经在bundle目录中有
						return resolvedAssetSource;
					}
					let isFileExist =  Smartassets.isFileExist(resPath);
					if(isFileExist===true){//文件存在
						return resolvedAssetSource;
					}else {//不存在，使用R文件的图片
						return this.resourceIdentifierWithoutScale();
					}
				}else {
					return this.resourceIdentifierWithoutScale();
				}
			} else {//ios的处理
				if(bundlePath!=null){
					this.jsbundleUrl = bundlePath;
				}
				let iOSAsset = this.scaledAssetURLNearBundle();
				let isFileExist =  Smartassets.isFileExist(iOSAsset.uri);
				if(isFileExist) {
					return iOSAsset;
				}else{
					let oriJsBundleUrl = 'file://'+defaultMainBundePath+'/'+iOSRelateMainBundlePath;
					iOSAsset.uri = iOSAsset.uri.replace(this.jsbundleUrl, oriJsBundleUrl);
					return iOSAsset;
				}
			}
		});
	},
	//必须传入js文件的父路径
	//否则会导致一个图片路径bug
	setBundlePath(bundlePathNew){
		bundlePath = bundlePathNew;
	},
	setiOSRelateMainBundlePath(relatePath){
		iOSRelateMainBundlePath = relatePath;
	}
}
```

### setBundlePath传参

**特别注意** setBundlePath传参形式不当，会导致图片路径bug

js文件地址：`/sdcard/rn/LiveShoppingMall.js`

setBundlePath **唯一标准参数**：`file:///sdcard/rn/`（js文件父路径，必须file://前缀，以/结尾）

如果setBundlePath传入js文件的路径(而不是期望的js文件父路径，并以/结尾)，那么加载图片的地址就是 **js文件 + 图片地址** `/sdcard/rn/LiveShoppingMall.jsdrawable-xhpi/js_assets_common_ic_phone_kefu.png`

setBundlePath是怎么调用的呢

在框架提供的基础包打包入口文件 `platformDep.js`中，监听了 `sm-bundle-changed` 事件来触发调用

```js
import { SmartAssets } from 'react-native-smartassets';
SmartAssets.initSmartAssets();
DeviceEventEmitter.addListener('sm-bundle-changed', 
    bundlePath => {
        SmartAssets.setBundlePath(bundlePath);
    });
```

所以，我们需要在java代码中发送这个事件

```java
if(scriptPath!=null){//scriptPath是js完整路径
    scriptPath = "file://"+scriptPath.substring(0,scriptPath.lastIndexOf(File.separator)+1);
reactContext
        .getJSModule(DeviceEventManagerModule.RCTDeviceEventEmitter.class)
        .emit("sm-bundle-changed", bundleAssetPath);    
}
```

# 参考&扩展

- [react-native-multibundler](https://github.com/smallnew/react-native-multibundler)