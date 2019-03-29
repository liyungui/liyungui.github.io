---
title: Linux设置环境变量
date: 2018-12-16 11:35:29
categories:
  - 电脑使用
tags:
  - Linux
---

# export 命令

**设置或显示环境变量**

语　　法：`export [-fnp][变量名称]=[变量设置值]`

 一个变量创建时，不会自动地为在它之后创建的shell进程所知。
 
 export可以向shell执行的脚本传递变量的值。
 
# 三种实现方法设置环境变量

## 终端中直接使用 export -- 临时变量

直接使用 export 设置的变量都是临时变量，退出当前的 shell ，该变量定义的值便失效了

## 修改 /etc/profile

	sudo gedit  /etc/profile

在文件末尾添加

	export JAVA_HOME=/usr/lib/jdk1.8.0_45
	
	export CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$CLASSPATH 多值间用冒号连接
	
	export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH 别忘记最后加上原来的$PATH，否则就把先前的环境变量覆盖了

保存退出

使其生效

	sudo source /etc/profile 

	提示找不到source命令则需要切换到root用户执行 source /etc/profile

此时只有执行过 sudo source /etc/profile 命令的终端所在的线程才可以使用 Java 环境变量，而其他线程则还不可以。

重启之后则都可以了

## 修改 .bashrc 文件 -- 当前用户 shell 下生效
# 环境变量切换

	export JAVA_6_HOME=/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home
	export JAVA_7_HOME=/Library/Java/JavaVirtualMachines/jdk1.7.0_79.jdk/Contents/Home
	export JAVA_8_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_131.jdk/Contents/Home

	#创建默认的jdk版本
	export JAVA_HOME=$JAVA_6_HOME

	#创建alias命令，实现动态切换
	alias jdk8='export JAVA_HOME=$JAVA_8_HOME'
	alias jdk7='export JAVA_HOME=$JAVA_7_HOME'
	alias jdk6='export JAVA_HOME=$JAVA_6_HOME'

保存并退出编辑器

在terminal中输入命令：`source .bash_profile` 使配置生效

验证配置与切换

	在terminal中 
		输入  jdk6
		再输入java -version 查看当前版本即可实现动态切换，		jdk7，jdk8同样。
		
# Mac系统环境变量，加载顺序

* 系统级别
	* /etc/profile
	* /etc/paths 
* 用户级别
	* ~/.bash_profile 
	* ~/.bash_login 
	* ~/.profile 以上3个按照从前往后的顺序读取，读取到一个就停止
	* ~/.bashrc bash shell打开的时候载入的