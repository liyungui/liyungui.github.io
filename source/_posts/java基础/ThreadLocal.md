---
title: ThreadLocal
date: 2019-03-27 15:49:53
categories:
  - Java
tags: 
	- Java
---

ThreadLocal，线程本地变量，也叫做线程本地存储

ThreadLocal为变量在每个线程中创建一个副本，每个线程可以访问自己内部的副本变量。

ThreadLocal类提供的几个方法：

	public T get() { } //获取ThreadLocal在当前线程中保存的变量副本
	public void set(T value) { } //设置当前线程中变量的副本
	public void remove() { } //移除当前线程中变量的副本
	protected T initialValue() { } //一个延迟加载方法

# 基本使用 #

	ThreadLocal<Object> threadLocal = new ThreadLocal<Object>();
	threadLocal.set("123");
	threadLocal.get();

# 实现原理 #

	public T get() {
        Thread t = Thread.currentThread();
        ThreadLocalMap map = getMap(t);
        if (map != null) {
            ThreadLocalMap.Entry e = map.getEntry(this);
            if (e != null)
                return (T)e.value;
        }
        return setInitialValue();
    }
	ThreadLocalMap getMap(Thread t) {
        return t.threadLocals;
    }
	public class Thread implements Runnable {
		ThreadLocal.ThreadLocalMap threadLocals = null;//存储线程变量副本
	}
	static class ThreadLocalMap {
        static class Entry extends WeakReference<ThreadLocal> {
            Object value; //The value associated with this ThreadLocal.
            Entry(ThreadLocal k, Object v) {//使用ThreadLocal作为键值
                super(k);
                value = v;
            }
        }
	}
	每个线程Thread内部有一个ThreadLocal.ThreadLocalMap类型的成员变量threadLocals，用来存储变量副本的，键值为当前ThreadLocal变量，value为变量副本（即T类型的变量）。

**线程本地变量存储：**

`Thread.ThreadLocalMap<ThreadLocal, Object>;`

	1、Thread: 当前线程，可以通过Thread.currentThread()获取。
	
	2、ThreadLocal：我们的static ThreadLocal变量。
	
	3、Object: 当前线程共享变量。

调用ThreadLocal.get()，实际上是从当前线程中获取ThreadLocalMap<ThreadLocal, Object>，然后根据当前ThreadLocal获取当前线程本地变量Object。ThreadLocal.set，ThreadLocal.remove实际上是同样的道理。

 

**这种存储结构的好处：**

1、线程死去的时候，线程共享变量ThreadLocalMap则销毁。

2、ThreadLocalMap<ThreadLocal,Object>键值对数量为ThreadLocal的数量，一般来说ThreadLocal数量很少，相比在ThreadLocal中用Map<Thread, Object>键值对存储线程共享变量（Thread数量一般来说比ThreadLocal数量多），性能提高很多。


**关于ThreadLocalMap<ThreadLocal, Object>弱引用问题：**

当线程没有结束，但是ThreadLocal已经被回收，则可能导致线程中存在ThreadLocalMap<null, Object>的键值对，造成内存泄露。（ThreadLocal被回收，ThreadLocal关联的线程共享变量还存在）。

虽然ThreadLocal的get，set方法可以清除ThreadLocalMap中key为null的value，但是get，set方法在内存泄露后并不会必然调用，所以为了防止此类情况的出现，我们有两种手段。

1、使用完线程共享变量后，显式调用ThreadLocalMap.remove方法清除线程共享变量；

2、JDK建议ThreadLocal定义为private static，这样ThreadLocal的弱引用问题则不存在了。

