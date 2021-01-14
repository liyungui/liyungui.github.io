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
   
# 创建线程导致OOM排查

## 工具介绍

需要查看当前的线程的状态

排查方法:

- Android Profiler 
	- 可以看到当前创建的所有线程基本信息，线程状态等；可以看到对应的线程数和线程名称，以及线程的状态
	- 比较卡顿
	- 不能分类统计
- ps 命令
	- 查看当前进程状态 process status
	- 方便统计

## ps命令排查线程OOM

`adb shell ps | grep xxx` 根据包名获取进程pid
	
`adb shell ps -T | grep 12583`	查看进程所有线程

可以使用 `wc -l` 来统计线程数量

`adb shell ps -T | grep 12583 | wc -l` 统计进程的线程数量

在操作APP时可以实时看到线程数量，并且观察哪类线程名字在增多

我们按照复现路径使用APP后，发现线程数达到500，接近崩溃平台所暴露的问题了。仔细观察了所有线程名的输出发现以 `pool-` 前缀的线程非常之多。

```
u0_a620      12583 14269   485 2764024 333604 0                   0 S pool-308-thread
u0_a620      12583 14270   485 2764024 333604 0                   0 S pool-309-thread
u0_a620      12583 14279   485 2764024 333604 0                   0 S pool-310-thread
u0_a620      12583 14280   485 2764024 333604 0                   0 S pool-311-thread
u0_a620      12583 14295   485 2764024 333604 0                   0 S pool-327-thread
u0_a620      12583 14298   485 2764024 333604 0                   0 S pool-328-thread
u0_a620      12583 14299   485 2764024 333604 0                   0 S pool-329-thread
u0_a620      12583 14301   485 2764024 333604 0                   0 S pool-330-thread
u0_a620      12583 14315   485 2764024 333604 0                   0 S pool-331-thread
u0_a620      12583 14316   485 2764024 333604 0                   0 S pool-332-thread
u0_a620      12583 14317   485 2764024 333604 0                   0 S pool-333-thread
u0_a620      12583 14366   485 2764024 333604 0                   0 S pool-339-thread
u0_a620      12583 14367   485 2764024 333604 0                   0 S pool-340-thread
u0_a620      12583 14368   485 2764024 333604 0                   0 S pool-341-thread
u0_a620      12583 14369   485 2764024 333604 0                   0 S pool-342-thread
u0_a620      12583 14385   485 2764024 333604 0                   0 S pool-347-thread
u0_a620      12583 14390   485 2764024 333604 0                   0 S pool-351-thread
```

`adb shell ps -T | grep 12583 | grep pool | wc -l` 统计数量达到348

我们知道线程池里`DefaultThreadFactory()`默认创建的线程名称就是以pool-来命名的

那我们就清楚了这个问题的所在，有一个地方在不断地创建线程池导致OOM

review代码发现, AspectStorageManager.getInstance()对线程池使用有问题，每次都会创建一个新的线程池。复用线程池即可解决

```java
public class AspectStorageManager {
    private ExecutorService mSingleThreadExecutor;

    protected AspectStorageManager() {}

    protected static final class Holder {
        private static final AspectStorageManager instance = new AspectStorageManager();
    }

    public static AspectStorageManager getInstance() {
        // 设置线程池只有一个线程，并且任务数最大不超过150
        Holder.instance.mSingleThreadExecutor = new ThreadPoolExecutor(1, 1,
                0L, TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<Runnable>(150));

        Holder.instance.mUdid = DeviceHelper.getUniqueId(LiveApplicationLike.appContext);
        Holder.instance.mBlackList = new HashMap<>();
        return Holder.instance;
    }
}
```

修复后，再次检测，发现线程数量稳定在250到280之间

## 微信的解决方案

限制线程数量，可以一定程度避免 OOM 的发生。所以我们也开始对微信的线程数进行了监控统计。

我们在灰度版本中通过一个定时器 10 分钟 dump 出应用所有的线程，当线程数超过一定阈值时，将当前的线程上报并预警，

我们发现微信在某些特殊场景下，确实存在线程泄漏以及短时间内线程暴增，导致线程数过大（500+）的情况，这种情况下再创建线程往往容易出现 OOM。

在定位并解决这几个问题后，我们的 crash 系统和厂商反馈中这种类型 OOM 确实降低了不少。所以**监控线程数，收敛线程**也成为我们降低 OOM 的有效手段之一。

## 监控线程数量

项目变大后收敛线程

避免恶化的监控预防手段

### Thread.getAllStackTraces

不完整，500线程时，统计回来才220+

### ThreadGroup.activeCount

不完整，500线程时，统计回来才410+

`enumerate()`可以遍历线程组所有活跃线程

```java
ThreadGroup group = Thread.currentThread().getThreadGroup();
ThreadGroup topGroup = group;
// 遍历线程组树，获取根线程组
while (group != null) {
    topGroup = group;
    group = group.getParent();
}
// 激活的线程数再加一倍，防止枚举时有可能刚好有动态线程生成
int slackSize = topGroup.activeCount() * 2;
Thread[] slackThreads = new Thread[slackSize];
// 获取根线程组下的所有线程，返回的actualSize便是最终的线程数
int actualSize = topGroup.enumerate(slackThreads);
Thread[] atualThreads = new Thread[actualSize];
// 复制slackThreads中有效的值到atualThreads
System.arraycopy(slackThreads, 0, atualThreads, 0, actualSize);

//打印线程数量和线程名
System.out.println("Threads size is " + atualThreads.length);
for (Thread thread : atualThreads) {
    System.out.println("Thread name : " + thread.getName());
}
```
 
### Runtime执行ps命令

命令输出内容为空

```java
/**
 * 执行shell 命令， 命令中不必再带 adb shell
 *
 * @param cmd
 * @return Sting  命令执行在控制台输出的结果
 */
public static String execByRuntime(String cmd) {
    Process process = null;
    BufferedReader bufferedReader = null;
    InputStreamReader inputStreamReader = null;
    try {
        process = Runtime.getRuntime().exec(cmd);
        inputStreamReader = new InputStreamReader(process.getInputStream());
        bufferedReader = new BufferedReader(inputStreamReader);

        int read;
        char[] buffer = new char[4096];
        StringBuilder output = new StringBuilder();
        while ((read = bufferedReader.read(buffer)) > 0) {
            output.append(buffer, 0, read);
        }
        return output.toString();
    } catch (Exception e) {
        e.printStackTrace();
        return null;
    } finally {
        if (null != inputStreamReader) {
            try {
                inputStreamReader.close();
            } catch (Throwable t) {

            }
        }
        if (null != bufferedReader) {
            try {
                bufferedReader.close();
            } catch (Throwable t) {

            }
        }
        if (null != process) {
            try {
                process.destroy();
            } catch (Throwable t) {

            }
        }
    }
}
```    

## 监控线程的创建

项目源码、三方库、aar中都有线程的创建

那怎么去定位到具体的有问题的代码片段呢？

可以监控线程创建(hook Thread构造方法)，在里面打印堆栈信息帮助我们**快速锁定线程创建者** 

推荐使用 [epic](https://github.com/tiann/epic) 库

## Android线程优化实战

线程使用准则：

- 提供基础线程池供各个业务线使用
	- 严禁直接 new Thread
	- 避免各个业务线各自维护一套线程池，导致线程数过多
- 创建线程必须命名
	- 方便定位线程归属。
	- 运行期 Thread.currentThread().setName修改名字
- 重视优先级设置
	- Process.setThreadPriority();
	- 可以设置多次
- 根据任务类型选择合适的异步方式
	- 优先级低，长时间执行，HandlerThread
- 监控关键异步任务
	- 异步不等于不耗时。
	- 可通过AOP的方式来做监控

## Android异步方式汇总

### new Thread

最简单、常见的异步方式

不易复用，频繁创建及销毁开销大

复杂场景不易使用

### HandlerThread

自带消息循环的线程

串行执行（优先级低）

长时执行，需要不断从队列中获取任务

### IntentService

继承自Service在内部创建 HandlerThread

异步，不占用主线程

优先级较高，不易被系统Kill

### AsyncTask

Android提供的工具类

无需自己处理线程切换

需要注意版本不一致问题

### 线程池

易复用，减少频繁创建、销毁的时间

功能强大： 定时、任务队列、并发数控制等

### RxJava

由强大的Scheduler集合提供

不同类型的区分：IO、Computation

各种异步方式的线程优先级？写Demo

# 参考&扩展

- [Probe：Android线上OOM问题定位组件](https://mp.weixin.qq.com/s/tO1yxFs2qNQlQ2bJ8vGzQA) 美团技术团队
- [Android进阶性能调优；不可思议的OOM](https://www.jianshu.com/p/31f207782915)
- [Probe：Android线上OOM问题定位组件](https://mp.weixin.qq.com/s/tO1yxFs2qNQlQ2bJ8vGzQA) 美团，体系化，全面详细
- [一次线程OOM排查看线程使用注意事项](https://juejin.im/post/6850037281621803015)
- [微信 Android 终端内存优化实践](https://toutiao.io/posts/5fz748/preview)
- [五. Android 线程优化](https://www.jianshu.com/p/ddcdfae9e30d)






