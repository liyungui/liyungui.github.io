---
title: ES6-函数的扩展
date: 2018-07-31 10:39:20
tags:
	- JS
	- ES6
---

# 函数参数的默认值 #

ES6 允许为函数的参数设置默认值，即直接写在参数定义的后面。

	function log(x, y = 'World') {
	  console.log(x, y);
	}
	
	log('Hello') // Hello World
	log('Hello', 'China') // Hello China
	log('Hello', '') // Hello

使用参数默认值时，函数不能有同名参数

	// 不报错
	function foo(x, x, y) {
	  // ...
	}
	
	// 报错
	function foo(x, x, y = 1) {
	  // ...
	}
	// SyntaxError: Duplicate parameter name not allowed in this context

参数默认值是惰性求值的

	let x = 99;
	function foo(p = x + 1) {
	  console.log(p);
	}
	
	foo() // 100
	
	x = 100;
	foo() // 101

## 参数默认值的位置 ##

- 函数的尾参数有默认值，可以省略
- 其他位置，不能省略。显式输入undefined

示例

// 例一
function f(x = 1, y) {
  return [x, y];
}

	f() // [1, undefined]
	f(2) // [2, undefined])
	f(, 1) // 报错
	f(undefined, 1) // [1, 1]

## 函数的 length 属性 ##

指定了默认值以后，函数的length属性，将返回没有指定默认值的参数个数。也就是说，指定了默认值后，length属性将失真。

## 作用域 ##

一旦设置了参数的**默认值**，函数进行声明**初始化**时，参数会形成一个**单独的作用域**（context）。等到初始化结束，这个作用域就会消失。这种语法行为，在不设置参数默认值时，是不会出现的。

	var x = 1;
	function f(x, y = x) {
	  console.log(y);
	}
	f(2) // 2
	调用函数f时，参数形成一个单独的作用域。
	在这个作用域里面，默认值变量x指向第一个参数x，而不是全局变量x，所以输出是2。

	let x = 1;
	function f(y = x) {
	  let x = 2;
	  console.log(y);
	}
	f() // 1

	function f(y = x) {
	  let x = 2;
	  console.log(y);
	}
	f() // ReferenceError: x is not defined

如果参数的默认值是一个函数，该函数的作用域也遵守这个规则

	let foo = 'outer';
	
	function bar(func = () => foo) {
	  let foo = 'inner';
	  console.log(func());
	}
	
	bar(); // outer

## 指定参数是否可以省略 ##

不得省略，如果省略就抛出一个错误

	function throwIfMissing() {
	  throw new Error('Missing parameter');
	}
	
	function foo(mustBeProvided = throwIfMissing()) {
	  return mustBeProvided;
	}
	
	foo()
	// Error: Missing parameter

	参数mustBeProvided的默认值等于throwIfMissing函数的运行结果（注意函数名throwIfMissing之后有一对圆括号），这表明参数的默认值不是在定义时执行，而是在运行时执行。

将参数默认值设为undefined，表明这个参数是可以省略的。

	function foo(optional = undefined) { ··· }

# rest 参数 #

- 形式为 `...变量名`
	- 用于获取函数的多余参数，这样就不需要使用arguments对象了。
	- 是一个数组
		- arguments对象不是数组，而是一个类似数组的对象。
		- 所以为了使用数组的方法，必须使用Array.prototype.slice.call先将其转为数组。
- 只能是最后一个参数
- 函数的length属性，不包括 rest 参数

实例

	function add(...values) {
	  let sum = 0;
	  for (var val of values) {
	    sum += val;
	  }
	  return sum;
	}
	
	add(2, 5, 3) // 10

实例：rest 参数代替arguments变量

	// arguments变量的写法
	function sortNumbers() {
	  return Array.prototype.slice.call(arguments).sort();
	}
	
	// rest参数的写法
	const sortNumbers = (...numbers) => numbers.sort();

# 严格模式 #

从 ES5 开始，函数内部可以设定为严格模式。

ES2016 规定只要函数参数使用了默认值、解构赋值、或者扩展运算符，那么函数内部就不能显式设定为严格模式，否则会报错。

- 函数内部的严格模式，同时适用于函数体和函数参数。
- 函数先执行函数参数，再执行函数体。
- 这就有一个不合理的地方，只有从函数体之中，才能知道参数是否应该以严格模式执行，但是参数却应该先于函数体执行

两种方法可以规避这种限制

- 设定全局性的严格模式
- 把函数包在一个无参数的立即执行函数里面

代码

	'use strict';
	function doSomething(a, b = a) {
	  // code
	}

	const doSomething = (function () {
	  'use strict';
	  return function(value = 42) {
	    return value;
	  };
	}());

# name 属性 #

函数的name属性，返回该函数的函数名

将一个匿名函数赋值给一个变量，ES5 的name属性，会返回空字符串，而 ES6 的name属性会返回实际的函数名。

	var f = function () {};
	
	// ES5
	f.name // ""
	
	// ES6
	f.name // "f"

# 箭头函数 #

## 基本使用 ##

ES6 允许使用“箭头”（=>）定义函数

	(参数)=>{代码行;
			return 返回值;}

- 省略 function 关键字
- 如果参数个数=1，省略小括号
- 如果函数体代码行=1，省略大括号和return
- 参数支持变量解构
- 如果箭头函数**返回对象**，必须在**对象外面加上括号**，否则会报错
	- 因为 大括号被解释为代码块

实例

	var sum = (num1, num2) => { return num1 + num2; }

	var f = v => v;
	// 等同于
	var f = function (v) {
	  return v;
	};

	var f = () => 5;
	// 等同于
	var f = function () { return 5 };
	
	var sum = (num1, num2) => num1 + num2;
	// 等同于
	var sum = function(num1, num2) {
	  return num1 + num2;
	};

	const full = ({ first, last }) => first + ' ' + last;
	// 等同于
	function full(person) {
	  return person.first + ' ' + person.last;
	}

	//返回对象，在对象外面加上括号
	let getTempItem = id => ({ id: id, name: "Temp" });

	let foo = () => { a: 1 };
	foo() // undefined
	始意图是返回一个对象{ a: 1 }，但是由于引擎认为大括号是代码块，所以执行了一行语句a: 1。这时，a被解释为语句的标签，因此实际执行的语句是1;，然后函数就结束了，没有返回值

实例：rest 参数与箭头函数结合
	
	const numbers = (...nums) => nums;
	numbers(1, 2, 3, 4, 5)
	// [1,2,3,4,5]
	
	const headAndTail = (head, ...tail) => [head, tail];
	headAndTail(1, 2, 3, 4, 5)
	// [1,[2,3,4,5]]

## 注意点 ##

- 函数体内的**this对象指向不可变**
	- 就是**定义时所在的对象**，而不是使用时所在的对象。
		- 箭头函数根本没有自己的this，导致内部的this就是外层代码块的this。正是因为它没有this，所以也就不能用作构造函数
		- 箭头函数可以绑定this对象，大大减少了显式绑定this对象的写法（call、apply、bind）
	- 有**利于封装回调函数**
- 不可以当作构造函数
	- 不可以使用new命令，否则会抛出一个错误。
- 不可以使用arguments对象
	- 该对象在函数体内不存在。如果要用，可以用 rest 参数代替。
- 不可以使用yield命令，因此箭头函数不能用作 Generator 函数。

箭头函数转成 ES5 的代码如下，转换后的 ES5 版本清楚地说明了，箭头函数里面根本没有自己的this，而是引用外层的this

	// ES6
	function foo() {
	  setTimeout(() => {
	    console.log('id:', this.id);
	  }, 100);
	}
	
	// ES5
	function foo() {
	  var _this = this;
	  setTimeout(function () {
	    console.log('id:', _this.id);
	  }, 100);
	}

## 箭头函数嵌套 ##

# 函数绑定”（function bind）运算符 #

将对象绑定到函数上面

- 两个冒号（::） `对象::函数`
	- 对象为空，将方法绑定在该对象上
	- 运算结果为对象，可以采用链式写法
- 用来取代call、apply、bind调用

实例：

	foo::bar;
	// 等同于
	bar.bind(foo);

	let log = ::console.log;
	// 等同于
	var log = console.log.bind(console);

	import { map, takeWhile, forEach } from "iterlib";
	getPlayers()
	::map(x => x.character())
	::takeWhile(x => x.strength > 100)
	::forEach(x => console.log(x));

# 尾调用优化 #

## 尾调用(Tail Call) ##

- 函数式编程的一个重要概念，
- 某个函数的最后一步是调用另一个函数

实例：

	//尾调用
	function f(x){
	  return g(x);
	}

	//函数m和n都属于尾调用
	function f(x) {
	  if (x > 0) {
	    return m(x)
	  }
	  return n(x);
	}


	//非尾调用。调用函数g之后，还有赋值操作
	function f(x){
	  let y = g(x);
	  return y;
	}
	
	//非尾调用。调用函数g之后，还有加法操作
	function f(x){
	  return g(x) + 1;
	}
	
	//非尾调用。调用函数g之后，还有return undefined;
	function f(x){
	  g(x);
	}

## 调用帧和调用栈 ##

函数调用会在内存形成一个“调用记录”，又称“**调用帧**”（call frame），保存调用位置和内部变量等信息。

所有的调用帧，就形成一个“**调用栈**”（call stack）

## 尾调用优化(Tail call optimization) ##

**直接用内层函数的调用帧，取代外层函数的调用帧。这将大大节省内存**

- 只在严格模式下有效
	- 正常模式下，函数内部有两个变量，可以跟踪函数的调用栈
		- func.arguments：返回调用时函数的参数。
		- func.caller：返回调用当前函数的那个函数。
	- 尾调用优化发生时，函数的调用栈会改写，因此上面两个变量就会失真。
	- 严格模式禁用这两个变量

因为尾调用是函数的最后一步操作，**一般**调用位置、内部变量等信息都不会再用到了，不需要保留外层函数的调用帧。

	function f() {
	  let m = 1;
	  let n = 2;
	  return g(m + n);
	}
	f();
	
	// 等同于
	function f() {
	  return g(3);
	}
	f();
	
	// 等同于
	g(3);

	不需要保存内部变量m和n的值、g的调用位置等信息，所以执行到最后一步，完全可以删除f(x)的调用帧，只保留g(3)的调用帧

实例：无法进行“尾调用优化”

内层函数inner用到了外层函数addOne的内部变量one

	function addOne(a){
	  var one = 1;
	  function inner(b){
	    return b + one;
	  }
	  return inner(a);
	}

## 尾递归 ##

函数调用自身，称为递归。如果**尾调用自身**，就称为尾递归。

递归非常耗费内存，因为需要同时保存成千上百个调用帧，很容易发生“栈溢出”错误（stack overflow）。但对于尾递归来说，由于只存在一个调用帧，所以永远不会发生“栈溢出”错误

### 递归函数的改写 ###

尾递归的实现，往往需要改写递归函数，确保最后一步只调用自身。

做到这一点的方法，就是把**所有用到的内部变量改写成函数的参数**。

**缺点：不太直观**

实例：n的阶乘

阶乘函数 factorial 需要用到一个中间变量total，那就把这个中间变量改写成函数的参数。

这样做的缺点就是不太直观，第一眼很难看出来，为什么计算5的阶乘，需要传入两个参数5和1？

	//最多需要保存n个调用记录，复杂度 O(n) 
	function factorial(n) {
	  if (n === 1) return 1;
	  return n * factorial(n - 1);
	}
	factorial(5) // 120
	
	//改写成尾递归，只保留一个调用记录，复杂度 O(1) 
	function factorial(n, total) {
	  if (n === 1) return total;
	  return factorial(n - 1, n * total);
	}
	factorial(5, 1) // 120

实例：Fibonacci 数列

	function Fibonacci (n) {
	  if ( n <= 1 ) {return 1};
	  return Fibonacci(n - 1) + Fibonacci(n - 2);
	}
	Fibonacci(10) // 89
	Fibonacci(100) // 堆栈溢出
	Fibonacci(500) // 堆栈溢出

	//尾递归优化
	function Fibonacci2 (n , ac1 = 1 , ac2 = 1) {
	  if( n <= 1 ) {return ac2};
	
	  return Fibonacci2 (n - 1, ac2, ac1 + ac2);
	}
	Fibonacci2(100) // 573147844013817200000
	Fibonacci2(1000) // 7.0330367711422765e+208
	Fibonacci2(10000) // Infinity

### 尾递归的优雅实现 ###

#### 柯里化(currying) ####

尾递归函数之外，再提供一个正常形式的函数

	function tailFactorial(n, total) {
	  if (n === 1) return total;
	  return tailFactorial(n - 1, n * total);
	}
	
	function factorial(n) {
	  return tailFactorial(n, 1);
	}
	
	factorial(5) // 120

柯里化

- 函数式编程的一个概念
- 意将多参数的函数转换成单参数的形式。

代码

	function tailFactorial(n, total) {
	  if (n === 1) return total;
	  return tailFactorial(n - 1, n * total);
	}
	
	function currying(fn, n) {//fn柯里化的函数，n是柯里化的参数
	  return function (m) {
	    return fn.call(this, m, n);
	  };
	}
	
	const factorial = currying(tailFactorial, 1);
	
	factorial(5) // 120

#### 采用ES6的函数默认值 ####

	function factorial(n, total = 1) {
	  if (n === 1) return total;
	  return factorial(n - 1, n * total);
	}
	factorial(5) // 120

### 自己实现尾递归优化 ###

#### 递归本质上是一种循环操作 ####

**纯粹的函数式编程语言没有循环操作命令**，所有的循环都用递归实现，这就是为什么尾递归对这些语言极其重要。

对于其他支持“尾调用优化”的语言（比如 Lua，ES6），只需要知道循环可以用递归代替，而一旦使用递归，就最好使用尾递归。

#### 实现尾递归优化 ####

尾递归优化只在严格模式下生效，那么正常模式下，可以自己实现尾递归优化

原理：尾递归之所以需要优化，原因是调用栈太多，造成溢出，那么只要减少调用栈，就不会溢出。怎么做可以减少调用栈呢？就是采用“循环”换掉“递归”。

# 函数参数的尾逗号 #

ES2017 允许**函数定义和调用最后一个参数有尾逗号**(trailing comma)。因此，函数参数与数组和对象的尾逗号规则，保持一致了。
	
	function clownsEverywhere(
	  param1,
	  param2,
	) { /* ... */ }
	
	clownsEverywhere(
	  'foo',
	  'bar',
	);
