---
title: Android Hook原理
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[Android inline hook之原理分析篇 ](http://www.sanwho.com/248.html)

||	修改GOT|	inLine|
|:---|:---|:---|
|实现难易|比较容易，只需知道elf文件中调用外部符号的地址|比较难，需要分析函数实现汇编码，保持堆栈平衡|
|使用频率|基本都是用此方式||
|功能强弱|比较弱，只能hookGOT调用方式（通过java层调用API真实实现代码）|很强大，能hookjni调用真实实现API的方式|
|R11|fp|桢指针|
|R12|ip|指令指针，内部过程调用寄存器|
|R13|sp|栈指针|
|R14|lr|返回地址，连接寄存器|
|R15|pc|程序计数器|

