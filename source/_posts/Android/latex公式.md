---
title: latex公式
date: 2020-03-06 16:12:33
categories:
  - Android
tags:
  - RxJava
---

# LaTex

## MathJax

运行在浏览器中的开源的数学符号渲染引擎

可以解析Latex、MathML和ASCIIMathML的标记语言

# MathJax基本语法

## 公式标记

需要用一些适当的标记告诉MathJax某段文本是公式代码

MathJax中的公式排版有两种方式：

- inline。行内（公式嵌入到文本段中）
- displayed。独立（行、块、段落）

默认的displayed公式分隔符有 `$$...$$` 和 `\[...\]`，默认的inline公式分隔符为 `(...)` 。

当然可以通过参考文档配置自定义分隔符。下文中，自定义 `$...$` 作为inline分隔符。

公式：c=(a平方+b平台)开根号

```
$ c = \sqrt{a^{2}+b^{2}} $

$$ c = \sqrt{a^{2}+b^{2}} $$
```
## 上下标

- `^` 表示上标, `_` 表示下标。
- 如果上下标的内容多于一个字符，要用 `{}` 把这些内容括起来当成一个整体。
- 上下标是可以嵌套的，也可以同时使用

## 转义

以下几个字符: `# $ % & ~ _ ^ \ { }`有特殊意义，需要表示这些字符时，需要转义，即在每个字符前加上 `\`

# 原生渲染Latex

|方案|特性|备注|
| --- | ---| --- |
|jlatexmath-android| JLaTexMath移植到Android ||
|JLaTexMath-andriod|基于jlatexmath-android改进；</br> 针对化学、生物类的中文公式做了优化；</br> ||
| FlexibleRichTextView |使用JLaTexMath-andriod渲染；</br> |公式弧只支持 ${ab}^{\frown}$ 两个点；</br> |
| MathView|依赖webview；</br> 支持双渲染引擎MathJax and KaTeX；</br> KaTeX 比 MathJax 快，但 MathJax 支持更多的特性，而且更漂亮|用`\(...\)`代替`$...$`表示行内公式；</br> MathJax在Android上的bug导致有些字符是空白的；</br> Java中注意反斜杠、引号等转义字符(`\\`转义成了`\`)|

# 参考&扩展

- [latex](https://www.latex-project.org/)
- [mathjax](https://www.mathjax.org/)
- [MathJax 语法参考](https://qianwenma.cn/2018/05/17/mathjax-yu-fa-can-kao/)
- [LATEX 公式总结](https://www.jianshu.com/p/22117d964baf)
- [JLaTexMath](https://github.com/opencollab/jlatexmath) A Java API to render LaTeX
- [jlatexmath-android](https://github.com/mksmbrtsh/jlatexmath-android)
- [JLaTexMath-andriod](https://github.com/sixgodIT/JLaTexMath-andriod)
- [FlexibleRichTextView](https://github.com/daquexian/FlexibleRichTextView)
- [MathView](https://github.com/jianzhongli/MathView)





