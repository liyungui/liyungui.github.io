---
title: ES6-Symbol
date: 2018-08-10 16:30:20
tags:
	- JS
	- ES6
---

# 概述 #

目的：**从根本上防止属性名的冲突**

**新的原始数据类型Symbol，表示独一无二的值**

- 不能使用new命令。因为是原始类型，不是对象

**Symbol 值通过Symbol函数生成，描述参数可省略，保证每次生成的值都独一无二**

	let s1 = Symbol('foo');
	let s2 = Symbol('foo');
	s1 === s2 // false

**Symbol 值可以显式转为字符串**

## 作为属性名 ##

**Symbol 值作为对象属性名时，不能用点运算符**

	let mySymbol = Symbol();
	
	// 第一种写法
	let a = {};
	a[mySymbol] = 'Hello!';
	
	// 第二种写法
	let a = {
	  [mySymbol]: 'Hello!'
	};
	
	// 第三种写法
	let a = {};
	Object.defineProperty(a, mySymbol, { value: 'Hello!' });