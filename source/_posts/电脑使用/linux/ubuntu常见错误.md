---
title: Ubuntu常见错误
date: 2018-12-20 09:07:53
categories:
  - 电脑使用
tags:
  - Linux
---
# `sudo apt update` 无法获得锁#

- 错误：
	- 无法获得锁 `/var/lib/dpkg/lock 资源暂时不可用. `

- **原因：**
	- 1. 其他窗口在使用资源，正在进行更新
	- 2. 软件中心正在安装
	- 3. 某些软件异常终结。比如上次更新某个软件异常错误或强制退出

- **解决方案：**
	- 关闭其他使用资源的窗口
	- 等待其他软件安装完毕
	- 删除锁

		sudo rm   /var/lib/dpkg/lock
		sudo dpkg --configure -a //重新进行配置设置 
		sudo apt update

    
# `sudo dpkg --configure -a` config.dat被锁 #

- **错误：**

   		debconf: DbDriver "config": /var/cache/debconf/config.dat is locked by another process: Resource temporarily unavailable
- **解决方案：**

		sudo lsof /var/cache/debconf/config.dat

		lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1000/gvfs
	      Output information may be incomplete.
		COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
		frontend 8149 root    4uW  REG    8,6    49446 4070702 /var/cache/debconf/config.dat
	
		sudo kill 8149

# `sudo source /etc/profile` 找不到source命令 #

用su直接切换到root，再执行

	source /etc/profile

