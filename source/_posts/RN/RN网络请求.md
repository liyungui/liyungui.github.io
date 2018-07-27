---
title: RN网络请求
date: 2018-07-27 10:31:15
tags:
	- RN
---

# Fetch #

## 使用XMLHttpRequest ##

React Native提供了和web标准一致的Fetch API，内置了XMLHttpRequest API(即俗称的ajax)

	fetch('https://mywebsite.com/endpoint/', {
	  method: 'POST',
	  headers: {
	    'Accept': 'application/json',
	    'Content-Type': 'application/json',
	  },
	  body: JSON.stringify({
	    firstParam: 'yourValue',
	    secondParam: 'yourOtherValue',
	  })
	})

Fetch 方法会返回一个Promise

## 使用其他的网络库 ##

一些基于XMLHttpRequest封装的第三方库也可以使用，例如frisbee或是axios等。但注意不能使用jQuery，因为jQuery中还使用了很多浏览器中才有而RN中没有的东西

# WebSocket #

React Native支持WebSocket