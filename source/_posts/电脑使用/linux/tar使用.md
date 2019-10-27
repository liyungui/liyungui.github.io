---
title: tar使用
date: 2019-09-16 17:40:53
categories:
  - 电脑使用
tags:
  - Linux
---

# 打包和压缩

打包:是指将一大堆文件或目录变成一个总的文件.

压缩:则是将一个大的文件通过一些压缩算法变成一个小文件。


Linux中很多压缩程序只能针对一个文件进行压缩，这样当你想要压缩一大堆文件时，你得先将这一大堆文件先打成一个包（最常用的打包程序就是tar），然后再用压缩程序进行压缩（gzip bzip2命令）

# 命令

## tar `.tar`

	tar [参数] [tar包名] [源文件，解包不需要]

打包解包

本身不具有压缩功能。他是调用压缩功能实现压缩

## gzip `.gz`
 
	压缩： gzip FileName
	解压1： gunzip FileName.gz
	解压2： gzip -d FileName.gz

## bzip2 `.bz2`

	压缩： bzip2 -z FileName
	解压1：bzip2 -d FileName.bz2
	解压2：bunzip2 FileName.bz2
	
## rar `.rar`

	压缩：rar a FileName.rar DirName
	解压：rar x FileName.rar

## zip `. zip`	
	
	压缩：zip FileName.zip DirName
	解压：unzip FileName.zip
	
## compress `.z`	

	压缩：zip FileName.zip DirName
	解压：unzip FileName.zip

# 参数

|参数|描述|
|---|---|
|-c	|或--create，建立新的压缩文件|
|-x	|或--extrac，从压缩的文件中提取文件|
|-z	|或--gzip或--ungzip,通过gzip指令解压缩文件|
|-j|	通过bzip2指令解压缩文件|
|-Z	|通过compress指令解压文件|
|-p	|或--same-permissions 用原来的文件权限还原文件|
|-v|显示操作过程|
|-f|	指定压缩文件。必要参数，放最后，后面只能接档案名|
|-t|	或--list ，列出压缩文件的内容|
|-r|	或--append 新增文件到已存在的压缩文件的结尾部分|
|-u	|或--update 仅置换较压缩文件内的文件更新的文件|
|-d	|或-diff，记录文件的差别|

# 实例

## 打包


	tar -cvf log.tar 1.log 仅打包，不压缩！
	tar -zcvf log.tar.gz 1.log 打包后，以 gzip 压缩
	tar -jcvf log.tar.bz2 1.log 打包后，以 bzip2 压缩
	
在加参数 f 之后的文件档名是自己取的

我们习惯上都用 .tar 来作为辨识。 

如果加 z 参数，则以 .tar.gz 或 .tgz 来代表 gzip 压缩过的 tar包； 

如果加 j 参数，则以 .tar.bz2 来作为tar包名。


## 解包

	tar -zxvf /home/hc/test/log.tar.gz 