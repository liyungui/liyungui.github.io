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

## 文件描述符(fd)数目超限

即**proc/pid/fd**下文件数目突破**/proc/pid/limits**中的限制。

可能的发生场景有：

短时间内大量请求导致socket的fd数激增，大量（重复）打开文件等

### /proc/pid/limits

linux 系统对**对应进程的限制**

用排除法筛选上面文件中的 limits：

- Max stack size，Max processes 的限制是整个系统的，不是针对某个进程的，排除；
- Max locked memory ，排除，后面会分析，线程创建过程中分配线程私有 stack 使用的 mmap 调用没有设置 MAP_LOCKED，所以这个限制与线程创建过程无关 ；
- Max pending signals，c 层信号个数阈值，无关，排除 ；
- Max msgqueue size，Android IPC 机制不支持消息队列，排除。
- **Max open files** 这一项限制最可疑。表示 每个进程最大打开文件的数目，进程 每打开一个文件就会产生一个文件描述符 fd（记录在 /proc/pid/fd 下面），这个限制表明 fd 的数目不能超过 Max open files 规定的数目。线程创建过程中涉及到文件描述符

### 验证

触发大量网络连接（每个连接处于独立的线程中）并保持，每打开一个 socket 都会增加一个 fd（/proc/pid/fd 下多一项）

注：不只有这一种增加 fd 数的方式，也可以用其他方法，比如打开文件，创建 handlerthread 等等

实验结果：当 fd 数目到达 /proc/pid/limits 中规定的 Max open files 时，继续开线程确实会导致 OOM 的产生

此外从 虚拟机的 Log 中看出，还有一个关键的信息 `art: ashmem_create_region failed for 'indirect ref table': Too many open files`

## 线程数超限

即**proc/pid/status**中记录的线程数（threads项）突破**/proc/sys/kernel/threads-max**中规定的**每个进程创建线程数目的上限**

可能的发生场景有：

app内多线程使用不合理，如多个不共享线程池的OKhttpclient；
**rxjava的Scheduler.io使用不合理极易导致OOM**(自增无上限的线程池，每个线程保活60s)

### 验证

创建大量的空线程（不做任何事情，直接 sleep）

实验结果：在 Android7.0 及以上的华为手机（EmotionUI_5.0 及以上）的手机产生 OOM，这些手机的线程数限制都很小 (应该是华为 rom 特意修改的 limits)，每个进程只允许最大同时开 500 个线程，因此很容易复现了。

## 传统的java堆内存超限

即申请堆内存大小超过了 Runtime.getRuntime().maxMemory()

## 32位系统进程逻辑空间被占满导致OOM

低概率

每个线程通常需要 mapp 1MB 左右的 stack 空间（stack 大小可以自行设置），32 为系统进程逻辑地址 4GB，用户空间少于 3GB。逻辑地址空间不够（已用逻辑空间地址可以查看 /proc/pid/status 中的 VmPeak/VmSize 记录）

## 其他

# 监控措施

可以利用linux的inotify机制进行监控:

	watch /proc/pid/fd来监控app打开文件的情况,
	watch /proc/pid/task来监控线程使用情况．

捕获到OutOfMemoryError 时记录 /proc/pid 目录下的如下信息：

1. /proc/pid/fd 目录下文件数 (fd 数)

2. /proc/pid/status 中 threads 项（当前线程数目）

# Demo

[POC(Proof of concept) 代码](https://github.com/piece-the-world/OOMDemo)

# 参考&扩展

[Android进阶性能调优；不可思议的OOM](https://www.jianshu.com/p/31f207782915)





