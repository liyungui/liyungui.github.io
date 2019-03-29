---
title: URL和URI
date: 2019-03-27 15:50:53
categories:
  - Java
tags: 
	- Java
---
	
	Android 从网页中跳转到APP http://blog.csdn.net/buptlzx/article/details/9837137

就Android平台而言，URI主要分三个部分：`scheme, authority, path`。其中`authority`又分为`host和port`。格式如下： 

	scheme://host:port/path 

举个实际的例子： 

	content://com.example.project:200/folder/subfolder/etc 
	\---------/  \--------------/ \-/ \-------------------/ 
	scheme              host      port         path 
                 		\-----------/ 
                      	  authority    

data flag 

	<data android:host="string" 
	      android:mimeType="string" 
	      android:path="string" 
	      android:pathPattern="string" 
	      android:pathPrefix="string" 
	      android:port="string" 
	      android:scheme="string" /> 

api

	 Uri uri = intent.getData();  
	        System.out.println("scheme:"+scheme);  
	        if (uri != null) {  
	            String host = uri.getHost();  
	            String dataString = intent.getDataString();  
	            String id = uri.getQueryParameter("d");  
	            String path = uri.getPath();  
	            String path1 = uri.getEncodedPath();  
	            String queryString = uri.getQuery();  