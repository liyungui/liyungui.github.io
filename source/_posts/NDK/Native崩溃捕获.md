---
title: Native崩溃捕获
date: 2019-09-05 11:39:14
categories:
  - Android
tags:
  - NDK
---

# 现有的方案

{% asset_img 现有方案.png %}

其实3个方案在Android平台的实现原理都是基本一致的，综合考虑，可以基于coffeecatch改进。

# 信号机制

在Unix-like系统中，异常发生时，CPU通过异常中断的方式，触发异常处理流程。不同的处理器，有不同的异常中断类型和中断处理方式。

linux把这些中断处理，统一为信号量，可以注册信号量向量进行处理。

信号机制是进程之间相互传递消息的一种方法，信号全称为软中断信号。

信号机制是进程之间相互传递消息的一种方法，信号全称为软中断信号。

{% asset_img 用户态内核态切换.png %}

## 接收信号

接收信号的任务是由内核代理的，当内核接收到信号后，会将其放到对应进程的信号队列中，同时向进程发送一个中断，使其陷入内核态。

注意，此时信号还只是在队列中，对进程来说暂时是不知道有信号到来的。

## 检测信号

进程陷入内核态后，有两种场景会对信号进行检测：

- 进程从内核态返回到用户态前进行信号检测

- 进程在内核态中，从睡眠状态被唤醒的时候进行信号检测

当发现有新信号时，便会进入下一步，处理信号。

## 处理信号

信号处理函数是运行在用户态的

调用处理函数前，内核会将当前内核栈的内容备份拷贝到用户栈上，并且修改指令寄存器（eip）将其指向信号处理函数。

接下来进程返回到用户态中，执行相应的信号处理函数。

信号处理函数执行完成后，还需要返回内核态，检查是否还有其它信号未处理。

如果所有信号都处理完成，就会将内核栈恢复（从用户栈的备份拷贝回来），同时恢复指令寄存器（eip）将其指向中断前的运行位置，最后回到用户态继续执行进程。

# 信号量定义

`kill -l` 可以查看所有的信号量

`signal.h`

```
 SIGHUP 1   挂起
 SIGINT 2   中断，比如命令行用户输入Ctrl+C时由终端驱动程序发送INT信号
 SIGQUIT 3  退出，默认处理是内存转储
 SIGILL 4   非法指令，损坏的可执行文件或代码区损坏
 SIGTRAP 5
 SIGABRT 6
 SIGIOT 6
 SIGBUS 7  总线错误，硬件或系统错误，如不存在的物理地址
 SIGFPE 8  浮点运算错误，如除0，余0，整形溢出
 SIGKILL 9 杀死进程
 SIGUSR1 10
 SIGSEGV 11 段错误，空指针，野指针，数组越界，栈溢出，访问不存在的地址，访问内核区，写只读空间
 SIGUSR2 12
 SIGPIPE 13 管道错误，如
 SIGALRM 14
 SIGTERM 15 终止，默认处理没有内存转储
 SIGSTKFLT 16
 SIGCHLD 17
 SIGCONT 18 继续执行，取消挂起
 SIGSTOP 19 挂起/暂停，直到收到CONT
 SIGTSTP 20 STOP信号的“软”版本，用户输入Ctrl+Z时由终端驱动程序发送的信号
 SIGTTIN 21
```

程序崩溃99%都是BUS与SEGV这两个错误导
致的。内核对二者的默认处理是内存转储(memory dump)。进程可以捕获和封锁这两类错误。

## 常见信号量

{% asset_img 常见信号量.png %}

# 捕捉

## signal

```
legacy_signal_inlines.h
sighandler_t signal(int s, sighandler_t f)

系统也定义了一些宏 
SIG_IGN 忽略信号
SIG_DFL 使用默认的信号处理函数

1. 进入信号处理函数之后 这个信号会被 阻塞（block）
   直到信号处理函数 返回。
2. 信号函数处理完之后，会将该信号处理函数恢复为默认处理函数，所以在下一次用到的时候要重新调用signal这个函数绑定
```

```cpp
#include <jni.h>
#include <string>
#include <signal.h>
#include <android/log.h>
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, "lyg", __VA_ARGS__)

void recvSignal(int sig)
{
    LOGD("received signal %d !!!\n",sig);
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_jni_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
    signal(SIGTRAP,recvSignal);
    char *p = "123";
    char *p2;
    strcpy(p2,p);
    return env->NewStringUTF(p2);
}
```

日志

```
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
2019-12-26 16:56:18.392 29534-29534/? D/lyg: received signal 5 !!!
```

错误发生后 ，系统 发送 SIGSEGV ，然后 中断了程序 跳到 recvSignal 处理函数中去 ，处理完成后 ，再跳回来错误发生的地方 ，然后继续产生错误 ，继续发送 SIGSEGV  信号

## sigaction

```
struct sigaction {
    void     (*sa_handler)(int);
    void     (*sa_sigaction)(int, siginfo_t *, void *);
    sigset_t   sa_mask;
    int        sa_flags;
    void     (*sa_restorer)(void);
}

sa_handler 信号处理函数，该函数只有一个参数
sa_sigaction 信号处理函数，sa_flags中存在SA_SIGINFO标志时使用这个函数处理信号量
sa_mask： 信号处理函数执行的过程中应被阻塞的信号
sa_flags：信号处理过程行为的标志，由0个或多个标志通过or运算组合而成，比如SA_RESETHAND，SA_ONSTACK | SA_SIGINFO
sa_restorer： 已废弃
```

```
int sigaction(int signum,const struct sigaction *act,struct sigaction *oldact));

signum：代表信号编码
	除SIGKILL及SIGSTOP外的任何一个特定有效的信号
	如果为这两个信号定义自己的处理函数，将导致信号安装错误。

act：指向结构体sigaction的一个实例的指针
	该实例指定了对特定信号的处理
	如果设置为空，进程会执行默认处理。

oldact：和参数act类似，只不过保存的是原来对相应信号的处理
	也可设置为NULL。
```

```
#include <jni.h>
#include <string>
#include <signal.h>
#include <android/log.h>

#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG, "lyg", __VA_ARGS__)

static void SignalHandler(int signo, siginfo_t *info, void *context) {
    LOGD("received signal %d !!!\n", signo);
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_jni_MainActivity_stringFromJNI(
        JNIEnv *env,
        jobject /* this */) {
    struct sigaction sa_old;
    struct sigaction sa;
    memset(&sa, 0, sizeof(sa));
    sigemptyset(&sa.sa_mask);
    sa.sa_sigaction = SignalHandler;
    sa.sa_flags = SA_SIGINFO;
    sigaction(SIGTRAP, &sa, &sa_old);

    char *p = "123";
    char *p2;
    strcpy(p2, p);
    return env->NewStringUTF(p2);
}
```

问题：跟signal一样，会重复打印捕获到的信号量，然后ANR；

自定义信号处理函数，处理完之后，调用原来注册的处理函数，处理完退出应用

# 参考&扩展

- [Android 平台 Native 代码的崩溃捕获机制及实现](https://mp.weixin.qq.com/s/g-WzYF3wWAljok1XjPoo7w?) 腾讯Bugly分享
- [linux的常用信号量和进程的四种状态](https://blog.csdn.net/ysdaniel/article/details/6819142)
- [linux SIGSEGV 信号捕捉，保证发生段错误后程序不崩溃](https://blog.csdn.net/work_msh/article/details/8470277)
- [Android native 崩溃信息捕获实践](https://jekton.github.io/2019/04/06/native-crash-catching/)