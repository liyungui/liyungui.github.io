---
title: avada主题
date: 2019-10-09 18:11:14
categories:
  - web
tags:
  - wordpress
---

# 正版和盗版的区别

Avada盗版主题，是别人购买后分享出来的安装文件，没有激活密钥，可以正常安装，但没有以下权限：

- 许可证证书
- 购买代码（Purchase Code）
- 主题说明书
- 免费主题升级服务
- DEMO导入权限
- Avada社区账号使用权限
- Theme Fusion未来6个月的售后支持服务
- 向开发者提问的权限
- 主题bug和错误解决方案
- 新功能更新的通知等等

[Websoft9 Avada5.7.2 官方原版下载](http://libs.websoft9.com/apps/wordpress/wordpress5.0.2-avada5.7.2-en.tar.gz)

[avada完全汉化版 爱壹主题](http://iesay.com/avada-wordpress-theme-zh-cn/)

# 破解Avada主题

这里使用的是 Websoft9 Avada5.7.2 官方原版

共三处修改

Mac系统中搜索默认会搜索文件内容(Windows系统应该也有类似软件)

在 `Avada/include` 路径下，搜索 `envato` 关键字可以找到注册的相关文件

## 修改 `envato-api`返回

`wordpress/wp-content/themes/Avada/includes/lib/inc/class-fusion-envato-api.php`

**第一处修改** 注释掉以下两行

```php
$response_code    = wp_remote_retrieve_response_code( $response );
$response_message = wp_remote_retrieve_response_message( $response );
```	

详细代码逻辑

```php
/**
 * Query the Envato API.
 *
 * @access public
 * @uses wp_remote_get() To perform an HTTP request.
 * @since 1.0.0
 * @param  string $url API request URL, including the request method, parameters, & file type.
 * @param  array  $args The arguments passed to `wp_remote_get`.
 * @return array  The HTTP response.
 */
public function request( $url, $args = array() ) {
	$defaults = array(
		'headers' => array(
			'Authorization' => 'Bearer ' . $this->token,
			'User-Agent' => 'WordPress - Fusion Library',
		),
		'timeout' => 20,
		'headers_data' => false,
	);
	$args = wp_parse_args( $args, $defaults );

	if ( empty( $this->token ) ) {
		return new WP_Error( 'api_token_error', __( 'An API token is required.', 'Avada' ) );
	}

	// Make an API request.
	$response = wp_remote_get( esc_url_raw( $url ), $args );

	// Check the response code.
	$response_code    = wp_remote_retrieve_response_code( $response );
	$response_message = wp_remote_retrieve_response_message( $response );

	if ( empty( $response_code ) && is_wp_error( $response ) ) {
		return $response;
	}

	$envato_string = '';
	$headers = isset( $response['headers'] ) ? (array) $response['headers'] : array();

	if ( ! empty( $headers ) && isset( $headers[ "\0*\0" . 'data' ] ) ) {
		$headers_data = $headers[ "\0*\0" . 'data' ];
		$date = $headers_data['date'];
		$cf_ray = $headers_data['cf-ray'];

		$envato_string = '(Date: ' . $date . ' | CF-RAY: ' . $cf_ray . ')';
	}

	if ( 200 !== $response_code && ! empty( $response_message ) ) {
		return new WP_Error( $response_code, $response_message . $envato_string );
	}
	if ( 200 !== $response_code ) {
		return new WP_Error( $response_code, __( 'An unknown API error occurred.', 'Avada' ) );
	}
	...
}	
```
		
注释掉 `$response_code` 和 `$response_message`，就会返回未知API错误 `new WP_Error( $response_code, __( 'An unknown API error occurred.', 'Avada' )`

## 修改 `product-registration`判断逻辑

`wordpress/wp-content/themes/Avada/includes/lib/inc/class-fusion-product-registration.php`

**第二处修改，核心修改** `is_registered` 函数最后一行改为 `return true;`

**第三处修改** `product_exists` 函数 改 `set_site_transient( 'fusion_envato_api_down', true, 600 );` 改为 `set_site_transient( 'fusion_envato_api_down', true, 0 );`

详细代码逻辑

```php
/**
 * Checks if the product is part of the themes or plugins
 * purchased by the user belonging to the token.
 *
 * @access private
 * @since 1.0.0
 * @param string $token A token to check.
 * @param int    $page  The page number if one is necessary.
 * @return bool
 */
private function product_exists( $token = '', $page = '' ) {

	// Set the new token for the API call.
	if ( '' !== $token ) {
		$this->envato_api()->set_token( $token );
	}
	if ( 'theme' === $this->args['type'] ) {
		$products = $this->envato_api()->themes( array(), $page );
	} elseif ( 'plugin' === $this->args['type'] ) {
		$products = $this->envato_api()->plugins( array(), $page );
	}

	// If a WP Error object is returned we need to check if API is down.
	if ( is_wp_error( $products ) ) {

		// 401 ( unauthorized ) and 403 ( forbidden ) mean the token is invalid, apart from that Envato API is down.
		if ( 401 !== $products->get_error_code() && 403 !== $products->get_error_code() && '' !== $products->get_error_message() ) {
			set_site_transient( 'fusion_envato_api_down', true, 600 );
		}

		$this->envato_api_error = $products;
		return false;
	}

	// Check iv product is part of the purchased themes/plugins.
	foreach ( $products as $product ) {
		if ( isset( $product['name'] ) ) {
			if ( $this->args['name'] === $product['name'] ) {
				return true;
			}
		}
	}

	if ( 100 === count( $products ) ) {
		$page = ( ! $page ) ? 2 : $page + 1;
		return $this->product_exists( '', $page );
	}
	return false;
}
```

```php
/**
 * Has user associated with current token purchased this product?
 *
 * @access public
 * @since 1.0.0
 * @return bool
 */
public function is_registered() {

	// Get the option.
	$registered = get_option( 'fusion_registered' );

	// Is the product registered?
	if ( isset( $registered[ $this->product_id ] ) && true === $registered[ $this->product_id ] ) {
		return true;
	}

	// Is the Envato API down?
	if ( get_site_transient( 'fusion_envato_api_down' ) ) {
		return true;
	}

	// Fallback to false.
	return false;
}
```
	
[破解avada主题，100%有效](https://www.iesay.com/how-to-null-avada-wordpress-theme-100-working.html) 爱壹主题

# 主题相关的插件

Avada -- 插件，可以看到主题相关的插件

- Fusion Core（主题必装的核心插件，）
- Fusion Builder（主题必装的页面构建器）其他主题也能用；
- LayerSlider WP（高级幻灯片插件）激活主题才能安装
- Slider Revolution（高级幻灯片插件）激活主题才能安装
- Contact Form 7 （联系表单）可以方便用户在线留言，创建表单；
- Fusion White Label Branding： 主题品牌白标插件，也就是将主题与 avada 或后台 WordPress 有关的字符可以替换成你品牌词，一般用不上，给客户做项目时可以用。
- Convert Plus： 促销提高转化率的插件，类似访问某些网站会自动弹出窗口然后要求订阅或者显示广告那种；
- Advanced Custom Fields PRO： 高级自定义字段，开发用的，普通用户用不上；
- WooCommerce：电子商务系统；
- Yoast SEO： 目前 WordPress 最好的 SEO 插件；
- - bbPress：WordPress 简约论坛系统；
- The Events Calendar ：活动日历，比较适合需要用户互动或者在线订票等网站；

建议安装前面四个插件

# 设置英文网站字体

在  Avada – Theme Options 中，点击 Typography。

在 Body Typography 中，点击 Font Family 的下拉菜单，选择一个更好看的英文字体。国外使用较多的是 Roboto 或 Open Sans 字体。选好后，点击 Save Changes。

接着，Headers Typography 中，把 H1 – H 6，Post Title 的 Font Family 都选择 Roboto 或 Open Sans (下拉菜单那里可以直接输入字体名)

# 登录状态下，前台页面隐藏 Admin Bar

登录状态下浏览网站的时候，总是在顶部有条黑色的 admin bar 很烦人

在【Appearance】(外观) – 【Editor】里我们可以添加代码屏蔽。在右侧的 Templates 那里点击 functions.php 文件，然后粘贴下面代码：

```php
/**
 * 登录状态下，前台页面隐藏 Admin Bar
 */
function hide_admin_bar($flag) {
 return false;
}
add_filter('show_admin_bar', 'hide_admin_bar');

```

# 创建导航菜单

在做网站之前，最好你已经在网页收藏夹中收藏了5-10个非常不错的国外同行的网站了。你可以多看多借鉴一下页面结构，菜单频道和页面风格等。顶部菜单准备放哪些，哪些下面有二级菜单，这些都先想好。如果有时间的话，你应该至少在纸上或者 Xmind 文档上做过结构图，这样可以帮助你清晰地创建网站结构，你的网页 URL  结构也会很清晰。

{% asset_img website-menu-guide.png %}

【Appearance】(外观) – 【Menu】(菜单)

填写菜单名称（比如 “main-menu”），点击 “【Create Menu】（创建菜单）”

创建成功后，自动进入菜单编辑页面

{% asset_img create-menu-1.pn %}g

- 左侧是可以添加到菜单的内容
- 右侧顶部是菜单的结构（从左侧添加，可以上下拖拽排序，左右拖拽修改层级关系）
- 右侧底部是菜单设置（菜单显示位置）

## 菜单内容支持的类型

- Post。WordPress 是从博客系统发展成 CMS管理系统的，因此，WP 中最重要的类型就是 Post，而且多数的 WP 函数也是基于 post。
- Page。特殊类型的Post
- 自定义链接。链接锚文本（站内或站外链接，链接为空则点击不跳转，可以做下拉菜单的父级占位文字）
- 文章分类
- 等等

# 隐藏 Page Title Bar

页面（比如Home页面）编辑器页面，下方有 Fusion Page Options 区域

{% asset_img page-title-bar.png %}

Page Title Bar 显示每个页面的页面名，没什么用。

在 Page Title Bar 那里选择 Hide，不显示。

# 修改最底部的 Copyright 文字

Theme Options 搜索框里输入：copyright。发现是在 Footer Content 中设置版权信息。
 
修改 Copyright Text 即可
 
这里可以放置一些主要产品的锚文本，更利于 SEO。

比如我们看看 http://www.sanyglobal.com/ 三一重工的网站的底部 Copyright bar 是这样布局的：左侧版权信息，右侧是产品的tags链接锚文本

```
<p style="float:left">Copyright © 2011-2017 LSMK INDUSTRIAL CO., LTD. All RIGHTS RESERVED</p>
<p style="float:right">TAGS: 
<a href="http://www.ledlightsmfg.com/#">Product1</a>
<a href="http://www.ledlightsmfg.com/#">LedBulb2</a>
<a href="http://www.ledlightsmfg.com/#">Special3</a></p>
```
 
我们先用了3个锚文本 Product1, LedBulb2, Special3 来占位。等我们后面产品页做好以后，我们再修改具体的链接和锚文本文字。

# 用 LayerSlider 创建 Homepage Slider

WP后台左侧下方 LayerSlider WP -- Sliders --  add new slider

输入slider名字：Homepage Slider

页面顶部三个tag：slider settings、slides、event callbacks

## slider settings

layout -- Slider type & dimensions，选择 responsive（响应式，genuine设备屏幕自适应）

宽高根据图片实际尺寸填写

## slides

默认 slide #1 ，点击 add new，添加新的 slide #2， slide #3等

### slide options

slide background image 上传图片

Slide Timing 建议设置为 duration:3000，shift:1000

# 编辑首页

使用Avada 主题的编辑器 Fusion Builde

添加一个 1/1 的 Container (布局容器)

在Container里面点击 Element

在 Fusion Page Options 的 sliders 中选择 LayerSlider，在列表中选择之前创建的 homepage slider。

# 参考案例

- [三一重工官网](https://www.sanyglobal.com/)

# 参考&扩展

- [哪些网站是用Avada主题做的？Avada真实案例分享](https://www.1deng.me/avada-examples.html)
- [WordPress外贸建站,WordPress操作流程全攻略（详细图文教程）](https://www.liaosam.com/wordpress-build-website-operation.html)