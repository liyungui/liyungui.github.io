---
title: wp打开慢问题解决
date: 2019-10-06 16:35:14
categories:
  - web
tags:
  - wordpress
---

# Google Open Sans字体

## 后台

### 禁用字体

禁用 WordPress 后台的英文字体会变成你当前系统默认的

不好看

#### 插件禁用

Disable Google Fonts 或者 Remove Open Sans font Link from WP core

#### 代码禁用

没有使用WP自带的官方主题

添加下面的代码到当前所用的主题的 `functions.php`

```php
/**
 * WordPress 后台禁用Google Open Sans字体，加速网站
 * https://www.wpdaxue.com/disable-google-fonts.html
 */
add_filter( 'gettext_with_context', 'wpdx_disable_open_sans', 888, 4 );
function wpdx_disable_open_sans( $translations, $text, $context, $domain ) {
  if ( 'Open Sans font: on or off' == $context && 'on' == $text ) {
    $translations = 'off';
  }
  return $translations;
}
```

### 替换字体源

#### 插件

[DW Replace Open Sans插件](http://m.devework.com/files/dw-replace-open-sans.zip) 

#### 代码

添加到主题的 `functions.php` 文件中

```php
/**
 * Plugin Name: WPDX Replace Open Sans
 * Plugin URI:  https://www.wpdaxue.com/dw-replace-open-sans.html
 * Description: 将WordPress 后台和登录界面的open-sans字体加载源从Google Fonts替换为360的CDN加载源。
 * Author:      Changmeng Hu
 * Author URI:  https://www.wpdaxue.com/
 * Version:     1.0
 * License:     GPL
 */
function wpdx_replace_open_sans() {
  wp_deregister_style('open-sans');
  wp_register_style( 'open-sans', '//fonts.useso.com/css?family=Open+Sans:300italic,400italic,600italic,300,400,600' );
  if(is_admin()) wp_enqueue_style( 'open-sans');
}
add_action( 'init', 'wpdx_replace_open_sans' );
```
# 参考&扩展

- [WordPress 后台禁用Google Open Sans字体，加速网站](https://www.wpdaxue.com/disable-google-fonts.html)
- [将WordPress后台的open-sans字体加载源从Google Fonts换为360 CDN](https://www.wpdaxue.com/dw-replace-open-sans.html)