---
title: CentOS 安装PHP7的正确姿势
date: 2018-12-24 17:31:25
categories:
  - Web
tags:
  - PHP
---

# SCL

CentOS上的PHP版本都十分古老(5.4)，满足不了一些框架对PHP版本的要求。

于是，出现了许多第三方软件库。第三方软件库是提供的软件没有经过CentOS官方测试，在安装软件的同时，可能会替换掉系统的一些核心文件，造成系统不稳定。

推荐用SCL（Software Collections）软件库安装高版本的PHP。SCL属于CentOS官方的软件库，经过充分测试，安装软件时不会替换系统的核心文件，保证了系统的稳定性。SCL以 scl enable 方式管理软件，虽然在使用上增加了一点点的麻烦，但这绝对地保证了系统稳定性。而且这么做还有一个好处：就是系统上可以多个PHP版本共存而互相不冲突。方便你测试代码或者框架，在各个版本PHP上的兼容性。

# 安装

## 安装SCL

`yum install centos-release-scl-rh`

## 在yum中搜到新版的PHP

`yum search php`

结果如下

	php54-runtime.x86_64
	php55-runtime.x86_64
	rh-php56-runtime.x86_64
	rh-php70-runtime.x86_64
	
	rh- 前缀是RedHat的意思，标识这是官方提供的PHP而不是第三方库提供的
	
## 安装PHP7.0

`yum install rh-php70`

PHP实际会安装在 `/opt/rh` 目录下 

## scl enable 显示执行php

SCL的风格就是把软件对系统的影响减少到最小，安装完PHP，php命令不会被添加到 $PATH 变量中。需要通过 scl enable 命令显示执行：

	scl enable rh-php70 "php -v" //执行 php -v
	
	scl enable rh-php70 bash //执行 bash 命令，新开的shell就能自动识别php了


