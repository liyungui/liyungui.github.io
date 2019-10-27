---
title: Shadowsocks使用
date: 2019-10-27 16:26:53
categories:
  - 电脑使用
tags:
  - 科学上网
---

# 代理模式

## 全局模式

所有流量都经过代理服务器中转

### 缺陷

- 国内网站速度变慢
- 浪费服务器流量

## 编辑PAC

Proxy auto-config，简称PAC，代理自动配置

是一种网页浏览器技术，用于定义浏览器该如何自动选择适当的代理服务器来访问一个网址。

在Shadowsocks里面，编辑PAC可以有如下两个方式

## 添加到 pac.txt 文件中

如果使用gfwlist更新PAC规则，则文件名是 `gfwlist.txt`

```
var proxy = "__PROXY__";
var rules = [
	"||windowscentral.com",
]
```

ShadowSocks的PAC文件实际是不停的更新的，如果自己编辑了PAC文件就不要再去更新PAC文件了，不然添加的内容就没有了。

或者可以把PAC上传到你的服务器上，在ShadowSocks使用在线PAC规则选项来调用

## 添加到 user-rule.txt 文件中


每一行表示一个URL通配符，但是通配符语法类似

```
! Put user rules line by line in this file.
! See https://adblockplus.org/en/filter-cheatsheet
||flykostage.com
```
