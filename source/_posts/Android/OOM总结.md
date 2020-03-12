---
title: OOM总结
date: 2018-11-26 11:36:53
tags: 
	- Android
---

# 背景

App对于应用稳定性的要求非常高，体现App稳定性的一个重要数据就是Crash率，而在众多Crash中最棘手最难定位的就是OOM问题。构建快速定位线上OOM问题的组件非常有必要

# OOM原因

要定位OOM问题，首先需要弄明白Android中有哪些原因会导致OOM

## 分配堆内存失败

Android 虚拟机最终抛出OutOfMemoryError的代码位于 `/art/runtime/thread.cc`

```
void Thread::ThrowOutOfMemoryError(const char* msg)
参数 msg 携带了 OOM 时的错误信息
```

### Java堆内存不足

#### 错误日志

```
Failed to allocate a 536870924 byte allocation with 16777216 free bytes and 221MB until OOM
```

#### 源码

`/art/runtime/gc/heap.cc`

```
void Heap::ThrowOutOfMemoryError(Thread* self, size_t byte_count, AllocatorType allocator_type)
抛出时的错误信息：
    oss << "Failed to allocate a " << byte_count << " byte allocation 
    with " << total_bytes_free  << " free bytes and "
     << PrettySize(GetFreeMemoryUntilOOME()) << " until OOM";
```

### 连续的Java堆内存不足

进程中存在大量的内存碎片导致的

#### 错误日志

```
Failed to allocate a 458 byte allocation with 1613776 free bytes and 1575KB until OOM; 
failed due to fragmentation (required continguous free 32768 bytes for a new buffer where largest contiguous free 4096 bytes)
```

比Java堆内存不足的OOM堆栈多出一段信息

#### 源码

`art/runtime/gc/allocator/rosalloc.cc` [链接](https://android.googlesource.com/platform/art/+/a9033d7%5E%21/)

```
required_bytes = numOfPages[SizeToIndex(failed_alloc_bytes)] * kPageSize;
new_buffer_msg = " for a new buffer";
if (required_bytes > largest_continuous_free_pages) {
	os << "; failed due to fragmentation ("
	<< "required contiguous free " << required_bytes << " bytes" << new_buffer_msg
	<< ", largest contiguous free " << largest_continuous_free_pages << " bytes"
	<< ", total free pages " << total_free << " bytes"
	<< ", space footprint " << footprint_ << " bytes"
	<< ", space max capacity " << max_capacity_ << " bytes"
	<< ")" << std::endl;
```

## 创建线程失败

创建线程的源码 `/art/runtime/thread.cc`

```
void Thread::CreateNativeThread(JNIEnv* env, jobject java_peer, size_t stack_size, bool is_daemon)
抛出时的错误信息：
    "Could not allocate JNI Env"
  或者
    StringPrintf("pthread_create (%s stack) failed:
     %s", PrettySize(stack_size).c_str(), 
     strerror(pthread_create_result)));
```
   
Android中创建线程的步骤，其中两个关键节点是创建JNIEnv结构体和创建线程，而这两步均有可能抛出OOM。 

{% asset_img 创建线程.png %} 
   
### 创建JNI失败

#### FD到达上限

```
E/art: ashmem_create_region failed for 'indirect ref table': Too many open files
 java.lang.OutOfMemoryError: Could not allocate JNI Env
   at java.lang.Thread.nativeCreate(Native Method)
   at java.lang.Thread.start(Thread.java:730) 
```

#### 进程虚拟内存耗尽

```
E/art: Failed anonymous mmap(0x0, 8192, 0x3, 0x2, 116, 0): Operation not permitted. See process maps in the log.
java.lang.OutOfMemoryError: Could not allocate JNI Env
  at java.lang.Thread.nativeCreate(Native Method)
  at java.lang.Thread.start(Thread.java:1063)
```

### 创建线程失败

#### 进程虚拟内存耗尽

```
W/libc: pthread_create failed: couldn't allocate 1073152-bytes mapped space: Out of memory
W/tch.crowdsourc: Throwing OutOfMemoryError with VmSize  4191668 kB "pthread_create (1040KB stack) failed: Try again"
java.lang.OutOfMemoryError: pthread_create (1040KB stack) failed: Try again
        at java.lang.Thread.nativeCreate(Native Method)
        at java.lang.Thread.start(Thread.java:753)
```

#### 线程数超限

```
W/libc: pthread_create failed: clone failed: Out of memory
W/art: Throwing OutOfMemoryError "pthread_create (1040KB stack) failed: Out of memory"
java.lang.OutOfMemoryError: pthread_create (1040KB stack) failed: Out of memory
  at java.lang.Thread.nativeCreate(Native Method)
  at java.lang.Thread.start(Thread.java:1078)
```

## 总结

{% asset_img OOM原因.png %} 

# OOM问题定位

## 堆内存不足

Debug.dumpHprofData得到当前进程的Java内存快照文件，分析内存对象

## FD数超出限制

在 `/proc/pid/limits` 描述着Linux系统对对应进程的限制，其中Max open files就代表可创建FD的最大数目。

进程中创建的FD记录在 `/proc/pid/fd` 中

当检测到FD数量达到阈值时（FD最大限制的95%），读取当前进程的所有FD信息归并后上报。

## 线程数超出限制

`/proc/sys/kernel/threads-max` 规定了每个进程创建线程数目的上限。大部分手机上限1万多，华为机型修改为500

## 虚拟内存耗尽

`/proc/pid/status` 文件的 `VmPeak/VmSize` 记录了进程所使用的虚拟内存
   
# 参考&扩展

- [Probe：Android线上OOM问题定位组件](https://mp.weixin.qq.com/s/tO1yxFs2qNQlQ2bJ8vGzQA) 美团技术团队
- [Android进阶性能调优；不可思议的OOM](https://www.jianshu.com/p/31f207782915)
- [Probe：Android线上OOM问题定位组件](https://mp.weixin.qq.com/s/tO1yxFs2qNQlQ2bJ8vGzQA) 美团，体系化，全面详细






