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

示例

	var test;
	var test = "hi";
	test = 55;
	var test = "hi", age = 25;

## 变量值 ##

- 原始值
	- 存储在栈（stack）中
	- **原始类型**
		- 5 种。即 Undefined、Null、Boolean、Number 和 String 
		- 占据空间是固定的。所以存在栈中
		- 在许多语言中，字符串都被看作引用类型，而非原始类型，因为字符串的长度是可变的。

- 引用值
	- 存储在堆（heap）中
	- 对象
	- 是一个指针（point），指向存储对象的内存处

### 原始类型 ###

#### Undefined 类型 ####

Undefined 类型只有一个值，即 undefined

变量未初始化时，该变量的默认值是 undefined

#### Null 类型 ####

另一种只有一个值的类型是 Null，它只有一个专用值 null，即它的字面量。值 undefined 实际上是从值 null 派生来的，因此 ECMAScript 把它们定义为相等的。

	alert(null == undefined);  //输出 "true"

#### typeof 运算符 ####

返回值：

- undefined - 变量是 Undefined 类型的
- boolean - 变量是 Boolean 类型的
- number - 变量是 Number 类型的
- string - 变量是 String 类型的
- object - 变量是一种引用类型或 Null 类型的
	- typeof 运算符对于 null 值会返回 "Object"实际上是 JavaScript 最初实现中的一个错误，然后被 ECMAScript 沿用了。现在，null 被认为是对象的占位符，从而解释了这一矛盾，但从技术上来说，它仍然是原始值。
	
### 引用类型 ###

ECMAScript 定义了“对象定义”，逻辑上等价于其他程序设计语言中的类。ECMA-262 中根本没有出现“类”这个词。所以精确的说，应该称为“对象”

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

因为是弱类型

- 参数，不必声明类型，直接参数名
- 返回值，不必声明类型，直接return返回

示例

	function functionName(arg0, arg1, ... argN) {
	  statements
	}

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

## 函数其实是 Function 对象 ##

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

## 闭包 closure ##

函数对象在变量作用域之外，访问变量。**改变了变量作用域**

全局变量是一个简单的闭包实例

	var sMessage = "hello world";

	function sayHelloWorld() {
	  alert(sMessage);
	}
	
	sayHelloWorld();

在一个函数中定义另一个

	var iBaseNum = 10;
	
	function addNum(iNum1, iNum2) {
	  function doAdd() {
	    return iNum1 + iNum2 + iBaseNum;
	  }
	  return doAdd();
	}

# 面向对象 #

ECMA-262 把对象（object）定义为“属性的无序集合，每个属性存放一个原始值、对象或函数”。严格来说，这意味着对象是无特定顺序的值的数组。

## 实例化 ##

无参构造函数，可以省略括号

	var oStringObject = new String();
	var oStringObject = new String;

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

## 对象类型 ##

ECMAScript 中，可以创建并使用的对象有三种：

- **本地对象**(native object)。 **独立于宿主环境**的 ECMAScript 实现提供的对象
	- **内置对象**(built-in object)。 在 ECMAScript **程序开始执行时被实例化**。
		- 这意味着开发者不必明确实例化内置对象，它已被实例化了。
		- 每个内置对象都是本地对象
- **宿主对象**(host object)。 **所有非本地对象**
	- 所有 BOM 和 DOM 对象都是宿主对象

**出于安全原因，本地类和宿主类不能作为基类。防止恶意攻击。**

### 本地对象 ###

包括：

- Object
- Boolean
- Number
- String
- Date
- Array
- Function
- RegExp
- Error
- EvalError
- RangeError
- ReferenceError
- SyntaxError
- TypeError
- URIError

### 内置对象 ###

包括：

- Global
- Math

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

