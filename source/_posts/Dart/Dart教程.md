---
title: Dart教程
date: 2018-06-29 15:00:04
tags:
	- Dart
	- Flutter
---

# A basic Dart program #

	printInteger(int aNumber) {
	  print('The number is $aNumber.'); // Print to console.
	}
	
	main() {//程序入口
	  var number = 42; // Declare and initialize a variable.
	  printInteger(number); // Call a function.
	}

# Important concepts #

- **万物皆对象。包括 函数 null。** 
	- `Object`是最顶层基类
	- 很多语言，函数都是一级对象(first-class objects)，如Ruby，Python
- 支持类型推断。虽然Dart是强类型语言
- 支持泛型
- 支持嵌套函数。create functions within functions (nested or local functions)
- 下划线前缀表示private to its library。没有作用域关键字`public, protected, and private`
- 精确区分`表达式和语句块(expression and statement)`
- The `new` keyword became optional in Dart 2. 

# Variables #
	
	String name = 'Bob';
	var name = 'Bob';//自动推断，String类型。局部变量建议使用此方式
	dynamic name = 'Bob';//动态类型
	Object name = 'Bob';//同上

- 变量保存引用

## 默认值 ##

默认值为null。即使是数字类型，因为Dart万物皆对象

## final and const ##

- final
	- 只允许赋值一次
- const
	- 编译时常量
	- 较弱的final
	- 成员变量不能声明为const

示例

	final name = 'Bob'; // Without a type annotation
	final String nickname = 'Bobby';

# Built-in types #

## num ##

- int。最长 64 bits。转为JavaScript 最长54位
- double。 64位

## Strings ##

- `var s = 'string interpolation';`
- ` ${s}` 引用字符串
- `==` 比较内容是否一致
- `+` 拼接字符串
- `'''多行字符串'''`
- raw String。 `var s = r"In a raw string, even \n isn't special.";`

## bool ##

##  List ##

	var list = [1, 2, 3];
	list[0] = 1;

## Map ##

	var gifts = {
	  // Key:    Value
	  'first': 'partridge',
	  'second': 'turtledoves',
	  'fifth': 'golden rings'
	};
	gifts['first'] = 'partridge';
	
	var nobleGases = {
	  2: 'helium',
	  10: 'neon',
	  18: 'argon',
	};
	nobleGases[2] = 'helium';

## Runes ##

UTF-32 code points of a string

## Symbol ##

代表一个操作或者符号

获取一个Symbol `#bar`

# Function #

	bool isNoble(int atomicNumber) {
	  return _nobleGases[atomicNumber] != null;
	}

- 返回值可省略。不建议省略
- 函数体只有一个表达式。简写
	-  `bool isNoble(int atomicNumber) => _nobleGases[atomicNumber] != null;`
	-  The => notation is sometimes referred to as fat arrow syntax.
	- Dart严格区分表达式和语句块，支持单表达式简写
		- if 语句块 不支持
		- 条件表达式 支持

## Optional parameters ##

### Optional named parameters ###

	void enableFlags({bool bold, bool hidden}) {
	  // ...
	}

### Optional positional parameters ###

	String say(String from, String msg, [String device]) {
	  var result = '$from says $msg';
	  if (device != null) {
	    result = '$result with a $device';
	  }
	  return result;
	}

### Default parameter values for Optional parameters ###

默认值必须为 compile-time constants

	void enableFlags({bool bold = false, bool hidden = false}) {
	  // ...
	}

## The main() function ##

入口函数

- returns void 
- has an optional `List<String> parameter` for arguments

## Functions as first-class objects 函数作为对象 ##

作为函数参数

	void printElement(int element) {
	  print(element);
	}
	
	var list = [1, 2, 3];
	
	// Pass printElement as a parameter.
	list.forEach(printElement);

作为变量值

	var loudify = (msg) => '!!! ${msg.toUpperCase()} !!!';
	assert(loudify('hello') == '!!! HELLO !!!');
	匿名函数 + 简写

## Anonymous functions ##

有时又称 closures

	([[Type] param1[, …]]) { 
	  codeBlock; 
	}; 

示例

	var list = ['apples', 'bananas', 'oranges'];
	list.forEach((item) {
	  print('${list.indexOf(item)}: $item');
	});

	单表达式，简写
	list.forEach(
    	(item) => print('${list.indexOf(item)}: $item'));


## closures 闭包 ##

匿名函数的一种，匿名函数对象在变量作用域之外，访问变量。改变了变量作用域

	Function makeAdder(num addBy) {//闭包改变addBy的作用域
	  return (num i) => addBy + i;
	}
	
	void main() {
	  // Create a function that adds 2.
	  var add2 = makeAdder(2);
	
	  // Create a function that adds 4.
	  var add4 = makeAdder(4);
	
	  assert(add2(3) == 5);
	  assert(add4(3) == 7);
	}

# Classes #

## Instance variables ##

	class Point {
	  num x;
	  num y = 0;//创建对象就初始化这个成员变量值，before the constructor and its initializer list execute
	}
	
	void main() {
	  var point = Point();
	  point.x = 4; // Use the setter method for x.
	}

- 所有成员变量 自动/隐式(implicit)生成 getter方法. 
- Non-final成员变量 自动/隐式(implicit)生成  setter方法

## Constructors ##

- 和类名同名函数，自动调用父类的默认构造函数(如果没有手动调用父类其他构造函数)
- 默认构造函数(unnamed, no-argument)。如果没有声明构造函数，会自动生成一个无参构造函数
- 构造函数不会自动继承。可以手动复写
- 初始化顺序
	- initializer list。用来初始化final成员变量很方便(handy)
	- superclass’s no-arg constructor
	- main class’s no-arg constructor
	- 构造函数body
- 先于自身构造函数执行的代码无法访问成员变量/成员方法/this。比如上面的：initializer list的赋值，传递给父类构造函数参数的值

示例

	class Point {
	  num x, y;
	
	  Point(num x, num y) {
	    this.x = x;//变量名冲突，所以加this.
	    this.y = y;
	  }
	}

	class Point {
	  num x, y;
	
	  Point(this.x, this.y);// Syntactic sugar for setting x and y, before the constructor body runs.
	}


### Named constructors ###

	class Point {
	  num x, y;
	
	  Point(this.x, this.y);
	
	  // Named constructor
	  Point.origin() {
	    x = 0;
	    y = 0;
	  }
	}

### Invoking constructors ###

#### Invoking a non-default superclass constructor ####

	构造函数：父类构造函数{
	}

示例

	class Person {
	  String firstName;
	
	  Person.fromJson(Map data) {
	    print('in Person');
	  }
	}
	
	class Employee extends Person {
	  Employee.fromJson(Map data) : super.fromJson(data) {
	    print('in Employee');
	  }
	}
	
	main() {
	  var emp = new Employee.fromJson({});
	}

	输出
		in Person
		in Employee

示例2

	class Employee extends Person {
	  Employee() : super.fromJson(getDefaultData());
	  // ···
	}

#### Redirecting constructors ####

	class Point {
	  num x, y;
	
	  Point(this.x, this.y); // The main constructor for this class.
	
	  Point.alongXAxis(num x) : this(x, 0); // Delegates to the main constructor.
	}

### Initializer list ###

	构造函数:Initializer1,Initializer2{
	}

示例

	Point.fromJson(Map<String, num> json)
	    : x = json['x'],
	      y = json['y'] {
	  print('In Point.fromJson(): ($x, $y)');
	}

示例2：初始化final成员变量，很方便

	import 'dart:math';
	
	class Point {
	  final num x;
	  final num y;
	  final num distanceFromOrigin;
	
	  Point(x, y)
	      : x = x,
	        y = y,
	        distanceFromOrigin = sqrt(x * x + y * y);
	}
	
	main() {
	  var p = new Point(3, 4);
	  print(p.distanceFromOrigin);
	}

	输出 5.0


### Constant constructors ###

define a const constructor and make sure that all instance variables are final

	class ImmutablePoint {
	  static final ImmutablePoint origin =
	      const ImmutablePoint(0, 0);
	
	  final num x, y;
	
	  const ImmutablePoint(this.x, this.y);
	}

### Factory constructors ###

factory修饰构造函数，返回一个缓存对象或者子类对象

	class Logger {
	  final String name;
	  bool mute = false;
	
	  // _cache is library-private
	  static final Map<String, Logger> _cache = <String, Logger>{};
	
	  factory Logger(String name) {
	    if (_cache.containsKey(name)) {
	      return _cache[name];
	    } else {
	      final logger = Logger._internal(name);
	      _cache[name] = logger;
	      return logger;
	    }
	  }
	
	  Logger._internal(this.name);
	
	  void log(String msg) {
	    if (!mute) print(msg);
	  }
	}

## Using class members ##

	var p = Point(2, 2);
	
	p.y = 3;// Set the value of the instance variable y.
	
	p?.y = 4;// If p is non-null, set its y value to 4.

# `mixins`复用 #

mixins是一种方便重用一个类的代码的方法。给类添加新的功能

使用`with` 关键字来实现mixins的功能。

	class Musician extends Performer with Musical {
	  // ...
	}