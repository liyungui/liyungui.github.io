---
title: OOM总结
date: 2018-11-26 11:36:53
tags: 
	- Android
---

# 常规OOM--Java堆内存不够导致的OOM

	java.lang.OutOfMemoryError: 
		Failed to allocate a XXX byte allocation with XXX free bytes and XXXKB until OOM
下面是几个关于Android官方声明内存限制阈值的API：

	ActivityManager.getMemoryClass()：     虚拟机java堆大小的上限，分配对象时突破这个大小就会OOM
	ActivityManager.getLargeMemoryClass()：manifest中设置largeheap=true时虚拟机java堆的上限
	Runtime.getRuntime().maxMemory() ：    当前虚拟机实例的内存使用上限，为上述两者之一
	Runtime.getRuntime().totalMemory() ：  当前已经申请的内存，包括已经使用的和还没有使用的
	Runtime.getRuntime().freeMemory() ：   上一条中已经申请但是尚未使用的那部分。那么已经申请并且正在使用的部分used=totalMemory() - freeMemory()
	ActivityManager.MemoryInfo.totalMem:   设备总内存
	ActivityManager.MemoryInfo.availMem:   设备当前可用内存
	/proc/meminfo                                           记录设备的内存信息

 **通常认为OOM发生是由于java堆内存不够用了**，即

	Runtime.getRuntime().maxMemory()这个指标满足不了申请堆内存大小时

这种OOM可以非常方便的验证（比如: 通过new byte[]的方式尝试申请超过阈值maxMemory()的堆内存）

## 图片消耗内存计算

	Bitmap.Config.ALPHA_8：只有透明度，8位。
	Bitmap.Config.ARGB_4444：16位。显示图片不清楚
	Bitmap.Config.ARGB_8888：32位。Bitmap默认，最占空间
	Bitmap.Config.RGB_565：16位。性能优化最常使用
	
	2000*2000*4 bytes =15M

## Bitmap是否需要调用 recycle()

Bitmap需调用 recycle() 是历史问题，在 Android 3.0之前，Bitmap 的图片数据是在底层C中处理的，因此在 Android3.0 之前 recycle() 是应该调用的

现在在 Bitmap 置 null 后图片数据会被GC回收。 

# [不可思议的OOM](https://www.jianshu.com/p/e574f0ffdb42)

**特征：崩溃时java堆内存和设备物理内存都充足**

**关键字：**

`Could not allocate JNI Env`, `pthread_create failed`

## OOM 一

	java.lang.OutOfMemoryError: 
		Could not allocate JNI Env
	
	在Android6.0，Android7.0上各个机型均有发生
	
	文件描述符(FD)数受限导致创建线程时JNIENV创建不成功
	
## OOM 二	

	java.lang.OutOfMemoryError: 
		pthread_create (1040KB stack) failed: Out of memory
	在Android7.0及以上的华为手机（EmotionUI_5.0及以上）
	
	线程数受限导致创建线程时clone failed
	
	Threads上限: 500
	
# 源码分析

基于Android6.0的代码进行简单分析

Android虚拟机最终抛出OutOfMemoryError的代码位于 `/art/runtime/thread.cc`

	void Thread::ThrowOutOfMemoryError(const char* msg)
	参数msg携带了OOM时的错误信息
        
搜索代码可以发现以下几个地方调用了上述方法抛出OutOfMemoryError错误

**第一个地方是堆操作时**

Java堆OOM

	系统源码文件：
	    /art/runtime/gc/heap.cc
	函数：
	    void Heap::ThrowOutOfMemoryError(Thread* self, size_t byte_count, AllocatorType allocator_type)
	抛出时的错误信息：
	    oss << "Failed to allocate a " << byte_count << " byte allocation with " << total_bytes_free  << " free bytes and " << PrettySize(GetFreeMemoryUntilOOME()) << " until OOM";

这种抛出的其实就是堆内存不够用的时候，即前面提到的申请堆内存大小超过了Runtime.getRuntime().maxMemory()

**第二个地方是创建线程时**

线程创建时OOM

	系统源码文件：
	    /art/runtime/thread.cc
	函数：
	    void Thread::CreateNativeThread(JNIEnv* env, jobject java_peer, size_t stack_size, bool is_daemon)
	抛出时的错误信息：
	    "Could not allocate JNI Env"
	  或者
	    StringPrintf("pthread_create (%s stack) failed: %s", PrettySize(stack_size).c_str(), strerror(pthread_create_result)));
	    
对比错误信息，可以知道我们遇到的OOM崩溃就是这个时机，即创建线程的时候（Thread::CreateNativeThread）产生的。

# 导致OOM发生的原因

综上，可以导致OOM的原因有以下几种：

- 文件描述符(fd)数目超限，即proc/pid/fd下文件数目突破/proc/pid/limits中的限制。可能的发生场景有：
短时间内大量请求导致socket的fd数激增，大量（重复）打开文件等
- 线程数超限，即proc/pid/status中记录的线程数（threads项）突破/proc/sys/kernel/threads-max中规定的最大线程数。可能的发生场景有：
app内多线程使用不合理，如多个不共享线程池的OKhttpclient；
**rxjava的Scheduler.io使用不合理极易导致OOM**(自增无上限的线程池，每个线程保活60s)
- 传统的java堆内存超限，即申请堆内存大小超过了 Runtime.getRuntime().maxMemory()
- （低概率）32位系统进程逻辑空间被占满导致OOM.
- 其他

# 监控措施

可以利用linux的inotify机制进行监控:

	watch /proc/pid/fd来监控app打开文件的情况,
	watch /proc/pid/task来监控线程使用情况．
	
# Demo

[POC(Proof of concept) 代码](https://github.com/piece-the-world/OOMDemo)






