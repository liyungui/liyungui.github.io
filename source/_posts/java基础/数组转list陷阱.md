---
title: 数组list陷阱
date: 2019-03-27 15:41:53
categories:
  - Java
tags: 
	- Java
---

	String[] artistTypes = getResources().getStringArray(R.array.artist_type);
	List<String> list = Arrays.asList(artistTypes); 

上面代码是毫无问题的。

	String[] artistTypes = getResources().getStringArray(R.array.artist_type);
	ArrayList<String> list = (ArrayList<String>) Arrays.asList(artistTypes); 

运行报错。java.util.Arrays$ArrayList cannot be cast to java.util.ArrayList

这就说明，Arrays.asList转出来的是Arrays$ArrayList（内部类），只是和java.util.ArrayList名字相同。

为什么转为List不报错呢？因为Arrays$ArrayList实现了List接口
	
	public class ArrayList<E> extends AbstractList<E> implements Cloneable, Serializable, RandomAccess {

	public class Arrays {
	    private static class ArrayList<E> extends AbstractList<E> implements
	            List<E>, Serializable, RandomAccess {


研究过程发现

	Arrays.asList转出来的是Arrays$ArrayList继承AbstractList。remove，add等method在AbstractList中是默认throw UnsupportedOperationException而且不作任何操作。
	java.util.Arrays$ArrayList继承了静态数组 大小 固定不变的特性。

找了很久，找到下面的解决方法

	List myList = new ArrayList(); 
	String[] myStringArray = new String[] {"Java", "is", "Cool"};
	Collections.addAll(myList, myStringArray);