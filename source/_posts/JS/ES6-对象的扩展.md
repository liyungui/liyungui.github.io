---
title: ES6-对象的扩展
date: 2018-08-01 10:11:20
tags:
	- JS
	- ES6
---

# 属性简洁表示法 #

**直接写入变量和函数，作为对象的属性和方法。**

- 键值对同名。即属性的键名和值名相同
	- 属性简写：省略 属性名和冒号
	- 方法简写：省略 冒号和function
		- 方法的值是一个 Generator 函数，前面需要加上星号
- 简洁写法的属性名总是字符串
- 属性名是字符串，直接取变量名;属性值是变量值

实例

	function people(name, age) {
        return {
            name: name,
            age: age
			getName: function() {
	            console.log(this.name)
	        }
        };
    }

	function people(name, age) {
        return {
            name,
            age
			getName () {
	            console.log(this.name)
	        }
        };
    }
	
	const obj = {
	  * m() {
	    yield 'hello world';
	  }
	};

	const foo = 'bar';
	const baz = {foo};
	baz // {foo: "bar"}//属性名是字符串，直接取变量名;属性值是变量值
	// 等同于
	const baz = {foo: foo};

	const obj = {
	  class () {}
	};
	// 等同于
	var obj = {
	  'class': function() {}
	};

# 属性名表达式 #

ES6 允许**字面量定义对象(使用大括号)**时，**用表达式作为对象的属性名** 即把表达式放在方括号内

	let lastWord = 'last word';
	const a = {
	  'first word': 'hello',
	  [lastWord]: 'world'
	};
	a['first word'] // "hello"
	a[lastWord] // "world"
	a['last word'] // "world"

**属性名表达式与简洁表示法，不能同时使用**，会报错。

	// 报错
	const foo = 'bar';
	const bar = 'abc';
	const baz = { [foo] };
	
	// 正确
	const foo = 'bar';
	const baz = { [foo]: 'abc'};

**属性名表达式是对象，默认情况下自动将对象转为字符串[object Object]**

	const keyA = {a: 1};
	const keyB = {b: 2};
	const myObject = {
	  [keyA]: 'valueA',
	  [keyB]: 'valueB'
	};
	myObject // Object {[object Object]: "valueB"}

	[keyA]和[keyB]得到的都是[object Object]
	所以[keyB]会把[keyA]覆盖掉，而myObject最后只有一个[object Object]属性

# 属性的可枚举性和遍历 #

## 可枚举性 ##

### 描述对象（Descriptor） ###

- 用来控制该属性的行为。
- 对象的每个属性都有一个描述对象，
- 获取该属性的描述对象 `Object.getOwnPropertyDescriptor()`

实例：描述对象

	let obj = { foo: 123 };
	Object.getOwnPropertyDescriptor(obj, 'foo')
	//  {
	//    value: 123,
	//    writable: true,
	//    enumerable: true,
	//    configurable: true
	//  }

### 可枚举性 ###

- **描述对象的enumerable属性**
- 最初目的，就是让某些属性可以规避掉for...in操作

**目前，有四个操作会忽略enumerable为false的属性。**

- for...in循环：只遍历**对象自身**的和**继承**的**可枚举**的属性。
- Object.keys()：返回**对象自身**的所有**可枚举**的属性的键名。
- Object.assign()： 只拷贝**对象自身**的**可枚举**的属性。
- JSON.stringify()：只串行化**对象自身**的**可枚举**的属性。

实例：toString和length属性不可枚举

	Object.getOwnPropertyDescriptor(Object.prototype, 'toString').enumerable
	// false
	
	Object.getOwnPropertyDescriptor([], 'length').enumerable
	// false
	
		上面代码中，toString和length属性的enumerable都是false，
		因此for...in不会遍历到这两个继承自原型的属性。

**ES6 规定，所有 Class 的原型的方法都是不可枚举的**

Object.getOwnPropertyDescriptor(class {foo() {}}.prototype, 'foo').enumerable
// false
总的来说，操作中引入继承的属性会让问题复杂化，大多数时候，我们只关心对象自身的属性。所以，尽量不要用for...in循环，而用Object.keys()代替。

## 属性的遍历 ##

### 五种遍历对象的属性的方法 ###

ES6 一共有 5 种方法可以遍历对象的属性。

#### for...in ####

for...in循环遍历**对象自身**的和**继承**的**可枚举属性**（不含 Symbol 属性）。

#### Object.keys(obj) ####

Object.keys返回一个数组，包括**对象自身**的（不含继承的）所有**可枚举**属性（不含 Symbol 属性）的键名。

#### Object.getOwnPropertyNames(obj) ####

Object.getOwnPropertyNames返回一个数组，包含**对象自身**的所有属性（不含 Symbol 属性，但是包括不可枚举属性）的键名。

#### Object.getOwnPropertySymbols(obj) ####

Object.getOwnPropertySymbols返回一个数组，包含**对象自身**的所有 **Symbol** 属性的键名。

#### Reflect.ownKeys(obj) ####

Reflect.ownKeys返回一个数组，包含**对象自身**的所有键名，不管键名是 **Symbol** 或字符串，也不管是否可枚举。

### 属性遍历次序规则 ###
以上的 5 种方法遍历对象的键名，都遵守同样的属性遍历次序规则。

- 所有数值键，按照数值升序排列。
- 所有字符串键，按照加入时间升序排列。
- 所有 Symbol 键，按照加入时间升序排列。

实例：

	Reflect.ownKeys({ [Symbol()]:0, b:0, 10:0, 2:0, a:0 })
	// ['2', '10', 'b', 'a', Symbol()]
	上面代码中，Reflect.ownKeys方法返回一个数组，包含了参数对象的所有属性。这个数组的属性次序是这样的，首先是数值属性2和10，其次是字符串属性b和a，最后是 Symbol 属性。

# 方法的 name 属性 #

对象方法也是函数，因此也有name属性，**返回函数名**

- 对象的方法使用了取值函数(getter)和存值函数(setter)，
	- name属性不在该方法上面
	- 在该方法的属性的描述对象的get和set属性上面
	- 返回值是方法名前加上get和set
- 两种特殊情况
	- bind方法创造的函数
		- name属性返回bound加上原函数的名字；
	- Function构造函数创造的函数
		- name属性返回anonymous
实例

	onst obj = {
	  get foo() {},
	  set foo(x) {}
	};
	
	obj.foo.name
	// TypeError: Cannot read property 'name' of undefined
	
	const descriptor = Object.getOwnPropertyDescriptor(obj, 'foo');
	descriptor.get.name // "get foo"
	descriptor.set.name // "set foo"

	(new Function()).name // "anonymous"
	
	var doSomething = function() {
	  // ...
	};
	doSomething.bind().name // "bound doSomething"

# Object.is() #

**是否严格相等**

比较两个值是否相等三种方法：

- 相等运算符（==）
	- 缺点：
		- **自动转换数据类型**
- 严格相等运算符（===）
	- 缺点：
		- NaN不等于自身
		- +0等于-0
- is()
	-ES6 提出
	- “Same-value equality”（同值相等)算法
	- 两个值是否**严格相等**
		- 解决了严格比较运算符（===）的两个缺点

# Object.assign() #

## 基本使用 ##

**合并对象，将源对象的所有可枚举属性，复制到目标对象**

	Object.assign(target, ... source)

- **浅拷贝**
- **属性覆盖** 后面的属性会覆盖前面的属性
	- 目标对象与源对象有同名属性
	- 多个源对象有同名属性
- 只有一个参数
	- 直接返回该参数
- 参数不是对象，自动转成对象
	- 非首参(源对象)
		- 数值和布尔值，无效果
			- 包装对象不产生可枚举属性
		- 字符串，以数组形式拷入目标对象(属性名为元素索引)
			- 包装对象产生可枚举属性
- undefined和null无法转成对象
	- 首参，会报错
	- 非首参，跳过
- 取值函数的处理
	- 求值后复制值
实例

	const target = { a: 1, b: 1 };
	const source1 = { b: 2, c: 2 };
	const source2 = { c: 3 };
	Object.assign(target, source1, source2);
	target // {a:1, b:2, c:3}

	const obj = {a: 1};
	Object.assign(obj) === obj // true
	
	Object.assign(undefined) // 报错
	let obj = {a: 1};
	Object.assign(obj, undefined) === obj // true

实例：字符串的处理，转为数组对象

	const v1 = 'abc';
	const v2 = true;
	const v3 = 10;
	const obj = Object.assign({}, v1, v2, v3);
	console.log(obj); // { "0": "a", "1": "b", "2": "c" }

实例：数组对象的处理

	Object.assign([1, 2, 3], [4, 5])
	// [4, 5, 3]
		把数组视为属性名为 0、1、2 的对象
		因此源数组的 0 号属性4覆盖了目标数组的 0 号属性1

实例：取值函数的处理

	const source = {
	  get foo() { return 1 }
	};
	const target = {};
	Object.assign(target, source)
	// { foo: 1 }

## 常见用途 ##

### 合并对象/克隆对象 ###

### 为对象添加属性 ###

将x属性和y属性添加到Point类的对象实例

class Point {
  constructor(x, y) {
    Object.assign(this, {x, y});
  }
}

### 为对象添加方法 ###

	Object.assign(SomeClass.prototype, {
	  someMethod(arg1, arg2) {
	    ···
	  },
	  anotherMethod() {
	    ···
	  }
	});
	
	// 等同于下面的写法
	SomeClass.prototype.someMethod = function (arg1, arg2) {
	  ···
	};
	SomeClass.prototype.anotherMethod = function () {
	  ···
	};

### 为属性指定默认值 ###

EFAULTS对象是默认值，options对象是用户提供的参数

Object.assign方法将DEFAULTS和options合并成一个新对象，如果两者有同名属性，则option的属性值会覆盖DEFAULTS的属性值

	const DEFAULTS = {
	  logLevel: 0,
	  outputFormat: 'html'
	};
	function processContent(options) {
	  options = Object.assign({}, DEFAULTS, options);
	  console.log(options);
	  // ...
	}

# 对象的扩展运算符 #

扩展运算符（`...`）

## 解构赋值 ##

**解构赋值必须是最后一个参数**，否则会报错。

	let { x, y, ...z } = { x: 1, y: 2, a: 3, b: 4 };
	x // 1
	y // 2
	z // { a: 3, b: 4 }

**变量声明**语句之中，如果使用**解构赋值**，**扩展运算符**后面必须是一个**变量**名，而不能是一个解构赋值表达式

**扩展运算符的解构赋值，只能复制对象自身的属性**。 继承的属性无法复制

	const o = Object.create({ x: 1, y: 2 });
	o.z = 3;
	let { x, ...newObj } = o;//这里的扩展运算符后只能是变量，所以引入了中间变量newObj
	let { y, z } = newObj;
	x // 1
	y // undefined
	z // 3

	变量x是单纯的解构赋值，所以可以读取对象o继承的属性；
	变量y和z是扩展运算符的解构赋值，只能读取对象o自身的属性
		所以变量z可以赋值成功，变量y取不到值
