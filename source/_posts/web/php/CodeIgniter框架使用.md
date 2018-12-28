---
title: CodeIgniter框架使用
date: 2018-12-20 16:08:25
categories:
  - Web
tags:
  - PHP
---

小巧简单，上手容易，适用于小项目敏捷开发

MVC架构

# 快速上手

## 安装配置

1. [下载解压](https://codeigniter.org.cn/)
2. 配置。
	- 全局配置 `application/config/config.php` 
	- 数据库配置 `application/config/database.php`

## 工作原理

![](https://ss0.baidu.com/6ONWsjip0QIZ8tyhnq/it/u=206154531,2389930621&fm=173&s=00B0EC339E80BE01958CE540030070B2&w=639&h=188&img.JPEG)

- index.php 文件作为前端控制器，初始化运行 CodeIgniter 所需的基本资源； 
- Router 检查 HTTP 请求，以确定如何处理该请求； 如果存在缓存文件，将直接输出到浏览器，不用走下面正常的系统流程； 在加载应用程序控制器之前，对 HTTP 请求以及任何用户提交的数据进行安全检查； 控制器加载模型、核心类库、辅助函数以及其他所有处理请求所需的资源； 最后一步，渲染视图并发送至浏览器，如果开启了缓存，视图被会先缓存起来用于 后续的请求。

## 两个主要目录

- application目录：用于开发者编写相应的配置以及逻辑处理，开发者只需在这个目录下添加自己需要的开发文件。 
- system目录：框架的系统库，里面包括核心库，类库，辅助类库，数据库等，这些文件，开发者最好不要擅自修改。

## CI框架的MVC和数据库辅助类

### 控制器

application/controller 目录

开发者添加自己的controller 控制器控制器都要继承核心库里的基类 CI_Controller，它已获取到整个框架的核心类库对象，通过它基本可以调用CI框架下的核心方法。 

### 模型

application/models 目录

专门用来和数据库打交道的 PHP 类，开发者定义自己的模型类都要继承 模型基类 CI_Mode。当你在控制下调用模型，只需要下面一行代码就实例化了：$this->load->model('model_name'); 

### 视图 

application/controller 目录

视图用于显示在浏览器中

### 辅助函数

application/helpers 目录

开发者可以创建自己的辅助类，调用的方式与系统的辅助类一致。

### 数据库

CI框架封装了多种数据库驱动与连接方法，让你轻松配置就能连接上，且封装了一些查询构造器与生成查询结果，让代码看起来方便简洁

## API快速冒烟
分页获取用户列表，包含id，username,password

### 创建数据库和表

创建test库user表

create table user(
	id int primary key auto_increment,
	username varchar(20),
	password varchar(20)
);

### 创建控制类

创建文件 `application/controllers/Test.php`

```php
<?php
class User{
	public $id;
	public $username;
	public $password;
}

class Test extends CI_Controller {
    public function getUsers() {
		if(isset($_GET['page_size'])){
			$pageSize = $_GET['page_size'];
		}else{
			$pageSize = 10;
		}
		if(isset($_GET['page'])){
			$page = $_GET['page'];
		}else{
			$page = 0;
		}
		$startIndex = $page*$pageSize;
		$this->load->database(); //加载数据库类
		$sql = "SELECT * FROM user limit $startIndex, $pageSize";
		$query = $this->db->query($sql); //执行sql语句
		$rows = $query->custom_result_object('User'); //转换成数组
		$viewArray = array("jsonArray" => $rows);
		ob_start(); //开启缓存
		$this->load->view('json', $viewArray); //输出信息到json.php视图
		ob_end_flush(); //关闭缓存
		exit(); //退出
    }
}
?>
```

### 创建View视图

创建文件 `application/views/json.php`

```php
<?php
header('Content-type: application/json');//通信头设置
$outputarray = array('status' => 'OK', 'data' => $jsonArray);
echo json_encode($outputarray);//数组转json，然后echo输出
?>
```

### URL访问接口

CodeIgniter框架URL规则，上面接口的访问方法为
`http://localhost:8888/index.php/test/getusers?page=1`

规则 `host/index.php/controller/method?param`