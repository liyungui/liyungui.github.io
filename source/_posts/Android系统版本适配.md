---
title: Android系统版本适配
date: 2018-05-24 18:40:36
tags: 适配
---

# FileProvider替代file://Uri #

不再允许在app中把file://Uri暴露给其他app，包括但不局限于通过Intent或ClipData 等方法

Android7 提供了FileProvider，使用它生成content://Uri来替代file://Uri。

## 原因 ##

使用file://Uri会有一些风险，比如：

- 文件是私有的，接收file://Uri的app无法访问该文件。
- Android6.0引入运行时权限，如果接收file://Uri的app没有申请READ_EXTERNAL_STORAGE权限，在读取文件时会引发崩溃。

## FileProvider ##

manifest application节点下

	<provider
		android:authorities="${applicationId}.fileProvider"
		android:exported="false"
		android:grantUriPermissions="true">
		<meta-data
            android:name="android.support.FILE_PROVIDER_PATHS"
			android:resource="@xml/provider_paths"/>
    </provider>

res/xml/provider_paths.xml 指定路径和转换规则

	<?xml version="1.0" encoding="utf-8"?>
	<paths xmlns:android="http://schemas.android.com/apk/res/android">
	    <files-path name="cache_pdf" path="cache/pdf/"/>
	    <external-files-path name="external_cache_pdf" path="cache/pdf/"/>
	    <external-path name="external_image" path="zywx/image/"/>
	</paths>

代码

	//Uri photoOutputUri = Uri.fromFile(photoOutputFile);
	Uri photoOutputUri = FileProvider.getUriForFile(
	                    mContext,
	                    mActivity.getPackageName() + ".fileprovider",
	                    photoOutputFile);
	            intent.putExtra(MediaStore.EXTRA_OUTPUT, photoOutputUri);

## 注意 ##

android.support.v4.content.FileProvider 类只可以在manifest中注册一次。就如同一个Activity只可以注册一次一样

	Error:
		Element provider#android.support.v4.content.FileProvider at AndroidManifest.xml:119:9-131:20 duplicated with element declared at AndroidManifest.xml:105:9-117:20

一些第三方sdk为了适配android 7 也添加了这个节点

解决方案：

- 自定义类 继承自FileProvider
- 使用合并规则替换resource为我们的xml，然后把第三方sdk中的路径配置copy到provider_paths.xml
	- 如果 authorities 不一致，就是利用合并规则替换了，也会报错。因为第三方库java代码大概率写死了 authorities。
		- 代码不要写死 authorities，从manifest动态获取

## 异常处理 ##

- FileUriExposedException

		android.os.FileUriExposedException: file:///storage/emulated/0/Android/data/com.zy.course.dev/1467180514061025%23kefuchannelapp54752/test_22616/video/1527152182117.mp4 exposed beyond app through Intent.getData()
			at android.os.StrictMode.onFileUriExposed(StrictMode.java:1799)
			at android.net.Uri.checkFileUriExposed(Uri.java:2346)

	- 解决方案：使用FileProvider代替Uri.fromFile


- java.lang.SecurityException: Provider must not be exported
	- 解决方案：android:exported必须设置成false


- Attempt to invoke virtual method 'android.content.res.XmlResourceParser android.content.pm.PackageItemInfo.loadXmlMetaData(android.content.pm.PackageManager, java.lang.String)' on a null object reference
	- 解决方案：AndroidManifest.xml处的android:authorities必须跟 mActivity.getPackageName() + ".fileProvider" 一样

# AlarmManager #

## 定时任务的最佳实践 ##

- Handler 依赖于 Handler 所在的线程的，如果线程结束，就起不到定时任务的效果；
- Timer 手机关屏后长时间不使用，CPU 就会进入休眠模式。Timer 无法唤醒 CPU，定时任务就会失败
- AlarmManager 依赖 Android 系统服务，具备唤醒机制

AlarmManager实质是一个全局的定时器，是Android中常用的一种系统级别的提示服务，在指定时间或周期性发送`PendingIntent`广播  启动其它组件（包括Activity,Service,BroadcastReceiver）

## 版本适配 ##

查阅 [Android官网中关于 Android 4.4 变更](https://developer.android.google.cn/about/versions/android-4.4)发现Google 为了追求系统省电，`set()` 或 `setRepeating()` 创建的闹铃将变得不准确。还要追求精准的闹钟定时任务，要使用 `setExact()` 方法

[查阅 Android官网中关于 Android 6.0 变更](https://developer.android.google.cn/about/versions/marshmallow/android-6.0-changes) ，发现在 Android 6.0 中引入了低电耗模式和应用待机模式，标准 AlarmManager 闹铃（包括 `setExact()` 和 `setWindow()`）推迟到下一维护时段。
如果您需要设置在低电耗模式下触发的闹铃，请使用 `setAndAllowWhileIdle()` 或 `setExactAndAllowWhileIdle()`。触发闹铃的时间间隔都不能超过 9 分钟

	public static void setAlarmTimer(Context context, long triggerAtMillis,
                                     String action, int AlarmManagerType, int alarmId, String tutorTeacherName) {
        Intent myIntent = new Intent();
        myIntent.putExtra("tutorTeacherName", tutorTeacherName);//闹铃广播可以传递数据
        myIntent.setAction(action);
        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, alarmId, myIntent, 0);
        AlarmManager alarmManager = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            alarmManager.setExactAndAllowWhileIdle(AlarmManagerType, triggerAtMillis, pendingIntent);
        } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
            alarmManager.setExact(AlarmManagerType, triggerAtMillis, pendingIntent);
        } else {
            alarmManager.set(AlarmManagerType, triggerAtMillis, pendingIntent);
        }
    }

	public static void cancelAlarmTimer(Context context, String action) {
        Intent myIntent = new Intent();
        myIntent.setAction(action);
        PendingIntent sender = PendingIntent.getBroadcast(context, 0, myIntent, 0);
        AlarmManager alarm = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
        alarm.cancel(sender);
    }

广播接收者接收闹铃广播

	public class AlarmReceiver extends BroadcastReceiver {
	    public final static String TIMER_ACTION_REPEATING = "com.shensz.TIMER_ACTION_REPEATING";// 周期性的闹钟
	    public final static String TIMER_ACTION = "com.shensz.TIMER_ACTION";// 定时闹钟
	
	    @Override
	    public void onReceive(Context context, Intent intent) {
	        if (intent.getAction().equals(TIMER_ACTION_REPEATING)) {
	        } else if (intent.getAction().equals(TIMER_ACTION)) {
	            String tutorTeacherName = intent.getStringExtra("tutorTeacherName");
	            if (!TextUtils.isEmpty(tutorTeacherName)) {
	                sendNotification(context, tutorTeacherName);
	            }
	        }
	    }
	    
	}

注册广播接收者

		<receiver android:name="com.shensz.course.module.main.AlarmReceiver">
        <intent-filter>
            <action android:name="com.shensz.TIMER_ACTION_REPEATING" />
            <action android:name="com.shensz.TIMER_ACTION" />
        </intent-filter>
    </receiver>

## int type 和 long triggerAtMillis ##

这个需要注意文档的描述。不留神triggerAtMillis没有加上基准时间(根据type而不同)，就会发现广播都是马上触发(因为触发时间已过，所以马上发送广播)

type：闹钟类型

- ELAPSED_REALTIME：
	- 在指定的延时过后，发送广播，但不唤醒设备（闹钟在睡眠状态下不可用）。如果在系统休眠时闹钟触发，它将不会被传递，直到下一次设备唤醒。
	- 延时是要把系统启动到现在的时间SystemClock.elapsedRealtime()(基准时间)算进去的。
- ELAPSED_REALTIME_WAKEUP：
	- 同上，唯一区别就是 会唤醒设备
- RTC：
	- 当系统调用System.currentTimeMillis()方法返回的值等于triggerAtTime时，发送广播，但不唤醒设备。
		- 可以设置系统时间触发闹铃广播
- RTC_WAKEUP：
	- 同上，唯一区别就是 会唤醒设备
- POWER_OFF_WAKEUP：
	- 闹钟在手机关机状态下也能正常进行提示功能，所以是5个状态中用的最多的状态之一
	- 该状态下闹钟也是用绝对时间，状态值为4；不过本状态好像受SDK版本影响，某些版本并不支持。

示例：

	AlarmManager.RTC，System.currentTimeMillis()+10 * 60 * 1000
	AlarmManager.ELAPSED_REALTIME，SystemClock.elapsedRealtime()+10 * 60 * 1000





