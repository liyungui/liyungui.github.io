---
title: nginx使用
date: 2019-06-13 12:54:14
categories:
  - web
tags:
  - nginx
---

# 概念介绍

Nginx (engine x) 是一个**高性能**(占有内存少，并发能力强)**高可扩展**的 HTTP和反向代理web服务器，同时也提供了IMAP/POP3/SMTP服务。

高并发的情况下，Nginx是Apache服务不错的替代品

兼容性：Linux系统,Windows NT系统

# 版本选择

Nginx高性能，高可扩展。但并非指随便下载一款事先编译好的，就能满足要求，尤其是**不建议使用官方编译好的Windows版本**

## 官方编译的Windows版本基本事实：

1. 使用的是内生Win32 API，不是通过Cygwin的模拟层。

2. 仅用了select()连接方法，无缘高性能、高可扩展。

3. Nginx运行时有两种进程，一个是主进程，一个是工作进程。Windows版的，只有一个有效的工作进程，虽然你可以运行多个工作进程。

4. 没有windows服务进程版，计划在下个版本加入。


# 安装

## Mac版安装

1. 安装Command Line tools

`xcode-select --install`

2. 安装brew

`ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`

3. 安装nginx

`brew install nginx`

安装完毕的提示

```
==> Caveats
==> openssl
A CA file has been bootstrapped using certificates from the SystemRoots
keychain. To add additional certificates (e.g. the certificates added in
the System keychain), place .pem files in
  /usr/local/etc/openssl/certs

and run
  /usr/local/opt/openssl/bin/c_rehash

openssl is keg-only, which means it was not symlinked into /usr/local,
because Apple has deprecated use of OpenSSL in favor of its own TLS and crypto libraries.

If you need to have openssl first in your PATH run:
  echo 'export PATH="/usr/local/opt/openssl/bin:$PATH"' >> ~/.bash_profile

For compilers to find openssl you may need to set:
  export LDFLAGS="-L/usr/local/opt/openssl/lib"
  export CPPFLAGS="-I/usr/local/opt/openssl/include"

==> nginx
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:
  brew services start nginx
Or, if you don't want/need a background service you can just run:
  nginx

```

# 启动

`brew services start nginx`

访问 [http://localhost:8080/](http://localhost:8080/)

重启

`brew services restart nginx`
# 配置

## 配置文件

`/usr/local/etc/nginx/nginx.conf`

参考&扩展

- [官方文档](http://nginx.org/en/)



