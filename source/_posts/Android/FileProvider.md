---
title: FileProvider
date: 2020-01-16 16:49:53
categories:
  - Android
tags:
	- Android
---

# 背景

为了提高 **私有目录** 的安全性，防止应用信息的泄漏，从 Android 7.0 开始，应用私有目录的访问权限被做限制。

具体表现为，开发人员不能够再简单地通过 `file://` URI 访问其他应用的私有目录文件或者让其他应用访问自己的私有目录文件。否者会抛出 `FileUriExposedException` 引发 Crash。

`android.os.FileUriExposedException: file:///storage/emulated/0/xxx exposed beyond app through Intent.getData()`

所有包含 `file://` 的URI 的 Intent 离开你的 App ，都受此限制

安卓提供的解决方案是 FileProvider，通过 `comtent://` 的模式替换掉 `file://` 

FileProvider 本质上就是一个 ContentProvider。ContentProvider 其实就是在可控的范围内，向外部其他的 App 分享数据。

## 场景

- 调用相机拍照。
- 剪裁图片。
- 调用系统安装器去安装 Apk。

{% asset_img 映射.png %}

# 参考&扩展

- [我想把 FileProvider 聊的更透彻一些](https://juejin.im/post/5974ca356fb9a06bba4746bc)
- [关于 Android 7.0 适配中 FileProvider 部分的总结](https://juejin.im/post/590bbf33ac502e006cdb341a)
- [Android 7.0 DownloadManager与FileProvider的坑](https://www.jianshu.com/p/c58d17073e65)
