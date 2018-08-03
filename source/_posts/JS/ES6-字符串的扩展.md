---
title: ES6-字符串的扩展
date: 2018-08-01 17:11:20
tags:
	- JS
	- ES6
---

# Unicode 表示法 #

JavaScript 内部，字符以 **UTF-16** 的格式储存，**每个字符固定为2个字节**

Unicode 码点大于0xFFFF的字符，需要4个字节储存，JavaScript 会认为它们是两个字符

JavaScript

- 用**\uxxxx**形式表示一个字符
	- 只限于码点在\u0000~\uFFFF之间的字符。
- 超出范围的字符，必须用**两个双字节**的形式表示。

**ES6将码点放入大括号，支持全码点**

**大括号表示法与四字节的 UTF-16 编码是等价的**

	"\u0061" // "a"

	"\u20BB7" // " 7"。 
		JavaScript 会理解成\u20BB+7。
		由于\u20BB是一个不可打印字符，所以只会显示一个空格，后面跟着一个7。

	"\uD842\uDFB7" // "𠮷"

	"\u{20BB7}" // "𠮷"
	
	'\u{1F680}' === '\uD83D\uDE80' // true
		大括号表示法与四字节的 UTF-16 编码是等价的

这样共有 6 种方法可以表示一个字符

	'\z' === 'z'  // true
	'\172' === 'z' // true
	'\x7A' === 'z' // true
	'\u007A' === 'z' // true
	'\u{7A}' === 'z' // true

# codePointAt() #

对于这种4个字节的字符，JavaScript 不能正确处理

- 字符串长度会误判为2
- charAt方法无法读取整个字符
- charCodeAt方法只能分别返回前两个字节和后两个字节的值

ES6 提供了codePointAt方法，能够正确处理 4 个字节储存的字符，返回一个字符的十进制码点。

	let s = '𠮷a';
	s.codePointAt(0).toString(16) // "20bb7"
	s.codePointAt(2).toString(16) // "61"

# String.fromCodePoint #

弥补了String.fromCharCode方法的不足(不能识别大于0xFFFF的码点)。

作用正好与codePointAt方法相反

# 字符串的遍历器接口 #

ES6 为字符串添加了遍历器接口，使得字符串可以被 `for...of` 循环遍历

最大的优点是可以识别大于0xFFFF的码点

	for (let codePoint of 'foo') {
	  console.log(codePoint)
	}
	// "f"
	// "o"
	// "o"

# at() #

charAt()不能识别码点大于0xFFFF的字符

	'𠮷'.charAt(0) // "\uD842"
	'𠮷'.at(0) // "𠮷"

# normalize() #

许多欧洲语言有**语调符号和重音符号**。

为了表示它们，Unicode 提供了两种方法。在**视觉和语义上都等价**

- **直接提供**带重音符号的字符
	- 比如Ǒ（\u01D1）。
- **提供合成**符号（combining character），即原字符与重音符号的合成，两个字符合成一个字符，
	- 比如O（\u004F）和ˇ（\u030C）合成Ǒ（\u004F\u030C）

JavaScript不能识别，**将合成字符视为两个字符**

ES6 提供**normalize()**，用来将字符的不同表示方法统一为同样的形式，这称为 **Unicode 正规化**

- 目前不能识别三个或三个以上字符的合成
	- 只能使用正则表达式，通过 Unicode 编号区间判断
- 接受一个参数来指定normalize的方式
	- **NFC**，**默认**参数
		- “标准等价合成”（Normalization Form Canonical Composition）
		- 视觉和语义上等价。
	- **NFD**
		- “标准等价分解”（Normalization Form Canonical Decomposition）
	- **NFKC**
		- “兼容等价合成”（Normalization Form Compatibility Composition），
		- 语义上等价，但视觉上不等价，比如“囍”和“喜喜”。（这只是用来举例，normalize方法不能识别中文。）
	- **NFKD**
		- “兼容等价分解”（Normalization Form Compatibility Decomposition

canonical	英[kəˈnɒnɪkl] 权威的

# includes(), startsWith(), endsWith() #

第二个参数(可省略)，表示开始搜索的位置

- 从第n个位置
- endsWith，前n个字符

实例

	let s = 'Hello world!';
	s.startsWith('world', 6) // true
	s.includes('Hello', 6) // false
	s.endsWith('Hello', 5) // true

# repeat()  #

将原字符串重复n次，返回一个新字符串

	'hello'.repeat(2) // "hellohello"
	'na'.repeat(0) // ""
	
# padStart()，padEnd() #

补全长度

两个参数

- 第一个参数用来指定字符串的**最小长度**
	- 原字符串的长度 >= 最小长度，返回原字符串
	- 原字符串长度+补全字符串长度 > 最小长度，截去超出位数的补全字符串
- 第二个参数是**用来补全的字符串**
	- 默认值为空格

实例

	'abc'.padStart(10, '0123456789')
	// '0123456abc'

# matchAll() #

返回一个正则表达式在当前字符串的所有匹配

# 模板字符串(template string) #

**增强版**的字符串，用**反引号 `** 标识。

- 当作普通字符串
- 定义多行字符串
	- 所有的空格和缩进都会被保留在输出之中
		- 不想要，可以使用trim方法消除
- 在字符串中嵌入变量。
	- 变量名写在 `${}` 之中
	- 变量可以是任意的 JavaScript 表达式。本质就是执行JavaScript代码
		- 运算
		- 对象属性
		- 函数调用

在模板字符串中使用反引号，则前面要用反斜杠转义

	`User ${user.name} is not authorized to do ${action}.`;

	`Hello ${'World'}`
	// "Hello World"
		本质就是执行JavaScript代码。字符串，将会原样输出

**模板字符串能嵌套**

# 标签模板(tagged template) #

- 其实不是模板
- 而是**函数调用**的一种特殊形式。
	- “标签”指的就是函数
	- 紧跟在后面的模板字符串就是它的参数。
		- 模板字符里面有变量，会将模板字符串先处理成多个参数，再调用函数

## 应用 ##

- **过滤 HTML 字符串，防止用户输入恶意内容**
- **国际化**处理。多语言转换

实例

	let a = 5;
	let b = 10;
	tag`Hello ${ a + b } world ${ a * b }`;
	// 等同于
	tag(['Hello ', ' world ', ''], 15, 50);
	
		第一个参数是一个数组
			该数组的成员是模板字符串中那些没有变量替换的部分
		其他参数
			模板字符串各个变量被替换后的值

# String.raw() #

返回 **斜杠都被转义**和**变量都被替换**的模板字符串

	String.raw`Hi\n${2+3}!`;
	// 返回 "Hi\\n5!"
	
	String.raw`Hi\u000A!`;
	// 返回 "Hi\\u000A!"

	String.raw`Hi\\n`
	// 返回 "Hi\\\\n"