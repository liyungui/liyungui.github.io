---
title: JS教程
date: 2018-07-27 11:53:34
tags:
	- JS
---

# 语法 #

## 区分大小写 ##

## 变量是弱类型的 ##

## 变量可以不声明直接使用 ##

## 每行结尾的分号可有可无 ##

推荐书写分号

- 编码规范
- 没有分号在有些浏览器不能正确运行

## 注释与 Java、C 和 PHP 语言的注释相同 ##

	//this is a single-line comment
	
	/*this is a multi-
	line comment*/

## 括号表示代码块 ##

从 Java 中借鉴

	if (test1 == "red") {
	    test1 = "blue";
	    alert(test1);
	}

# 变量 #

- 弱类型
- 可以不声明直接使用

## 命名变量 ##

- 第一个字符必须是字母、下划线（_）或美元符号（$）
- 余下的字符还可以是数字字符

## 声明变量 ##

- 不一定要初始化
- 弱类型。
	- 无需明确的类型声明
	- 变量可以存放不同类型的值
- 同一个 var 语句定义的变量不必具有相同的类型

示例

	var test;
	var test = "hi";
	test = 55;
	var test = "hi", age = 25;

## 变量值 ##

- 原始值
	- 存储在栈（stack）中
	- **原始类型**
		- 5 种。即 Undefined、Null、Boolean、Number 和 String 
		- 占据空间是固定的。所以存在栈中
		- 在许多语言中，字符串都被看作引用类型，而非原始类型，因为字符串的长度是可变的。

- 引用值
	- 存储在堆（heap）中
	- 对象
	- 是一个指针（point），指向存储对象的内存处

### 原始类型 ###

#### Undefined 类型 ####

Undefined 类型只有一个值，即 undefined

变量未初始化时，该变量的默认值是 undefined

#### Null 类型 ####

另一种只有一个值的类型是 Null，它只有一个专用值 null，即它的字面量。值 undefined 实际上是从值 null 派生来的，因此 ECMAScript 把它们定义为相等的。

	alert(null == undefined);  //输出 "true"

#### typeof 运算符 ####

返回值：

- undefined - 变量是 Undefined 类型的
- boolean - 变量是 Boolean 类型的
- number - 变量是 Number 类型的
- string - 变量是 String 类型的
- object - 变量是一种引用类型或 Null 类型的
	- typeof 运算符对于 null 值会返回 "Object"实际上是 JavaScript 最初实现中的一个错误，然后被 ECMAScript 沿用了。现在，null 被认为是对象的占位符，从而解释了这一矛盾，但从技术上来说，它仍然是原始值。
	
### 引用类型 ###

ECMAScript 定义了“对象定义”，逻辑上等价于其他程序设计语言中的类。ECMA-262 中根本没有出现“类”这个词。所以精确的说，应该称为“对象”

# 运算符 #

## 一元运算符 ##

### delete ###

删除 对象中开发者定义的属性或方法的引用

	var o = new Object;
	o.name = "David";
	alert(o.name);	//输出 "David"
	delete o.name;
	alert(o.name);	//输出 "undefined"

	delete o.toString; //报错。 toString() 方法是原始的 ECMAScript 方法，不是开发者定义的

### void ###

对任何值返回 undefined。通常用于避免输出不应该输出的值

	<a href="javascript:void(window.open('about:blank'))">Click me</a>

# 流程控制 #

## if ##

	if（）{
	}else if(){
	}else{
	}

## switch ##

- 可以用于字符串，
- 可以不是常量值

示例

	var BLUE = "blue", RED = "red", GREEN  = "green";
	switch (sColor) {
	  case BLUE: alert("Blue");
	    break;
	  case RED: alert("Red");
	    break;
	  case GREEN: alert("Green");
	    break;
	  default: alert("Other");
	}

## 迭代 ##

	do{
	}while()

	while(){
	}

	for (var i = 0; i < iCount; i++) {
	  alert(i);
	}

	for (sProp in window) {
	  alert(sProp);
	}

## with ##

设置代码在特定对象中的作用域

**运行缓慢**，尤其是在已设置了属性值时。最好**避免使用**

	var sMessage = "hello";
	with(sMessage) {
	  alert(toUpperCase());	//输出 "HELLO"
	}

	调用 toUpperCase() 方法时，将检查该方法是否是本地函数。如果不是，它将检查伪对象 sMessage，看它是否为该对象的方法。成功找到了字符串 "hello" 的 toUpperCase() 方法。

# 函数 #

因为是弱类型

- 参数，不必声明类型，直接参数名
- 返回值，不必声明类型，直接return返回

示例

	function functionName(arg0, arg1, ... argN) {
	  statements
	}

## 参数使用 arguments 对象 ##

保存了函数所有参数

- ECMAScript 不会验证传递给函数的参数个数是否等于函数定义的参数个数
- 可以接受任意个数的参数（根据 Netscape 的文档，最多可接受 255 个）
- 遗漏的参数都会以 undefined 传递给函数，多余的函数将忽略

使用

- arguments.length 参数个数
- arguments[0] 第一个参数

### 模拟函数重载 ###

用 arguments 对象判断传递给函数的参数个数，即可模拟函数重载。

虽然不如重载那么好，不过已足以避开 ECMAScript 的这种限制。

	function doAdd() {
	  if(arguments.length == 1) {
	    alert(arguments[0] + 5);
	  } else if(arguments.length == 2) {
	    alert(arguments[0] + arguments[1]);
	  }
	}
	
	doAdd(10);	//输出 "15"
	doAdd(40, 20);	//输出 "60"

## 函数其实是 Function 对象 ##

- 函数实际上是对象
- 函数名只是指向函数对象的引用值
- 函数可以作为参数传递给另一个函数

### 用 Function 直接创建函数 ###

语法如下：

	var function_name = new Function(arg1, arg2, ..., argN, function_body)


- 参数必须是**字符串**
- 最后一个参数是函数主体（要执行的代码）
- **最好不要使用**
- 弊端：
	- **书写很困难**，因为参数都是字符串，需要就涉及到内部真正字符的转义
- 优势：
	- **帮助理解函数是引用类型**，传统方式定义的函数行为与用 Function 明确创建的函数行为是相同的

实例：用 Function 直接创建函数

	function sayHi(sName, sMessage) {
	  alert("Hello " + sName + sMessage);
	}
	sayHi("David", " Nice to meet you!");
	
	var sayHi = new Function("sName", "sMessage", "alert(\"Hello \" + sName + sMessage);");
	sayHi("David", " Nice to meet you!");

	function doAdd(iNum) {
	  alert(iNum + 20);
	}
	
	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	doAdd(10);	//输出 "20"

实例：理解函数只不过是一种引用类型

	function doAdd(iNum) {
	  alert(iNum + 20);
	}
	
	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	doAdd(10);	//输出 "20"。因为第二个函数重载了第一个函数

	如果以下面的形式重写该代码块，这个概念就清楚了：

	var doAdd = new Function("iNum", "alert(iNum + 20)");
	var doAdd = new Function("iNum", "alert(iNum + 10)");
	doAdd(10);
	doAdd 的值被改成了指向不同对象的指针。函数名只是指向函数对象的引用值

### 函数作为参数传递给另一个函数 ###

	function callAnotherFunc(fnFunction, vArgument) {
	  fnFunction(vArgument);
	}
	
	var doAdd = new Function("iNum", "alert(iNum + 10)");
	
	callAnotherFunc(doAdd, 10);	//输出 "20"

### Function 对象的 length 属性 ###

声明了函数期望的参数个数

	function sayHi() {
	  alert("Hi");
	}
	
	alert(sayHi.length);	//输出 "0"

### Function 对象的方法 ###

valueOf() 方法和 toString() 方法，返回的都是函数的源代码，在调试时尤其有用

	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	document.write(doAdd.toString());

## 闭包 closure ##

函数对象在变量作用域之外，访问变量。**改变了变量作用域**

全局变量是一个简单的闭包实例

	var sMessage = "hello world";

	function sayHelloWorld() {
	  alert(sMessage);
	}
	
	sayHelloWorld();

在一个函数中定义另一个

	var iBaseNum = 10;
	
	function addNum(iNum1, iNum2) {
	  function doAdd() {
	    return iNum1 + iNum2 + iBaseNum;
	  }
	  return doAdd();
	}

