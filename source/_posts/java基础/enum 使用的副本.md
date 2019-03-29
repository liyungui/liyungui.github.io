---
title: enum使用
date: 2019-03-27 15:46:53
categories:
  - Java
tags: 
	- Java
---

## emun也是class ##

经过反编译知道，enum也是被编译成了一个class文件。

	public final class RoomType extends java.lang.Enum{ }

如果命名意义明确，enum可以单独作为一个类。

## 枚举项的值默认为从0开始递增的int值 ##

	enum MyEnum{
	    FIRST_ELEMENT,
	    SECOND_ELEMENT,
	}
	ordinal()返回值的序列号，从0开始

## 自定义枚举项的值 ##

	enum FruitEnum {
	    APPLE(1), ORANGE(2); //调用构造函数来构造枚举项
	
	    private int value = 0;
	
	    private FruitEnum(int value) { //必须是private的构造方法，否则编译错误
	        this.value = value;
	    }
	
	    public static FruitEnum valueOf(int value) { //值(这里是int，可以使string等)到enum的转换函数
	        switch (value) {
	        case 1:
	            return APPLE;
	        case 2:
	            return ORANGE;
	        default:
	            return null;
	        }
	    }
	
	    public int value() { //enum到值的转换函数
	        return this.value;
	    }
	}

	如果是int到enum自然排序转换，还可以调用values()(系统api，返回enum数组)
	public enum RoomType {
		Single("single"), Group("group");
	
		String value;
	
		RoomType(String value) {
			this.value = value;
		}
	
		public String getValue() {
			return value;
		}
	
		public static RoomType fromInt(int i) {//参数只能是索引
			return values()[i];
		}
	}
	RoomType.fromInt(0) 返回的是第一个enum项Single