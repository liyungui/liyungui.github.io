---
title: Android dalvik hook原理与实现
date: 2018-05-18 16:44:42
tags: 
	- Hook

---


[Android dalvik hook的另外一种实现形式](http://bbs.pediy.com/showthread.php?t=187522&highlight=dalvik+hook) 

[注入安卓进程,并hook java世界的方法](http://bbs.pediy.com/showthread.php?t=186054) 

# 替换方法实现--修改Method对象的insns字段 #

dalvik中，每一个java方法都有一个对应的Method对象（Method结构体声明在源码目录树下的dalvik/vm/oo/Object.h文件内）

Method结构体字段insns保存着java方法具体的实现代码。

下面用代码实现说明

	public class HelloJni extends Activity {
		static {
			System.loadLibrary("hello-jni");
		}
	
		public void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
	
			TextView tv = new TextView(this);
			tv.setText(truth());
			setContentView(tv);
		}
	
		public String truth() {
			return "hello from truth";
		}
	
		public String fake() {
			return "fake string";
		}
	
	}
	-----------------------c code --------------------
	#include <string.h>
	#include <jni.h>
	
	jint JNI_OnLoad(JavaVM* vm, void* reserved) {
		JNIEnv *env;
	
		if ((*vm)->GetEnv(vm, (void**) &env, JNI_VERSION_1_6) != 0) {
			return -1;
		}
		jclass father = (*env)->FindClass(env, "com/example/hellojni/HelloJni"); //搜索java类
	
		jmethodID truthMethod = (*env)->GetMethodID(env, father, "truth", "()Ljava/lang/String;"); //搜索java方法
		jmethodID fakeMethod = (*env)->GetMethodID(env, father, "fake", "()Ljava/lang/String;");
	
		// jmethodID 是一个ClassObject 的指针类型，
		// ClassObject 对象的偏移地址32位处为insns字段。
		*(int *) ((int) truthMethod + 32) = *(int *) ((int) fakeMethod + 32);
	
		int result = JNI_OK;
		return ((result != JNI_OK) ? result : JNI_VERSION_1_6);
	}

# 替换方法为native方法--native方法替换java方法 #

正常情况下,只能在Java世界通过jni调用native方法,而native不能在没有任何java上的支持下干涉java世界。

传统的linux进程注入技术在安卓上只能进入目标进程的native世界。

本教程是要注入别的进程,并hook java世界的java 方法!

程序大致的流程是这样的：

	so.so注入到目标进程 --> 执行Hook()函数 
					  --> Hook()加载libTest.so,获取libTest.so定义的Hook信息.接着用ClassMethodHook()hook java世界的方法.

  关键一,从native世界进入java世界。我们只要获得一个JNIEnv就能进入到java世界了。突破点就在android::AndroidRuntime::getJavaVM();这个静态方法能够获取一个JavaVM,JavaVM->GetEnv方法能够获得一个JNIEnv了。JNIEnv是和线程相关的,使用前一定记得将其附加到当前进程,也要在适当的时候将其销毁。

  关键二,怎么影响内存里的java代码。替换内存是不现实的,但是可以取巧，在运行时将一个不是native的方法修改成native方法。我们知道java代码里将一个方法声明为native方法时,对此函数的调用就会到native世界里找。

# 两种方法的比较 #

||	替换方法实现|替换方法为native方法|
|:---|:---|:---|
|难度|容易，只要修改insns字段|难，多个字段|
|线程安全|安全|非安全，修改字段过多|
