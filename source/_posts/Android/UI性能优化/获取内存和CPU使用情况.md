---
title: 获取内存和CPU使用情况
date: 2019-03-01 14:16:53
categories:
  - Android
tags:
  - 性能优化
---

# CPU使用

## 设备CPU使用情况

`/proc/stat` 

`CPU 152342 1421 28562 1600830 12389 553 273 0 0`

totalCpuTime: CPU后面7个属性(2-8)的和

通过 

## 指定pid应用CPU使用情况

`/proc/pid/stat`  `Process.myPid()获取pid`

`2341 (com.xxxx.xxxx) S 1131 1131 0 0 -1 3912246 12450 0 2 0 3321 612 0 0 20 0`
 
processCpuTime：3321 612两个属性(13-14)的和
 
## 解析代码

读取第一行，空格分割

```java
String procStatString = procStatFile.readLine();
String procStats[] = procStatString.split(" ");
totalCpuTime = Long.parseLong(procStats[2]) + Long.parseLong(procStats[3])
        + Long.parseLong(procStats[4]) + Long.parseLong(procStats[5])
        + Long.parseLong(procStats[6]) + Long.parseLong(procStats[7])
        + Long.parseLong(procStats[8]);

String appStatString = appStatFile.readLine();
String appStats[] = appStatString.split(" ");
processCpuTime = Long.parseLong(appStats[13]) + Long.parseLong(appStats[14]);
```
# 内存使用

## 设备内存使用情况

通过 `dumpsys meminfo` 获取的free mem大约为1.4G。使用android手机自带的内存管理器查看也是1.4G

```
Total RAM: 3,498,412K (status normal)
 Free RAM: 1,420,845K (  554,397K cached pss +   729,900K cached kernel +   136,548K free)
 Used RAM: 2,125,902K (1,741,086K used pss +   384,816K kernel)
 Lost RAM:   268,850K
   Tuning: 256 (large 512), oom   325,000K, restore limit   108,333K (high-end-gfx)
```

`/proc/meminfo` 

```
MemTotal:        3498412 kB
MemFree:          136596 kB
MemAvailable:    1500252 kB
Buffers:          150052 kB
Cached:          1313300 kB
SwapCached:        89844 kB
Active:          1218484 kB
Inactive:        1171716 kB
Active(anon):     472168 kB
....
```

free mem大约为0.13G

linux思想，内存不用白不用，因此它尽可能的cache和buffer一些数据，以方便下次使用。但实际上这些内存也是可以立刻拿来使用的。所以空闲内存=free+buffers+cached

dumpsys meminfo获得的free mem = cached pss + cached kernel + ion cached + gpu cached + + free

## 指定pid应用内存使用情况

```java
activityManager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
Debug.MemoryInfo[] memInfo = activityManager.getProcessMemoryInfo(new int[]{Process.myPid()});
int totalPss = memInfo[0].getTotalPss();//in KB
```

### 当前应用JavaHeap内存使用情况

```java
Runtime runtime = Runtime.getRuntime();
int M = 1024 * 1024;
Log.d("jvm", "最大可用内存: " + runtime.maxMemory() / M);
Log.d("jvm", "当前可用内存: " + runtime.totalMemory() / M);
Log.d("jvm", "当前空闲内存:" + runtime.freeMemory() / M);
```  

#### maxMemory

Dalvik虚拟机，每个App默认的最大可用内存由系统指定（在`/system/build.prop`文件中定义）

在Manifest application 里面添加`android:allowBackup="true"` 可以增加最大可用内存至512M

为什么有些APP（比如大型游戏）可以超过这个值？那是因为Java内存又分为Java Heap和Native Heap，Native Heap是不受该值约束的。

#### totalMemory

一般为16M

如果设置为“-Xms1024m -Xmx1024m”，那么totalMemory=maxMamory

{% asset_img 内存.png %}
    
