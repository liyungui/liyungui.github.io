---
title: Travis CI 使用
date: 2018-09-13 11:31:14
tags: CI
---

# 关于 #

新兴的开源持续集成构建项目，与jenkins，GO的明显的特点在于

- 采用yaml格式，简洁清新独树一帜。

- 在线环境，不用本地部署

目前大多数的github项目都已经移入到Travis CI的构建队列中

# 基本使用 #

## GitHub 生成供Travis使用的token ##

- Settings -- Developer settings -- Personal access tokens

- 填写token的描述，如hexoblog

- 选择repo

- Generate token

- 复制生成的token(只允许看见一次)

## Travis 设置集成仓库 ##

- 使用GitHub账号登录 [Travis 免费网站](https://travis-ci.org)(com是付费私有仓库)

- Settings -- 打开需要集成的仓库 -- Settings 页面

	- Environment Variables 新增一个变量记录token(变量名HEXO_TOKEN)

		`如果有仓库未同步过来，手动同步 Sync account`

	- Cron Jobs 设置需要构建的分支名

## 配置 `.travis.yml` ##

项目根目录下新建 `.travis.yml` 文件

### hexo 博客构建 ##

node_js 实现的md生成静态博客系统

	language: node_js
	node_js: stable
	cache:
	  apt: true
	  directories:
	  - node_modules
	before_install:
	- export TZ='Asia/Shanghai'
	install:
	- npm install
	script:
	- hexo clean
	- hexo g && gulp
	after_script:
	- git clone https://${GH_REF} .deploy_git
	- cd .deploy_git
	- git checkout master
	- cd ../
	- mv .deploy_git/.git/ ./public/
	- cd ./public
	- git config user.name "lyg"
	- git config user.email "liyungui@163.com"
	- git add .
	- git commit -m "Travis CI Auto Builder at `date +"%Y-%m-%d %H:%M"`"
	- git push --force --quiet "https://${HEXO_TOKEN}@${GH_REF}" master:master
	branches:
	  only:
	  - master
	env:
	  global:
	  - GH_REF: github.com/liyungui/liyungui.github.io.git
	notifications:
	  email:
	  - liyungui89@163.com
	  on_success: change
	  on_failure: always
	  
  - HEXO_TOKEN：集成配置的token变量名
  - GH_REF：GitHub仓库地址(不要https://前缀)
  