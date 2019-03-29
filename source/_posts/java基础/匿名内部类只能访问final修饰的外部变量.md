---
title: 匿名内部类只能访问final修饰的外部变量
date: 2019-03-27 15:41:53
categories:
  - Java
tags: 
	- Java
---

匿名内部类用法

	public class TryUsingAnonymousClass {
	    public void useMyInterface() {
	        final Integer number = 123;
	        System.out.println(number);
	
	        MyInterface myInterface = new MyInterface() {
	            @Override
	            public void doSomething() {
	                System.out.println(number);
	            }
	        };
	        myInterface.doSomething();
	
	        System.out.println(number);
	    }
	}

编译后的结果

	class TryUsingAnonymousClass$1
	        implements MyInterface {
	    private final TryUsingAnonymousClass this$0;
	    private final Integer paramInteger;
	
	    TryUsingAnonymousClass$1(TryUsingAnonymousClass this$0, Integer paramInteger) {
	        this.this$0 = this$0;
	        this.paramInteger = paramInteger;
	    }
	
	    public void doSomething() {
	        System.out.println(this.paramInteger);
	    }
	}

- 匿名内部类最终用会编译成一个单独的类
- 被该类使用的变量会以构造函数参数的形式传递给该类
- 如果变量 不定义成final的，在匿名内部类被可以被修改，进而造成和外部的不一致的问题，为了避免这种不一致的情况，Java 规定匿名内部类只能访问final修饰的外部变量。