---
title: npm使用
date: 2018-12-20 08:56:53
categories:
  - 电脑使用
tags:
  - npm
---
# 配置镜像 #

镜像使用方法（三种办法任意一种都能解决问题，建议使用第三种，将配置写死，下次用的时候配置还在）:

1.通过config命令

	npm config set registry https://registry.npm.taobao.org 
	npm config list
	配置正确会出现下面内容
		; userconfig C:\Users\My\.npmrc
		registry = "https://registry.npm.taobao.org/"
2.命令行指定

	npm --registry https://registry.npm.taobao.org info underscore 
3.编辑 ~/.npmrc 加入下面内容。操作中发现，没有使用第一种方法配置过，找不到.npmtc文件

	registry = https://registry.npm.taobao.org

# 缓存问题 #

node module 有时候会有缓存问题。

npm cache clean --force 无效

重启大法 无效

更改工程文件夹名，解决缓存问题