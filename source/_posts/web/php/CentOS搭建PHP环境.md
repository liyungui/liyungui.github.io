---
title: CentOS搭建PHP环境
date: 2018-12-24 22:31:25
categories:
  - Web
tags:
  - PHP
---

# 安装Apache

	yum install httpd httpd-devel mod_ssl
	
	httpd -V //查看httpd版本
	 
	ps aux |grep httpd //查看开启的 httpd 服务
	
	rpm -qi httpd //版本信息

## 配置Apache

### 修改配置文件

`/etc/httpd/conf/httpd.conf`

	cp httpd.conf httpd.conf.bak    //修改前将原有配置文件备份
	
### 设置为自动启动

	systemctl enable httpd.service
	
## 开启与关闭Apache

	systemctl start  httpd.service
	systemctl stop  httpd.service
	
# 安装MySQL

	yum install mysql mysql-server
	
# 安装PHP

## 安装php7.2

centos中的yum安装版本是5.4。因此我们手动更新rpm为第三方的php版本

### 获取rpm

	rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm   
	
	rpm -Uvh https://mirror.webtatic.com/yum/el7/webtatic-release.rpm
	
### 查看php版本

	yum list php*

### 安装php7.2

	yum -y install php72w
	
### 安装拓展包

	yum -y install php72w-cli php72w-common php72w-devel php72w-mysql

# 配置Apache支持php7.2

配置Apache的 php配置信息文件

`/etc/httpd/conf/httpd.conf` 文件

	PHPIniDir /etc/php.ini
	
# 重启Apache