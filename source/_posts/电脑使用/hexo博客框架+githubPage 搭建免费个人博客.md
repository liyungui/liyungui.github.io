---
title: hexo博客框架+githubPage 搭建免费个人博客
date: 2018-12-20 08:57:53
categories:
  - 电脑使用
tags:
  - hexo
---
[hexo博客框架+githubPage 搭建免费个人博客](http://blog.csdn.net/jzooo/article/details/46781805)

使用hexo生成静态博客并架设在免费的github page平台 

Hexo 是一个简单地、轻量地、基于Node的一个静态博客框架，可以方便的生成静态网页托管在github和Heroku上

GitHub Pages 可以被认为是用户编写的、托管在github上的静态网页。默认域名是 username.github.io 或者 username.github.io/project-name

# 一、GitHub #

## 1. 申请账号 ##

## 2. New repository ##

	Repository name: yourname.github.io

## 3. 设置Repository，开启 GitHub Pages ##

进入 Repository，点击右边的“Setting”菜单,点击”Launch automatic page generator” 

新版本开启 GitHub Pages 方法改为：Theme chooser 选择一个主题，就会生成 master分支和index.md。

少了这步是无法push到github的，因为Repository没有master分支

## 4. 安装git ##

- 你习惯如何使用git命令行
	- use git bash only 默认，只在git bash中使用
	- run git from the windows command prompt 会在系统终端使用（将git添加到环境变量）
	- run git and included unix tools from the windows command prompt （将git和unix tools添加到环境变量）

# 二、Hexo #

## 1. 安装 Node.js（Hexo 基于Node） ##

验证正确安装（自动添加到环境变量）。 cmd控制台输入

	node -v
	npm -v

## 2. 安装 Hexo ##

国内被墙，使用淘宝npm镜像，等待命令完成

	npm install -g cnpm --registry=https://registry.npm.taobao.org

使用淘宝镜像安装 Hexo，等待命令完成

	cnpm install -g hexo-cli

继续输入命令，等待完成

	cnpm install hexo --save

安装完成，验证安装正确

	hexo -v
	我安装的是 3.7.1

## 3. 本地运行hexo ##

新建一个文件夹 `github_blog`, cd 进入该文件夹

初始化hexo

	hexo init

安装生成器

	cnpm install

本地运行博客，命令完成后，浏览器访问 localhost:4000,就可以在本地看到你的个人博客了 

	hexo s -g 
	如果无响应，大概率是端口被占用。 hexo s -p 4001

停止运行博客

	Ctrl+C

## 4. 配置hexo ##

- 目录文件结构

	![](http://img2.tuicool.com/yIVFfaZ.png!web)

	1、 scaffolds ：模板文件夹，新建文章时，Hexo 会根据 scaffold 来建立文件。

		Hexo 有三种默认布局： post 、 page 和 draft ，它们分别对应不同的路径（新建的文件会放到source文件夹下对应同名文件夹，如 source/_post）。
		新建文件的默认布局是 post ，可以在配置文件中更改布局。

	2、 source ：资源文件夹是存放用户资源的地方。

		source/_post ：文件箱。
		source/_draft ：草稿箱。低版本的hexo才会存在
		除 _posts 文件夹之外，开头命名为 _ (下划线)的文件/ 文件夹和隐藏的文件将会被忽略。
		Markdown 和 HTML 文件会被解析并放到 public 文件夹，
		而其他文件会被拷贝过去

	3、 themes ：主题文件夹。Hexo 会根据主题来生成静态页面。

		themes/landscape ：默认的皮肤文件夹

	4、 _config.yml ：全局的配置文件，每次**更改要重启服务**。

	5、 scripts文件夹 ：低版本的Hexo才会生成，里面用于保存扩展Hexo的脚本文件。

	6、 public文件夹 : 生成的静态网页文件夹，用来对外发布。如果使用git发布，就会把所有子对象拷贝到 .deploy_git文件夹
	
	7、 .deploy_git文件夹 ：生成的部署到github的文件夹

- 全局配置 _config.yml

	修改全局配置时，注意缩进，同时注意冒号后面要有一个空格。

		# Hexo Configuration
		## Docs: http://hexo.io/docs/configuration.html
		## Source: https://github.com/hexojs/hexo/

		# Site 站点配置
		title: Hexo-demo #网站标题
		subtitle: hexo is simple and easy to study #网站副标题
		description: this is hexo-demo #网栈描述
		author: pomy #你的名字
		language: zh-CN #网站使用的语言
		timezone: Asia/Shanghai #网站时区

		# URL #可以不用配置
		## If your site is put in a subdirectory, set url as 'http://yoursite.com/child' and root as '/child/'
		url: http://yoursite.com #网址，搜索时会在搜索引擎中显示
		root: / #网站根目录
		permalink: :year/:month/:day/:title/ #永久链接格式
		permalink_defaults: #永久链接中各部分的默认值

		# Directory 目录配置
		source_dir: source #资源文件夹，这个文件夹用来存放内容
		public_dir: public #公共文件夹，这个文件夹用于存放生成的站点文件
		tag_dir: tags #标签文件夹
		archive_dir: archives #归档文件夹
		category_dir: categories #分类文件夹
		code_dir: downloads/code #Include code 文件夹
		i18n_dir: :lang #国际化文件夹
		skip_render: #跳过指定文件的渲染，您可使用 glob 来配置路径

		# Writing 写作配置
		new_post_name: :title.md # 新文章的文件名称
		default_layout: post #默认布局
		titlecase: false # Transform title into titlecase
		external_link: true # Open external links in new tab
		filename_case: 0 #把文件名称转换为 (1) 小写或 (2) 大写
		render_drafts: false #显示草稿
		post_asset_folder: false #是否启动资源文件夹
		relative_link: false #把链接改为与根目录的相对位址
		future: true
		highlight: #代码块的设置
			enable: true
			line_number: true
			auto_detect: true
			tab_replace:

		# Category & Tag 分类 & 标签
		default_category: uncategorized #默认分类
		category_map: #分类别名
		tag_map: #标签别名

		# Date / Time format 时间和日期
		## Hexo uses Moment.js to parse and display date
		## You can customize the date format as defined in
		## http://momentjs.com/docs/#/displaying/format/
		date_format: YYYY-MM-DD
		time_format: HH:mm:ss

		# Pagination 分页
		## Set per_page to 0 to disable pagination
		per_page: 10 #每页显示的文章量 (0 = 关闭分页功能)
		pagination_dir: page #分页目录

		# Extensions 扩展
		## Plugins: http://hexo.io/plugins/ 插件
		## Themes: http://hexo.io/themes/ 主题
		theme: landscape #当前主题名称

		# Deployment #部署到github
		## Docs: http://hexo.io/docs/deployment.html
		deploy:
		  	type: git
		  	repository: https://github.com/liyungui/liyungui.github.io.git
		  	branch: master

- 主题配置

	主题的配置文件在 /themes/主题文件夹/_config.yml(跟站点全局配置文件同名，注意区分目录)，主题的文件目录必须在 themes 目录下

	一般包括导航配置(menu)，内容配置(content)，评论插件，图片效果(fancybox)和边栏(sidebar)。

	Hexo提供了大量的主题，可以在全局配置文件中更改主题：

		# Extensions 扩展
		## Plugins: http://hexo.io/plugins/ 插件
		## Themes: http://hexo.io/themes/ 主题
		theme: 你的主题名称

	[Hexo主题更换教程](https://github.com/dwqs/nx)

	更多Hexo主题戳此： [Hexo Themes](https://github.com/hexojs/hexo/wiki/Themes) 。

## 5. 管理博客 ##

- 新建一篇博客 

	命令完成后生成一个md文件(/博客目录/source/_posts/)，用 md编辑器 编辑即可

	如果需要自定义目录，需要指定完整文件名

		hexo n "hello"
		
		hexo n "JavaScript和ECMAScript的区别" -p ./JS/JavaScript和ECMAScript的区别.md
			INFO  Created: F:\github_blog\source\_posts\JS\JavaScript和ECMAScript的区别.md


- 发布博客

	- hexo git 插件 发布更新博客
		
		- 设置git身份信息
		- 安装hexo git 插件

				cnpm install hexo-deployer-git --save
		- 发布更新博客
		
				hexo d -g
				输入用户名密码即可

	- [手动git 发布更新博客](http://www.tuicool.com/articles/ueI7naV)
	
		- 生成静态博客
		
				hexo g 

		- 部署到github
			
				hexo d -g 
				输入gitgub 用户名和密码即部署成功
				此命令必须在git bash中运行。在cmd终端会报错，无法弹出用户名和密码输入框

## 6. Hexo常用命令总结  ##

	hexo n == hexo new
	hexo g == hexo generate
	hexo s == hexo server
	hexo d == hexo deploy
	hexo clean 清除缓存文件 (db.json) 和已生成的静态文件 (public)

## 7. Tip ##

一定要验证Github的验证邮件

出现其他任何问题，清理，再部署远程博客

# 三、多台电脑设备同步管理 #

**思路**

- `master` 分支用于保存博客静态资源，提供博客页面供人访问；
- `hexo` 分支用于备份博客部署文件，供自己维护更新

注意点：

- 每次换电脑更新博客的时候, 在修改之前最好也要git pull拉取一下最新的更新
- 每次更新博客之后, 都要把相关修改上传到hexo分支

## 上传部署文件到仓库 ##

1. `username.github.io` 新建 `hexo` 分支，并设为默认分支(方便后期维护更新)
2. 克隆 `hexo` 分支到本地 
3. 将本地博客目录 `github_blog` 的部署文件(全部)全部拷贝到 username.github.io 目录
4. 提交到 `hexo` 分支
	- 将themes目录中的.git目录删除（如果有），因为一个git仓库中不能包含另一个git仓库，否则提交主题文件夹会失败
	- 后期需要更新主题时在另一个地方git clone下来该主题的最新版本，然后将内容拷到当前主题目录即可

## 同步到其他电脑 ##

1. 新电脑上克隆 `hexo` 分支到本地
2. cd到 username.github.io目录，执行npm install
	1. 因为 .gitignore文件，里面默认是忽略掉 node_modules文件夹的，该目录并没有同步到git仓库，所以需要install下
	2. node_modules文件没有丢失, 可不执行该操作

# 四、图片 #

1. 放在 `source/images` 文件夹中，通过常规 markdown语法访问 `![](/images/image.jpg)
	- 生成的html： `<img src="/images/image.jpg" alt="">`
	- 生成时会将图片复制到 `public/images` 文件夹。博客图片太多的话，不利于管理
2. 文章资源文件夹
	- 开启文章资源文件夹
		- 站点配置 `post_asset_folder` 选项设为 `true `
		- 开启后，每次 `hexo new [layout] <title>` 都会生成与MD文件同名的文件夹
		- 将图片放于文章资源文件夹
	- 相对路径引用的标签插件
		- 使用下列的标签插件而不是 markdown语法引用图片。确保图片能正确显示在文章和主页、归档页(md语法后两者无法显示)

				{% asset_path slug %}
				{% asset_img slug [title] %}
				{% asset_link slug [title] %}
				例如：{% asset_img example.jpg This is an example image %}
		- 生成的html： `<img src="/2018/04/25/test/test.jpg">`
		- 生成时会将图片复制到 `public/2018/04/25/test/test.jpg`。博客图片太多的话，不利于管理

# GithubPage展示多个项目

Github 上 yourname.github.io 上只能展示一个项目，如果想展示多个静态项目的话，仅需在每个项目下建立一个 gh-pages 分支，这样你就可以通过 yourname.github.io/projectName/ 访问了




