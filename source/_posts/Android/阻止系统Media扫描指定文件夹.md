---
title: 阻止系统Media扫描指定文件夹
date: 2018-08-17 11:48:53
tags: 
	- Android
	- Media扫描
	- 相册
---

最近项目需求不让系统图库扫描到APP的图片或者不想对用户浏览图片造成影响

Android提供了对此的支持

**.nomedia文件/文件夹**：让系统不扫描父文件夹下所有媒体文件(图片，mp3,视频)

例如：sd卡根目录/myapp，里面有我们的图片，不想让系统扫描到图库，直接在该文件夹下，添加 `.nomedia文件/文件夹`

之前已经扫描出来的资源图片/视频等等，添加nomedia文件后还是会显示。