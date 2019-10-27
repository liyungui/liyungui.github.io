---
title: CocosCreator生成项目的启动流程
date: 2019-10-21 11:17:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# 安卓的启动

AppActivity是启动Activity

## Activity.onCreate

1. Cocos2dxActivity.onCreate
	- 隐藏手机虚拟按键
	- 注册电量广播
	- 加载cocos2djs.so
	- new Cocos2dxHandler
	- Cocos2dxHelper.init()
		- nativeSetAudioDeviceInfo
		- nativeSetApkPath
	- CanvasRenderingContext2DImpl.init()
		- 注入 Context
	- Cocos2dxActivity.init()
		1. mFrameLayout = new RelativeLayout
		2. addSurfaceView，返回 renderer
			1. mGLSurfaceView = AppActivity.onCreateView() 
				1. new Cocos2dxGLSurfaceView()
				2. SDKWrapper.setGLSurfaceView()
					- SDKWrapper.loadSDKClass()
						- 读取project.json
						- serviceClassPath字段值
						- 赋值给sdkClasses
					- 遍历sdkClasses
					- 调用其setGLSurfaceView
				3. return glSurfaceView
			2. renderer = new Cocos2dxRenderer
			3. mGLSurfaceView.setCocos2dxRenderer
			4. mFrameLayout.addView(this.mGLSurfaceView);
			5. return renderer
		3. addDebugInfo
		4. setContentView(mFrameLayout);
	- new Cocos2dxVideoHelper
	- new Cocos2dxWebViewHelper
2. SDKWrapper.init
	- 遍历sdkClasses
	- 调用其init 

```java
public class AppActivity extends Cocos2dxActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        // Workaround in https://stackoverflow.com/questions/16283079/re-launch-of-activity-on-home-button-but-only-the-first-time/16447508
        if (!isTaskRoot()) {
            // Android launched another instance of the root activity into an existing task
            //  so just quietly finish and go away, dropping the user back into the activity
            //  at the top of the stack (ie: the last state of this task)
            // Don't need to finish it again since it's finished in super.onCreate .
            return;
        }
        // DO OTHER INITIALIZATION BELOW

        SDKWrapper.getInstance().init(this);
    }

    @Override
    public Cocos2dxGLSurfaceView onCreateView() {
        Cocos2dxGLSurfaceView glSurfaceView = new Cocos2dxGLSurfaceView(this);
        // TestCpp should create stencil buffer
        glSurfaceView.setEGLConfigChooser(5, 6, 5, 0, 16, 8);

        SDKWrapper.getInstance().setGLSurfaceView(glSurfaceView);

        return glSurfaceView;
    }
}    
```

```java
public abstract class Cocos2dxActivity extends Activity implements Cocos2dxHelperListener {
    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        Log.d(TAG, "Cocos2dxActivity onCreate: " + this + ", savedInstanceState: " + savedInstanceState);
        super.onCreate(savedInstanceState);

        Utils.setActivity(this);

        // Workaround in https://stackoverflow.com/questions/16283079/re-launch-of-activity-on-home-button-but-only-the-first-time/16447508
        if (!isTaskRoot()) {
            // Android launched another instance of the root activity into an existing task
            //  so just quietly finish and go away, dropping the user back into the activity
            //  at the top of the stack (ie: the last state of this task)
            finish();
            Log.w(TAG, "[Workaround] Ignore the activity started from icon!");
            return;
        }

        Utils.hideVirtualButton();

        Cocos2dxHelper.registerBatteryLevelReceiver(this);

        onLoadNativeLibraries();

        sContext = this;
        this.mHandler = new Cocos2dxHandler(this);
        
        Cocos2dxHelper.init(this);
        CanvasRenderingContext2DImpl.init(this);
        
        this.mGLContextAttrs = getGLContextAttrs();
        this.init();

        if (mVideoHelper == null) {
            mVideoHelper = new Cocos2dxVideoHelper(this, mFrameLayout);
        }

        if(mWebViewHelper == null){
            mWebViewHelper = new Cocos2dxWebViewHelper(mFrameLayout);
        }

        Window window = this.getWindow();
        window.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
        this.setVolumeControlStream(AudioManager.STREAM_MUSIC);
    }
    
    public void init() {
        ViewGroup.LayoutParams frameLayoutParams =
                new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT,
                                           ViewGroup.LayoutParams.MATCH_PARENT);
        mFrameLayout = new RelativeLayout(this);
        mFrameLayout.setLayoutParams(frameLayoutParams);

        Cocos2dxRenderer renderer = this.addSurfaceView();
        this.addDebugInfo(renderer);

        // Should create EditBox after adding SurfaceView, or EditBox will be hidden by SurfaceView.
        mEditBox = new Cocos2dxEditBox(this, mFrameLayout);

        // Set frame layout as the content view
        setContentView(mFrameLayout);
    }
    
    private Cocos2dxRenderer addSurfaceView() {
        this.mGLSurfaceView = this.onCreateView();
        this.mGLSurfaceView.setPreserveEGLContextOnPause(true);
        // Should set to transparent, or it will hide EditText
        // https://stackoverflow.com/questions/2978290/androids-edittext-is-hidden-when-the-virtual-keyboard-is-shown-and-a-surfacevie
        mGLSurfaceView.setBackgroundColor(Color.TRANSPARENT);
        // Switch to supported OpenGL (ARGB888) mode on emulator
        if (isAndroidEmulator())
            this.mGLSurfaceView.setEGLConfigChooser(8, 8, 8, 8, 16, 0);

        Cocos2dxRenderer renderer = new Cocos2dxRenderer();
        this.mGLSurfaceView.setCocos2dxRenderer(renderer);

        mFrameLayout.addView(this.mGLSurfaceView);

        return renderer;
    }
}
```

## GLSurfaceView.Renderer.onSurfaceCreated

- Cocos2dxRenderer.onSurfaceCreated
	- Cocos2dxRenderer. nativeInit
	- `JniImp.cpp nativeInit`
		1. main.cpp `cocos_android_app_init`
			- AppDelegate.cpp new AppDelegate(Application子类)
			- return g_app
		2. `CCApplication_android.cpp g_app->start();`
			- `AppDelegate.cpp applicationDidFinishLaunching`
				1. 创建ScriptEngine
				2. `jsb_register_all_modules`
				3. 启动ScriptEngine
				4. 加载脚本 `jsb-builtin.js`
				5. 加载脚本 `main.js`

```java
public class Cocos2dxRenderer implements GLSurfaceView.Renderer {
    @Override
    public void onSurfaceCreated(final GL10 GL10, final EGLConfig EGLConfig) {
        mNativeInitCompleted = false;
        Cocos2dxRenderer.nativeInit(this.mScreenWidth, this.mScreenHeight, mDefaultResourcePath);
        mOldNanoTime = System.nanoTime();
        this.mLastTickInNanoSeconds = System.nanoTime();
        mNativeInitCompleted = true;
        if (mGameEngineInitializedListener != null) {
            Cocos2dxHelper.getActivity().runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mGameEngineInitializedListener.onGameEngineInitialized();
                }
            });
        }
    }
    
    private static native void nativeInit(final int width, final int height, final String resourcePath);
}
```    

```cpp
//JniImp.cpp
    JNIEXPORT void JNICALL JNI_RENDER(nativeInit)(JNIEnv*  env, jobject thiz, jint w, jint h, jstring jDefaultResourcePath)
    {
        g_width = w;
        g_height = h;
        
        g_app = cocos_android_app_init(env, w, h);

        g_isGameFinished = false;
        ccInvalidateStateCache();
        std::string defaultResourcePath = JniHelper::jstring2string(jDefaultResourcePath);
        LOGD("nativeInit: %d, %d, %s", w, h, defaultResourcePath.c_str());
        

        if (!defaultResourcePath.empty())
            FileUtils::getInstance()->setDefaultResourceRootPath(defaultResourcePath);

        se::ScriptEngine* se = se::ScriptEngine::getInstance();
        se->addRegisterCallback(setCanvasCallback);

        EventDispatcher::init();

        g_app->start();
        g_isStarted = true;
    }
```

```cpp
//main.cpp
//called when onSurfaceCreated()
Application *cocos_android_app_init(JNIEnv *env, int width, int height)
{
    LOGD("cocos_android_app_init");
    auto app = new AppDelegate(width, height);
    return app;
}
```

```cpp
//CCApplication_android.cpp
void Application::start()
{
    if(!applicationDidFinishLaunching())
        return;
}
```

```cpp
//AppDelegate.cpp; cocos2d-x-lite/tools/simulator/frameworks/runtime-src/Classes/AppDelegate.cpp
bool AppDelegate::applicationDidFinishLaunching()
{
    se::ScriptEngine *se = se::ScriptEngine::getInstance();
    
    jsb_set_xxtea_key("fdc00166-0dea-4c");
    jsb_init_file_operation_delegate();
    
#if defined(COCOS2D_DEBUG) && (COCOS2D_DEBUG > 0)
    // Enable debugger here
    jsb_enable_debugger("0.0.0.0", 6086, false);
#endif
    
    se->setExceptionCallback([](const char *location, const char *message, const char *stack) {
        // Send exception information to server like Tencent Bugly.
    });
    
    jsb_register_all_modules();
    
    se->start();
    
    se::AutoHandleScope hs;
    jsb_run_script("jsb-adapter/jsb-builtin.js");
    jsb_run_script("main.js");
    
    se->addAfterCleanupHook([]() {
        JSBClassType::destroy();
    });
    
    return true;
}
```

### runScript


```cpp
// cocos/scripting/js-bindings/manual/jsb_global.cpp
bool jsb_run_script(const std::string& filePath, se::Value* rval/* = nullptr */)
{
    se::AutoHandleScope hs;
    return se::ScriptEngine::getInstance()->runScript(filePath, rval);
}
```

```cpp
// cocos/scripting/js-bindings/jswrapper/v8/ScriptEngine.hpp
bool ScriptEngine::runScript(const std::string& path, Value* ret/* = nullptr */)
{
    assert(!path.empty());
    assert(_fileOperationDelegate.isValid());

    std::string scriptBuffer = _fileOperationDelegate.onGetStringFromFile(path);

    if (!scriptBuffer.empty())
    {
        return evalString(scriptBuffer.c_str(), scriptBuffer.length(), ret, path.c_str());
    }

    SE_LOGE("ScriptEngine::runScript script %s, buffer is empty!\n", path.c_str());
    return false;
}
```

```cpp

void jsb_init_file_operation_delegate()
{
    static se::ScriptEngine::FileOperationDelegate delegate;
    if (!delegate.isValid())
    {
        delegate.onGetStringFromFile = [](const std::string& path) -> std::string{
            assert(!path.empty());
				
			// 优先读取字节码文件。将文件后缀名js改为jsc就是字节码文件路径
            std::string byteCodePath = removeFileExt(path) + BYTE_CODE_FILE_EXT;
            if (FileUtils::getInstance()->isFileExist(byteCodePath)) {
                Data fileData = FileUtils::getInstance()->getDataFromFile(byteCodePath);
                ...
            }
            if (FileUtils::getInstance()->isFileExist(path)) {
                return FileUtils::getInstance()->getStringFromFile(path);
            }
            else {
                SE_LOGE("ScriptEngine::onGetStringFromFile %s not found, possible missing file.\n", path.c_str());
            }
            return "";
        };

        assert(delegate.isValid());

        se::ScriptEngine::getInstance()->setFileOperationDelegate(delegate);
    }
}
```

```cpp
// cocos/platform/CCFileUtils.cpp
std::string FileUtils::getStringFromFile(const std::string& filename)
{
    std::string s;
    getContents(filename, &s);
    return s;
}

FileUtils::Status FileUtils::getContents(const std::string& filename, ResizableBuffer* buffer)
{
    if (filename.empty())
        return Status::NotExists;

    auto fs = FileUtils::getInstance();

    std::string fullPath = fs->fullPathForFilename(filename);
    if (fullPath.empty())
        return Status::NotExists;

    FILE *fp = fopen(fs->getSuitableFOpen(fullPath).c_str(), "rb");
    if (!fp)
        return Status::OpenFailed;

#if defined(_MSC_VER)
    auto descriptor = _fileno(fp);
#else
    auto descriptor = fileno(fp);
#endif
    struct stat statBuf;
    if (fstat(descriptor, &statBuf) == -1) {
        fclose(fp);
        return Status::ReadFailed;
    }
    size_t size = statBuf.st_size;

    buffer->resize(size);
    size_t readsize = fread(buffer->buffer(), 1, size, fp);
    fclose(fp);

    if (readsize < size) {
        buffer->resize(readsize);
        return Status::ReadFailed;
    }

    return Status::OK;
}

std::string FileUtils::fullPathForFilename(const std::string &filename) const
{
    if (filename.empty())
    {
        return "";
    }

    if (isAbsolutePath(filename))
    {
        return normalizePath(filename);
    }

    // Already Cached ?
    auto cacheIter = _fullPathCache.find(filename);
    if(cacheIter != _fullPathCache.end())
    {
        return cacheIter->second;
    }

    // Get the new file name.
    const std::string newFilename( getNewFilename(filename) );

    std::string fullpath;

    for (const auto& searchIt : _searchPathArray)
    {
        for (const auto& resolutionIt : _searchResolutionsOrderArray)
        {
            fullpath = this->getPathForFilename(newFilename, resolutionIt, searchIt);

            if (!fullpath.empty())
            {
                // Using the filename passed in as key.
                _fullPathCache.insert(std::make_pair(filename, fullpath));
                return fullpath;
            }
        }
    }

    if(isPopupNotify()){
        CCLOG("fullPathForFilename: No file found at %s. Possible missing file.", filename.c_str());
    }

    // The file wasn't found, return empty string.
    return "";
}
```

最终调用了 `fullPathForFilename` ，根据文件名获取完整路径。需要注意的是为了优化性能，`_fullPathCache` 会缓存已经搜索过的文件名的完整路径。

而 `addSearchPath` API并没有情况这个缓存，会造成添加了搜索路径却无法使用新路径的bug。 推荐使用 `setSearchPaths`这个AP，会清空缓存；或者`addSearchPath` 后手动清空 `_fullPathCache`
    

# 时序图

{% asset_img 初始化序列图.png %} 

# main.js

每个项目都会生成一个 main.js 文件。Cocos Creator 默认link 方式生成的项目位于 `build/jsb-link/main.js`


Cocos 通过加载 main.js 启动游戏

```js
//main.js 
if (false) {
    ...
    window.boot();
}
else if (window.jsb) {

    var isRuntime = (typeof loadRuntime === 'function');
    if (isRuntime) {
        require('src/settings.79e2c.js');
        require('src/cocos2d-runtime.js');
        require('jsb-adapter/engine/index.js');
    }
    else {
        require('src/settings.79e2c.js');
        require('src/cocos2d-jsb.b6bb9.js');
        require('jsb-adapter/jsb-engine.js');
    }

    cc.macro.CLEANUP_IMAGE_CACHE = true;
    window.boot();
}
```

## window.boot()

```js
window.boot = function () {
	//settings是在上面加载的 settings.79e2c.js 中的设置
    var settings = window._CCSettings;
    window._CCSettings = undefined;

	//处理settings
    if ( !settings.debug ) {
    	//省略了各配置项遍历处理的逻辑
        var uuids = settings.uuids;
        var rawAssets = settings.rawAssets;
        var assetTypes = settings.assetTypes;
        var realRawAssets = settings.rawAssets = {};
        var scenes = settings.scenes;
        var packedAssets = settings.packedAssets;
        var subpackages = settings.subpackages;
    }
    
    //设置闪屏(场景加载中的背景)
    function setLoadingDisplay () {
        // Loading splash scene
        var splash = document.getElementById('splash');
        var progressBar = splash.querySelector('.progress-bar span');
        cc.loader.onProgress = function (completedCount, totalCount, item) {
            var percent = 100 * completedCount / totalCount;
            if (progressBar) {
                progressBar.style.width = percent.toFixed(2) + '%';
            }
        };
        splash.style.display = 'block';
        progressBar.style.width = '0%';

        cc.director.once(cc.Director.EVENT_AFTER_SCENE_LAUNCH, function () {
            splash.style.display = 'none';
        });
    }

	//游戏开始时的回调，通过内部定义的loadScene函数加载初始化场景(settings 设置的)
    var onStart = function () {
        cc.loader.downloader._subpackages = settings.subpackages;

        cc.view.enableRetina(true);
        cc.view.resizeWithBrowserSize(true);

        if (!false && !false) {
            if (cc.sys.isBrowser) {
                setLoadingDisplay();
            }

            if (cc.sys.isMobile) {
                if (settings.orientation === 'landscape') {
                    cc.view.setOrientation(cc.macro.ORIENTATION_LANDSCAPE);
                }
                else if (settings.orientation === 'portrait') {
                    cc.view.setOrientation(cc.macro.ORIENTATION_PORTRAIT);
                }
                cc.view.enableAutoFullScreen([
                    cc.sys.BROWSER_TYPE_BAIDU,
                    cc.sys.BROWSER_TYPE_WECHAT,
                    cc.sys.BROWSER_TYPE_MOBILE_QQ,
                    cc.sys.BROWSER_TYPE_MIUI,
                ].indexOf(cc.sys.browserType) < 0);
            }

            // Limit downloading max concurrent task to 2,
            // more tasks simultaneously may cause performance draw back on some android system / browsers.
            // You can adjust the number based on your own test result, you have to set it before any loading process to take effect.
            if (cc.sys.isBrowser && cc.sys.os === cc.sys.OS_ANDROID) {
                cc.macro.DOWNLOAD_MAX_CONCURRENT = 2;
            }
        }

        function loadScene(launchScene) {
            cc.director.loadScene(launchScene,
                function (err) {
                    if (!err) {
                        if (cc.sys.isBrowser) {
                            // show canvas
                            var canvas = document.getElementById('GameCanvas');
                            canvas.style.visibility = '';
                            var div = document.getElementById('GameDiv');
                            if (div) {
                                div.style.backgroundImage = '';
                            }
                        }
                        cc.loader.onProgress = null;
                        console.log('Success to load scene: ' + launchScene);
                    }
                    else if (CC_BUILD) {
                        setTimeout(function () {
                            loadScene(launchScene);
                        }, 1000);
                    }
                }
            );

        }

        var launchScene = settings.launchScene;

        // load scene
        loadScene(launchScene);

    };

    // jsList；工程内的 js文件列表
    var jsList = settings.jsList;
 	
	//游戏运行选项 
     var option = {
        id: 'GameCanvas',
        scenes: settings.scenes,
        debugMode: settings.debug ? cc.debug.DebugMode.INFO : cc.debug.DebugMode.ERROR,
        showFPS: !false && settings.debug,
        frameRate: 60,
        jsList: jsList,
        groupList: settings.groupList,
        collisionMatrix: settings.collisionMatrix,
    }

    // init assets
    cc.AssetLibrary.init({
        libraryPath: 'res/import',
        rawAssetsBase: 'res/raw-',
        rawAssets: settings.rawAssets,
        packedAssets: settings.packedAssets,
        md5AssetsMap: settings.md5AssetsMap,
        subpackages: settings.subpackages
    });

	//核心代码：开始游戏
    cc.game.run(option, onStart);
};
```

# CCGame.js

位于 `js引擎/cocos2d/core/CCGame.js`，[Github链接](https://github.com/cocos-creator/engine/blob/44d068bea8120146521ec334827cb5b67a7d9b8f/cocos2d/core/CCGame.js)

`CCGame.js`编译后会复制到 `build/jsb-link/src/cocos2d-jsb.b6bb9.js`

包含游戏主体信息并负责驱动游戏的游戏对象

## cc.game.run()

```js
//CCGame.js

/**
 * @module cc
 */

/**
 * !#en An object to boot the game.
 * !#zh 包含游戏主体信息并负责驱动游戏的游戏对象。
 * @class game
 * @static
 * @extends EventTarget
 */
var game = {
	...
	
    /**
     * !#en Run game with configuration object and onStart function.
     * !#zh 运行游戏，并且指定引擎配置和 onStart 的回调。
     * @method run
     * @param {Object} config - Pass configuration object or onStart function
     * @param {Function} onStart - function to be executed after game initialized
     */
    run: function (config, onStart) {
        this._initConfig(config);
        this.onStart = onStart;
        this.prepare(game.onStart && game.onStart.bind(game));
    },

...    
};

EventTarget.call(game);
cc.js.addon(game, EventTarget.prototype);

/**
 * @property game
 * @type Game
 */
cc.game = module.exports = game; // 将这个模块导出到 cc.game   
```

## prepare(cb)

```js
    /**
     * !#en Prepare game.
     * !#zh 准备引擎，请不要直接调用这个函数。
     * @param {Function} cb
     * @method prepare
     */
    prepare (cb) {
        // Already prepared
        if (this._prepared) {
            if (cb) cb();
            return;
        }

        // Load game scripts
        let jsList = this.config.jsList;
        if (jsList && jsList.length > 0) {
            var self = this;
            cc.loader.load(jsList, function (err) {
                if (err) throw new Error(JSON.stringify(err));
                self._prepareFinished(cb);
            });
        }
        else {
            this._prepareFinished(cb);
        }
    },
```

通过 loader把配置的 jsList 全部 加载进来。

然后执行 准备结束函数 _prepareFinished

## _prepareFinished(cb)

```js
    _prepareFinished (cb) {
        this._prepared = true;

        // Init engine
        this._initEngine();
        // Log engine version
        console.log('Cocos Creator v' + cc.ENGINE_VERSION);

        this._setAnimFrame();// 设置动画帧频率
        this._runMainLoop();

        this.emit(this.EVENT_GAME_INITED);

        if (cb) cb();
    }, 
```

## _initEngine()

```js
    
    _initEngine () {
        if (this._rendererInitialized) {
            return;
        }

        this._initRenderer();// 初始化 渲染相关

        if (!CC_EDITOR) {
            this._initEvents();
        }

        this.emit(this.EVENT_ENGINE_INITED);
    }, 
```

## _runMainLoop

```js
    //Run game.
    _runMainLoop: function () {
        var self = this, callback, config = self.config,
            director = cc.director,
            skip = true, frameRate = config.frameRate;

        debug.setDisplayStats(config.showFPS);

        callback = function () {
            if (!self._paused) {
                self._intervalId = window.requestAnimFrame(callback);
                if (frameRate === 30) {
                    if (skip = !skip) {
                        return;
                    }
                }
                director.mainLoop();
            }
        };

        self._intervalId = window.requestAnimFrame(callback);
        self._paused = false;
    },
```    

`cc.director.mainLoop();` 开始游戏
 
# CCDirector.js

位于 `js引擎/cocos2d/core/CCDirector.js`，[Github链接](https://github.com/cocos-creator/engine/blob/44d068bea8120146521ec334827cb5b67a7d9b8f/cocos2d/core/CCDirector.js)

`CCDirector.js`编译后会复制到 `build/jsb-link/src/cocos2d-jsb.b6bb9.js`
   
`cocos/base/CCDirector.cpp`  [Github链接](https://github.com/cocos-creator/cocos2d-x-lite/blob/1.6.1/cocos/base/CCDirector.cpp) 查看发版记录可知是2.0版本移除了这个文件

cc.director 一个管理你的游戏的逻辑流程的单例对象。

负责创建和处理主窗口并且管理什么时候执行场景

同步定时器与显示器的刷新速率

还负责

- 初始化 OpenGL 环境。<br/>
- 设置OpenGL像素格式。(默认是 RGB565)<br/>
- 设置OpenGL缓冲区深度 (默认是 0-bit)<br/>
- 设置空白场景的颜色 (默认是 黑色)<br/>
- 设置投影 (默认是 3D)<br/>
- 设置方向 (默认是 Portrait)<br/>

# 参考&扩展

- [CocosCreator生成项目的启动流程](https://gowa.club/Cocos-Creator/Cocos%20Creator%E7%94%9F%E6%88%90%E9%A1%B9%E7%9B%AE%E7%9A%84%E5%90%AF%E5%8A%A8%E5%B7%A5%E4%BD%9C%E6%B5%81%E7%A8%8B.html#initEngine)
- [Cocos Creator 之旅](http://www.supersuraccoon-cocos2d.com/cocos_creator/cocos_creator.html) 比较Cocos Creator v1.2 和Cocos2d，以及Creator为了实现 基于组件的实体系统开发模式 而对Cocos2d的改造