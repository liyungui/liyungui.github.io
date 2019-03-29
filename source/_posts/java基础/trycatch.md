---
title: trycatch
date: 2019-03-27 15:49:53
categories:
  - Java
tags: 
	- Java
---
	
	public static void main(String[] args) {
		try {
			System.out.println("before try  catch exception");
			int a = 0 / 0;
			System.out.println("after tyr catch exception");//无法执行到
		} catch (Exception e) {
			System.out.println(e.getMessage());
			System.out.println("catch");
		} finally {
			System.out.println("finally");
		}
		System.out.println("before un try catch exception");
		int a = 0 / 0;
		System.out.println("after un try catch exception");//无法执行到
	}

结果

	before try  catch exception
	/ by zero
	catch
	finally
	before un try catch exception
	Exception in thread "main" java.lang.ArithmeticException: / by zero
		at MainTest.main(MainTest.java:20)

结论

	1. try语句块中，异常后面的代码无法执行
	2. try catch语句块外的代码，正常执行。try catch最大意义所在（最常用场景）--保证try catch语句块后面的代码正常执行