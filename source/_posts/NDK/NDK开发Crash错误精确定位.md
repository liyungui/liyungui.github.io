---
title: NDK开发Crash错误精确定位
date: 2019-12-17 15:08:53
tags: 
	- NDK
categories:
	- Android
---

# 背景

在Android开发中，程序Crash分三种情况：未捕获的异常、ANR（Application Not Responding）和闪退（NDK引发错误）。

未捕获的异常会弹出一个退出应用的提示框，根据logcat打印的堆栈信息很容易定位错误。

ANR错误也好查，ANR错误会弹出一个系统提示框，让用户选择继续等待或立即关闭程序。并会在 `/data/anr` 目录下生成一个 `traces.txt` 文件，记录系统产生anr异常的堆栈和线程信息。

NDK错误应用直接崩溃（闪退），不会像在Java层产生的异常时弹出提示框。logcat打印出来的日志比较难定位错误的根源。

# 实例

## 源码

```cpp
#include <jni.h>
#include <string>

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_jni_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
//    std::string hello = "Hello from C++";
    char *p = "123";
    char *p2;
    strcpy(p2,p);//野指针
    return env->NewStringUTF(p2);
}
```

## 崩溃日志

```
2019-12-17 15:06:14.213 23322-23322/? A/libc: Fatal signal 11 (SIGSEGV), code 1, fault addr 0x0 in tid 23322 (com.example.jni)
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: Build fingerprint: 'HONOR/LLD-AL20/HWLLD-H2:8.0.0/HONORLLD-AL20/139(C00):user/release-keys'
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: Revision: '0'
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: ABI: 'arm64'
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: pid: 23322, tid: 23322, name: com.example.jni  >>> com.example.jni <<<
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG: Cause: null pointer dereference
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x0   0000000000000000  x1   000000706bdcd6e0  x2   0000000000000000  x3   3b031b0100333231
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x4   0000007fc6268058  x5   0000008080000000  x6   00ffffffffffffff  x7   0000000000000020
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x8   7f7f7f7f7f7f7f7f  x9   845c9f2e9b4ac914  x10  0000000000430000  x11  0101010101010101
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x12  0000000000000018  x13  42ad620927458c63  x14  000000708d4c8000  x15  ffffffffffffffff
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x16  000000706bdddfe8  x17  000000708bf03f24  x18  0000007fc6266a4c  x19  0000007088aa3a00
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x20  00000000700b3000  x21  0000007088aa3a00  x22  0000007fc6267ddc  x23  000000706c092a1f
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x24  0000000000000004  x25  0000007088aa3aa0  x26  000000706c092a1f  x27  0000000000000001
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     x28  0000007fc6268220  x29  0000007fc6267b30  x30  000000706bdcd678
2019-12-17 15:06:14.277 23465-23465/? A/DEBUG:     sp   0000007fc6267b10  pc   000000708bf03f7c  pstate 0000000000000000
2019-12-17 15:06:14.279 23465-23465/? A/DEBUG: backtrace:
2019-12-17 15:06:14.279 23465-23465/? A/DEBUG:     #00 pc 000000000001cf7c  /system/lib64/libc.so (strcpy+88)
2019-12-17 15:06:14.279 23465-23465/? A/DEBUG:     #01 pc 0000000000000674  /data/app/com.example.jni-QYw6ZMLyA62sF49s4crsYA==/lib/arm64/libnative-lib.so (Java_com_example_jni_MainActivity_stringFromJNI+40)
2019-12-17 15:06:14.279 23465-23465/? A/DEBUG:     #02 pc 000000000006a27c  /data/app/com.example.jni-QYw6ZMLyA62sF49s4crsYA==/oat/arm64/base.odex (offset 0x20000)
```

`signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0`
signal 11 (SIGSEGV)提示这是一个 `无效的内存引用` 错误，这个信号是由linux内核发出来的。SEGV是SegmentationViolation（段违例）的缩写。SEGV_MAPERR表示堆栈映射错误，原因后面说明了，使用了错误的地址0

下面重点看第backtrace的日志，backtrace日志可以看作是JNI调用的堆栈信息，以“#两位数字 pc”开头的都是backtrace日志。分析是我们自己编译的so文件 `Java_com_example_jni_MainActivity_stringFromJNI`
函数引发了异常，导致程序崩溃。但具体崩在函数的哪个位置，我们是不确定的。这时候就需要靠NDK为我们提供的工具来精确定位了

我们先记录下让程序崩溃的汇编指令地址 0000000000000674

# 调试工具

NDK提供了三个调试工具：`addr2line、objdump和ndk-stack`，能够精确定位到产生错误的根源

`ndk-stack`位置：`android-ndk-r16b`根目录下

``addr2line、objdump`位置：`android-ndk-r16b/toolchains/arm-linux-androideabi-4.9/prebuilt/darwin-x86_64/bin`目录下。NDK针对不同的CPU架构实现了多套相同的工具。所以在选择 `addr2line和objdump` 的时候，要根据目标机器的CPU架构来选择。

如果不知道目标机器的CPU架构，可以用 `cat /proc/cpuinfo` 查看手机的CPU信息中的 `cpu architecture`。推荐看崩溃logcat确定使用的是哪个架构的so库，更加精确。

**注意：调试必须使用带符号表和调试信息的so**

`/项目/module/build/intermediates/ndkBuild/release/obj/local/armeabi-v7a`

或 `/项目/module/build/intermediates/cmake/release/obj/arm64-v7a` 

## `ndk-stack`

特点：步聚简便，直接定位到代码出错的位置。

### 实时分析日志

将最近发生的错误的汇编地址解析成源码地址

`adb logcat | /Users/liyungui/Downloads/android-ndk-r16b/ndk-stack -sym /Users/liyungui/StudioProjects/jni/app/build/intermediates/cmake/debug/obj/arm64-v8a`

需要注意：-sym 指定是so库路径只是到so文件父目录

```
********** Crash dump: **********
Build fingerprint: 'HONOR/LLD-AL20/HWLLD-H2:8.0.0/HONORLLD-AL20/139(C00):user/release-keys'
pid: 23322, tid: 23322, name: com.example.jni  >>> com.example.jni <<<
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0
Stack frame #00 pc 000000000001cf7c  /system/lib64/libc.so (strcpy+88)
Stack frame #01 pc 0000000000000674  /data/app/com.example.jni-QYw6ZMLyA62sF49s4crsYA==/lib/arm64/libnative-lib.so (Java_com_example_jni_MainActivity_stringFromJNI+40): Routine Java_com_example_jni_MainActivity_stringFromJNI at /Users/liyungui/StudioProjects/jni/app/src/main/cpp/native-lib.cpp:11
Stack frame #02 pc 000000000006a27c  /data/app/com.example.jni-QYw6ZMLyA62sF49s4crsYA==/oat/arm64/base.odex (offset 0x20000)
Crash dump is completed
```
第11行，跟源码完全对应

### 指定崩溃日志


`/Users/liyungui/Downloads/android-ndk-r16b/ndk-stack -sym /Users/liyungui/StudioProjects/jni/app/build/intermediates/cmake/debug/obj/arm64-v8a -dump crash.log`

得到的结果跟上面实时分析一模一样

## addr2line

`./aarch64-linux-android-addr2line -e /Users/liyungui/StudioProjects/jni/app/build/intermediates/cmake/debug/obj/arm64-v8a/libnative-lib.so 0000000000000674`

```
-e：指定so文件路径

0000000000000674：出错的汇编指令地址；如果有多个地址需要解析，地址间以空格分隔
```

结果如下

`/Users/liyungui/StudioProjects/jni/app/src/main/cpp/native-lib.cpp:11`

第11行，跟源码完全对应

## objdump

上面两种方法都是将错误的汇编地址解析成了源码地址，但是不知道函数的上下文信息，不是那么完美

直接导出so的函数表信息和汇编码

`./aarch64-linux-android-objdump -S -D /Users/liyungui/StudioProjects/jni/app/build/intermediates/cmake/debug/obj/arm64-v8a/libnative-lib.so > ~/Desktop/dump.log`

打开 `dump.log`，搜索错误地址 674

```
extern "C" JNIEXPORT jstring JNICALL
Java_com_example_jni_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
 64c:	d100c3ff 	sub	sp, sp, #0x30
 650:	a9027bfd 	stp	x29, x30, [sp,#32]
 654:	910083fd 	add	x29, sp, #0x20
 658:	90000008 	adrp	x8, 0 <__cxa_finalize@plt-0x5d0>
 65c:	911b6108 	add	x8, x8, #0x6d8
 660:	f81f83a0 	stur	x0, [x29,#-8]
 664:	f9000be1 	str	x1, [sp,#16]
//    std::string hello = "Hello from C++";
    char *p = "123";
 668:	f90007e8 	str	x8, [sp,#8]
    char *p2;
    strcpy(p2,p);
 66c:	f94003e0 	ldr	x0, [sp]
 670:	f94007e1 	ldr	x1, [sp,#8]
 674:	97ffffdf 	bl	5f0 <strcpy@plt>
    return env->NewStringUTF(p2);
 678:	f85f83a8 	ldur	x8, [x29,#-8]
 67c:	f94003e1 	ldr	x1, [sp]
 680:	aa0803e0 	mov	x0, x8
 684:	97ffffd7 	bl	5e0 <_ZN7_JNIEnv12NewStringUTFEPKc@plt>
 688:	a9427bfd 	ldp	x29, x30, [sp,#32]
 68c:	9100c3ff 	add	sp, sp, #0x30
 690:	d65f03c0 	ret
```
这个跟ida逆向出来的一模一样

```
.text:000000000000064C ; =============== S U B R O U T I N E =======================================
.text:000000000000064C
.text:000000000000064C ; Attributes: bp-based frame
.text:000000000000064C
.text:000000000000064C ; jstring Java_com_example_jni_MainActivity_stringFromJNI(JNIEnv *env, jobject)
.text:000000000000064C                 EXPORT Java_com_example_jni_MainActivity_stringFromJNI
.text:000000000000064C Java_com_example_jni_MainActivity_stringFromJNI
.text:000000000000064C                                         ; DATA XREF: LOAD:0000000000000308↑o
.text:000000000000064C
.text:000000000000064C var_20          = -0x20
.text:000000000000064C var_18          = -0x18
.text:000000000000064C var_10          = -0x10
.text:000000000000064C env             = -8
.text:000000000000064C var_s0          =  0
.text:000000000000064C
.text:000000000000064C ; __unwind {
.text:000000000000064C                 SUB             SP, SP, #0x30
.text:0000000000000650                 STP             X29, X30, [SP,#0x20+var_s0]
.text:0000000000000654                 ADD             X29, SP, #0x20
.text:0000000000000658                 ADRP            X8, #unk_6D8@PAGE
.text:000000000000065C                 ADD             X8, X8, #unk_6D8@PAGEOFF
.text:0000000000000660                 STUR            X0, [X29,#env]
.text:0000000000000664                 STR             X1, [SP,#0x20+var_10]
.text:0000000000000668                 STR             X8, [SP,#0x20+var_18]
.text:000000000000066C                 LDR             X0, [SP,#0x20+var_20]
.text:0000000000000670                 LDR             X1, [SP,#0x20+var_18]
.text:0000000000000674                 BL              .strcpy
.text:0000000000000678                 LDUR            X8, [X29,#env]
.text:000000000000067C                 LDR             X1, [SP,#0x20+var_20] ; char *
.text:0000000000000680                 MOV             X0, X8  ; this
.text:0000000000000684                 BL              ._ZN7_JNIEnv12NewStringUTFEPKc ; _JNIEnv::NewStringUTF(char const*)
.text:0000000000000688                 LDP             X29, X30, [SP,#0x20+var_s0]
.text:000000000000068C                 ADD             SP, SP, #0x30
.text:0000000000000690                 RET
.text:0000000000000690 ; } // starts at 64C
.text:0000000000000690 ; End of function Java_com_example_jni_MainActivity_stringFromJNI
```
# 参考&扩展

- [Android NDK开发Crash错误定位](https://segmentfault.com/a/1190000013532735)