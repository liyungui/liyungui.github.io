---
title: MVVM dataBinding 常用表达式
date: 2019-01-14 09:10:56
categories:
  - 编程思想
tags:
  - 编程思想
---

@{}和@={}

	@{}单向绑定。VM变化会映射到View
	@={}双向绑定。VM变化会映射到View，View变化也会映射到VM。如EditText输入变化，VM值也会自动变化，不需getText
	VM的成员变量必须继承BaseObservable或定义为ObservableField类型。

visibility

	android:visibility="visible" 
	android:visibility="@{titleVM.showBackIcon ? View.VISIBLE : View.GONE}"
	引用View的属性，所以必须import View类型，
		<import type="android.view.View" />
	否则报错：Identifiers must have user defined types from the XML file. View is missing it
	