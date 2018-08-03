---
title: ES6-Promise对象
date: 2018-07-31 15:39:20
tags:
	- JS
	- ES6
---

# Promise 的含义 #

## Promise ##

- Promise 是异步编程的一种解决方案
- 比传统的解决方案——回调函数和事件——更合理和更强大。
- 它由社区最早提出和实现，ES6 将其写进了语言标准，统一了用法，原生提供了Promise对象

## Promise对象 ##

### 两个特点 ###

- 状态不受外界影响。Promise对象代表一个异步操作，
	- 有三种状态：
		- pending（进行中）
		- fulfilled（已成功）
		- rejected（已失败）。
	- 只有异步操作的结果，可以决定当前是哪一种状态，任何其他操作都无法改变这个状态。
		- 这也是Promise这个名字的由来
		- 它的英语意思就是“承诺”，表示其他手段无法改变。

- 一旦状态改变，就**不会再变**，**任何时候**都可以得到这个结果。
	- Promise对象的状态一旦变为fulfilled或rejected，状态就凝固了，这时就称为 resolved（已定型）。
	- 如果改变已经发生了，你再对Promise对象添加回调函数，也会立即得到这个结果。
		- 这与事件（Event）完全不同，事件的特点是，如果你错过了它，再去监听，是得不到结果的。

### 作用 ###

- 将异步操作以同步操作的流程表达出来，避免了层层嵌套的回调函数。
- 提供统一的接口，使得控制异步操作更加容易

### 缺点 ###

- **一旦新建立即执行，无法取消**
- 如果不设置回调函数，Promise内部抛出的错误，不会反应到外部。
- 当处于pending状态时，无法得知目前进展到哪一个阶段（刚刚开始还是即将完成）。

如果某些**事件不断地反复发生**，一般来说，**使用 Stream 模式**是比部署Promise更好的选择。

# 基本使用 #

## 创建实例 ##

Promise构造函数接受一个函数作为参数，该函数的两个参数分别是resolve和reject两个函数，由 JavaScript 引擎提供，不用自己部署。

	const promise = new Promise(function(resolve, reject) {
	  // ... some code
	
	  if (/* 异步操作成功 */){
	    resolve(value);
	  } else {
	    reject(error);
	  }
	});

## then()设置回调 ##

Promise实例生成以后，可以用then方法分别指定resolved状态和rejected状态的回调函数(第二个参数可选)。	

## 实例 ##

实例：异步加载图片

	function loadImageAsync(url) {
	  return new Promise(function(resolve, reject) {
	    const image = new Image();
	
	    image.onload = function() {
	      resolve(image);
	    };
	
	    image.onerror = function() {
	      reject(new Error('Could not load image at ' + url));
	    };
	
	    image.src = url;
	  });
	}
	
	loadImageAsync('http://www.baidu.com').then(function(image) {
	  console.log('resolved');
	}, function(error) {
	  console.error('出错了', error);
	});

实例：Ajax 操作

	const getJSON = function(url) {
	  const promise = new Promise(function(resolve, reject){
	    const handler = function() {
	      if (this.readyState !== 4) {
	        return;
	      }
	      if (this.status === 200) {
	        resolve(this.response);
	      } else {
	        reject(new Error(this.statusText));
	      }
	    };
	    const client = new XMLHttpRequest();
	    client.open("GET", url);
	    client.onreadystatechange = handler;
	    client.responseType = "json";
	    client.setRequestHeader("Accept", "application/json");
	    client.send();
	
	  });
	
	  return promise;
	};
	
	getJSON("/posts.json").then(function(json) {
	  console.log('Contents: ' + json);
	}, function(error) {
	  console.error('出错了', error);
	});

## 回调函数顺序 ##

- 创建实例指定的回调函数
	- 函数中调用resolve或reject并不会终结回调函数的执行
- 当前脚本所有同步任务
- then()指定的状态回调函数
	- 立即 resolved 的 Promise 也要在本轮事件循环的末尾执行(JS是事件循环驱动)

实例：

	let promise = new Promise(function(resolve, reject) {
	  console.log('Promise');
	  resolve();
	});
	
	promise.then(function() {
	  console.log('resolved.');
	});
	
	console.log('Hi!');
	
	// Promise
	// Hi!
	// resolved
	Promise 新建后立即执行，所以首先输出的是Promise。然后，then方法指定的回调函数，将在当前脚本所有同步任务执行完才会执行，所以resolved最后输出。

实例：

	new Promise((resolve, reject) => {
	  resolve(1);
	  console.log(2);//还是会执行，并且会首先打印出来。，then方法指定的回调函数，将在当前脚本所有同步任务执行完才会执行
	}).then(r => {
	  console.log(r);
	});
	// 2
	// 1

一般来说，调用resolve或reject以后，Promise 的使命就完成了，后继操作应该放到then方法里面，而不应该直接写在resolve或reject的后面。所以，最好在它们前面加上return语句，这样就不会有意外。

	new Promise((resolve, reject) => {
	  return resolve(1);
	  // 后面的语句不会执行
	  console.log(2);
	})


# then() #

## 链式调用 ##

then方法返回的是一个新的Promise实例（注意，不是原来那个Promise实例）。因此可以采用链式写法，即then方法后面再调用另一个then方法

	getJSON("/posts.json").then(function(json) {
	  return json.post;
	}).then(function(post) {
	  // ...
	});

## 异步结果是另一个异步操作 ##

非链式调用

	const p1 = new Promise(function (resolve, reject) {
	  // ...
	});
	
	const p2 = new Promise(function (resolve, reject) {
	  // ...
	  resolve(p1);
	})

p1的状态就会传递给p2，也就是说，p1的状态决定了p2的状态

链式调用：访问一个url获取新url，访问新url获取结果

	getJSON("/post/1.json").then(function(post) {
	  return getJSON(post.commentURL);
	}).then(function funcA(comments) {
	  console.log("resolved: ", comments);
	}, function funcB(err){
	  console.log("rejected: ", err);
	});

采用箭头函数，上面的代码可以写得更简洁。

	getJSON("/post/1.json").then(
	  post => getJSON(post.commentURL)
	).then(
	  comments => console.log("resolved: ", comments),
	  err => console.log("rejected: ", err)
	);

# catch() #

catch()是then(null, rejection)的别名，用于指定发生错误时的回调函数。

一般来说，不要在then方法里面定义 Reject 状态的回调函数（即then的第二个参数），总是使用catch方法。

	getJSON('/posts.json').then(function(posts) {
	  // ...
	}).catch(function(error) {
	  // 处理 getJSON 和 then()指定的回调函数运行时发生的错误
	  console.log('发生错误！', error);
	});

# finally() #

用于指定不管 Promise 对象最后状态如何，都会执行的操作。该方法是 ES2018 引入标准的。

# resolve() #

**返回一个resolved状态的 Promise 对象**

	Promise.resolve('foo')
	// 等价于
	new Promise(resolve => resolve('foo'))

resolve()的参数分成四种情况

## 参数是 Promise 实例 ##

不做任何修改、原封不动地返回这个实例。

## 参数是thenable对象 ##

thenable对象指的是**具有then方法的对象**

将这个对象转为 Promise 对象，然后就立即执行thenable对象的then方法。then方法一般会将状态置为resolved

	let thenable = {
	  then: function(resolve, reject) {
	    resolve(42);
	  }
	};
	
	let p1 = Promise.resolve(thenable);
	//thenable对象的then方法执行后，对象p1的状态就变为resolved，从而立即执行下面then方法指定的回调函数，输出 42。
	p1.then(function(value) {
	  console.log(value);  // 42
	});

## 参数不是thenable对象，或根本不是对象 ##

返回一个resolved状态的 Promise 对象。

	const p = Promise.resolve('Hello');
	p.then(function (s){
	  console.log(s)
	});
	// Hello

## 不带有任何参数 ##

返回一个resolved状态的 Promise 对象。

	const p = Promise.resolve();
	p.then(function () {
	  // ...
	});

# reject()  #

**返回一个rejected状态的 Promise 对象**

	const p = Promise.reject('出错了');
	// 等同于
	const p = new Promise((resolve, reject) => reject('出错了'))

**注意：Promise.reject()方法的参数，会原封不动地作为reject的理由，变成后续方法的参数。这一点与Promise.resolve方法不一致**

	const thenable = {
	  then(resolve, reject) {
	    reject('出错了');
	  }
	};
	
	Promise.reject(thenable)
	.catch(e => {
	  console.log(e === thenable)
	})
	// true

	Promise.reject方法的参数是一个thenable对象，执行以后，后面catch方法的参数不是reject抛出的“出错了”这个字符串，而是thenable对象。

# all() #

将多个 Promise 实例，包装成一个新Promise实例。

	const p = Promise.all([p1, p2, p3]);

## 参数 ##

### 数组 ###

所有数组元素会被 Promise.resolve() 转为Promise 实例

### 对象：有Iterator接口且成员都是Promise实例 ###

## 新Promise实例状态回调 ##

p的状态由p1、p2、p3决定，分成两种情况。

- p1、p2、p3的状态都变成fulfilled，p的状态才会变成fulfilled
	- 此时p1、p2、p3的返回值组成一个数组，传递给p的回调函数
- p1、p2、p3之中有一个被rejected，p的状态就变成rejected
	- 此时第一个被reject的实例的返回值，会传递给p的回调函数。
	

如果作为参数的 Promise 实例，自己定义了catch方法，那么它一旦被rejected，并不会触发Promise.all()的catch方法

	const p1 = new Promise((resolve, reject) => {
	  resolve('hello');
	})
	.then(result => result)
	.catch(e => e);
	
	const p2 = new Promise((resolve, reject) => {
	  throw new Error('报错了');
	})
	.then(result => result)
	.catch(e => e);
	
	Promise.all([p1, p2])
	.then(result => console.log(result))
	.catch(e => console.log(e));
	// ["hello", Error: 报错了]

	p2首先会rejected
	但是p2有自己的catch方法，该方法返回的是一个新的 Promise 实例，p2指向的实际上是这个实例。
	该实例执行完catch方法后，也会变成resolved，导致Promise.all()方法参数里面的两个实例都会resolved
	因此会调用then方法指定的回调函数，而不会调用catch方法指定的回调函数。

# race() #

将多个 Promise 实例，包装成一个新Promise实例。

跟 all()很相似。**最大的区别就是新Promise实例状态回调不同**

	const p = Promise.race([p1, p2, p3]);

只要p1、p2、p3之中有一个实例率先改变状态，p的状态就跟着改变。那个率先改变的 Promise 实例的返回值，传递给p的回调函数。

# try() #

**为同步操作和异步操作提供了统一的处理机制，而且能统一处理同步异常和异步异常**

	const f = () => console.log('now');
	Promise.try(f);
	console.log('next');
	// now
	// next