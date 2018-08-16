---
title: webview上传图片
date: 2018-08-16 18:20:53
tags: 
	- Android
	- webview
---

最近项目需要在ViewWeb页面上点击 `<input type="file">`，调用手机系统相册来上传图片，开发过程中发现无法正常唤起系统相册来选择图片

# 实现 #

既然浏览器可以，那先参考一下android brower的代码-_-

## 思路 ##

- 重写WebChromeClient。系统升级API使用的delete，而不是@deprecated。谨慎做好系统兼容**(大坑一)**
	- openFileChooser
		- 是系统方法
			- 不需要 @Override **(大坑二)**
			- 非继承，所以需要额外添加混淆规则 **(大坑三)**
	- onShowFileChooser
- 在WebViewActivity中接收选择到的文件Uri
- 回调接口把文件Uri传给页面。即使取消选择也必须回调，否则阻塞页面 **(大坑四)**
	- WebChromeClient提供了回调接口

## 重写WebChromeClient的openFileChooser()和onShowFileChooser()  ##

	// For Android < 3.0
    public void openFileChooser(ValueCallback<Uri> uploadMsg) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = uploadMsg;
        mHandler.openFileChooser("*/*");
    }
    // For Android 3.0+
    public void openFileChooser(ValueCallback uploadMsg, String acceptType) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = uploadMsg;
        String type = TextUtils.isEmpty(acceptType) ? "*/*" : acceptType;
        mHandler.openFileChooser(type);
    }
    // For Android > 4.1.1
    public void openFileChooser(ValueCallback<Uri> uploadMsg, String acceptType, String capture) {
        if (mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
        }
        mUploadMessage = uploadMsg;
        String type = TextUtils.isEmpty(acceptType) ? "*/*" : acceptType;
        mHandler.openFileChooser(type);
    }
    //Android 5.0+
    @Override
    @SuppressLint("NewApi")
    public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback, WebChromeClient.FileChooserParams fileChooserParams) {
        if (mFilePathCallback != null) {
            mFilePathCallback.onReceiveValue(null);
        }
        mFilePathCallback = filePathCallback;
        String type = "*/*";
        if (fileChooserParams != null && fileChooserParams.getAcceptTypes() != null
                && fileChooserParams.getAcceptTypes().length > 0) {
            type = fileChooserParams.getAcceptTypes()[0];
        }
        mHandler.openFileChooser(type);
        return true;
    }

## 回调传递文件Uri ##

	public void notifyFileChooser(Uri uri) {
        if(mUploadMessage != null) {
            mUploadMessage.onReceiveValue(uri);
            mUploadMessage = null;
        }

        if(mFilePathCallback != null) {
            if(uri == null){
                mFilePathCallback.onReceiveValue(null);
            } else {
                Uri[] uris = new Uri[]{uri};
                mFilePathCallback.onReceiveValue(uris);
            }
            mFilePathCallback = null;
        }
    }

## 退出页面时收尾 ##

**修复页面被阻塞bug**

调用系统app选择文件的时候，若弹出选择框，cancel掉选择框之后，发现webview无响应了，无法刷新，加载，点击，甚至退出这个activity也无法加载！后果很严重~

原因是当你选择上传文件的时候，webview的**ValueCallback对象（就是选择图片的回调）会持有这个webview，在没有收到回调之前，你无法对这个webview做任何的操作！**

知道原因之后，就很好解决了，如果cancel了，那么直接调用该对象的onReceiveValue()方法，传入null即可，webview就可以正常操作了

	public void reset() {
        if(mUploadMessage != null) {
            mUploadMessage.onReceiveValue(null);
            mUploadMessage = null;
        }

        if(mFilePathCallback != null) {
            mFilePathCallback.onReceiveValue(null);
            mFilePathCallback = null;
        }

    }

## 添加权限 ##

	<uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.MOUNT_UNMOUNT_FILESYSTEMS" />
    <uses-permission android:name="android.permission.CAMERA" />

## 添加混淆规则 ##

	-keepclassmembers class * extends android.webkit.WebChromeClient{
	    public void openFileChooser(...);
	}

# 部分系统版本无法实现上传(大坑五) #

android 4.4更改webkit内核为chromium，**4.4.0到4.4.2**删除了该API，开发团队解释，正在开发一个新的更好的共有的api，会在正式版本上推出。结果呢，在4.4.3版本，又把这个api加回来了。简直是花样作死啊！一般升级api的套路：@deprecated掉旧的api，加入新的api并保留对原有api的支持

## 解决方案 ##

### 用js调用java方法，强烈推荐 ###

### 使用第三方webview ###

比如腾讯x5内核
