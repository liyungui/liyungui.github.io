---
title: AndroidStudio快捷键
date: 2018-11-06 18:40:53
tags: 
	- AndroidStudio
---

keymap 是 Mac OS X 10.5+
		
# 查找

```
搜索任意内容(all,class,symbol,action)：双击sft
搜索类：cmd + o
搜索symbol(类/方法/参数)：cmd + opt + o
搜索action：cmd + sft + a

当前文件查找/替换：cmd + f/r。
	下/上一个高亮：cmd/(cmd + sft) + g
全局文件查找/替换：cmd + sft + f/r。

最近访问文件列表：cmd + e

类/方法在当前文件引用：cmd + fn + F7
类/方法在全局文件引用：opt + fn + F7

列出方法被调用的层级结构：ctr + opt + h
列出实现类：cmd + opt + b
跳转至超类的方法：cmd + u

在当前文件快速导航(列出成员方法列表，支持搜索)：cmd + fn + F12
跳转至行数：cmd + l
返回上次编辑位置：cmd + [/]
					cmd + opt + ←/→
跳转至错误或警告：fn + F2
					
列出函数的有效参数：cmd + p	
查看类/方法的文档注释： fn + F1	
```

# 编辑

```
复制(没有选择区域则复制一行)：cmd + c
粘贴：cmd + v
列出最近使用的粘贴板内容，然后选择并粘贴：cmd + sft + v
复制并粘贴(没有选择区域则复制一行)：cmd + d

向前删除：delete  
向后删除：fn + delete
删除行：cmd + delete


撤销/反撤销：cmd + z/(sft + z)

以词语(中英驼峰)为单位移动光标：alt + ←/→

智能选中区域(可重复多次，或不断扩缩)：alt + ↑/↓

局部代码块(可重复多次，极限是当前函数)展开/收缩：cmd + +/-
全部代码块(当前类所有方法和方法注释)展开/收缩：cmd + sft + +/- 
   
Surround with(if，for，try-catch等)：cmd + opt + t
生成模板代码块(if，while等)：cmd + j
生成方法(getter/setter，构造，toString等)：cmd + n
自动补全(分号，()，{})：cmd + sft + enter
意图猜测：opt + enter
重写父类方法：ctr + o
实现抽象方法：ctr + i

单行注释：cmd + /
多行注释：cmd + opt + /

逐行移动代码：opt + sft + ↑/↓
相邻两行代码互换：cmd + sft + ↑/↓

切换大小写：cmd + sft + u

切换文件：ctr + tab

合并为一行：ctr + sft + j 相当于删除了换行

列编辑：alt + 鼠标框选

格式化代码： cmd + opt + l
自动缩进对齐：ctr + alt + i

清除无效导包： ctr + opt + o

隐藏窗口：sft + esc
```

# 代码重构

```
重命名(类，方法，变量)：sft + fn + F6
方法抽离：cmd + opt + m
抽成方法参数：cmd + opt + p
抽成局部变量：cmd + opt + v
抽成成员变量：cmd + opt + f
```

# 编译运行

```
运行：ctr + r
调试：ctr + d
```

# git

```
打开git操作列表：ctr + v
commit：cmd + k
push：cmd + sft + k
revert：cmd + sft + z
fetch：ctr + f
pull：ctr + p
```
