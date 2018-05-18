---
title: Visual Studio Code 使用
date: 2018-05-17 18:09:14
tags: VisualStudioCode
---

# 预览模式与编辑模式 #

| 操 作 | 模式 | 文件标题 |
| -- | -- |
| 单击 | 预览模式 | 斜体 |
| 双击 | 编辑模式 | 正常 |

在资源管理器双击文件，或者文件标题栏双击文件，都可以进入 编辑模式

## 禁用预览模式 ##

设置文件修改

	// 控制是否将打开的编辑器显示为预览。预览编辑器将会重用至其被保留(例如，通过双击或编辑)，且其字体样式将为斜体。
	"workbench.editor.enablePreview": true,
	
	// 控制 Quick Open 中打开的编辑器是否显示为预览。预览编辑器可以重新使用，直到将其保留(例如，通过双击或编辑)。
	"workbench.editor.enablePreviewFromQuickOpen": true