---
title: Crash防护
date: 2019-06-22 11:26:53
categories: 
	- Android
tags: 
	- Android
---

# 捕获所有异常

虽然强行捕获所有运行时异常，会导致各种UI上的奇葩问题发生，但可以最大程度的保证APP正常运行，很多时候我们希望即使主线程抛出异常也不影响app的正常使用

**核心：保证主线程Looper继续Loop**

## try-catch机制的性能损耗

研究方式：

### 函数耗时

写两个一样逻辑的函数，一个包含try-catch代码块，一个不包含，分别循环调用百万次，通过System.nanoTime()来比较两个函数百万次调用的耗时；

测试发现基本无区别

### 反编译字节码

反编译出指令发现加了try-catch块的代码跟没有加的代码运行时的指令是完全一致的

如果程序运行过程中不产生异常的话，try catch 几乎是不会对运行产生任何影响的。只是在产生异常的时候jvm会追溯异常栈。这部分耗时就相对较高了。

## 异常类型

Android的View绘制，事件分发，Activity启动，Activity的生命周期回调等等都是一个个的Message，系统会把这些Message插入到主线程中唯一的queue中，所有的消息都排队等待Looper将其取出，并在主线程执行

- 一般线程异常。
- UI主线程异常。
	- View导致Choreographer异常。
		- 可能黑白屏。关闭当前异常的界面
	- Activity异常。
		- 生命周期异常。可能黑白屏。关闭当前异常的界面
	- 四大组件生命周期异常。

## 一般线程-默认的线程未捕获异常Handler

**Thread.UncaughtExceptionHandler** 接口，处理 未捕获的异常

```java
public static interface UncaughtExceptionHandler {
    void uncaughtException(Thread thread, Throwable ex);
}
```

Android中，应用进程fork出来后会为虚拟机中的每个线程设置一个默认的 UncaughtExceptionHandler -- **UncaughtHandler**

**Thread.setDefaultUncaughtExceptionHandler(new UncaughtHandler());**

**UncaughtHandler**

```java
//RuntimeInit.java中的zygoteInit函数
public static final void zygoteInit(int targetSdkVersion, String[] argv, ClassLoader classLoader)
        throws ZygoteInit.MethodAndArgsCaller {
    ............
    commonInit();
    ............
}
private static final void commonInit() {
    ...........
    /* set default handler; this applies to all threads in the VM */
    Thread.setDefaultUncaughtExceptionHandler(new UncaughtHandler());
    ...........
}
```

### 思路：自定义UncaughtExceptionHandler

我们可以给应用设置我们自定义的UncaughtExceptionHandler

如果自定义UncaughtExceptionHandler捕获异常后不做任何处理：

- 子线程发生未捕获异常，不会Crash。子线程被终止，主线程还在运行
- **主线程**发生未捕获异常，会**ANR**。主线程被终止

## UI主线程-消息循环机制

**Android 消息循环机制：Handler和Looper**

Android应用启动流程可知，进程创建完成之后，Android应用程序框架层就会在这个进程中 执行 主线程的入口方法 **ActivityThread.main()**

```java
//ActivityThread .java
//主线程的入口方法
public static void main(String[] args) {
     ......

     //创建主线程的Looper和MessageQueue
     Looper.prepareMainLooper();

    //创建一个ActivityThread实例，然后调用它的attach函数，
    //ActivityManagerService通过Binder进程间通信机制通知ActivityThread，启动应用首页
     ActivityThread thread = new ActivityThread();
     thread.attach(false);

     if (sMainThreadHandler == null) {
         sMainThreadHandler = thread.getHandler();
     }
    .......
   //开启主线程的消息循环。
     Looper.loop();

     throw new RuntimeException("Main thread loop unexpectedly exited");
}
```

### 思路：捕获每个消息循环的异常

- 通过Handler往主线程的queue中添加一个Runnable 
- 该Runnable是while死循环
- while死循环中调用Looper.loop()
	- 使主线程又开始不断的读取queue中的Message并执行，也就是**主线程并不会被阻塞**。
	- 又可以保证**以后**主线程的**所有异常**都会从我们手动调用的Looper.loop()处抛出

Android应用的主线程是阻塞在ActivityThread.main()中的Looper.loop()的for(;;)循环里，后来for循环取到我们的runnable之后，程序的流程就阻塞在了我们的runnable里面了。

必须通过Handler往主线程的queue中添加一个Runnable，而不能在主线程中直接开启while循环，原因还是会阻塞主线程

```java
new Handler(Looper.getMainLooper()).post(
	new Runnable() {
        @Override
        public void run() {
           //主线程异常拦截
            while (true) {
                try {
                    Looper.loop();//主线程的异常会从这里抛出
                } catch (Throwable e) {
                                            
                }
            }
        }
    });
   
sUncaughtExceptionHandler = Thread.getDefaultUncaughtExceptionHandler();
 //所有线程异常拦截，由于主线程的异常都被我们catch住了，所以下面的代码拦截到的都是子线程的异常
Thread.setDefaultUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
    @Override
    public void uncaughtException(Thread t, Throwable e) {
        
    }
});
```

## View导致Choreographer异常-关闭页面

可能会黑白屏

```java
//DefenseCore.java
//遍历错误堆栈，如果是Choreographer.doFrame()，可能会黑白屏
StackTraceElement[] elements = error.getStackTrace();
if (elements == null) {
    return;
}

for (int i = elements.length - 1; i > -1; i--) {
    if (elements.length - i > 20) {
        return;
    }
    StackTraceElement element = elements[i];
    if ("android.view.Choreographer".equals(element.getClassName())
            && "Choreographer.java".equals(element.getFileName())
            && "doFrame".equals(element.getMethodName())) {
        dispatcher.mayBeBlackScreen(e);
        return;
    }
}
```

## Activity异常

### 反射替换ActivityThread的Instrumentation

Android framework 通过**Instrumentation**来调用Activity的所有生命周期方法，通过反射替换ActivityThread的成员变量**mInstrumentation**来尝试修复Activity生命周期回调中的崩溃。

```java
//HookInstrumentation.java
// 先获取到当前的ActivityThread对象
Class<?> activityThreadClass = Class.forName("android.app.ActivityThread");
Method currentActivityThreadMethod = activityThreadClass.getDeclaredMethod("currentActivityThread");
currentActivityThreadMethod.setAccessible(true);
Object currentActivityThread = currentActivityThreadMethod.invoke(null);

// 拿到原始的 mInstrumentation字段
Field mInstrumentationField = activityThreadClass.getDeclaredField("mInstrumentation");
mInstrumentationField.setAccessible(true);
mOriginInstrumentation = (Instrumentation) mInstrumentationField.get(currentActivityThread);
mCustomInstrumentation = new DefenseInstrumentation(mOriginInstrumentation);
mCustomInstrumentation.setExceptionDispatcher(mExceptionDispatcher);

// 创建代理Instrumentation对象
Instrumentation evilInstrumentation = mCustomInstrumentation;

// 偷梁换柱
mInstrumentationField.set(currentActivityThread, evilInstrumentation);
```

### 反射为ActivityThread的Handler增加callback

反射ActivityThread的**mH**，给该**Handler**添加回调方法，因为在ActivityThread中该handler未实现callback

```java
//HookH.java
// 先获取到当前的ActivityThread对象
Class activityThreadClass = Class.forName("android.app.ActivityThread");
Object activityThread = activityThreadClass.getDeclaredMethod("currentActivityThread").invoke(null);

// 拿到原始的 mH字段
Field mhField = activityThreadClass.getDeclaredField("mH");
mhField.setAccessible(true);
mHHandler = (Handler) mhField.get(activityThread);
Field callbackField = Handler.class.getDeclaredField("mCallback");
callbackField.setAccessible(true);
//设置mCallback
callbackField.set(mHHandler, mCallback);
```

## Service和BroadcastReceiver异常

Android framework 在调用四大组件生命周期的时候，如果出现了异常，会回调**Instrumentation.onException()**方法

通过Instrumentation的方法onException返回true来尝试修复Service和BroadcastReceiver生命周期回调中的崩溃。同时手动执行framework未完成的代码，防止生命周期不完整引起的ANR

# 重启恢复

不对未捕获异常进行try-catch的话，那就只能让程序按照系统默认的处理杀掉进程。然后重启进程 恢复crash之前的Activity栈，达到比直接退出应用程序稍微好点的体验。实际使用时屏幕还是会有一个白屏闪烁，用户还是能够感知到APP崩溃了。有点鸡肋。

在启动每个Activity都记录起Activity的class对象以及所需要的Intent对象，应用崩溃后重启进程再通过这些缓存起来的Intent对象一次性把所有的Activity都启动起来。

但如果是启动过程中必现的BUG，这种方式会导致无限循环重启进程、恢复Activity。所以在一分钟内闪退两次就杀掉进程不再重启。

# 参考&扩展

- [Android开发之打造永不崩溃的APP——Crash防护](https://www.jianshu.com/p/01b69d91a3a8)
- [如何优雅的避免android(安卓)运行时崩溃](https://www.jianshu.com/p/76bff59b5418?utm_source=oschina-app)
- [Android应用程序进程启动过程的源代码分析](https://blog.csdn.net/luoshengyang/article/details/6747696)
- [Android中MotionEvent的来源和ViewRootImpl](https://blog.csdn.net/singwhatiwanna/article/details/50775201)
- [GitHub Cockroach](https://github.com/android-notes/Cockroach)
- [DefenseCrash](https://www.jianshu.com/p/76bff59b5418?utm_source=oschina-app)  **比较全面，View，Activity**
	- [DefenseCrash GitHub](https://github.com/xuuhaoo/DefenseCrash)
- [CrashDefend](https://blog.csdn.net/luweicheng24/article/details/88831327)
	- [CrashDefend GitHub](https://github.com/luweicheng24/CrashDefend)
- [GodBlessYou](https://juejin.im/post/5a38e9da51882506a463beb9) **koltin，修复Service和BroadcastReceiver中的Crash**
	- [GodBlessYou GitHub](https://github.com/ximsfei/GodBlessYou)
- [How the Java virtual machine handles exceptions](https://www.javaworld.com/article/2076868/how-the-java-virtual-machine-handles-exceptions.html)
- [Recovery GitHub](https://github.com/Sunzxyong/Recovery)
- [从字节码的角度来看try-catch-finally和return的执行顺序](https://blog.csdn.net/u010412719/article/details/50043865)
- [浅谈Android的编舞者Choreographer](https://www.jianshu.com/p/0a12a85809df)