---
title: ES6-数组的扩展
date: 2018-08-02 10:57:20
tags:
	- JS
	- ES6
---

# 扩展运算符 #

## 概念 ##

- 三个点 `...`
- rest 参数的逆运算
- 将数组转为**逗号分隔的参数序列**

## 使用场景 ##

### 函数调用 ###

主要用于**函数调用**。 

	function add(x, y) {
	  return x + y;
	}
	const numbers = [4, 38];
	add(...numbers) // 42

扩展运算符与正常的函数参数结合使用，非常灵活。

	console.log(1, ...[2, 3, 4], 5)
	// 1 2 3 4 5

### 表达式 ###

扩展运算符后面还可以放置**表达式**

	const arr = [
	  ...(x > 0 ? ['a'] : []),
	  'b',
	];

### 替代函数的 apply 方法 ###

不再需要apply方法，将数组转为函数的参数

	// ES5 的写法
	function f(x, y, z) {
	  // ...
	}
	var args = [0, 1, 2];
	f.apply(null, args);
	
	// ES6的写法
	function f(x, y, z) {
	  // ...
	}
	let args = [0, 1, 2];
	f(...args);

### 复制数组和合并数组 ###

实例：克隆数组a1

	//ES5 只能用变通方法来复制数组。
	const a1 = [1, 2];
	const a2 = a1.concat();
	a2[0] = 2;
	a1 // [1, 2]

	//ES6简便写法
	const a1 = [1, 2];
	// 写法一
	const a2 = [...a1];
	// 写法二
	const [...a2] = a1;

实例：合并数组

	const arr1 = ['a', 'b'];
	const arr2 = ['c'];
	const arr3 = ['d', 'e'];
	
	// ES5 的合并数组
	arr1.concat(arr2, arr3);
	// [ 'a', 'b', 'c', 'd', 'e' ]
	
	// ES6 的合并数组
	[...arr1, ...arr2, ...arr3]
	// [ 'a', 'b', 'c', 'd', 'e' ]

**注意**：扩展运算符和concat都是**浅拷贝**

### 与解构赋值结合 ###

实例：与解构赋值结合起来，用于生成数组

	// ES5
	a = list[0], rest = list.slice(1)
	// ES6
	[a, ...rest] = list

注意：**扩展运算符用于数组赋值，只能放在参数的最后一位**，否则会报错

### 将Iterator 接口对象转为真正的数组 ###

**扩展运算符内部调用的是数据结构的 Iterator 接口**，只要具有 Iterator 接口的对象，都可以使用扩展运算符

#### 字符串 ####

**能够正确识别四个字节的 Unicode 字符**

	[...'hello']
	// [ "h", "e", "l", "l", "o" ]

#### Map 和 Set 结构 ####

#### Generator 函数 ####

# Array.from() #

**将两类对象转为数组**：

- **类似数组的对象**(array-like object)
	- 必须**有length属性**
- **可遍历的对象**(iterable object)
	- **Iterator 接口对象**
		- 包括 ES6 新增的数据结构 Set 和 Map
		- 扩展运算符只支持这一种对象转真正数组

实例：类似数组的对象转为真正的数组

	let arrayLike = {
	    '0': 'a',
	    '1': 'b',
	    '2': 'c',
	    length: 3
	};
	
	// ES5的写法
	var arr1 = [].slice.call(arrayLike); // ['a', 'b', 'c']
	
	// ES6的写法
	let arr2 = Array.from(arrayLike); // ['a', 'b', 'c']

**第二个参数**，作用类似于数组的**map**方法，用来对每个元素进行处理，将处理后的值放入返回的数组

	Array.from([1, 2, 3], (x) => x * x)
	// [1, 4, 9]
	Array.from([1, 2, 3]).map((x) => x * x);

如果map函数里面用到了this关键字，还可以传入Array.from的**第三个参数**，用来**绑定this**。

# Array.of() #

**将一组值转换为数组**。主要目的：弥补数组构造函数行为差异问题，**统一数组创建行为**

	Array() // []
	Array(3) // [, , ,]
	Array(3, 11, 8) // [3, 11, 8]
	
	Array.of() // []
	Array.of(3) // [3]
	Array.of(3, 11, 8) // [3,11,8]

# copyWithin() #

将指定位置的成员复制到其他位置(覆盖原有成员)，然后返回当前数组

	copyWithin(target, start = 0, end = this.length)
		负值，表示倒数。从-1开始
		正值，顺数，从0开始
		start,end是前开后闭区间。即最后位置=end位置-1

实例：

	[1, 2, 3, 4, 5].copyWithin(0, 3)
	// [4, 5, 3, 4, 5]
	
	// 将3号位复制到0号位
	[1, 2, 3, 4, 5].copyWithin(0, 3, 4)
	// [4, 2, 3, 4, 5]
	
	// -2相当于3号位，-1相当于4号位
	[1, 2, 3, 4, 5].copyWithin(0, -2, -1)
	// [4, 2, 3, 4, 5]

# find() 和 findIndex() #

find()返回**第一个**符合条件的数组成员。没有符合条件的成员返回**undefined**

findIndex()返回**第一个**符合条件的数组成员的位置。没有符合条件的成员返回**-1**。

这两个方法都**可以发现NaN**，弥补了数组的indexOf方法的不足

- 两个参数
	- 一个回调函数
		- 可以接受三个参数(后两个可以省略)，依次为
			- 当前的值
			- 当前的位置
			- 原数组。
	- 一个对象。可省略
		- 绑定回调函数的this对象
- 所有数组成员依次执行该回调函数
- 直到找出第一个返回值为true的成员
- 然后返回该成员/成员的位置

实例：

	[1, 4, -5, 10].find((n) => n < 0)
	// -5

	[1, 5, 10, 15].find(function(value, index, arr) {
	  return value > 9;
	}) // 10

# fill() #

使用给定值，填充一个数组

	fill(target, start = 0, end = this.length)
		前开后闭区间
		如果填充的类型为对象，那么被赋值的是同一个内存地址的对象，而不是深拷贝对象

实例

	['a', 'b', 'c'].fill(7)
	// [7, 7, 7]

	let arr = new Array(3).fill({name: "Mike"});
	arr[0].name = "Ben";
	arr
	// [{name: "Ben"}, {name: "Ben"}, {name: "Ben"}]

# entries()，keys() 和 values() #

返回一个**遍历器对象**，用于遍历数组

**数组的键名就是索引值**

# includes() #

某个数组是否包含给定的值。

**支持NaN**

	includes(target, start = 0)
		负数，倒数，从-1开始

实例

	[1, 2, 3].includes(2)     // true
	[1, 2, NaN].includes(NaN) // true

# 空位 #

**空位，数组的某一个位置没有任何值(等于undefined，依然是有值的)**

Array构造函数返回的数组都是空位

	Array(3) // [, , ,]

**空位的处理规则非常不统一，避免出现空位**

遍历，查找等数组操作，对空位处理不统一，有跳过的，有转为undefined的