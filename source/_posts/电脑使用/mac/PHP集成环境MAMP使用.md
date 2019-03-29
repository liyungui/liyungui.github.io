---
title: PHP集成环境MAMP使用
date: 2019-01-09 14:41:53
categories:
  - 电脑使用
tags:
  - Mac
  - PHP
---

# 配置

## 配置mysql密码

### 修改mysql密码

`/Applications/MAMP/Library/bin/mysqladmin -u root -p password`

输入mysql密码，并且确认密码。就OK了

### 配置文件修改mysql密码

`/Applications/MAMP/bin/phpMyAdmin-X.X.X/config.inc.php`

找到 `$cfg[‘Servers’][$i][‘password’]`，修改密码。

