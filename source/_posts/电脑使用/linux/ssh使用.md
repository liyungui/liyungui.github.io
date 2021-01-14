---
title: ssh使用
date: 2019-09-16 17:32:53
categories:
  - 电脑使用
tags:
  - Linux
---

Secure Shell

Linux/Unix 支持四种远程连接协议

- ssh。安全shell
- telnet。远程登录
- ftp。文件传输
- sftp。安全文件传输。支持的shell命令有限。rm只能删除文件

# MAC中生成SSH key

检查是否已经存在SSH keys

`ls -al ~/.ssh`

如果已存在，则结果会列出目录文件列表。

默认的文件名为`id_rsa`和`id_rsa.pub`

如果不存在，则创建

`ssh-keygen -t rsa -b 4096 -C "tom@gmail.com"`

回车，输入密码(8位以上)，确认密码，即可创建成功

把`id_rsa.pub`放到远程服务器，即可使用私钥登录

# 登录

`ssh root@192.168.25.137`

登录之后支持执行 shell

# 安全拷贝 scp

scp是远程安全拷贝，cp为本地拷贝
                   
可以推送过去，也可以拉过来                   
                 
每次都是全量拷贝(效率不高，适合第一次)，增量拷贝用 `rsync`
 
`scp [-r递归，文件夹] [src源路径] [dest目标路径]`

	把本机/var/www/目录下的test.php文件上传到192.168.0.101这台服务器上的/var/www/目录中  
	scp /var/www/test.php root@192.168.0.101:/var/www/
	
             
# sftp

基于ssh的安全加密传输 

## sftp user@ip(或者域名)

输入密码，建立sftp连接

登录成功，所有命令都是默认在远程服务器执行。

想在本地执行，命令前前缀 `!` 或 `l` ，例如 `!pwd` `lpwd`

## 目录查到

- pwd 查看远程服务器当前目录
- lpwd 查看本地当前目录
- ls 查看远程服务器当前目录的文件
- lls 查看本地当前目录的文件

## 文件传输 

- put local [remote] 上传
- get remote [local] 下载

如果是传输文件夹，加上 `-r` 参数

建议打包上传。文件夹目录结构复杂的话，特别耗时

## exit和quit

# 参考&扩展

- [MAC中生成SSH key](https://blog.csdn.net/chduan_10/article/details/94558773)



