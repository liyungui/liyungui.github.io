---
title: JS教程
date: 2018-07-27 11:53:34
tags:
	- JS
---

# 语法 #

## 区分大小写 ##

## 变量是弱类型的 ##

## 变量可以不声明直接使用 ##

## 每行结尾的分号可有可无 ##

推荐书写分号

- 编码规范
- 没有分号在有些浏览器不能正确运行

## 注释与 Java、C 和 PHP 语言的注释相同 ##

	//this is a single-line comment
	
	/*this is a multi-
	line comment*/

## 括号表示代码块 ##

从 Java 中借鉴

	if (test1 == "red") {
	    test1 = "blue";
	    alert(test1);
	}

# 变量 #

- 弱类型
- 可以不声明直接使用
	
## 命名变量 ##

- 第一个字符必须是字母、下划线（_）或美元符号（$）
- 余下的字符还可以是数字字符

## 声明变量 ##

- 不一定要初始化
- 弱类型。
	- 无需明确的类型声明
	- 变量可以存放不同类型的值
- 同一个 var 语句定义的变量不必具有相同的类型
- 函数内部声明变量的时候，一定要使用var命令。如果不用的话，实际上声明了一个全局变量

示例：声明变量

	var test;
	var test = "hi";
	test = 55;
	var test = "hi", age = 25;

实例：函数内部声明变量

	function f1(){
	　　n = 999;
	}
	f1();
	console.log(n);　　//999

# 作用域和作用域链

## 执行环境（execution context）

- 在运行和执行代码的时候才存在
- 每个执行环境都有与之对应的**变量对象**（variable object）
- 保存着
	- 	该环境中**定义的变量**
	-  该环境中**定义的函数**
	-  **函数有权访问的其他数据**。
-  无法通过代码来访问变量对象
-  解析器处理数据时会在后台使用到它。
- 分为
	- 全局执行环境（也称全局环境）
		- 运行浏览器时创建
	- 函数执行环境
		- 调用函数时创建

### 全局执行环境

　　在web浏览器中，我们可以认为他是window对象，因此所有的全局变量和函数都是作为window对象的属性和方法创建的。代码载入浏览器时，全局环境被创建，关闭网页或者关闭浏览时全局环境被销毁。

### 函数执行环境
　　
　　每个函数都有自己的执行环境，当执行流进入一个函数时，函数的环境就被推入一个环境栈中，当函数执行完毕后，栈将其环境弹出，把控制权返回给之前的执行环境。

## 作用域（scope）

对应于执行环境，作用域分为

- 全局作用域（globe scope）
- 局部作用域（local scope）**函数作用域**

只有函数级作用域。**没有块级作用域**

## 作用域链（scope chain）

- 用于搜索变量和函数
- 可以保证对(执行环境有权访问的)所有变量和函数的有序访问。
- 是函数被创建的作用域中对象的集合
- 每次进入一个新的执行环境，都会创建一个
- 最前端始终是当前执行的代码所在环境的变量对象（如果该环境是函数，则将其活动对象作为变量对象），依次往上，直到全局执行环境的变量对象。
- 标识符解析是沿着作用域一级一级的向上搜索标识符的过程，直到找到标识符（找不到，就会导致错误发生）。

{% asset_img 作用域链.png %}

	var name1 = "haha";
	function changeName(){
	    var name2="xixi";
	    function swapName(){
	        console.log(name1);//haha
	        console.log(name2);//xixi
	        var tempName=name2;
	        name2=name1;
	        name1=tempName;
	        console.log(name1);//xixi
	        console.log(name2);//haha
	        console.log(tempName);//xixi
	    }
	    swapName();
	    console.log(name1);//xixi
	    console.log(name2);//haha
	    console.log(tempName);//抛出错误：Uncaught ReferenceError: tempName is not defined
	}
	changeName();
	console.log(name1);//xixi
	console.log(name2); //抛出错误：Uncaught ReferenceError: name2 is not defined
	console.log(tempName);//抛出错误：Uncaught ReferenceError: tempName is not defined

	上述代码中，一共有三个执行环境：全局环境、changeName()的局部环境和 swapName() 的局部环境。所以，
	
	　1.函数 swapName()的作用域链包含三个对象：自己的变量对象----->changeName()局部环境的变量对象 ----->全局环境的变量对象。
	
	　2.函数changeName()的作用域包含两个对象：自己的变量对象----->全局环境的变量对象。
	
	就上述程序中出现的变量和函数来讲（不考虑隐形变量）：
	
	　1.swapName() 局部环境的变量对象中存放变量 tempName；
	
	　2.changeName() 局部环境的变量对象中存放变量 name2 和 函数swapName()；
	
	　3.全局环境的变量对象中存放变量 name1 、函数changeName();

### 词法作用域规则(lexical scoping rules)

函数被执行时(executed)使用的作用域链(scope chain)是被**定义时的scope chain**，而不是执行时的scope chain

	var scope = "global scope"; 
	function checkScope() {
	    var scope = "local scope";
	    function f() {
	        return scope;
	    }
	    return f();
	}
	checkScope();   //"local scope"
	
	var scope = "global scope"; 
	function checkScope() {
	    var scope = "local scope";
	    function f() {
	        return scope;
	    }
	    return f;
	}
	checkScope()();   //"local scope"

## 提升（hoisting）

**把声明语句提升到函数体的顶部(第一句)**

### 变量提升（variable hoisting）

把变量声明提升到函数的顶部。**变量提升只是提升变量的声明，不会把变量的值也提升上来**

	var name="haha";
	function changeName(){
	  var name;
	  console.log(name);//undefined
	  name="xixi";
	}
	changeName();
	console.log(name);//haha

changeName() 的作用域链： 自己的变量对象 -----> 全局变量对象。解析器在函数执行环境中发现变量 name，因此不会再向全局环境的变量对象中寻找。但是，解析器在解析第3句代码时，还不知道变量name的值（因为还没有执行第4句代码），因此输出是 undefined

所以上述代码等价下面的形式：

	var name="haha";
	function changeName(){
	  var name;
	  console.log(name);
	  name="xixi";
	}
	changeName();
	console.log(name);
 
###  函数提升

**只有函数声明形式才能被提升！**

函数的创建方式有三种：

- 函数声明（静态的）
- 函数表达式（函数字面量）
- 函数构造法（动态的，匿名的）

函数创建方式实例

	function func(){ 
	    //function body;
	} 
	var func = function(n1,n2){
  		//function body;
	};
	var func = new Function("para1","para2",...,"function body");  
	
函数提升实例

	//函数声明
	function myTest1(){ 
	    func(); //我可以被提升
	    function func(){ 
	        console.log("我可以被提升"); 
	    } 
	} 
	myTest1();
	
	//函数表达式
	function myTest2(){ 
	    func(); //Uncaught TypeError: func is not a function
	    var func = function(){ 
	        console.log("我不能被提升"); 
	    } 
	} 
	myTest2(); 
	
# 运算符 #

## 一元运算符 ##

### delete ###

删除 对象中开发者定义的属性或方法的引用

	var o = new Object;
	o.name = "David";
	alert(o.name);	//输出 "David"
	delete o.name;
	alert(o.name);	//输出 "undefined"

	delete o.toString; //报错。 toString() 方法是原始的 ECMAScript 方法，不是开发者定义的

### void ###

对任何值返回 undefined。通常用于避免输出不应该输出的值

	<a href="javascript:void(window.open('about:blank'))">Click me</a>

# 流程控制 #

## if ##

	if（）{
	}else if(){
	}else{
	}

## switch ##

- 可以用于字符串，
- 可以不是常量值

示例

	var BLUE = "blue", RED = "red", GREEN  = "green";
	switch (sColor) {
	  case BLUE: alert("Blue");
	    break;
	  case RED: alert("Red");
	    break;
	  case GREEN: alert("Green");
	    break;
	  default: alert("Other");
	}

## 迭代 ##

	do{
	}while()

	while(){
	}

	for (var i = 0; i < iCount; i++) {
	  alert(i);
	}

	for (sProp in window) {
	  alert(sProp);
	}

## with ##

设置代码在特定对象中的作用域

**运行缓慢**，尤其是在已设置了属性值时。最好**避免使用**

	var sMessage = "hello";
	with(sMessage) {
	  alert(toUpperCase());	//输出 "HELLO"
	}

	调用 toUpperCase() 方法时，将检查该方法是否是本地函数。如果不是，它将检查伪对象 sMessage，看它是否为该对象的方法。成功找到了字符串 "hello" 的 toUpperCase() 方法。

# 函数 #

## 函数的三种创建方式

- 函数声明（静态的）
- 函数表达式（函数字面量）
- 函数构造法（动态的，匿名的）

实例

	function func(){ 
	    //function body;
	} 
	var func = function(n1,n2){
  		//function body;
	};
	var func = new Function("para1","para2",...,"function body");   

### 函数声明

因为是弱类型

- 参数，不必声明类型，直接参数名
- 返回值，不必声明类型，直接return返回

示例

	function functionName(arg0, arg1, ... argN) {
	  statements
	}

### 匿名函数

	function(arg0, arg1, ... argN) {
	  statements
	}

### 函数其实是 Function 对象 ##

- 函数实际上是对象
- 函数名只是指向函数对象的引用值
- 函数可以作为参数传递给另一个函数

### 用 Function 直接创建函数 ###

语法如下：

	var function_name = new Function(arg1, arg2, ..., argN, function_body)


- 参数必须是**字符串**
- 最后一个参数是函数主体（要执行的代码）
- **最好不要使用**
- 弊端：
	- **书写很困难**，因为参数都是字符串，需要就涉及到内部真正字符的转义
- 优势：
	- **帮助理解函数是引用类型**，传统方式定义的函数行为与用 Function 明确创建的函数行为是相同的

实例：用 Function 直接创建函数

	function sayHi(sName, sMessage) {
	  alert("Hello " + sName + sMessage);
	}
	sayHi("David", " Nice to meet you!");
	
	var sayHi = new Function("sName", "sMessage", "alert(\"Hello \" + sName + sMessage);");
	sayHi("David", " Nice to meet you!");

	function doAdd(iNum) {
	  alert(iNum + 20);
	}
	
	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	doAdd(10);	//输出 "20"

实例：理解函数只不过是一种引用类型

	function doAdd(iNum) {
	  alert(iNum + 20);
	}
	
	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	doAdd(10);	//输出 "20"。因为第二个函数重载了第一个函数

	如果以下面的形式重写该代码块，这个概念就清楚了：

	var doAdd = new Function("iNum", "alert(iNum + 20)");
	var doAdd = new Function("iNum", "alert(iNum + 10)");
	doAdd(10);
	doAdd 的值被改成了指向不同对象的指针。函数名只是指向函数对象的引用值

### 函数作为参数传递给另一个函数 ###

	function callAnotherFunc(fnFunction, vArgument) {
	  fnFunction(vArgument);
	}
	
	var doAdd = new Function("iNum", "alert(iNum + 10)");
	
	callAnotherFunc(doAdd, 10);	//输出 "20"

### Function 对象的 length 属性 ###

声明了函数期望的参数个数

	function sayHi() {
	  alert("Hi");
	}
	
	alert(sayHi.length);	//输出 "0"

### Function 对象的方法 ###

valueOf() 方法和 toString() 方法，返回的都是函数的源代码，在调试时尤其有用

	function doAdd(iNum) {
	  alert(iNum + 10);
	}
	
	document.write(doAdd.toString());

## 立即执行函数表达式（IIFE）

Immediately-Invoked Function Expression

立即执行函数常用于第三方库，好处在于隔离作用域

任何一个第三方库都会存在大量的变量和函数，为了避免变量污染（命名冲突），开发者们想到的解决办法就是使用立即执行函数。

创建了一个新的函数作用域，相当于创建了一个“私有”的命名空间，该命名空间的变量和方法，不会破坏污染全局的命名空间。此时若是想访问全局对象，将全局对象以参数形式传进去即可，如jQuery代码结构:

	(function(window,undefined){
		//jquery code
	})(window);
	
### 两个必要条件

- 函数体必须是**函数表达式**。
	- 使用运算符将匿名函数或函数声明转换为函数表达式
		- 运算符：()，！，+，-，= 等等
- **立即执行**。函数体后面要有小括号()，表示立即执行

### 两种形式(等价)

- `( function(){…} )()` 
	- 小括号 包裹 匿名函数，后面再跟一个小括号
- `( function (){…} () )`
	- 小括号 包裹 匿名函数后面跟一个小括号

实例

	匿名函数转为立即执行函数表达式
	(function(n){
		console.log(n);
	})(1);
	
	(function(n){
		console.log(n);
	}(1));
	
	+function(n){
		console.log(n);
	}(1);
	
	-function(n){
		console.log(n);
	}(1);
	
	!function(n){
		console.log(n);
	}(1);
	
	var fn=function(n){
		console.log(n);
	}(1);
	
	函数声明同理
	var fn=function func(n){
		console.log(n);
	}(1);
	
## 闭包 closure ##

初学者觉得闭包难理解，可能是没有理解闭包的用途/使用场景，实际开发中，闭包的运用非常广泛。

闭包是指可以包含自由（未绑定到特定对象）变量的代码块；这些变量不是在这个代码块内或者任何全局上下文中定义的，而是在定义代码块的环境中定义（局部变量）。“闭包” 一词来源于以下两者的结合：要执行的代码块（由于自由变量被包含在代码块中，这些自由变量以及它们引用的对象没有被释放）和为自由变量提供绑定的计算环境（作用域）。在PHP、Scala、Scheme、Common Lisp、Smalltalk、Groovy、JavaScript、Ruby、 Python、Go、Lua、objective c、swift 以及Java（Java8及以上）等语言中都能找到对闭包不同程度的支持

在javascript语言中，闭包就是函数和该函数作用域的组合。从这个概念上来讲，在js中，所有函数都是闭包（函数都是对象并且函数都有和他们相关联的作用域链scope chain）。

既然所有函数都是闭包，还有必要专门提这个概念吗？

大多数函数被调用时(invoked)，使用的作用域和他们被定义时(defined)使用的作用域是同一个作用域，这种情况下，闭包神马的，无关紧要。但是，当他们被invoked的时候，使用的作用域不同于他们定义时使用的作用域的时候，闭包就会变的非常有趣，并且开始有了很多的使用场景，这就是之所以要掌握闭包的原因。

### 理解“闭包” step 1：掌握嵌套函数的词法作用域规则(lexical scoping rules)

词法作用域的基础规则：函数被执行时(executed)使用的作用域链(scope chain)是被**定义时的scope chain**，而不是执行时的scope chain

	var scope = "global scope"; 
	function checkScope() {
	    var scope = "local scope";
	    function f() {
	        return scope;
	    }
	    return f();
	}
	checkScope();   //"local scope"
	
	var scope = "global scope"; 
	function checkScope() {
	    var scope = "local scope";
	    function f() {
	        return scope;
	    }
	    return f;
	}
	checkScope()();   //"local scope"

上面两个实例，展示了闭包的一种能力：**读取其他函数内部的变量**

实现原理：

- 在函数内部定义一个内部函数
	- 作用域链包含了外部函数，**可以读取函数内部的变量**
- 并返回定义的内部函数
	- 延长作用域链的生命周期，**函数内部变量保持在内存中**不被释放

所以，在这个场景中，就是使用闭包的特性，作为将函数内部和函数外部连接的一座桥梁。

实例：

	function f1(){
	　　var n = 999;
	　　nAdd = function(){
	　　　　n += 1;
	　　}
	　　function f2(){
	　　　　console.log(n);
	　　}
	　　return f2;
	}
	
	var result = f1();
	result();　　//999
	nAdd();　　//nAdd前面没有var，其实是全局变量
	result();　　//1000

以上实例证明：函数f1中的局部变量n 一直保存在内存中，并没有在f1调用后被自动清除。

原因就在于f1是f2的父函数，而f2被赋给了一个全局变量，这导致f2始终在内存中，不会再调用结束后，被垃圾回收机制(garbage collection)回收。

上例中另一个值得注意的地方，就是‘nAdd=function(){n+=1}’这一行，首先在nAdd前面没有使用var关键字，因此nAdd是一个全局变量，而不是局部变量。其次，nAdd的值是一个匿名函数(anonymous function)，而这个匿名函数本身也是一个闭包，所以nAdd相当于是一个setter，可以在函数外部对函数内部的局部变量进行操作。

### 使用闭包的注意点

- **不能滥用闭包**

	闭包会使得函数中的变量都被保存在内存中，**内存消耗**很大，会造成网页的性能问题，在IE中可能导致内存泄露。
	
	**解决方法**：在退出函数之前，将不使用的局部变量全部删除。

- 不要随便改变父函数内部变量的值

	闭包可以在父函数外部，改变父函数内部变量的值。
												
	如果把父函数当作对象(object)使用，把闭包当作它的公用方法，把内部变量当作它的私有属性，这时一定要小心，不要随便改变父函数内部变量的值。

### 理解“闭包” step 2：掌握闭包的使用场景

#### 经典使用场景一：通过循环给页面上多个dom节点绑定事件

场景描述：假如页面上有5个button,要给button绑定onclick事件，点击的时候，弹出对应button的索引编号。

	<!DOCTYPE html>
	<html>
	<head>
	     <meta charset="UTF-8">
	</head>
	<body>
	    <button>Button0</button>
	    <button>Button1</button>
	    <button>Button2</button>
	    <button>Button3</button>
	    <button>Button4</button>
	</body>
	</html>

先随手来一段for循环：

	var btns = document.getElementsByTagName('button');
	for(var i = 0, len = btns.length; i < len; i++) {
	    btns[i].onclick = function() {
	        alert(i);
	    }
	}

通过执行该段代码，发现不论点击哪个button ，均alert 5；

因为，onclick事件是被异步触发的，当事件被触发时，for循环早已结束，此时变量 i 的值已经是 5 。所以，当onlick事件函数顺着作用域链从内向外查找变量 i 时，找到的值总是 5 。

解决方案：“闭包”！

在闭包的作用下，定义事件函数的时候，每次循环的i值都被封闭起来，这样在函数执行时，会查找定义时的作用域链，这个作用域链里的i值是在每次循环中都被保留的，因此点击不同的button会alert出来不同的i。

可以采用“立即执行函数”的方式完成这个需求。

	for(var i = 0, len = btns.length; i < len; i++) {
	    (function(i) {
	        btns[i].onclick = function() {
	            alert(i);
	        }
	    }(i))
	}

#### 闭包使用场景二：封装变量

比如立即执行函数作为闭包的一种应用，常用于第三方库，用于隔离作用域

假如有一个计算乘积的函数，mult函数接收一些number类型的参数，并返回乘积结果。为了提高函数性能，我们增加缓存机制，将之前计算过的结果缓存起来，下次遇到同样的参数，就可以直接返回结果，而不需要参与运算。这里，存放缓存结果的变量不需要暴露给外界，并且需要在函数运行结束后，仍然保存，所以可以采用闭包。

上代码：

	var mult = (function(){
	    var cache = {};
	    var calculate = function() {
	        var a = 1;
	        for(var i = 0, len = arguments.length; i < len; i++) {
	            a = a * arguments[i];
	        }
	        return a;
	    }
	    
	    return function() {
	        var args = Array.prototype.join.call(arguments, ',');
	        if(args in cache) {
	            return cache[args];
	        }
	        
	        return cache[args] = calculate.apply(null, arguments);
	    }
	}())
	
#### 闭包使用场景三：延续局部变量的寿命

img对象经常用于数据上报，如下：

	var report = function(src) {
	    var img = new Image();
	    img.src = src;
	}
	report('http://xxx.com/getUserInfo');
	
这段代码在运行时，发现在一些低版本浏览器上存在bug，会丢失部分数据上报，原因是img是report函数中的局部变量，当report函数调用结束后，img对象随即被销毁，而此时可能还没来得及发出http请求，所以此次请求就会丢失。

因此，我们使用闭包把img对象封闭起来，就可以解决数据丢失的问题：

	var report = (function() {
	    var imgs = [];
	    return function(src) {
	        var img = new Image();
	        imgs.push(img);
	        img.src = src;
	    }
	}())

### 闭包＋设计模式

在诸多设计模式中，闭包都有广泛的应用。

对象＝＝数据＋方法。而闭包是在过程中以环境的形式包含了数据。因此，通常面向对象能实现的功能，使用闭包也可以实现。

涉及到设计模式，闭包就是一种理所当然的存在，必须熟练使用，才可以理解每种设计模式的意图。

## 参数使用 arguments 对象 ##

保存了函数所有参数

- arguments对象不是数组，而是一个类似数组的对象。
	- 所以为了使用数组的方法，必须使用Array.prototype.slice.call先将其转为数组。
- ECMAScript 不会验证传递给函数的参数个数是否等于函数定义的参数个数
- 可以接受任意个数的参数（根据 Netscape 的文档，最多可接受 255 个）
- 遗漏的参数都会以 undefined 传递给函数，多余的函数将忽略

使用

- arguments.length 参数个数
- arguments[0] 第一个参数

### 模拟函数重载 ###

用 arguments 对象判断传递给函数的参数个数，即可模拟函数重载。

虽然不如重载那么好，不过已足以避开 ECMAScript 的这种限制。

	function doAdd() {
	  if(arguments.length == 1) {
	    alert(arguments[0] + 5);
	  } else if(arguments.length == 2) {
	    alert(arguments[0] + arguments[1]);
	  }
	}
	
	doAdd(10);	//输出 "15"
	doAdd(40, 20);	//输出 "60"

# 面向对象 #

ECMA-262 把对象（object）定义为“属性的无序集合，每个属性存放一个原始值、对象或函数”。严格来说，这意味着对象是无特定顺序的值的数组。

# 对象

**对象是键/值对的集合**


声明（字面）形式**创建对象可以直接看到

	var myObj = {
		key: value
		// ...
	};
	
## 类型 ##

在JavaScript中一共有6种类型(术语是"语言类型")

具体哪6种的分歧在null和function

红宝书：

- 五种基本类型：number、string、boolean、undefined、null
- 对象类型：object

JavaScript语言精髓与编程实践：

- number、string、boolean、undefined、object、function

{% asset_img 对象类型.png %}

依据是typeof的结果只有6种（不包括宿主对象），其中null的类型也是object.

	var n = 1, s = '2', b = true, u, nu = null, f = function(){} 
	console.log(typeof m);//number
	console.log(typeof s); //string
	console.log(typeof b); //boolean
	console.log(typeof u); //undefined
	console.log(typeof nu); //object
	console.log(typeof f); //function

### null和object

null 被当作一种对象类型，是语言本身的一个 bug。实际上，null 本身是基本类型。原因是这样的：不同的对象在底层都表示为二进制，在 JavaScript 中二进制前三位都为 0 的话会被判 断为 object 类型，null 的二进制表示是全 0，自然前三位也是 0，所以执行 typeof 时会返回“object”。然后一直被 ECMAScript 沿用了(太多线上项目依赖这个bug，修复会引起问题)，现在，null 被认为是对象的占位符。

### null和undefined

undefined 实际上是从值 null 派生来的，因此 ECMAScript 把它们定义为相等的。

	alert(null == undefined);  //输出 "true"
	
### 值类型和引用类型

- **值**类型/基本类型
	- 存储在栈（stack）中
		- 占据空间是固定的。所以存在栈中
	- 在许多语言中，字符串都被看作引用类型，而非原始类型，因为字符串的长度是可变的。
- **引用值**
	- 存储在堆（heap）中
	- 是一个指针（point），指向存储对象的内存处
	
### 原生对象、宿主对象、内置对象

- 宿主对象(host object)：依赖于宿主环境的对象
	- 所有 BOM 和 DOM 对象都是宿主对象
- 原生对象(native object)：独立于宿主环境的对象
	- 内置对象(built-in object)： 在**程序开始执行时被实例化**
		- 这意味着开发者不必明确实例化内置对象，它已被实例化了。
	- 其他对象：在执行ECMAScript程序的过程中生成。比如 Arguments

**由于JS可以动态修改对象属性，出于安全原因，以上三种对象都不能作为基类。防止恶意攻击(复写)。**

### Error子类
	
EvalError、RangeError、ReferenceError、SyntaxError、TypeError、URIError

### JavaScript中一切皆对象 错误

number、string、boolean、undefined 自身不是object

function是对象的一种子类型

### 分类

从创建角度看，分为两类

- 手动创建的对象
- **内置对象**(对象的子类型)
	- 内置对象实际上是**内置函数**(可以当作构造函数使用)

## 对象实例化/创建 ##

### 两种创建形式

**声明（字面）形式** 常用。一次性添加多个键值对。ES6才支持动态键名

	var myObj = {
		key: value
		// ...
	};

**构造形式** 少见。只能一个一个添加属性。支持动态键名

	var myObj = new Object();
	myObj.key = value;

无参构造函数，可以省略括号

	var oStringObject = new String();
	var oStringObject = new String;

- null 和 undefined 只有字面量形式。
- Date 只有构造形式。

### 两种创建方式的区别

两种创建方式仅在创建字符串,数字,布尔三种类型时，创建的结果才会有区别

- 声明（字面）形式，创建的是一个不可变的基本字面值(不是一个对象)
- 构造形式，创建的是一个构造器创建的对象

其他的类型，两种方式都是创建对象

实例：两种创建方式的区别

	var strPrimitive = "I am a string";
	console.log(typeof strPrimitive);	 // "string"
	console.log(strPrimitive instanceof String); // false
	
	var strObject = new String( "I am a string" );
	console.log(typeof strObject); // "object"
	console.log(strObject instanceof String); // true
	
	// 考察 object 子类型
	console.log(Object.prototype.toString.call( strObject ));	// [object String]
	console.log(Object.prototype.toString.call( strPrimitive ));	// [object String] 需要时自动转换
	
	console.log(typeof strPrimitive);	 // "string"
	console.log(strPrimitive instanceof String); // false
	
	console.log(strPrimitive.length); // 13
	console.log(strPrimitive.charAt( 3 )); // "m"
	console.log(typeof strPrimitive);	 // "string"
	console.log(strPrimitive instanceof String); // false

### 字面形式自动转换为对象

- 通过字面量形式创建字符串,数字,布尔时,引擎会在需要时(访问对应对象内置的属性和方法)自动把字面量转换成 String 对象,Number对象,Boolean对象

实例见上例：两种创建方式的区别

## 对象内容/属性

### 访问

- **属性(property)访问** `.` **最常见**
	- 必须符合标识符命名规范
- **键(key)访问** `[""]`
	- 可以接受任意字符串
	- 可以动态字符串 

实例

	var myObject = {
		a: 2
	};
	
	myObject.a;		// 2
	myObject["a"];	// 2

### 属性名

属性名一定是**字符串** 类型。

string 以外的（基本）类型值，会首先被转换为字符串

- 构造形式创建的对象，支持动态属性名
- ES6开始，字面形式创建的对象，也开始支持动态属性名

实例：构造形式

	var myObject = { };
	myObject[true] = "foo";
	myObject[3] = "bar";
	myObject[myObject] = "baz";
	
	console.log(myObject["true"]);				// foo
	console.log(myObject["3"]);					// bar
	console.log(myObject["[object Object]"]);	// baz
	console.log(Object.prototype.toString.call(myObject)); // [object Object]

实例：字面形式

	var prefix = "foo";
	var myObject = {
		[prefix + "bar"]: "hello",
		[prefix + "baz"]: "world"
	};
	
	console.log(myObject["foobar"]); // hello
	console.log(myObject["foobaz"]); // world

### 属性(Property) vs. 方法(Method)

语言规范把属性值为函数引用的属性称为方法。

这诱使人们认为函数 属于 这个对象。从技术上讲，函数绝不会“属于”对象。

所以，说一个偶然在对象的引用上被访问的函数就自动地成为了一个“方法”，过于**牵强附会**。

一个从属性访问得来的函数没有任何特殊性。即使是隐含的 this 绑定

	有些函数内部拥有 this 引用
	因为 this 是在运行时在动态绑定的
	它与这个对象的关系至多是间接的。

### 数组

数组也属于对象，内容更加结构化，采用 `数字索引`

非数字的属性，不影响length

	var myArray = [ "0", 1, "2" ];
	console.log(myArray.length); // 3
	myArray.bar = "bar"; // 非数字的属性
	console.log(myArray.length); // 3
	myArray[3] = 3; // 数字的属性
	myArray["4"] = 4; // 可以转为数字的属性
	console.log(myArray[3]); // 3
	console.log(myArray["3"]); // 3 
	console.log(myArray.bar); // bar
	console.log(myArray.3); // 语法错误
	console.log(myArray[4]); // 4
	console.log(myArray["4"]); // 4

### 属性描述符(Property Descriptors)

ES5 开始，所有的属性都用 属性描述符 来描述

#### 获取属性描述符

Object.getOwnPropertyDescriptor()

	var myObject = {
		a: 2
	};
	console.log(Object.getOwnPropertyDescriptor( myObject, "a" ));
	// {value: 2, 
		writable: true, 
		enumerable: true, 
		configurable: true}

#### 设置属性描述符

Object.defineProperty()

	var myObject = {};
	Object.defineProperty( myObject, "a", {
		value: 2,
		writable: true,
		configurable: true,
		enumerable: true
	} );

#### 可写性

是否可以 **设置属性值**

false，无法改变。strict模式会抛出 `TypeError`
	
	var myObject = {};
	Object.defineProperty( myObject, "a", {
		value: 2,
		writable: false, // 不可写！
		configurable: true,
		enumerable: true
	} );
	
	myObject.a = 3; //11行
	console.log(myObject.a); // 2

	"use strict";//strict模式
	报错如下：
	Uncaught TypeError: Cannot assign to read only property 'a' of object '#<Object>'
	    at <anonymous>:11:13
		(anonymous) @ VM616:11

`writable:false`	等价于 定义一个空的 setter。在strict模式下，需要扔出一个 TypeError

#### 可配置性

是否可以 **设置属性描述符，设置属性值，delete属性**

false
	
	设置属性描述符 抛出 TypeError
	设置属性值：为true 可以设置为false；为false，不能设置为true
	delete属性 无效果
		strict模式，抛出
			Uncaught TypeError: Cannot delete property 'a' of #<Object>
    			at <anonymous>:17:1
				(anonymous) @ VM622:17
	
#### 可枚举性

是否可以被枚举。如 `for..in` 循环

### 不可变性(Immutability)

将属性或对象设置为不可改变的

#### 对象常量（Object Constant）

对象属性的 *常量*（不能被改变，重定义或删除）

通过将 `writable:false` 与 `configurable:false` 组合

```js
var myObject = {};
Object.defineProperty( myObject, "FAVORITE_NUMBER", {
	value: 42,
	writable: false,
	configurable: false
} );
console.log(myObject.FAVORITE_NUMBER);//42
```

#### 防止扩展（Prevent Extensions）

防止一个对象被添加新的属性

调用 `Object.preventExtensions(..)`：

```js
var myObject = {
	a: 2
};
Object.preventExtensions( myObject );
myObject.b = 3;
myObject.b; // undefined
```

非 `strict mode` 模式下，`b` 的创建会无声地失败。

`strict mode` 下，抛出 `TypeError`。

	Uncaught TypeError: Cannot add property b, object is not extensible
    	at <anonymous>:5:12
#### 封印（Seal）

既不能添加属性，也不能重新配置或删除既存属性（*可以* 修改它们的值）

`Object.seal(..)` 相当于 `Object.preventExtensions(..)`，同时也将它所有的既存属性标记为 `configurable:false`。

#### 冻结（Freeze）

最高级别的不可变性，阻止任何对对象或对象直属属性的改变

`Object.freeze(..)` 相当于 `Object.seal(..)`，同时也将它所有的“数据访问”属性设置为 `writable:false`

“深度冻结”一个对象：在这个对象上调用 `Object.freeze(..)`，然后递归地迭代所有它引用的（目前还没有受过影响的）对象，然后也在它们上面调用 `Object.freeze(..)`。但是要小心，这可能会影响其他你并不打算影响的（共享的）对象。

### `[[Get]]` 与 属性访问

根据语言规范，属性访问本质是在 对象 上执行了一个 `[[Get]]` 操作（有些像 `[[Get]]()` 函数调用）。

- 在 对象 上寻找被请求的名称的属性，如果找到，就返回相应的值
- 如果有 `[[Prototype]]` 链，遍历寻找被请求的名称的属性
- 都不能找到被请求的属性的值，返回 `undefined`

```js
var myObject = {
	a: 2
};

myObject.a; // 2
myObject.b; // undefined
```

这个行为和通过标识符名称来引用 **变量** 不同。引用一个在可用的词法作用域内无法解析的变量，其结果不是像对象属性那样返回 `undefined`，而是抛出一个 `ReferenceError`。

```js
var myObject = {
	a: undefined
};

myObject.a; // undefined
myObject.b; // undefined
```

从 *值* 的角度来说，这两个引用没有区别 —— 它们的结果都是 `undefined`。然而，在 `[[Get]]` 操作的底层，处理 `myObject.b` 的操作要多做一些潜在的“工作”。

如果仅仅考察结果的值，你无法分辨一个属性是存在并持有一个 `undefined` 值，还是因为属性根本 *不* 存在所以 `[[Get]]` 无法返回某个具体值而返回默认的 `undefined`。可以使用 **`hasOwnProperty`**判断某个属性的存在性

### `[[Put]]` 与 属性设置

- 属性在当前的对象中存在
	1. 这个属性是访问器描述符（属性拥有 getter 或 setter）
		- 有 setter，调用 setter 设置值
		- 没有 setter，无法设置值
			- 在非 `strict mode` 下无声地失败
			- 在 `strict mode` 下抛出 `TypeError`
	2. 这个属性是数据描述符
		- `writable` 为 `true`，设置既存属性的值
		- `writable` 为 `false` 无法设置值
			- 在非 `strict mode` 下无声地失败
			- 在 `strict mode` 下抛出 `TypeError`

- 属性在当前的对象中还不存在，`[[Put]]` 操作会变得更微妙和复杂。我们将在第五章讨论 `[[Prototype]]` 时再次回到这个场景，更清楚地解释它。

### Getters 与 Setters

对象默认的 `[[Put]]` 和 `[[Get]]` 操作分别完全控制着如何设置既存或新属性的值，和如何取得既存属性。

**注意：** 使用较先进的语言特性，覆盖整个对象（不仅是每个属性）的默认 `[[Put]]` 和 `[[Get]]` 操作是可能的。

ES5 引入了一个方法来覆盖这些默认操作的一部分，但不是在对象级别而是针对每个属性，就是通过 getters 和 setters。

Getter 是实际上调用一个隐藏函数来取得值的属性。Setter 是实际上调用一个隐藏函数来设置值的属性。

将一个属性定义为拥有 getter 或 setter 或两者兼备，那么它的定义就成为了“**访问器描述符**”（与“数据描述符”相对）。

对于访问器描述符，它的 `value` 和 `writable` 性质因没有意义而被忽略，取而代之的是 JS 将会考虑属性的 `set` 和 `get` 性质（还有 `configurable` 和 `enumerable`）。

代码：两种方式定义getter

```js
var myObject = {
	// 为 `a` 定义一个 getter
	get a() {
		return 2;
	}
};

Object.defineProperty(
	myObject,	// 目标对象
	"b",		// 属性名
	{			// 描述符
		// 为 `b` 定义 getter
		get: function(){ return this.a * 2 },

		// 确保 `b` 作为对象属性出现
		enumerable: true
	}
);

myObject.a; // 2

myObject.b; // 4
```

不管是通过在字面对象语法中使用 `get a() { .. }`，还是通过使用 `defineProperty(..)` 明确定义，我们都在对象上创建了一个没有实际持有值的属性，访问它们将会自动地对 getter 函数进行隐藏的函数调用，其返回的任何值就是属性访问的结果。

代码：只有getter时设置值

```js
var myObject = {
	// 为 `a` 定义 getter
	get a() {
		return 2;
	}
};

myObject.a = 3; //无声抛弃赋值，strict则模式报错

myObject.a; // 2
```

代码：getter 和 setter

```js
var myObject = {
	// 为 `a` 定义 getter
	get a() {
		return this._a_;
	},

	// 为 `a` 定义 setter
	set a(val) {
		this._a_ = val * 2;
	}
};

myObject.a = 2;

myObject.a; // 4
```

**注意：** 我们引入了另一个普通属性 `_a_`。因为如果在get 和set中访问自身(this.a)会造成无限递归调用，最后报错 `RangeError: Maximum call stack size exceeded`

	get a() {
		return this.a;//调用get方法获取值，从而无限递归
	}
## 对象废除 ##

ECMAScript 拥有无用存储单元收集程序（garbage collection routine），意味着不必专门销毁对象来释放内存。

把对象的**所有引用**都设置为 null，可以强制性地废除对象。下次运行无用存储单元收集程序时，该对象将被销毁。

每用完一个对象后，就将其废除，来释放内存，这是个好习惯。

## 绑定 ##

绑定（binding），即把对象的接口与对象实例结合在一起的方法。

- **早绑定**（early binding）是先定义类型再实例化。
	- 编译器或解释程序能提前检查对象类型，提前转换机器代码。
	- 强类型语言使用早绑定。如Java 
	- 可以在开发环境中使用 IntelliSense
		- 即给开发者提供对象中属性和方法列表的功能。
- **晚绑定**（late binding）
	- 编译器或解释程序在运行前，不知道对象的类型。只需检查对象是否支持属性和方法即可。
	- ECMAScript 中的所有变量都采用晚绑定方法。

## 作用域 ##

**ECMAScript 只有公用作用域。** 所有属性和方法默认都是公用的！

### 私有作用域 ###

开发者确定一个规约，说明哪些属性和方法应该被**看做**私有的。并不改变属性是公用属性的事实，它只是告诉其他开发者，应该把该属性看作私有的。

比如规定在属性前后加下划线：

	obj._color_ = "blue";

### 静态作用域 ###

函数是对象，对象可以有属性和方法。

利用函数对象的属性和方法实现静态作用域

	function sayHello() {
	  alert("hello");
	}
	
	sayHello.alternate = function() {
	  alert("hi");
	}
	
	sayHello();		//输出 "hello"
	sayHello.alternate();	//输出 "hi"

## 关键字 this ##

this 指向对象本身

## 定义对象 ##

对象的属性分为两种：

- 属性：非函数属性
- 方法：函数属性

### 原始方式 ###

	var oCar = new Object;
	oCar.color = "blue";
	oCar.doors = 4;
	oCar.mpg = 25;
	oCar.showColor = function() {//指向函数的指针，意味着该属性是个方法
	  alert(this.color);
	};

问题：**未封装**。不利于复用

### 工厂方法 ###

	function createCar() {
	  var oTempCar = new Object;
	  oTempCar.color = "blue";
	  oTempCar.doors = 4;
	  oTempCar.mpg = 25;
	  oTempCar.showColor = function() {
	    alert(this.color);
	  };
	  return oTempCar;
	}
	
	var oCar1 = createCar();
	var oCar2 = createCar();

**核心问题：函数属性重复创建函数对象**

每次调用函数 createCar()，都要创建新函数 showColor()，意味着每个对象都有自己的 showColor() 版本。而事实上，每个对象都共享同一个函数。

#### 在工厂方法外定义对象的方法 ####

	function showColor() {
	  alert(this.color);
	}
	
	function createCar(sColor,iDoors,iMpg) {
	  var oTempCar = new Object;
	  oTempCar.color = sColor;
	  oTempCar.doors = iDoors;
	  oTempCar.mpg = iMpg;
	  oTempCar.showColor = showColor;
	  return oTempCar;
	}
	
	var oCar1 = createCar("red",4,23);
	var oCar2 = createCar("blue",3,25);

问题：**封装不彻底**。解决了重复创建函数对象的问题；但是从语义上讲，该函数不太像是对象的方法

### 构造函数方式 ###

构造函数这个概念是 **开发者定义的**。

**和工厂方法的区别**：

- 创建对象实例时使用new关键字，**形式上很像使用构造函数**。

- **定义时没有创建对象**

代码

	function Car(sColor,iDoors,iMpg) {//首字母通常大写
	  this.color = sColor;//没有创建对象，而是使用 this 关键字
	  this.doors = iDoors;
	  this.mpg = iMpg;
	  this.showColor = function() {
	    alert(this.color);
	  };
	}
	
	var oCar1 = new Car("red",4,23);
	var oCar2 = new Car("blue",3,25);

函数内没有创建对象，而是使用 this 关键字。使用 new 运算符构造函数时，在执行第一行代码前先创建一个对象，只有用 this 才能访问该对象。然后可以直接赋予 this 属性，**默认情况下是构造函数的返回值（不必明确使用 return 运算符）**。

问题：重复创建函数对象

### 构造函数 + 工厂方法 ###

实际上实现跟工厂方法一样(定义时创建了对象)，也有重复定义函数对象问题。不建议使用

	function Car() {
	  var oTempCar = new Object;
	  oTempCar.color = "blue";
	  oTempCar.doors = 4;
	  oTempCar.mpg = 25;
	  oTempCar.showColor = function() {
	    alert(this.color);
	  };
	
	  return oTempCar;
	}

	var car = new Car();//由于在 Car() 构造函数内部调用了 new 运算符，所以忽略此处的 new 运算符（位于构造函数之外），在构造函数内部创建的对象被传递回变量 car。

### 构造函数 + 原型方式 ###

**利用对象的 prototype 属性设置的属性，指向同一个对象**

	function Car() {
	}
	
	Car.prototype.color = "blue";
	Car.prototype.doors = 4;
	Car.prototype.mpg = 25;
	Car.prototype.drivers = new Array("Mike","John");
	Car.prototype.showColor = function() {
	  alert(this.color);
	};
	
	var oCar1 = new Car();
	var oCar2 = new Car();
	
	oCar1.drivers.push("Bill");
	
	alert(oCar1.drivers);	//输出 "Mike,John,Bill"
	alert(oCar2.drivers);	//输出 "Mike,John,Bill"


**构造函数内定义非函数属性，而函数属性(方法)则利用原型属性定义**

	function Car(sColor,iDoors,iMpg) {
	  this.color = sColor;
	  this.doors = iDoors;
	  this.mpg = iMpg;
	  this.drivers = new Array("Mike","John");
	}
	
	Car.prototype.showColor = function() {
	  alert(this.color);
	};
	
	var oCar1 = new Car("red",4,23);
	var oCar2 = new Car("blue",3,25);
	
	oCar1.drivers.push("Bill");
	
	alert(oCar1.drivers);	//输出 "Mike,John,Bill"
	alert(oCar2.drivers);	//输出 "Mike,John"

问题：**封装不彻底**。属性和方法定义分离了

### 构造函数 + 动态原型方法 ###

**最优方案**

**增加一个变量标识是否已经用原型方法初始化过函数属性**

	function Car(sColor,iDoors,iMpg) {
	  this.color = sColor;
	  this.doors = iDoors;
	  this.mpg = iMpg;
	  this.drivers = new Array("Mike","John");
	  
	  if (typeof Car._initialized == "undefined") {
	    Car.prototype.showColor = function() {
	      alert(this.color);
	    };
		
	    Car._initialized = true;
	  }
	}

### 实例：自定义StringBuffer实现字符串拼接 ###

与其他语言类似，ECMAScript 的**字符串是不可变的**，即它们的值不能改变

#### 字符串连接性能问题： ####

	var str = "hello ";
	str += "world";

实际上，这段代码在幕后执行的步骤如下：

1. 创建 "hello " 字符串。
2. 创建 "world" 字符串。
3. 创建存储连接结果的字符串。
4. 把 str 的当前内容复制到结果中。
5. 把 "world" 复制到结果中。
6. 更新 str，使它指向结果。

这种操作非常消耗资源。

#### 解决方案：用 Array 对象存储字符串 ####

var arr = new Array();
arr[0] = "hello ";
arr[1] = "world";
var str = arr.join("");

**问题：可读性不好**

#### 自定义StringBuffer ####

	function StringBuffer () {
	  this._strings_ = new Array();
	}
	
	StringBuffer.prototype.append = function(str) {
	  this._strings_.push(str);
	};
	
	StringBuffer.prototype.toString = function() {
	  return this._strings_.join("");
	};

使用

	var buffer = new StringBuffer ();
	buffer.append("hello ");
	buffer.append("world");
	var result = buffer.toString();

## 修改已有对象 ##

**原理：使用prototype 属性 实现**

- 添加新属性，新方法
- 复写已有属性，已有方法

所有本地对象都继承了 Object 对象，所以如果我们对 Object 对象做任何改变，都会反应在所有本地对象上。

### 复写已有方法 ###

**特别注意**：指向的原始函数将被无用存储单元回收程序**回收**。所以在覆盖原始方法前，比较安全的做法是**存储原始函数的指针**。

	Function.prototype.originalToString = Function.prototype.toString;
	
	Function.prototype.toString = function() {
	  if (this.originalToString().length > 100) {
	    return "Function too long to display.";
	  } else {
	    return this.originalToString();
	  }
	};

### 极晚绑定（Very Late Binding） ###

**对象实例化后再定义它的方法**

根本**不存在**极晚绑定。**本书采用**该术语描述 ECMAScript 中的这种现象

	var o = new Object();
	
	Object.prototype.sayHi = function () {
	  alert("hi");
	};
	
	o.sayHi();//输出hi

# 继承 #

**出于安全原因，本地类和宿主类不能作为基类。防止恶意攻击。**

尽管 ECMAScript 并没有像其他语言那样严格地定义抽象类，但有时它的确会创建一些不允许使用的类。通常，我们称这种类为抽象类。

## 继承机制的实现 ##

ECMAScript中的继承机制**并不是明确规定的**，而是通过**模仿实现的**

### 对象冒充 ###

ECMAScript 根本没打算设计对象冒充（object masquerading `[mɑ:skə'reɪdɪŋ]
`）。它是在开发者使用 this 关键字才发展出来

	function ClassA(sColor) {
	    this.color = sColor;
	    this.sayColor = function () {
	        alert(this.color);
	    };
	}
		
	function ClassB(sColor, sName) {
	    this.newMethod = ClassA;
	    this.newMethod(sColor);
	    delete this.newMethod;//所有新属性和新方法都必须在删除了新方法的代码行后定义。否则，可能会覆盖超类的相关属性和方法：
	
	    this.name = sName;
	    this.sayName = function () {
	        alert(this.name);
	    };
	}
	
	var objA = new ClassA("blue");
	var objB = new ClassB("red", "John");
	objA.sayColor();	//输出 "blue"
	objB.sayColor();	//输出 "red"
	objB.sayName();		//输出 "John"

#### 对象冒充可以实现多重继承 ####

ClassZ 继承 ClassX 和 ClassY

如果 类 ClassX 和 ClassY 具有同名的属性或方法，ClassY 具有高优先级

	function ClassZ() {
	    this.newMethod = ClassX;
	    this.newMethod();
	    delete this.newMethod;
	
	    this.newMethod = ClassY;
	    this.newMethod();
	    delete this.newMethod;
	}

### call() 和 apply() ###

由于对象冒充这种继承方法的流行，ECMAScript 的第三版为 Function 对象加入了两个方法，即 call() 和 apply()

#### call() ####

**call() 第一个参数用作 调用该方法的对象。其他参数是真正的函数参数**

	function sayColor(sPrefix,sSuffix) {
	    alert(sPrefix + this.color + sSuffix);
	};
	
	var obj = new Object();
	obj.color = "blue";
	
	sayColor.call(obj, "The color is ", "a very nice color indeed.");//输出The color is blue, a very nice color indeed

**实现**：等价于对象冒充方法的赋值、调用和删除这三行代码

	function ClassB(sColor) {
	    //this.newMethod = ClassA;
	    //this.newMethod(color);
	    //delete this.newMethod;
	    ClassA.call(this, sColor);
	}

#### apply() ####

**apply()第一个参数用作 调用该方法的对象。第二个参数是真正的函数参数组成的数组**

	function sayColor(sPrefix,sSuffix) {
	    alert(sPrefix + this.color + sSuffix);
	};
	
	var obj = new Object();
	obj.color = "blue";
	
	sayColor.apply(obj, new Array("The color is ", "a very nice color indeed."));

**实现**

	function ClassB(sColor, sName) {
	    //this.newMethod = ClassA;
	    //this.newMethod(color);
	    //delete this.newMethod;
	    ClassA.apply(this, arguments);
	}

#### 总结 ####

- 超类中的参数顺序与子类中的**参数顺序完全一致**(参数个数可以不一致，多余参数直接舍弃)时，apply()传递参数对象 **arguments**。
- 参数顺序不完全一致
	- apply()创建一个单独的数组，按照正确的顺序放置参数。
	- 使用 call()

### 原型链（prototype chaining） ###

**用另一类型的对象重写类的 prototype 属性**

	function ClassA() {
	}
	
	ClassA.prototype.color = "blue";
	ClassA.prototype.sayColor = function () {
	    alert(this.color);
	};
	
	function ClassB() {
	}
	
	ClassB.prototype = new ClassA();//ClassB.prototype赋值为ClassA的对象
	ClassB.prototype.name = "";
	ClassB.prototype.sayName = function () {
	    alert(this.name);
	};
	
	var objA = new ClassA();
	var objB = new ClassB();
	objA.color = "blue";
	objB.color = "red";
	objB.name = "John";
	objA.sayColor();	//输出 "blue"
	objB.sayColor();	//输出 "red"
	objB.sayName();		//输出 "John"

#### 原型链和对象冒充的区别 ####

**原型链，对 ClassB 的所有实例，instanceof 为 ClassA 和 ClassB 都返回 true**。

	alert(objB instanceof ClassA);	//输出 "true"
	alert(objB instanceof ClassB);	//输出 "true"

**原型链，不能实现多继承。**

**对象冒充可以实现多继承**

**对象冒充使用的是构造函数**


### 混合方式 ###

定义类的最好方式是用构造函数定义属性，用原型定义方法。

这种方式同样适用于继承机制，用对象冒充继承构造函数的属性，用原型链继承 prototype 对象的方法。

用这两种方式重写前面的例子，代码如下：

	function ClassA(sColor) {
	    this.color = sColor;
	}
	
	ClassA.prototype.sayColor = function () {
	    alert(this.color);
	};
	
	function ClassB(sColor, sName) {
	    ClassA.call(this, sColor);
	    this.name = sName;
	}
	
	ClassB.prototype = new ClassA();
	
	ClassB.prototype.sayName = function () {
	    alert(this.name);
	};

	var objA = new ClassA("blue");
	var objB = new ClassB("red", "John");
	objA.sayColor();	//输出 "blue"
	objB.sayColor();	//输出 "red"
	objB.sayName();	//输出 "John"

