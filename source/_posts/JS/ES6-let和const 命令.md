---
title: ES6-let和const 命令
date: 2018-07-30 16:41:20
tags:
	- JS
	- ES6
---

参考 [ECMAScript 6 入门](http://es6.ruanyifeng.com/)

# let #

## 所声明的变量，只在let命令所在的代码块内有效 ##

	for (let i = 0; i < 3; i++) {
	  let i = 'abc';
	  console.log(i);//输出了 3 次abc
	}

for循环有一个特别之处，就是设置循环变量的那部分是一个父作用域，而循环体内部是一个单独的子作用域

## 不存在变量提升 ##

变量一定要在声明后使用，否则报错。

## 暂时性死区 ##

temporal dead zone，简称 TDZ

块级作用域内存在let命令，它所声明的变量就“绑定”（binding）这个区域，不再受外部的影响

	var tmp = 123;
	
	if (true) {
	  // TDZ开始
	  tmp = 'abc'; // ReferenceError
	  let tmp;//// TDZ结束
	}

有些“死区”比较隐蔽，不太容易发现。

	function bar(x = y, y = 2) {
	  return [x, y];
	}
	
	bar(); // 报错(某些实现可能不报错)。参数x默认值等于另一个参数y，而此时y还没有声明，属于”死区“。

## 不允许重复声明 ##

	// 报错
	function func() {
	  let a = 10;
	  var a = 1;
	}
	
	// 报错
	function func() {
	  let a = 10;
	  let a = 1;
	}

	function func(arg) {
	  let arg; // 报错
	}
	
	function func(arg) {
	  {
	    let arg; // 不报错
	  }
	}





