---
title: ES6-Module
date: 2018-08-06 10:41:20
tags:
	- JS
	- ES6
---

# 模块 #

ES6 模块的设计思想是尽量的**静态化**，使得**编译时**就能确定模块的依赖关系，以及输入和输出的变量。

- ES6 **模块不是对象**
- 通过export命令显式指定输出的代码，再通过import命令输入

“**编译时加载**”或者静态加载，即 ES6 可以在编译时就完成模块加载

## 严格模式 ##

严格模式主要有以下限制。

- 变量必须声明后再使用
- 函数的参数不能有同名属性，否则报错
- 不能使用with语句
- 不能对只读属性赋值，否则报错
- 不能使用前缀 0 表示八进制数，否则报错
- 不能删除不可删除的属性，否则报错
- 不能删除变量delete prop，会报错，只能删除属性delete global[prop]
- eval不会在它的外层作用域引入变量
- eval和arguments不能被重新赋值
- arguments不会自动反映函数参数的变化
- 不能使用arguments.callee
- 不能使用arguments.caller
- 禁止this指向全局对象
- 不能使用fn.caller和fn.arguments获取函数调用的堆栈
- 增加了保留字（比如protected、static和interface）

# export 命令 #

- **输出对外的接口**
	- 必须与模块内部的变量建立一一对应关系
		- 定义的时候直接export
		- 先定义，然后通过 `export {接口名}` 输出
	- **输出 变量、函数、类**
	- 对外接口名称
		- 默认就是原来的名字
		- 可以使用as关键字重命名
	- 接口与其对应的值是**动态绑定关系**
		- 即通过该接口，可以取到模块内部实时的值。

实例：export

建议使用第二种写法。因为这样就可以在脚本尾部，一眼看清楚输出了哪些变量

	// profile.js
	export var firstName = 'Michael';
	export var lastName = 'Jackson';
	export var year = 1958;

	// profile.js
	var firstName = 'Michael';
	var lastName = 'Jackson';
	var year = 1958;
	export {firstName, lastName, year};

实例：export对外提供接口，必须与模块内部一一对应

	// 报错
	export 1;
	
	// 报错
	var m = 1;
	export m;

		输出 1。1只是一个值，不是接口

	正确写法

	// 写法一
	export var m = 1;
	
	// 写法二
	var m = 1;
	export {m};

# import 命令 #

- 输入对外的接口
	- 通过 `import {接口名} from 'a.js'` 输入
		- 文件支持相对路径和绝对路径
			- 不带路径，就必须有配置文件，告诉引擎如何取到模块
		- .js 后缀可以省略
	- **输入 变量、函数、类**
		- 变量只读。
			- 因为本质就是输入接口。在加载模块的脚本中不允许改写接口
			- 变量属性改写。
				- 强烈建议不要改，很难差错
	- 对外接口名称
		- 默认就是原来的名字
		- 可以使用as关键字重命名
		- **支持通配符 `*`，表示整体加载模块**
			- 模块整体加载所在的那个对象，应该是可以静态分析的，所以**不允许运行时改变**
				- **对象本身及对象属性，不允许赋值**
- 静态执行
	- **不能使用表达式和变量**
		- 这些只有在运行时才能得到结果
	- 具有提升效果
		- 即使卸载文件末尾，也会提升到整个模块的头部，首先执行
	- 会**执行所加载的模块**
		- 多次重复执行同一句import语句，只会执行一次

实例：import

	// main.js
	import {firstName, lastName, year} from './profile.js';

实例：输入变量只读

	import {a} from './xxx.js'
	a = {}; // Syntax Error : 'a' is read-only;
	a.foo = 'hello'; // 合法操作。强烈建议不要改

实例：模块整体加载，所在对象不允许运行时修改

	// circle.js
	export function area(radius) {
	  return Math.PI * radius * radius;
	}
	export function circumference(radius) {
	  return 2 * Math.PI * radius;
	}
	
	// main.js 加载模块：逐一指定要加载的方法，整体加载的写法如下。
	import { area, circumference } from './circle';
	console.log('圆面积：' + area(4));
	console.log('圆周长：' + circumference(14));

	// main.js 加载模块：整体加载模块
	import * as circle from './circle';
	console.log('圆面积：' + circle.area(4));
	console.log('圆周长：' + circle.circumference(14));
	// 下面两行都是不允许的
	circle.foo = 'hello';
	circle.area = function () {};
		模块整体加载所在的那个对象（上例是circle），应该是可以静态分析的，
		所以不允许运行时改变。下面的写法都是不允许的。

# export default 命令 #

**为模块指定默认输出(唯一一个)**

- 方便用户，不用阅读文档就能加载模块
	- import命令需要知道所要加载的变量名或函数名
	- 默认输出只有唯一一个，在输出和输入时**接口名不需要大括号**
- 本质就是输出一个叫做default的接口。把default后面的值赋给default
	- 跟常量值
	- 跟变量
		- 不能跟变量声明
	- 跟类

实例：

	// export-default.js
	export default function () {
	  console.log('foo');
	}
	//第二种写法
	function foo() {
	  console.log('foo');
	}
	export default foo;

	// import-default.js
	import customName from './export-default';
	customName(); // 'foo'

实例：不能跟变量声明

	// 正确
	export var a = 1;
	
	// 正确
	var a = 1;
	export default a;
	
	// 错误
	export default var a = 1;

实例：一条import语句中，同时输入默认方法和其他接口

	import _, { each, each as forEach } from 'lodash';

# export 与 import 的复合写法 #

在一个模块之中，**先输入后输出同一个模块**

模块实际上并没有被导入当前模块，只是相当于**对外转发**了模块接口，导致当前模块不能直接使用改模块。

	export { foo, bar } from 'my_module';
	
	// 可以简单理解为
	import { foo, bar } from 'my_module';
	export { foo, bar };

实例：接口改名

	// 接口改名
	export { foo as myFoo } from 'my_module';

实例：整体输出

	export * from 'my_module';

实例：具名接口改为默认接口

	export { es6 as default } from './someModule';
	
	// 等同于
	import { es6 } from './someModule';
	export default es6;

实例：默认接口改名为具名接口

	export { default as es6 } from './someModule';

# 模块的继承 #

模块之间也可以继承

# 跨模块常量 #

	// constants.js 模块
	export const A = 1;
	export const B = 3;
	export const C = 4;
	
	// test1.js 模块
	import * as constants from './constants';
	console.log(constants.A); // 1
	console.log(constants.B); // 3
	
	// test2.js 模块
	import {A, B} from './constants';
	console.log(A); // 1
	console.log(B); // 3