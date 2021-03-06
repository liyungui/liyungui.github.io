---
title: RN第一个实例
date: 2018-05-17 11:25:12
tags: 
	- RN
---

RN版本 `0.48.4`

# RN工程结构

新建的RN工程结构如下

- android/: 
	- Android 原生代码目录，主要用于原生库、原生View的编写桥接、以及 ReactNative 第三方库的 link。
- ios/: 
	- iOS 原生代码目录，主要用于原生库、原生View的编写桥接、以及 ReactNative 第三方库的 link。
- index.js: 
	- RN项目的**入口**文件。
- package.json: 
	- npm 的包管理文件
	- 功能类似 Android 的 gradle，iOS 的 cocoaPods。
	- 说明了RN项目的名称，版本号，依赖等
	- NodeJS相关的目录
- node_modules/: 
	- npm install 命令node解析package.json **下载生成**的相关依赖
	- NodeJS相关的目录

如果搭建了 typescript 开发环境：

- tsconfig.json: 
	- typescript 环境配置文件。
- src/: 
	- typescript 搭建环境时新建目录，用于存放编写的 ts 代码。
- lib/: 
	- 执行 tsc 脚本后，根据已有 ts 代码，编译成的 js 代码目录，也是代码运行时的目录，即运行时代码都指向 lib 文件夹。

# 代码流程

## JS

新版本(0.49以上) `app.js`；老版本 `index.android.js`

```js
import React, { Component } from 'react';
import {
  AppRegistry,
  StyleSheet,
  Text,
  View
} from 'react-native';

export default class AwesomeProject extends Component {
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.welcome}>
          Welcome to React Native!
        </Text>
        <Text style={styles.instructions}>
          To get started, edit index.android.js
        </Text>
        <Text style={styles.instructions}>
          Double tap R on your keyboard to reload,{'\n'}
          Shake or press menu button for dev menu
        </Text>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

AppRegistry.registerComponent('AwesomeProject', () => AwesomeProject);
```

主要是四个部分

- import 导入依赖
- 定义 Component
- 创建样式 StyleSheet
- 注册Component `AppRegistry.registerComponent()`

```js
export namespace AppRegistry {
   function registerComponent(appKey: string, getComponentFunc: ComponentProvider): string;
}
```

## Native

```java
public class MainApplication extends Application implements ReactApplication {

  /**
   * ReactApplication接口唯一方法。Get the default {@link ReactNativeHost} for this app.
   */
  @Override
  public ReactNativeHost getReactNativeHost() {
    return mReactNativeHost;
  }

  @Override
  public void onCreate() {
    super.onCreate();
    SoLoader.init(this, /* native exopackage */ false);
  }

  private final ReactNativeHost mReactNativeHost = new ReactNativeHost(this) {
    // 表示是否启用开发者模式
    @Override
    public boolean getUseDeveloperSupport() {
      return BuildConfig.DEBUG;
    }

	// 模块列表，可添加原生Java模块
    @Override
    protected List<ReactPackage> getPackages() {
      return Arrays.<ReactPackage>asList(
              new MainReactPackage()
      );
    }
  };
}
```

```java
public class MainActivity extends ReactActivity {

    /**
     * Returns the name of the main component registered from JavaScript.
     * This is used to schedule rendering of the component.
     */
    @Override
    protected String getMainComponentName() {
        return "AwesomeProject";
    }
}
```
