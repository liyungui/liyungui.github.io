---
title: Linux的su和su -
date: 2018-12-20 08:58:53
categories:
  - 电脑使用
tags:
  - Linux
---
## su命令和su - 作用 ##

切换用户。切换到root用户可以省略用户名

## su命令和su -命令 区别 ##

是否改变 `shell` `工作目录` `环境变量`

### su ###

`shell` 未切换，原来用户（默认普通用户登录）

`工作目录` 未切换，原来用户（默认普通用户登录）

`环境变` 未切换，原来用户（默认普通用户登录）

	wina66@ubuntu:~$ su
	Password: 
	root@ubuntu:/home/wina66# pwd
	/home/wina66
	root@ubuntu:/home/wina66# echo $PATH
	/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
	root@ubuntu:/home/wina66# 

### su - ###

`shell` 切换，新用户（默认普通用户登录）

`工作目录` 切换，新用户（默认普通用户登录）

`环境变` 切换，新用户（默认普通用户登录）

	wina66@ubuntu:~$ su -
	Password: 
	root@ubuntu:~# pwd
	/root
	root@ubuntu:~# echo $PATH
	/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
	root@ubuntu:~# 