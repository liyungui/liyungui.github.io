---
title: Raw和Asset
date: 2019-05-21 19:19:53
categories:
  - Android
tags:
	- Android
---

# 联系

- 相同点：
    两个文件夹下的文件都不会被编译成二进制文件，都会被原封不动的放到apk中。

- 不同点：
    - asset下的文件不会被映射到R文件中，raw下的文件会被映射到R文件中(可以使用R.raw.xxx引用)。
    - asset下可以有目录结构，raw下不能有目录结构。

# 获取文件路径

## asset

`"file:///android_asset/Kotlin与ava共存.mp4"`

此种路径仅可用于webview加载

## raw

`String uri = "android.resource://" + getPackageName() + "/" + R.raw.video;
`

通过assets目录构造URI，不能用来播放视频，也不能播放音频。在raw目录下的文件构造URI可以播放音频，也能播放视频