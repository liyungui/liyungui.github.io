---
title: Android Hook原理
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[gdb演示Android ELF的GOT Hook](http://laokaddk.blog.51cto.com/368606/1168989/ ) 

需要Android源码环境编译，GOT时还需要源码库下的Android库的符号信息（包括libmym.so）

gdb '/home/liyunggui/桌面/testhook'

Reading symbols from /home/liyunggui/桌面/testhook...(no debugging symbols found)...done. 可能是因为编译过程跟博文不同，导致调试信息丢失而找不到


