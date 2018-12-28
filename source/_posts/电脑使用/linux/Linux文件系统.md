---
title: Linux文件系统
date: 2018-12-20 08:58:53
categories:
  - 电脑使用
tags:
  - Linux
---
# 一、linux版本 #

{% asset_img linux-1.jpg %}
{% asset_img linux-2.jpg %}

# [二、 类Unix系统目录结构](http://www.ruanyifeng.com/blog/2012/02/a_history_of_unix_directory_structure.html) #

![](http://image.beekka.com/blog/201202/bg2012020601.jpg)

## 目录结构的来历 ##

**规定**

- 第一块盘，专门放系统程序，挂载的目录点为根目录**"/"**（**斜杠**）
- 第二块盘，专门放用户自己的程序，挂载的目录点取名为/usr。
	- 两块盘的目录结构完全相同
	- 第一块盘的目录（/bin, /sbin, /lib, /tmp...）都在/usr目录下重新出现一次。
- 第三块盘，用于存放用户的数据，挂载的目录点取名为/home

这种目录结构就延续了下来。随着硬盘容量越来越大，各个目录的含义进一步得到明确

- `/`：存放系统程序，也就是At&t开发的Unix程序。
- `/usr`：存放Unix系统商（比如IBM和HP）开发的程序。
- `/usr/local`：存放用户自己安装的程序。
- `/opt`：在某些系统，用于存放第三方厂商开发的程序，所以取名为option，意为"选装"。

## 用户目录 ##

	/home/user
	~

## 上一目录 ##

	- 上一目录。最近一次切换目录之前的目录
	
## 相对路径、绝对路径 ##

绝对路径： /home

相对路径： `. 当前目录` `.. 父目录`

# 常用的linux文件权限： #

	444 r--r--r--
	600 rw-------
	644 rw-r--r--
	666 rw-rw-rw-
	700 rwx------
	744 rwxr--r--
	755 rwxr-xr-x
	777 rwxrwxrwx

## 文件和文件夹 ##

	drwxr-xr-x d表示文件夹（ubuntu用绿色字体展示文件夹名）
	-rwxr-xr-x -表示文件（ubuntu用白色字体展示文件名）

## 文件所有者、用户组、其他用户 ##
从左至右，1-3位数字代表文件所有者的权限，4-6位数字代表同组用户的权限，7-9数字代表其他用户的权限。

## 权限值 ##
读取的权限等于4，用r表示；写入的权限等于2，用w表示；执行的权限等于1，用x表示；

**通过4、2、1的组合，得到以下几种权限：**

	0（没有权限）；
	4（读取权限）；
	5（4+1 | 读取+执行）；
	6（4+2 | 读取+写入）；
	7（4+2+1 | 读取+写入+执行）

以755为例：

	1-3位7等于4+2+1，rwx，所有者具有读取、写入、执行权限；
	4-6位5等于4+1+0，r-x，同组用户具有读取、执行权限但没有写入权限；
	7-9位5，同上，也是r-x，其他用户具有读取、执行权限但没有写入权限。

## chmod语法 ##

**语法为：chmod abc file**

其中a,b,c各为一个数字，分别表示User、Group、及Other的权限（对应u,g,o，a表示三者一起设置）。

	r=4，w=2，x=1
	若要rwx属性则4+2+1=7；
	若要rw-属性则4+2=6；
	若要r-x属性则4+1=7。

范例：

	chmod a=rwx file 
	和
	chmod 777 file 
	效果相同

	chmod ug=rwx,o=x file 
	和
	chmod 771 file 
	效果相同

	若用chmod 4755 filename可使此程序具有root的权限

# 三、 ubuntu 设置终端文字大小 #

	调大： ctr + shift + +
	调小： ctr + -

# 终端命令技巧 #

- 输出命令帮助

		命令 -- help
		man 命令
			man后可以跟手册名指定要查阅的手册

- 自动补全功能

		Tab键 自动补全功能
			按一次tab，当前输入自动补全具唯一性，自动补全
					不具唯一性，没有反应
			连按两次tab，提示自动补全的候选项

- 历史命令

		上下键 选中历史命令
		history 列出所有执行过的命令

- 多参
		
		多参数可以只写一个 - 

- 查看命令位置

		which 命令

# 四、 文件操作命令 #

	ls 列出目录显式（非隐藏）文件/文件夹名称。list directory contents
		ls -l 列出目录显式（非隐藏）文件/文件夹属性
		ls - alh 列出目录所有文件/文件夹属性，文件大小格式化输出
	ll 列出当前目录所有文件/文件夹属性
	pwd 显示当前路径 print name of current/working directory
	cd 跳转目录
	clear 清空屏幕。 其实是假操作，往上翻还是能找到之前的记录
	touch 更新文件时间戳，不存在则创建新文件 change file timestamps
	cat 阅读/连接文件 concatenate files and print on the standard output
	more 分屏显示文件 file perusal filter for crt viewing 
	gpedit 编辑文件
	mkdir 创建目录 make directories
	rmdir 移除空目录 remove empty directories
	rm 删除文件/文件夹 remove files or directories
		-r, -R, --recursive
              remove directories and their contents recursively
		-f, --force
              ignore nonexistent files and arguments, never prompt
	grep [-选项] '搜索内容' 文件名 搜索文件内容
	find 查找文件 search for files in a directory hierarchy
	cp 拷贝文件/文件夹 copy files and directories
	mv 移动/重命名文件 move (rename) files
	tar tar归档工具 The GNU version of the tar archiving utility
	gzip 解压/压缩 compress or expand files
	bzip2
	zip、unzip
	chmod 修改文件权限
	chown 修改文件所有者
	chgrp 修改文件所属组

# 五、 输出重定向 #

	> 重定向（覆盖已有内容）
	>> 追加方式重定向

# 六、 管道 #

	| 一个命令的输出通过管道作为后一个命令的输入

# 七、 链接文件 #

硬链接：其实相当于复制源文件，只能链接文件。默认链接方式</br>
软链接：不占磁盘空间，源文件删除则软链接失效。

- 如果软链接文件与源文件不同目录，源文件必须用绝对路径

	ln -s 源文件 链接文件


