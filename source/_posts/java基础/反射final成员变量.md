---
title: 反射final成员变量
date: 2019-03-27 15:41:53
categories:
  - Java
tags: 
	- Java
---
	
	利用反射对修饰符为final的成员变量进行修改 http://my.oschina.net/dxqr/blog/215504

## 非final成员变量 ##
	class Entity {
		public int i = 1;
	}	

	try {
		Entity e = new Entity();
		System.out.println("before: " + e.i);
			
		Field f = Entity.class.getDeclaredField("i");
		f.setInt(e, 2);
		// 或者 f.set(e, 2);// java会自动装箱拆箱
		System.out.println("after: " + e.i);
	} catch (Exception e) {
		e.printStackTrace();
	}

## final成员变量 ##

	class Entity {
		public final int i = 1;
	}

反射会报异常:

	java.lang.IllegalAccessException: Can not set final int field com.test.Entity.i to (int)2

修改成员变量的final修饰符,使其变为public int i = 1;具体方法如下:
	
	try {
		Entity e = new Entity();
		System.out.println("before: " + e.i);
				
		Field f = Entity.class.getDeclaredField("i");
				
		Field modifiersField = Field.class.getDeclaredField("modifiers");
		modifiersField.setAccessible(true);
        System.out.println(f.getModifiers()); // 输出17:表示修饰符为:public final
		modifiersField.setInt(f, f.getModifiers() & ~Modifier.FINAL);
		System.out.println(f.getModifiers());// 输出1:表示修饰符已经被修改为:public
	
		f.setAccessible(true);
		f.setInt(e, 2);
		System.out.println("after: " + e.i);//输出还是1.没修过成功
	} catch (Exception e) {
		e.printStackTrace();
	}

发现还是没有修改成功。会不会跟是基本数据类型有关？修改成员变量的数据类型为 Integer

	class Entity {
		public final Integer i = 1;
	}

然后再执行,发现结果已经被修改了

**final成员变量，对象数据类型可以修改,基本数据类型不能修改**

**final成员变量，final String s = new String("a"); 可以修改,final String s = "a" 不能修改**
