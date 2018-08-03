---
title: ES6-class
date: 2018-08-02 10:34:20
tags:
	- JS
	- ES6
---

# 定义和使用 #

- **语法糖**。更像面向对象编程的语法而已
- **本质是函数**。可以看作构造函数的另一种写法
	- 但是**只能通过new调用**
- 属性。
	- 默认定义在原型上
	- 可以显式定义在其本身
		- 即定义在this对象上
- 方法定义前不需要function关键字
	- 类内定义的方法，都是不可枚举的
- **constructor()**
	- 类的默认方法
		- 没有显式定义，自动生成一个空实现
	- new对象实例时，自动调用该方法
	- 默认返回实例对象。不需要显式返回
		- 可以强制return其他对象
- **严格模式**
	- 类和模块的内部，默认就是严格模式
	- 所有的代码，其实都是运行在模块之中，所以 ES6 实际上把整个语言升级到了严格模式。
- **所有实例共享一个原型对象**
- **不存在变量提升**。 先定义，后使用
	- 此规定能保证子类在父类之后定义

实例：

	class Point {
	  constructor(x, y) {
	    this.x = x;
	    this.y = y;
	  }
	  toString() {
	    return '(' + this.x + ', ' + this.y + ')';
	  }
	}
	
	typeof Point // "function"
	Point === Point.prototype.constructor // true

	Object.keys(Point.prototype)
	// []
	Object.getOwnPropertyNames(Point.prototype)
	// ["constructor","toString"]

	point.hasOwnProperty('x') // true
	point.hasOwnProperty('y') // true
	point.hasOwnProperty('toString') // false
	point.__proto__.hasOwnProperty('toString') // true

实例：所有实例共享一个原型对象

	var p1 = new Point(2,3);
	var p2 = new Point(3,2);
	p1.__proto__ === p2.__proto__
	//true

## 匿名类 ##

	let person = new class {
	  constructor(name) {
	    this.name = name;
	  }
	
	  sayName() {
	    console.log(this.name);
	  }
	}('张三');
	person.sayName(); // "张三"

## 私有属性 ##

**ES6 不支持私有属性**

### 现有方案 ###

#### 约定前缀下划线表示私有 ####

#### 将方法移出模块 ####

因为模块内部的所有方法都是对外可见

	class Widget {
	  foo (baz) {
	    bar.call(this, baz);
	  }
	}
	function bar(baz) {
	  return this.snaf = baz;
	}
	bar实际上成为了当前模块的私有方法

#### 命名为一个Symbol值 ####

利用Symbol值的唯一性

	const bar = Symbol('bar');
	const snaf = Symbol('snaf');
	export default class myClass{
	  [bar](baz) {
	    return this[snaf] = baz;
	  }
	};

	bar和snaf都是Symbol值，导致第三方无法获取到它们
	因此达到了私有方法和私有属性的效果

### 私有属性的提案 ###

**使用#前缀表示私有属性**

- 没有采用private关键字，是因为 JavaScript 是动态语言，使用独立的符号似乎是唯一的可靠方法

实例

	class Foo {
	  #a;
	  #b;
	  #sum() { return #a + #b; }
	  constructor(a, b) { #a = a; #b = b; }
	}

# 静态方法 #

- 方法前，加上static关键字
- 直接通过类来调用
- 不会被实例继承
	- 在实例上调用静态方法，会抛出一个不存在该方法错误
- 静态方法中this关键字指的是类
- 可以被子类继承

ES6 明确规定，Class 内部只有静态方法，**没有静态属性**

# new.target 属性 #

**返回new命令作用于的构造函数**

- **返回值就是当前类**。子类继承父类时，返回**子类**
	- **类中**调用：类严格等于构造函数。类本质是函数，是构造函数的另一种写法
	- **函数中**调用：函数也是对象。
- 构造函数不是通过new命令调用的，new.target会返回**undefined**

实例

	function Person(name) {
	  if (new.target === Person) {
	    this.name = name;
	  } else {
	    throw new Error('必须使用 new 命令生成实例');
	  }
	}

	class Rectangle {
	  constructor(length, width) {
	    console.log(new.target === Rectangle); //true
	    this.length = length;
	    this.width = width;
	  }
	}

	class Square extends Rectangle {
	  constructor(length) { //false。返回的是子类
	    super(length, length);
	  }
	}	

# 继承 #

## extends ##

**通过extends关键字实现继承**

- 必须在constructor()中调用super方法
- 调用super之后，才可以使用this关键字

## Object.getPrototypeOf() ##

**获取父类**

	Object.getPrototypeOf(ColorPoint) === Point
	// true

# 原生构造函数的继承 #

## 原生构造函数 ##

**语言内置的构造函数，通常用来生成数据结构**

大致有下面这些。

- Object()
- Boolean()
- Number()
- String()
- Array()
- Date()
- Function()
- RegExp()
- Error()

## 继承的实现 ##

ES5 的继承，实质是**先创造子类的实例对象this**，然后再将父类的方法添加到this上面（Parent.apply(this)）。

ES6 的继承机制完全不同，实质是**新建父类的实例对象this**（所以必须先调用super方法），然后再用子类的构造函数修改this

## 原生构造函数的继承 ##

### ES5无法继承 ###

子类无法获得原生构造函数的内部属性，通过Array.apply()或者分配给原型对象都不行。原生构造函数会忽略apply方法传入的this，也就是说，原生构造函数的this无法绑定，导致拿不到内部属性。

ES5 是先新建子类的实例对象this，再将父类的属性添加到子类上，由于父类的内部属性无法获取，导致无法继承原生的构造函数。

### ES6允许继承原生构造函数 ###

**继承Object的子类，有一个行为差异。**

ES6 改变了Object构造函数的行为，一旦发现Object方法不是通过new Object()这种形式调用，Object构造函数会忽略参数。

	class NewObj extends Object{
	  constructor(){
	    super(...arguments);
	  }
	}
	var o = new NewObj({attr: true});
	o.attr === true  // false

# Mixin 模式的实现 #

**Mixin 指的是多个对象合成一个新的对象，新对象具有各个组成成员的接口**

实例：最简单实现

	const a = {
	  a: 'a'
	};
	const b = {
	  b: 'b'
	};
	const c = {...a, ...b}; // {a: 'a', b: 'b'}


