---
title: Activity
date: 2019-10-16 14:13:53
categories:
  - Android
tags:
	- Android
---

# 四种启动模式

    1. standard 标准默认

        默认启动模式，每次激活Activity都创建Activity，并放入任务栈中。

    2. singleTop 栈顶复用

        如果在任务的栈顶正好存在该Activity的实例， 就重用该实例，否者就会创建新的实例并放入栈顶(即使栈中已经存在该Activity实例，只要不在栈顶，都会创建实例)。

    3. singleTask 栈内复用

        如果在栈中已经有该Activity的实例，就重用该实例(会调用实例的onNewIntent())。重用时，会让该实例回到栈顶，因此在它上面的实例将会被移除栈。如果栈中不存在该实例，将会创建新的实例放入栈中。 

		如果是另外一个apk启动该Activity，则会创建新实例并放入全新的栈底

    4. singleInstance  实例复用（栈内复用加强版）

        在一个新栈中创建该Activity实例，并让多个应用共享改栈中的该Activity实例。一旦改模式的Activity的实例存在于某个栈中，任何应用再激活改Activity时都会重用该栈中的实例，其效果相当于多个应用程序共享一个应用，不管谁激活该Activity都会进入同一个应用中。

# Activity复用--onNewIntent

	1. anifest中对Activity设置lanuchMode=“singleTask”
	2. Activity中复写onNewIntent(intent)
		在onNewIntent() 中使用setIntent(intent)给Activity赋值新得到的Intent.否则，getIntent()都是得到老的Intent（没有附加数据或附加数据不对）。

`创建 Activity`执行onCreate()---->onStart()---->onResume()等后续生命周期函数，也就是说第一次启动Activity并不会执行到onNewIntent(). 

`复用 Activity`执行onNewIntent()---->onResart()------>onStart()----->onResume(). 注意onResart()和onStart()不一定会回调

 如果android系统由于内存不足把已存在Activity释放掉了，那么再次调用的时候会重新 `创建 Activity` 即执行onCreate()---->onStart()---->onResume()等。
 
# startActivityForResult

## resultCode和requestCode作用

resultCode：解决「区分多个异步任务」的问题

requestCode:异步调用结果码，告诉调用者成功/失败/其它信息

### requestCode必须大于等于0

[ActivityStarter.startActivityLocked()](http://androidxref.com/7.0.0_r1/xref/frameworks/base/services/core/java/com/android/server/am/ActivityStarter.java#266)

```java
259        ActivityRecord sourceRecord = null;
260        ActivityRecord resultRecord = null;
261        if (resultTo != null) {
262            sourceRecord = mSupervisor.isInAnyStackLocked(resultTo);
263            if (DEBUG_RESULTS) Slog.v(TAG_RESULTS,
264                    "Will send result to " + resultTo + " " + sourceRecord);
265            if (sourceRecord != null) {
266                if (requestCode >= 0 && !sourceRecord.finishing) {
267                    resultRecord = sourceRecord;
268                }
269            }
270        }
```
只有requestCode大于等于0，且sourceRecord没有结束，resultRecord才会指向sourceRecord

## setResult和finish

setResult和finish类似生产者/消费者模型，setResult 负责写入数据，finish 负责读取数据。

setResult把数据记录在 Activity.mResultCode 和 Activity.mResultData 变量中。两个变量由 Activity 对象锁保证线程安全，支持后台线程和 UI 线程分别进行 setResult 和 finish

所以 setResult 一定要在 finish 之前执行。

## API 内部原理/数据处理流程


AMS: ActivityManagerService
AMN: ActivityManagerNative
AMP: ActivityManagerProxy

- Client 端通过 AMP 把数据发送给 Server 端 AMS Binder 实体
- AMS 把数据包装成 ActivityResult 并保存在源 ActivityRecord 的 results 变量中
- AMS 通过 ApplicationThreadProxy 向 Client 端发送 pause 信息让栈顶 Activity 进入 paused 状态，并等待 Client 端回复或超时
- AMS 接收 Client 端已 paused 信息，恢复下一个获取焦点的 Activity ，读取之前保存在 ActivityRecord.results 变量的数据派发给 Client 端对应的 Activity
- Client 端数据经过 ApplicationThread 对象、ActivityThread 对象的分发最后到达 Activity

## singleTask和singleInstance造成onActivityResult错误

基本原则:源 Activity 和目标 Activity 无法在跨 Task 情况下通过 onActivityResult 传递数据

Android 5.0 以上 AMS 在处理 manifest.xml 文件中的 singleTask 和 singleInstance 信息「不会」创建新的 Task，因此可以收到正常回调

[链接：Cross Reference](http://androidxref.com/7.0.0_r1/xref/frameworks/base/services/core/java/com/android/server/am/ActivityStarter.java#1196)

Android 4.4.4 以下 AMS 在处理 manifest.xml 文件中的 singleTask(仅目标Activity) 和 singleInstance 信息「会」创建新的 Task，因此在 startActivity 之后立即收到取消的回调

[链接：Cross Reference](http://androidxref.com/4.4.4_r1/xref/frameworks/base/services/java/com/android/server/am/ActivityStackSupervisor.java#1399)

```java
1345    final int startActivityUncheckedLocked(ActivityRecord r,
1346            ActivityRecord sourceRecord, int startFlags, boolean doResume,
1347            Bundle options) {
...
1382        if (sourceRecord == null) {
1383            // This activity is not being started from another...  in this
1384            // case we -always- start a new task.
1385            if ((launchFlags&Intent.FLAG_ACTIVITY_NEW_TASK) == 0) {
1386                Slog.w(TAG, "startActivity called from non-Activity context; forcing " +
1387                        "Intent.FLAG_ACTIVITY_NEW_TASK for: " + intent);
1388                launchFlags |= Intent.FLAG_ACTIVITY_NEW_TASK;
1389            }
1390        } else if (sourceRecord.launchMode == ActivityInfo.LAUNCH_SINGLE_INSTANCE) {
1391            // The original activity who is starting us is running as a single
1392            // instance...  this new activity it is starting must go on its
1393            // own task.
1394            launchFlags |= Intent.FLAG_ACTIVITY_NEW_TASK;
1395        } else if (r.launchMode == ActivityInfo.LAUNCH_SINGLE_INSTANCE
1396                || r.launchMode == ActivityInfo.LAUNCH_SINGLE_TASK) {
1397            // The activity being started is a single instance...  it always
1398            // gets launched into its own task.
1399            launchFlags |= Intent.FLAG_ACTIVITY_NEW_TASK;
1400        }
```

通过 dumpsys activity activities 命令查看 AMS 状态，验证两个 Activity 是否属于不同的 Task

# 全屏

设置在setContentView()方法之前

```java
//无title    
requestWindowFeature(Window.FEATURE_NO_TITLE);    
//全屏    
getWindow().setFlags(WindowManager.LayoutParams. FLAG_FULLSCREEN , WindowManager.LayoutParams. FLAG_FULLSCREEN);
```

# 背景透明

- Activity使用自定义透明背景style
- Activity布局根view使用默认(不要设置)

```xml
android:theme="@style/activity_Transparent"
```

```xml
<style name="activity_Transparent" >
    <item name="android:windowBackground">@color/translucent</item>
    <item name="android:windowNoTitle">true</item>
    <item name="android:windowFullscreen">true</item>
    <item name="android:windowIsTranslucent">true</item>
    <item name="android:windowCloseOnTouchOutside">false</item>
    <item name="android:colorBackgroundCacheHint">@null</item>
    <item name="android:windowAnimationStyle">@android:style/Animation.Translucent</item>
</style>
```

```xml
<color name="translucent">#00000000</color>
```





