---
title: Visual Studio Code 使用
date: 2018-05-17 18:09:14
tags: VisualStudioCode
---

# VS Code 的介绍

VS Code 的全称是 Visual Studio Code，是一款开源的、免费的、跨平台的、高性能的、轻量级的代码编辑器。它在性能、语言支持、开源社区方面，都做的很不错。

## 编辑器 与 IDE

`IDE`和`编辑器`是有区别的：

- **IDE** ：对代码会有较好的智能提示，同时侧重于工程项目，对项目的开发、调试工作有较好的图像化界面的支持，因此比较笨重。比如 Eclipse 的定位就是 IDE。

- **编辑器**：要相对轻量许多，侧重于文本的编辑。比如 Sublime Text 的定位就是编辑器。再比如 Windows 系统自带的「记事本」就是最简单的编辑器。

需要注意的是，VS Code 的定位是`编辑器`，而非`IDE`。但 VS Code 又比一般的编辑器的功能要丰富许多。

## VS Code的一些补充

- VS Code 的使命，是让开发者在编辑器里拥有 IDE 那样的开发体验，比如代码的智能提示、语法检查、图形化的调试工具、插件扩展、版本管理等。

- VS Code 的源代码以MIT协议开源。

- VS Code 自带了 TypeScript 和 Node.js 的支持。也就是说，你在书写 JS 和 TS 时，是自带智能提示的。

- 有一点你可能不知道，VS Code 这个客户端软件是用 js 语言开发出来的（具体请自行查阅关键字`Electron`）。有句话说得好：能用 js 实现的功能，最终一定会用 js 实现。

# 常用快捷键

## 通用

```
显示/隐藏侧边栏：cmd + b
显示/隐藏底部控制栏：cmd + j

增加一个编辑器(均分编辑窗口)：cmd + \

在打开的文件间切换：ctr + tab
项目全局搜索文件：cmd + p
打开命令行面板：cmd + sft + p
当前文件中搜索：cmd + f
项目全局搜索：cmd + shift + f
```

## 移动光标

```
以字符为单位移动:  方向键←/→
移动到上/下一行相同水平位置：方向键↑/↓
以词语(中英)为单位移动:  Option + 方向键←/→
以行为单位移动:  Command + 方向键←/→
以代码块为单位移动:  Command + Shift + \
以整个文档为单位移动:  Command + 方向键↑/↓
将光标回到上一个位置：Command + U
```

## 滚动

```
翻页(Page Up/Down): fn + 方向键↑/↓
滚动至文稿开头/末尾（Home/End）：fn + 方向键←/→

```

## 选择文本

```
移动光标的快捷 + Shift
滚动的快捷 + Shift
```

## 编辑

```
向前删除：delete  
向后删除：fn + delete
整行删除：cmd + delete
当前行下新增一行：cmd + enter
移动代码：alt + ↑/↓
复制代码：alt + shift + ↑/↓
```

## 多光标

```
1. 按住 opt，然后在希望出现光标的位置点击鼠标
2. 选中文本，按 opt + shift + i，会在选中行的末尾都创建一个光标
```

## JS相关

```
单行注释：cmd + /
格式化：opt + shift + f
当前行下新增一行：cmd + enter
移动代码：alt + ↑/↓
复制代码：alt + ↑/↓
跳到指定行：ctr + g
在当前文件的方法间跳转：cmd + shift + o
```

# 设置

设置选项 都配置在一个 `settings.json` 文件中

## 两个设置

### User Settings 全局设置

用户目录下

- macOS：`$HOME/Library/Application Support/Code/User/settings.json`

### Workspace Settings 项目设置

只对当前项目的设置，会覆盖 全局设置

项目根目录下 `.vscode` 文件夹中

## 打开设置

### 点击菜单

- On Windows/Linux - `File > Preferences > Settings`
- On macOS - `Code > Preferences > Settings`

### 快捷键

- On macOS - `cmd + ,`

### 命令行面板

输入以下命令调出：

- open settings(Json)
- open user settings 等同于Json方式打开
- open settings(UI) UI配置
- open default settings(Json)

# 预览模式与编辑模式 #

| 操 作 | 模式 | 文件标题 |
| --- | --- | --- |
| 单击 | 预览模式 | 斜体 |
| 双击 | 编辑模式 | 正常 |

在资源管理器双击文件，或者文件标题栏双击文件，都可以进入 编辑模式

## 禁用预览模式 ##

设置文件修改

	// 控制是否将打开的编辑器显示为预览。预览编辑器将会重用至其被保留(例如，通过双击或编辑)，且其字体样式将为斜体。
	"workbench.editor.enablePreview": true,
	
	// 控制 Quick Open 中打开的编辑器是否显示为预览。预览编辑器可以重新使用，直到将其保留(例如，通过双击或编辑)。
	"workbench.editor.enablePreviewFromQuickOpen": true

# vs launch.json配置文件

vs自动为每个项目创建配置文件，目录为 `项目根目录\.vscode\launch.json`

## 让F5调试运行不停留在程序入口

	"stopOnEntry": false,

# 插件

## Code Runner

支持运行各种语言的代码

## GitLens

git插件，比vscode自带git更加好用

# Python

## 带参数调试Python

有些py文件需要命令行输入参数

configurations添加args

	"configurations": [
	        {
	            "name": "Python",
	            "type": "python",
	            "request": "launch",
	            "stopOnEntry": true,
	            "pythonPath": "${config:python.pythonPath}",
	            "program": "${file}",
	            "cwd": "${workspaceRoot}",
	            "env": {},
	            "envFile": "${workspaceRoot}/.env",
	            "debugOptions": [
	                "WaitOnAbnormalExit",
	                "WaitOnNormalExit",
	                "RedirectOutput"
	            ],
	            "args": [
	                "-b 1"
	            ]
	        },

## python插件

- 打开VScode，Ctrl+p
- 输入 "ext install python"，搜索时间可能会比较长
- 选择下载量最高的那个插件点击安装（根据网络情况，安装时间不确定，我当初装了挺久）
- ![](http://images2015.cnblogs.com/blog/1006394/201609/1006394-20160902181958590-957920055.gif)

- 编辑完代码按F5即可运行。初次运行会让你选环境，选择python
- 默认按F5后需要再按一次F5程序才会运行，如果要按F5马上运行需要将launch.json文件的 "stopOnEntry": true,改为 "stopOnEntry": false

### flake8

代码错误和格式规范静态检查

- 打开命令行
- 输入 "pip install flake8" 需要翻墙才能下载
- 安装flake8成功后，打开VScode，文件->首选项->用户设置，在settings.json文件中输入"python.linting.flake8Enabled": true

### yapf

安装yapf之后在VScode中按Alt+Shift+F即可自动格式化代码

- 打开命令行
- 输入 "pip install yapf"
- 安装yapf成功后，打开VScode，文件->首选项->用户设置，在settings.json文件中输入"python.formatting.provider": "yapf"
	
# JavaScript

## 插件

### Debugger for Chrome

在编辑器中打断点，在Chrome中调试js代码

	
	
# 参考&扩展	

- [vscode 配置及插件推荐](https://www.jianshu.com/p/21c99e461ad3)
- [VSCode写python的正确姿势](http://www.cnblogs.com/bloglkl/archive/2016/08/23/5797805.html)
- [带参数调试Python](https://www.zhihu.com/question/50700473/answer/130676317)