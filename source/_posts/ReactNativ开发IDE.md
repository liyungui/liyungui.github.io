---
title: ReactNative开发IDE
date: 2018-05-17 17:25:12
tags: 
	- VisualStudioCode
	- SublimeText
	- ReactNative
---

# 不推荐IDE排行榜： #

Top1：Nuclide

虽然是Facebook专门为React开发的，但依托于Atom的Nuclide真是慢的出奇，性能低到无法让人忍受

Top2：WebStorm

缺点是慢、卡、容易崩溃，而且是收费的

# 推荐IDE排行榜： #

## top 1：VS Code ##

### 下载 ###

### 添加RN开发插件 ###

- React Native Tools：微软官方出的ReactNative插件,非常好用
- Reactjs code snippets：react的代码提示，如componentWillMount方法可以通过cwm直接获得
- Auto Close Tag：自动闭合标签
- Auto Rename Tag：自动重命名标签，配合上面的插件使用，基本上能赶上IntelliJ IDEA系的功能了
- Path Intellisense：文件路径提示补全

### 常用快捷键&设置 ###

Ctrl + Space：代码提示，与输入快捷键冲突使用不了，可根据自己喜爱自行设置，设置：文件 => 首选项 => 键盘快捷方式 => 搜索“space”=>修改为自己的快捷键

### 配置VSCode自动运行和调试ReactNative ###

- 安装“React Native Tools”插件；
- 点击调试 => 增加配置 => 选择“React Native:Debug Android” => 插入代码，如图：

{% asset_img vscode_1.png %}

`查看 -- 打开视图 -- 调试` 打开调试视图，就可以看到 `Debug Android` 单击开始调试

## Top 2：Sublime Text 3 ##

启动和关闭的速度简直快的像打开text文本一般，当装完插件之后也好用的可以上天

### 下载 ###

### 安装Package Control ###

Win系统可以使用“Ctrl+`”快捷键或者通过View->Show Console菜单打开命令行，粘贴如下代码：

	import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())

### 安装需要用到的插件 ###

打开Sublime Text3 ，Win系统可以使用快捷键CTRL+SHIFT+P 打开或者，点击菜单栏的“Preferences”-->"Package Control"

打开的终端窗口，输入“install”,下方就会提示“Package Control:install package”,用鼠标点击，后输入要安装的插件：

- ReactJS：支持React开发，代码提示，高亮显示
- Emmet：前端开发必备
- Terminal：在sublime中打开终端并定位到当前目录
- react-native-snippets：react native 的代码片段
- JsFormat：格式化js代码


其中要单独设置的是JsFormat可以设置为保存时自动格式化，设置如下：打开preferences -> Package Settings -> JsFormat -> Setting - Users,输入以下代码：

	{
	 
	  "e4x": true,
	 
	  // jsformat options
	 
	  "format_on_save": true,
	 
	}

