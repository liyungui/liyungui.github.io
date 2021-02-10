---
title: Homebrew使用
date: 2019-04-15 18:32:53
categories:
  - 电脑使用
tags:
  - Mac
---

# Homebrew是什么

The missing package manager for macOS (or Linux)

# 安装 

	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	
# 使用
	
## 安装

	brew install wget

## 查看已安装的列表

`brew list`
	
## 查看安装路径

 默认安装路径 `/usr/local/Cellar`
 
 `brew list 软件名` 获取安装路径
 
## 卸载

`brew uninstall xxx` 

## 搜索软件

`brew search xxx`

## 更新软件

`brew upgrade xxx`

# 常见问题

## 长时间停在Updating Homebrew

在国内的网络环境下使用 Homebrew 安装软件的过程中可能会长时间卡在 Updating Homebrew 这个步骤

参考以下 2 种处理方法

### 关闭自动更新

```
vim ~/.bash_profile
# 新增一行
export HOMEBREW_NO_AUTO_UPDATE=true
```

### 取消本次更新操作

按住 control + c 之后命令行会显示 ^C，就代表已经取消了 Updating Homebrew 操作

大概不到 1 秒钟之后就会去执行我们真正需要的安装操作了

这个方法是临时的、一次性的

### 使用 Alibaba镜像源加速

brew 命令安装软件的时候，跟以下 3 个仓库地址有关：

```
brew.git
homebrew-core.git
homebrew-bottles
```

```
cd "$(brew --repo)"
git remote set-url origin https://mirrors.aliyun.com/homebrew/brew.git
cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
git remote set-url origin https://mirrors.aliyun.com/homebrew/homebrew-core.git
echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.aliyun.com/homebrew/homebrew-bottles' >> ~/.bash_profile
source ~/.bash_profile
```
 
# 参考&扩展

- [官网](https://brew.sh/)
- [homebrew长时间停在Updating Homebrew 这个步骤](https://www.cnblogs.com/tulintao/p/11134877.html)