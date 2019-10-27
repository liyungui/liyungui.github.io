---
title: 服务与IPC及AIDL
date: 2019-10-12 14:13:53
categories:
  - Android
tags:
	- Android
---

# Service

运行在后台的组件，可以理解为是没有前台的activity，适合用来运行不需要前台界面的代码。

activity不可见时(stop)是很容易被系统终止的，不能稳定运行下载等后台任务。
	
服务可以被手动关闭，不会重启，但是如果是被自动关闭，内存充足就会重启

## 进程优先级

1. 前台进程：拥有焦点activity（onResume方法被调用）
2. 可见进程：拥有可见activity（onPause方法被调用）
3. 服务进程：有服务，不到万不得已不会被回收，而且即便被回收，内存充足时也会被重启
4. 后台进程：有不可见activity（activity的onStop方法被调用了），很容易被回收
5. 空进程：没有运行任何activity，很容易被回收

## Service开发流程

1. 自定义类继承抽象类 Service。覆写方法  IBinder onBind(Intent intent)
2. 配置（注册service，intentfilter，权限）

## Service方法

- startService
- bindService
- unbindService
- stopService

startService和bindService都可能造成onCreate方法的调用。

startService可以被重复调用多次

bindService多次调用会导致程序报错。

stopService多次调用也会报错。

stopService与unbindService都有可能会触发onDestroy()，要触发就必须满足：服务停止，没有ServiceConnection绑定：

## 启动服务

两种启动方式

### startService

服务被启动之后，常驻内存(在running中可以看到服务进程)。即使启动它的组件销毁，也可以继续存在。

### bindService

如果启动它的组件销毁，服务也销毁。绑定可获得一IBinder对象，利用这个对象可以调用service的方法（AIDL规范必须使用接口对象接收IBinder对象，调用服务方法。）

系统服务都是通过bind方式启动的远程服务。

`bindService(Intent service, ServiceConnection conn, int flags)` flags一般设置为 `BIND_AUTO_CREATE`
		
`ServiceConnection`接口中的两个方法 

- onServiceConnected(ComponentName name, IBinder service)。可以通过返回的IBinder接口对象（一般用其实现类Binder）调用service中的方法。
- onServiceDisconnected(ComponentName name)
	
## Service生命周期

- onCreate 服务创建的时候调用。
- onStartCommand 每次启动服务的时候调用。同一个服务可以重复的启动
- onBind 绑定的时候调用。
- onDestroy 销毁服务的时候调用。

### startService启动服务的生命周期

`onCreate-onStartCommand-onDestroy` 

onStartCommand其实还是调用onStart方法，android觉得onStart不贴切，换了个名字

### bindService启动服务的生命周期
	
`onCreate-onBind-onDestroy` 

## 停止服务

两种启动方法混合使用，必须严格按照以下流程，否则可能导致莫名其妙的异常。

先start，再bind，销毁时先unbind，再stop
 	
# 本地服务

服务和启动它的组件在同一个进程

可以显式启动，绑定后返回IBinder对象

一般通过接口定义Service的接口，控制对外方法；服务中自定义Binder类实现该接口，绑定后将自定义Binder类对象强转为接口再返回，从而达到控制服务对外方法的目的

```java
public interface PublicBusiness {//定义service的接口，控制对外方法
    void QianXian();
}

public class BanZhengService extends Service {

	@Override
	public IBinder onBind(Intent intent) {
		return new ZhongJianRen();
	}

	public void BanZheng(){
		System.out.println("办证哪家强");
	}
	
	class ZhongJianRen extends Binder implements PublicBusiness{////继承Binder(IBinder接口实现类)，实现PublicBusiness接口（定义service的接口，控制对外方法）
		public void QianXian(){
			BanZheng();
		}
		
		public void daMaJiang(){
			
		}
	}
}
```

```java
public class MainActivity extends Activity {
    private MyServiceconn conn;
    private PublicBusiness zjr;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        conn = new MyServiceconn();
        Intent intent = new Intent(this, BanZhengService.class);
        bindService(intent, conn, BIND_AUTO_CREATE);
    }
 
    public void click(View v){
        zjr.QianXian();
    }
     
    class MyServiceconn implements ServiceConnection{
 
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
        	//强转为PublicBusiness，控制对外方法
            zjr = (PublicBusiness) service;
        }
 
        @Override
        public void onServiceDisconnected(ComponentName name) {
                         
        }
         
    }
     
}
```

# 远程服务

服务和启动它的组件不在同一个进程。

远程服务只能隐式启动

# 多进程支持

`android:process`

Android 四大组件 默认在同一个 进程运行（并且运行于主线程），`android:process` 这句配置可以 让相应的组件运行在 独立的进程中（主线程上）

`android:process`的值以**冒号**开头的话，那么该进程就是**私有进程**

```xml
<service android:name=".ProcessTestService" android:process=":secondProcess"/>
```

进程名为 `com.zy.course:secondProcess `

`android:process`的值以**小写字母**开头，那么该进程就是公有进程，公有进程名一定要有个**点号**(如com.secondProcess)

application元素也支持android:process属性，可以修改应用程序的默认进程名（默认值为包名）

# IPC

Android各进程内存地址相互独立，都有一个MainThread，MainLooper，MessageQueue

多进程就涉及到 进程间通信 **IPC**(Inter-Process Communication
)

## IPC方式

- **文件共享**，多进程读写一个相同的文件，获取文件内容进行交互；
- **Socket**
- **AIDL**，Android标准跨进程通讯API，非常灵活且强大。支持并发，传递数据，方法调用
- **Messenger**，基于AIDL实现的轻量级跨进程通讯方案，只能传递Message对象
- **Bundle**，只能在四大组件间传递Bundle对象;
- **ContentProvider**，常用于多进程共享数据，比如系统的相册，音乐等
- **广播**

# AIDL

安卓接口定义语言(Android interface definition language)

作用场景：和服务一起实现跨进程通信

一般通过AIDL定义Service的接口(将类文件名后缀改为`.aidl`)，控制对外方法；服务中自定义Binder类继承该 `接口.Stub`(自动生成)，绑定后将自定义Binder类对象强转(通过 `接口.Stub.asInterface()`)为接口再返回，从而达到控制服务对外方法的目的

## 数据传递

方法调用会涉及到数据传递(传参和返回值)

支持的数据类型

- Java 基本数据类型（如 int、long、float、double、byte、char、boolean）
- String和CharSequence
- Parcelable：实现了Parcelable接口的对象
- List：其中的元素需要被AIDL支持，另一端实际接收的具体类始终是 ArrayList，但生成的方法使用的是 List 接口
- Map：其中的元素需要被AIDL支持，包括 key 和 value，另一端实际接收的具体类始终是 HashMap，但生成的方法使用的是 Map 接口

### 注意事项

- Parcelable对象，需要在类文件相同路径下，创建同名`.aidl`文件，在文件中使用parcelable关键字声明这个类；
- `.aidl`跟普通接口的区别：只能声明方法，不能声明变量；
- 非基本数据类型的参数，需要标记数据流向：in、out、inout。基本数据类型流向只能in，所以不用标

#### in、out、inout

- in。输入的参数。跟普通参数传递一样的含义，接收调用方实际传递的值
- out。仅用于输出的参数。无论调用方传递了什么值过来，在方法执行的时候，这个参数的初始值总是空的,这个参数的值在方法被调用后填充。跟c语言里用指针返回结果类似
- inout。输入和输出的参数。

区分“in”、“out”是非常重要的，因为每个参数的内容必须编组（序列化，传输，接收和反序列化）。in/out标签允许Binder**跳过编组步骤**以获得更好的性能。

```java
// app/src/main/aidl/com/example/aidl/data/MessageModel.aidl
package com.example.aidl.data;
parcelable MessageModel;
```

```java
// app/src/main/java/com/example/aidl/data/MessageModel.java
package com.example.aidl.data;

public class MessageModel implements Parcelable {

    private String from;
    private String to;
    private String content;
    ...
}
```

```java
// app/src/main/aidl/com/example/aidl/MessageHandler.aidl
package com.example.aidl;
import com.example.aidl.data.MessageModel;

interface MessageHandler {
    void sendMessage(in MessageModel messageModel);

    void onMessageReceived(in MessageModel receivedMessage);
}
```

## 实例

调用远程的支付宝支付服务

支付宝远程服务

1. 定义服务接口，后缀名改成 `.aidl`
2. 自定义Binder类继承 `接口.Stub` (自动生成)
3. 自定义Service
4. 配置（注册service，intentfilter，权限）

需要支付的应用

1. 把刚才定义好的aidl文件拷贝过来，注意aidl文件所在的包名必须跟原包名一致。如果是在同一个工程，则不需要拷贝
2. 绑定服务，在onServiceConnected方法中拿到IBinder对象
3. 通过 `接口.Stub.asInterface()`方法强转成 接口对象
4. 调用接口的pay方法

```java
// PayInterface.aidl
interface PayInterface {
 void pay();
}

public class PayService extends Service {

	@Override
	public IBinder onBind(Intent intent) {
		return new MyBinder();
	}
	
	public void pay(){
		System.out.println("检测运行环境");
		System.out.println("支付");
	}
	
	class MyBinder extends PayInterface.Stub{

		@Override
		public void pay() throws RemoteException {
			PayService.this.pay();
		}
		
	}
	
}
```

```xml
<service android:name="com.itheima.alipay.PayService">
    <intent-filter ><action android:name="com.itheima.alipay"/></intent-filter>
</service>
```

```java
public class MainActivity extends Activity {
    private PayInterface pi;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent intent = new Intent();
        intent.setAction("com.itheima.alipay");
        bindService(intent, new MyServiceConn(), BIND_AUTO_CREATE);
    }
    
	public void click(View v){
        try {
            pi.pay();
        } catch (RemoteException e) {
            e.printStackTrace();
        }
         
    }
    
    class MyServiceConn implements ServiceConnection{
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            pi = PayInterface.Stub.asInterface(service);
        }
 
        @Override
        public void onServiceDisconnected(ComponentName name) {
             
        }
         
    }
     
}
```

## 所以然

分析 自动生成的接口类，目录在 `build/gen `

`asInterface` 把IBinder对象转换为 接口对象。判断IBinder是否处于相同进程，相同进程返回Stub实现的接口对象；不同进程，则返回Stub.Proxy实现的接口对象

`onTransact`同一进程时，不会触发。

{% asset_img aidl_flowchart.jpg %}

## Binder意外挂掉

IPC中，当Binder意外挂了的时候(比如服务端进程Crash了)
，客户端进程就无法调用服务端方法。所以我们需要检测Binder存活状态，如果挂掉了，需要进行相应操作(比如重连服务)。

### isBinderAlive

Binder中的 `isBinderAlive` 可以判断Binder是否死亡

### DeathRecipient

给Binder设置一个 `DeathRecipient` 对象，Binder挂掉可以在DeathRecipient接口的回调方法中收到通知

- linkToDeath -> 设置死亡代理 DeathRecipient 对象；
- unlinkToDeath -> Binder死亡的情况下，解除该代理。

```java
IBinder.DeathRecipient deathRecipient = new IBinder.DeathRecipient() {
   @Override
   public void binderDied() {
       if (messageSender != null) {
           messageSender.asBinder().unlinkToDeath(this, 0);
           messageSender = null;
       }
       //重连服务
       setupService();
   }
};
   
ServiceConnection serviceConnection = new ServiceConnection() {
   @Override
   public void onServiceConnected(ComponentName name, IBinder service) {
   	   //使用asInterface方法取得AIDL对应的操作接口
            messageSender = MessageSender.Stub.asInterface(service);
       try {
           //设置Binder死亡监听
           messageSender.asBinder().linkToDeath(deathRecipient, 0);
       } catch (RemoteException e) {
           e.printStackTrace();
       }
   }
};
```

## 权限验证

 两种常用验证方法：


### onTransact方法校验客户端包名

自定义类继承AIDL接口的Stub，复写onTransact方法，校验客户端包名，不通过校验直接return false，校验通过执行正常的流程。

```java
IBinder messageSender = new MessageSender.Stub() {
    @Override
    public boolean onTransact(int code, Parcel data, Parcel reply, int flags) throws RemoteException {
        String packageName = null;
        String[] packages = getPackageManager().getPackagesForUid(getCallingUid());
        if (packages != null && packages.length > 0) {
            packageName = packages[0];
        }
        if (packageName == null || !packageName.startsWith("com.example.aidl")) {
            Log.d("onTransact", "拒绝调用：" + packageName);
            return false;
        }
        return super.onTransact(code, data, reply, flags);
    }
};
```

### onBind中校验自定义permission

在服务端的onBind中校验自定义permission，如果通过了我们的校验，正常返回Binder对象，校验不通过返回null，返回null的情况下客户端无法绑定到我们的服务；

```xml
<permission
    android:name="com.example.aidl.permission.REMOTE_SERVICE_PERMISSION"
    android:protectionLevel="normal" />
<uses-permission android:name="com.example.aidl.permission.REMOTE_SERVICE_PERMISSION" />
```

```java
@Override
public IBinder onBind(Intent intent) {
    //自定义permission方式检查权限
    if (checkCallingOrSelfPermission("com.example.aidl.permission.REMOTE_SERVICE_PERMISSION") == PackageManager.PERMISSION_DENIED) {
        return null;
    }
    return messageSender;
}
```

# 多进程造成Application多次创建

每个进程创建，都会调用Application的onCreate方法

可以根据当前进程的pid，拿到当前进程的名字，根据当前进程的pid或者名字，做不同的初始化工作

```java
public class MyApp extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        Log.d("process name", getProcessName());//打印当前进程名字
    }
    //取得进程名
    private String getProcessName() {
        ActivityManager am = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        List<ActivityManager.RunningAppProcessInfo> runningApps = am.getRunningAppProcesses();
        if (runningApps == null) {
            return null;
        }
        for (ActivityManager.RunningAppProcessInfo procInfo : runningApps) {
            if (procInfo.pid == Process.myPid()) {
                return procInfo.processName;
            }
        }
        return null;
    }
}
```

# 跨进程更新UI

实例：通过Temp2Activity在MainActivity中添加两个Button

## 只使用AIDL

### 缺陷

- **繁琐**。使用到的View中的方法都需要在IPC中增加对应的方法
- **性能开销大**。View的每一个方法都会涉及到IPC操作，多次IPC带来的开销问题不容小觑。
- View中方法的某些参数可能**不支持IPC传输**。如OnClickListener接口没有序列化。

## AIDL配合RemoteViews

RemoteViews就是为跨进程更新UI而生的，内部封装了很多方法用来实现跨进程更新UI。

```java
// IremoteViewsManager.aidl
interface IremoteViewsManager {
    void addRemoteView(in RemoteViews remoteViews);
}
```

```java
// MainActivity.java
// RemoteViews转为View使用
View view = remoteViews.apply(context, mLinearLayout);
mLinearLayout.addView(view);
```

```java
// Temp2Activity.java
// 绑定服务拿到IremoteViewsManager对象
public void onServiceConnected(ComponentName name, IBinder service) {
    remoteViewsManager = IremoteViewsManager.Stub.asInterface(service);
}

//更新UI。添加两个button
public void UpdateUI(View view){
	//创建RemoteViews
    RemoteViews remoteViews = new RemoteViews(Temp2Activity.this.getPackageName(),R.layout.button_layout);
	//按钮点击事件绑定PendingIntent
    Intent intentClick = new Intent(Temp2Activity.this,FirstActivity.class);
    PendingIntent openFirstActivity = PendingIntent.getActivity(Temp2Activity.this,0,intentClick,0);    remoteViews.setOnClickPendingIntent(R.id.firstButton,openFirstActivity);
	//设置按钮文本
	remoteViews.setCharSequence(R.id.secondButton,"setText","想改就改");
	//调用AIDL的接口添加RemoteViews到布局中展示
    try {
        remoteViewsManager.addRemoteView(remoteViews);
    } catch (RemoteException e) {
        e.printStackTrace();
    }
}
```

### RemoteViews缺陷



- **目前支持的布局和View有限**
	- layout：
		- FrameLayout
		- LinearLayout
		- RelativeLayout
		- GridLayout
	- View：
		- AnalogClock
		- button
		- Chronometer
		- ImageButton
		- ImageView
		- ProgressBar
		- TextView
		- ViewFlipper
		- ListView
		- GridView
		- StackView
		- AdapterViewFlipper
		- ViewStub
	- 不支持自定义View

# 参考&扩展

- [巧用Android多进程，微信，微博等主流App都在用](https://cjw-blog.net/2017/02/26/AIDL/)
- [github 源码](https://github.com/V1sk/AIDL)
- [in、out、inout意义](http://stackoverflow.com/questions/4700225/in-out-inout-in-a-aidl-interface-parameter-value) stackoverflow
- [Android通过RemoteViews实现跨进程更新UI](https://blog.csdn.net/chenzheng8975/article/details/54969791)



