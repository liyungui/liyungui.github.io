---
title: 01 HTML5
date: 2020-02-14 15:28:14
categories:
  - web
tags:
  - web
---

# 浏览器内核

浏览器内核可以分成两部分：

## 渲染引擎

Rendering Engine，或者Layout Engineer

解析输出网页内容

不同内核对于网页的语法解释会有不同，所以渲染的效果也不相同。

## JS引擎

解析 Javascript 语言，执行 javascript语言来实现网页的动态效果。

最开始渲染引擎和 JS 引擎并没有区分的很明确，后来 JS 引擎越来越独立，内核就倾向于只指渲染引擎。

# Web标准

不同的浏览器内核，工作原理、解析、显示会有差别，需要一个统一标准

##  Web 标准构成

 Web标准是由W3C和其他标准化组织制定的一系列标准的集合。
 
 主要包括结构（Structure）、表现（Presentation）和行为（Behavior）三个方面。

### 结构标准

结构用于对网页元素进行整理和分类

主要包括XML和XHTML两个部分。

### 样式标准

表现用于设置网页元素的版式、颜色、大小等外观样式

主要指的是CSS。

### 行为标准

行为是指网页模型的定义及交互的编写

主要包括DOM和ECMAScript两个部分

# HTML 初识

HTML（Hyper Text Markup Language）中文译为“超文本标签语言”

主要是通过HTML标签对网页中的文本、图片、声音等内容进行描述。

关键词：文本 标签 语言

```html
<strong> 我是加粗的字体 </strong>
```

## HTML骨架格式

```html
<HTML>   
    <head>     
        <title></title>
    </head>
    <body>
    </body>
</HTML>
```

head标签中我们必须要设置的标签是title

## HTML标签分类

### 双标签

`<标签名> 内容 </标签名>`

### 单标签

`<标签名 />` 比如 `<br />`

## HTML标签关系

### 嵌套关系

`<head>  <title> </title>  </head>`

### 并列关系

```html
<head></head>
<body></body>
```

# 文档类型<!DOCTYPE>

位于文档的最前面

用于向浏览器说明当前文档使用的标准规范，保证浏览器能正确解析。

`<!DOCTYPE html>`

HTML5的文档类型兼容很好(向下兼容的原则)，所以使用HTML5的文档类型就好了。

# 字符集

`<meta charset="UTF-8">`

# HTML标签

## 标签属性

`<标签名 属性1="属性值1" 属性2="属性值2" …> 内容 </标签名>`

1. 标签可以拥有多个属性，必须写在开始标签中，位于标签名后面。

2. 属性之间不分先后顺序

3. 标签名与属性、属性与属性之间均以空格分开

4. 属性采取  键值对 的格式； key="value"  的格式

5. 属性都有默认值，省略该属性则取默认值

## 排版标签

显示网页结构的标签，是网页布局最常用的标签。

### 标题标签 h1

单词缩写：  head   头部. 标题 

HTML提供了6个等级的标题，即 `<h1>到<h6>`

### 段落标签 p

单词缩写：  paragraph  段落

### 水平线标签 hr

单词缩写：  horizontal  横线

### 换行标签 br

单词缩写：  break   打断 ,换行

### div span标签

单词缩写：  division  分割，分区

span, 跨度，跨距；范围   

网页布局主要的2个盒子

## 文本格式化标签

设置文本格式

|标签|缩写|显示效果|
|---|---|---|
|b strong|bold|粗体|
|i em|italic 斜体字；emphasize强调 |斜体|
|s del|strike out 删去；delete|删除线|
|u ins|underline；insert插入|下划线，插入线| 

b i s u 已经不推荐使用

## 图像标签 img

单词缩写：   image  图像

`<img src="图像URL" />`

src属性用于指定图像文件的路径和文件名，是img标签的必需属性。

## 链接标签 a

单词缩写：  anchor 锚

`<a href="跳转目标" target="目标窗口的弹出方式">文本或图像</a>`

网页中各种网页元素，如图像、表格、音频、视频等都可以添加超链接。

### 关键属性

#### href

指定链接目标的url地址

Hypertext Reference, 超文本引用  

取值有：

- 外部链接 `< a href="http:// www.baidu.com"> 百度 </a >`
- 内部链接 `< a href="index.html"> 首页 </a >`
- 空链接 `< a href="#"> 空链接 </a >`

### target

指定链接页面的打开方式

其取值有：

- `_self` 默认值
- `_blank` 在新窗口中打开方式

### 锚点定位

通过创建锚点链接，用户能够快速定位到目标内容。

创建锚点链接分为两步：

```html
1.使用相应的id名标注跳转目标的位置

2.使用 <a href=”#id名">“链接文本"</a> 创建链接文本
```

### 全局链接属性设置标签 base

设置整体链接的属性  

base 写在 head 之间

```html
<head>
<base target="_blank" />
</head>
```
设置所有链接都在在新窗口中打开

## 注释标签

```html
<!-- 单行注释语句 -->

<!--
多行
注释
语句
-->
```

## 无序列表 ul

列表项符号默认是点

```html
<ul>
  <li>列表项1</li>
  <li>列表项2</li>
  <li>列表项3</li>
  ......
</ul>
```

## 有序列表 ol

列表项符号默认是数字

```html
<ol>
  <li>列表项1</li>
  <li>列表项2</li>
  <li>列表项3</li>
  ......
</ol>
```

## 自定义列表 dl

列表项前没有任何项目符号

```html
<dl>
  <dt>名词1</dt>
  <dd>名词1解释1</dd>
  <dd>名词1解释2</dd>
  ...
  <dt>名词2</dt>
  <dd>名词2解释1</dd>
  <dd>名词2解释2</dd>
  ...
</dl>
```

## 表格 table

```html
<table>
  <tr>
    <td>单元格内的文字</td>
    ...
  </tr>
  ...
</table>
```

```
table 表格
tr 行；行内只能放单元格
td 单元格；
th 表头单元格（特殊的td）；一般位于表格的第一行或第一列；文本加粗居中
```

### 表格属性

|属性|含义|属性值|
|---|---|---|
|border|单元格边框像素|默认0像素，无边框|
|cellspacing|单元格外间距|默认2像素
|cellpadding|单元格内间距（内容与边框间距）|默认1像素|

## 合并单元格

跨行合并：rowspan    跨列合并：colspan

将多个内容合并的时候，就会有多余的东西，需要把它删除。例如 把 3个 td 合并成一个， 那就多余了2个，需要删除。

删除的个数  =  合并的个数  - 1

## 表单

一个完整的表单通常由3个部分构成：

- **表单域**。**容器**：容纳所有的表单控件和提示信息，定义处理表单数据所用程序的url地址，以及数据提交到服务器的方法。
- **表单控件**（也称为表单元素）。表单功能项，如单行文本输入框、密码输入框、复选框、提交按钮、重置按钮等。
- **提示信息**

### 表单域 form

```html
<form action="url地址" method="提交方式" name="表单名称">
  各种表单控件
</form>
```

常用属性：

```
1. Action
   在表单收集到信息后，需要将信息传递给服务器进行处理，action属性用于指定接收并处理表单数据的服务器程序的url地址。
2. method
   用于设置表单数据的提交方式，其取值为get或post。
3. name
   用于指定表单的名称，以区分同一个页面中的多个表单。
```

### 输入控件 input

<img src="media/html5/input.png" />

### 多行文本控件 textarea

```html
<textarea cols="每行中的字符数" rows="显示的行数">
  文本内容
</textarea>
```

### 下拉菜单 select


```html
<select>
  <option>选项1</option>
  <option>选项2</option>
  <option>选项3</option>
  ...
</select>
```

可以使用 `selected ="selected"`定义默认选中项

### 文本标签 label

为 input 定义标注（即绑定input），点击label的时候, 被绑定的表单元素就会获得输入焦点

for属性用来指定要绑定input的id

```html
<label for="male">Male</label>
<input type="radio" name="sex" id="male" value="male">
```

# 路径
 
## 相对路径

相对自身的路径

`../`表示父级文件夹

## 绝对路径

完整的路径地址（文件夹或网络地址）