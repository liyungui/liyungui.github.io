---
title: ES6-变量的解构赋值
date: 2018-07-30 17:41:20
tags:
	- JS
	- ES6
---

按照一定模式，从**数组和对象**中提取值，对变量进行赋值，这被称为**解构(Destructuring)**

等号右边的值不是对象或数组，就先将其转为对象。

# 数组的解构赋值 #

**数据结构具有 Iterator 接口，都可以采用数组形式的解构赋值**

**数组的元素是按次序排列的，变量的取值由它的位置决定；**

Set 结构，也可以使用数组的解构赋值

	let [x, y, z] = new Set(['a', 'b', 'c']);
	x // "a"

Generator 函数原生具有 Iterator 接口

	function* fibs() {
	  let a = 0;
	  let b = 1;
	  while (true) {
	    yield a;
	    [a, b] = [b, a + b];
	  }
	}
	
	let [first, second, third, fourth, fifth, sixth] = fibs();
	sixth // 5

数组解构

	let [a, b, c] = [1, 2, 3];

嵌套

	let [foo, [[bar], baz]] = [1, [[2], 3]];
	foo // 1
	bar // 2
	baz // 3
	
	let [ , , third] = ["foo", "bar", "baz"];
	third // "baz"
	
	let [x, , y] = [1, 2, 3];
	x // 1
	y // 3
	
	let [head, ...tail] = [1, 2, 3, 4];
	head // 1
	tail // [2, 3, 4]
	
	let [x, y, ...z] = ['a'];
	x // "a"
	y // undefined
	z // []

## 不完全解构 ##

	let [x, y] = [1, 2, 3];
	x // 1
	y // 2
	
	let [a, [b], d] = [1, [2, 3], 4];
	a // 1
	b // 2
	d // 4

## 解构不成功，变量的值就等于undefined。 ##

	let [foo] = [];
	let [bar, foo] = [1];

	以上两种情况都属于解构不成功，foo的值都会等于undefined。

## 等号的右边不是可遍历的结构，将会报错。 ##

	// 报错
	let [foo] = 1;
	let [foo] = false;
	let [foo] = NaN;
	let [foo] = undefined;
	let [foo] = null;
	let [foo] = {};

## 默认值 ##

**解构赋值允许指定默认值**

ES6 内部使用严格相等运算符（===），判断一个位置是否有值。所以，只有当一个数组成员**严格等于undefined，默认值才会生效**。

	let [foo = true] = [];
	foo // true
	
	let [x, y = 'b'] = ['a']; // x='a', y='b'

	let [x = 1] = [undefined];
	x // 1
	
	let [x = 1] = [null];
	x // null

如果默认值是一个表达式，那么这个**表达式是惰性求值的**，即只有在用到的时候，才会求值。

	function f() {
	  console.log('aaa');
	}
	
	let [x = f()] = [1];

	x能取到值，所以函数f根本不会执行

默认值可以引用解构赋值的其他变量，但该变量必须已经声明。

	let [x = 1, y = x] = [];     // x=1; y=1
	let [x = 1, y = x] = [2];    // x=2; y=2
	let [x = 1, y = x] = [1, 2]; // x=1; y=2
	let [x = y, y = 1] = [];     // ReferenceError: y is not defined

# 对象的解构赋值 #

**对象的属性没有次序，变量必须与属性同名，才能取到正确的值。**

对象的解构赋值的**内部机制**，是先找到同名属性，然后再赋给对应的变量。真正被赋值的是后者

完整形式：

	let { foo: foo, bar: bar } = { foo: "aaa", bar: "bbb" };
	foo // "aaa"
	bar // "bbb"

	let { foo: baz } = { foo: "aaa", bar: "bbb" };
	baz // "aaa"
	foo // error: foo is not defined

	foo是匹配的模式，baz才是变量。真正被赋值的是变量baz，而不是模式foo。

简写：

	let { foo, bar } = { foo: "aaa", bar: "bbb" };

嵌套

	let obj = {
	  p: [
	    'Hello',
	    { y: 'World' }
	  ]
	};
	
	let { p, p: [x, { y }] } = obj;
	x // "Hello"
	y // "World"
	p // ["Hello", {y: "World"}]

如果解构模式是嵌套的对象，而且子对象所在的父属性不存在，那么将会报错。

	// 报错
	let {foo: {bar}} = {baz: 'baz'};
	解构 foo属性对应的子对象的bar属性，报错。原因很简单，因为foo这时等于undefined，再取子属性就会报错

将一个**已经声明的变量用于解构赋值**，必须非常小心。**避免 JavaScript 将其解释为代码块**

	let x;
	{x} = {x: 1};// SyntaxError: syntax error
	
	let x;
	({x} = {x: 1});//不将大括号写在行首

## 很方便地将现有对象的方法，赋值到某个变量 ##

	let { log, sin, cos } = Math;
	将Math对象的对数、正弦、余弦三个方法，赋值到对应的变量上，使用起来就会方便很多。

## 对数组进行对象属性的解构 ##

**数组本质是特殊的对象**

	let arr = [1, 2, 3];
	let {0 : first, [arr.length - 1] : last} = arr;
	first // 1。 数组arr的0键对应的值是1
	last // 3。 2键，对应的值是3

# 字符串的解构赋值 #

字符串被转换成了一个类似数组的对象

	const [a, b, c, d, e] = 'hello';
	a // "h"
	b // "e"
	c // "l"
	d // "l"
	e // "o"

	let {length : len} = 'hello';
	len // 5

# 数值和布尔值的解构赋值 #

数值和布尔值，会先转为对象

	let {toString: s} = 123;
	s === Number.prototype.toString // true
	
	let {toString: s} = true;
	s === Boolean.prototype.toString // true

# undefined和null的解构赋值 #

undefined和null**无法转为对象**，所以对它们进行解构赋值，都会**报错**

	let { prop: x } = undefined; // TypeError
	let { prop: y } = null; // TypeError

# 函数参数的解构赋值 #

	function add([x, y]){
	  return x + y;
	}
	
	add([1, 2]); // 3

	传入参数的那一刻，数组参数就被解构成变量x和y。对于函数内部的代码来说，它们能感受到的参数就是x和y

示例

	[[1, 2], [3, 4]].map(([a, b]) => a + b);
	// [ 3, 7 ]

函数参数的解构也可以使用默认值

	//为变量x和y指定默认值
	function move({x = 0, y = 0} = {}) {
	  return [x, y];
	}
	
	move({x: 3, y: 8}); // [3, 8]
	move({x: 3}); // [3, 0]
	move({}); // [0, 0]
	move(); // [0, 0]
	
	//为函数move的参数指定默认值
	function move({x, y} = { x: 0, y: 0 }) {
	  return [x, y];
	}
	
	move({x: 3, y: 8}); // [3, 8]
	move({x: 3}); // [3, undefined]
	move({}); // [undefined, undefined]
	move(); // [0, 0]

# 圆括号问题 #

解构赋值虽然很方便，但是解析起来并不容易。对于编译器来说，一个式子到底是**模式，还是表达式**，没有办法从一开始就知道，必须解析到（或解析不到）等号才能知道。

由此带来的问题是，如果模式中出现圆括号怎么处理。ES6 的规则是，只要有**可能导致解构的歧义，就不得使用圆括号**。

但是，这条规则实际上不那么容易辨别，处理起来相当麻烦。因此，建议只要有可能，就不要在模式中放置圆括号。

## 不能使用圆括号的情况 ##

### 变量声明语句 ###

	let [(a)] = [1];

### 函数参数 ###

函数参数也属于变量声明

	function f([(z)]) { return z; }

### 赋值语句的模式 ###

	([a]) = [5];

## 可以使用圆括号的情况 ##

**赋值语句的非模式部分，可以使用圆括号**

- 赋值语句，而不是声明语句
- 非模式部分

	[(b)] = [3]; // 正确。模式是取数组的第一个成员，跟圆括号无关
	({ p: (d) } = {}); // 正确。模式是p，而不是d
	[(parseInt.prop)] = [3]; // 正确。模式是取数组的第一个成员，跟圆括号无关

# 用途 #

## 交换变量的值 ##

交换变量x和y的值

	let x = 1;
	let y = 2;
	
	[x, y] = [y, x];

## 从函数返回多个值 ##

函数只能返回一个值，如果要返回多个值，只能将它们放在数组或对象里返回。有了解构赋值，取出这些值就非常方便。

	// 返回一个数组
	function example() {
	  return [1, 2, 3];
	}
	let [a, b, c] = example();
	
	// 返回一个对象
	function example() {
	  return {
	    foo: 1,
	    bar: 2
	  };
	}
	let { foo, bar } = example();

## 函数参数的定义 ##

方便地将一组参数与变量名对应起来

	// 参数是一组有次序的值
	function f([x, y, z]) { ... }
	f([1, 2, 3]);
	
	// 参数是一组无次序的值
	function f({x, y, z}) { ... }
	f({z: 3, y: 2, x: 1});

## 函数参数的默认值 ##

## 提取 JSON 数据 ##

	let jsonData = {
	  id: 42,
	  status: "OK",
	  data: [867, 5309]
	};
	
	let { id, status, data: number } = jsonData;
	
	console.log(id, status, number);
	// 42, "OK", [867, 5309]

## 遍历 Map 结构 ##

任何部署了 Iterator 接口的对象，都可以用for...of循环遍历

Map 结构原生支持 Iterator 接口，配合变量的解构赋值，获取键名和键值就非常方便。

	const map = new Map();
	map.set('first', 'hello');
	map.set('second', 'world');
	
	for (let [key, value] of map) {
	  console.log(key + " is " + value);
	}
	// first is hello
	// second is world

	// 获取键名
	for (let [key] of map) {
	  // ...
	}
	
	// 获取键值
	for (let [,value] of map) {
	  // ...
	}

## 输入模块的指定方法 ##

const { SourceMapConsumer, SourceNode } = require("source-map");
