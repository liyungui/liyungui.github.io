---
title: PHP教程
date: 2019-01-20 11:32:25
categories:
  - Web
tags:
  - PHP
---

# 简介

## PHP

Hypertext Preprocessor 超文本预处理器

是一种通用开源脚本语言

**弱类型语言**

## PHP 文件

- 默认文件扩展名是 ".php"
- 可包含文本、HTML、JavaScript代码和 PHP 代码
- PHP 代码在服务器上执行，结果以纯 HTML 形式返回给浏览器
PHP 文件

# 语法

## 基本语法

- PHP 脚本以 `<?php` 开始，以 `?> `结束：

```php
<?php
// PHP 代码
?>
```

- 代码行必须以分号结束

## 注释

```php
<?php
// 这是 PHP 单行注释

/*
这是 
PHP 多行
注释
*/
```

# 变量

## 命名规则

- **以 $ 符号开始**，后面跟变量名称
- 变量名称以字母或者下划线开始
- 变量名称只能包含字母数字字符以及下划线（A-z、0-9 和 _ ）
- 变量名称区分大小写

## 创建/声明

弱类型语言，而且没有声明变量的命令。

变量在第一次赋值时被创建

## 作用域

- local 函数内可见
- global 函数外可见。函数内可以使用 `global`关键字访问
- static 使局部变量不被删除
- parameter 函数参数，函数内可见

### 全局变量

全局变量存储在一个名为 **$GLOBALS**[index] 的数组中。 index 保存变量的名称。这个数组可以在函数内部访问

```php
<?php
$x=5;
$y=10;
 
function myTest(){
    global $x,$y;//函数内访问全局变量需要使用global关键字
    $y=$x+$y;
}
 
myTest();
echo $y; // 输出 15
?>
```

上面的实例可以写成这样：

```php
<?php
$x=5;
$y=10;
 
function myTest()
{
    $GLOBALS['y']=$GLOBALS['x']+$GLOBALS['y'];
} 
 
myTest();
echo $y;
?>
```

### static

使局部变量不被删除。每次调用该函数时，static变量将会保留着函数前一次被调用时的值。

```php
<?php
function myTest()
{
    static $x=0;//只在第一次函数调用时赋值，然后保留着函数前一次被调用时的值
    echo $x;
    $x++;
}
 
myTest();//0
myTest();//1
myTest();//2
?>
```

# 常量

- 常量名命名规则同变量名
	- 常量用 define 声明
	- 变量 $变量名	 
- 值不可变
- 全局作用局

```php
bool define ( string $name , mixed $value [, bool $case_insensitive = false ] )
```
默认大小写敏感


# 数据类型

## Integer（整型）

支持10进制，16进制 `0x8C`，8进制 `047`

## Float（浮点型）

## Boolean（布尔型） 

true, false

## String（字符串）

单引号，双引号

### 操作

#### 拼接

并置运算符 `.`

```php
<?php 
$txt1="Hello world!"; 
$txt2="What a nice day!"; 
echo $txt1 . " " . $txt2; 
?>
```

#### api

	strlen() 长度
	strpos() 子字符串在字符串中的位置。未找到返回 FALSE

### EOF(heredoc)

## Array（数组）

## Object（对象）

## NULL（空值） 

可以通过设置变量值为 NULL 来清空变量数据







