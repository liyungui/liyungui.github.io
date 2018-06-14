---
title: CydiaSubstrate
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

Cydia Substrate可以修改任何主进程的代码，不管是用Java还是C/C++（native代码）编写的。而Xposed（开源）只支持 HOOK app_process中的java函数，因此Cydia Substrate是一款强大而实用的HOOK工具


Cydia Substrate

	参考自： 
		Android HOOK工具Cydia Substrate使用详解 http://mobile.51cto.com/aprogram-454091.htm
		周圣韬 Android上玩玩Hook：Cydia Substrate实战 http://www.csdn.net/article/2015-08-07/2825405 
	Cydia Substrate原名MobileSubstrate（类库中都是以MS开头），
	作者为大名鼎鼎的Jay Freeman（saurik）
	Cydia Substrate框架对于inline Hook(框架实现都是通过该方式)的操作目前还是存在一些bug，
		使用的时候可能会出现崩溃的现象，
		部分使用了国内定制ROM的设备在使用Cydia Substrate框架时会造成设备无法重新启动或无法Hook的现象。
		无法重启可以按住音量+ 键 跳过hook插件，进入系统。

1.安装substrate.apk，点击"Link Substrate Files"（连接本地的Substrate服务文件），
	这一步是需要Root权限的，连接后还需要重启设备才能够生效
	http://www.cydiasubstrate.com/download/com.saurik.substrate.apk
	
2.创建空Android工程。复制jar和so到libs文件夹中。
	其中的substrate.h头文件与lib文件夹下的so文件
		主要是substrate-api.jar
		.h和so是提供在使用NDK进行原生Hook程序开发中的函数支持库
	http://asdk.cydiasubstrate.com/zips/cydia_substrate-r2.zip
	
3.Manifest文件配置 权限和hook类（入口）
（1）需要指定权限：cydia.permission.SUBSTRATE
		manifest下 <uses-permission android:name="cydia.permission.SUBSTRATE"/>
（2）添加meta-data标签，指定自定义的hook类
		application下 <meta-data android:name="com.saurik.substrate.main" android:value=".Main"/>
			name 固定，value就是我们自定义的hook类完整类名（包含包名）
			
4.自定义hook类
	public class Main {
		static void initialize() { //插件加载时回调 static方法initialize
			 MS.hookClassLoad("android.content.res.Resources", new MS.ClassLoadHook() { //hook 类加载
				public void classLoaded(Class<?> resources) { //类被加载时回调		
					Method getColor; 
					try {
						getColor = resources.getMethod("getColor", Integer.TYPE);
					} catch (NoSuchMethodException e) {
						getColor = null;
					}

					if (getColor != null) {
						final MS.MethodPointer old = new MS.MethodPointer(); //原方法指针。可以在任何时候运行原方法（被hook方法）

						MS.hookMethod(resources, getColor, new MS.MethodHook() {
							public Object invoked(Object resources, Object... args)
								throws Throwable
							{
								int color = (Integer) old.invoke(resources, args);
								return color & ~0x0000ff00 | 0x00ff0000; //改变系统颜色
							}
						}, old);
					}
				}
			});
		}
	}
	
	也可以用以下代码实现hook
	MS.hookMethod(resources, getColor, new MS.MethodAlteration<Resources, Integer>() {
		public Integer invoked(Resources resources, Object... args)
			throws Throwable
		{
			return invoke(resources, args) & ~0x0000ff00 | 0x00ff0000;
		}
	});
		
5.安装apk，重启手机，生效。

关键api
	void hookClassLoad(String className, MS.ClassLoadHook hook); Hook一个指定的Class
	void hookMethod(Class _class, Member member, MS.MethodHook methodhHook, MS.MethodPointer old); 
	void hookMethod(Class _class, Member member, MS.MethodAlteration alteration);好用，稳定
		_class,需要hook的方法所属类
		member,需要hook的方法(或构造函数). 注意：不能HOOK字段 (在编译的时候会进行检测).
		methodhHook,MethodHook实例，其包含的invoked方法会被调用，用以代替被hook方法中的代码
		old,原方法指针，指向原方法（随时用该指针调用方法）
		alteration，MethodAlteration实例，其包含的invoked方法会被调用，用以代替被hook方法中的代码
			比MethodHook更好用稳定，在该方法直接调用invoke方法就是调用原方法
				不用自己定义 MS.MethodPointer old 指向原方法（随时用该指针调用方法）
	<T> T moveUnderClassLoader(ClassLoader loader, T object);   使用ClassLoder重载对象(少用)

6.补充
“卧槽”洗脑病毒分析 http://www.2cto.com/Article/201505/400301.html
	表现：所有字变为 卧槽。
	分析：跟上例改变字体颜色原理相同，只是hook的设置字体的方法
		TextView.setText(CharSequence) 
	复现：
		public class Main {         
			public static void initialize() {               
				MS.hookClassLoad("android.widget.TextView", new MS.ClassLoadHook() {  
					@Override 
					public void classLoaded(Class arg0) {                  
						Method smstest ;  
						try {     
						   smstest=arg0.getMethod("setText", CharSequence.class);  
						} catch (SecurityException e) {  
							smstest=null;  
							e.printStackTrace();                   
						} catch (NoSuchMethodException e) {  
							smstest=null;  
							e.printStackTrace();                    
						}  
						
					   if(smstest!=null){        
							final MS.MethodPointer old = new MS.MethodPointer();  
							MS.hookMethod(arg0, smstest, new MS.MethodHook() {  
							   @Override 
								public Object invoked(Object arg0, Object... arg1)throws Throwable {                                        
									return old.invoke(arg0, "爱破解，爱鬼哥");                                                                 
								}                             
							}, old);                          
						}                     
					}                
				});               
			}               				  
		}  

周圣韬 Android上玩玩Hook：Cydia Substrate实战 http://www.csdn.net/article/2015-08-07/2825405		
	开始实战（广告注入）
	针对Android操作系统的浏览器应用，Hook其首页Activity的onCreate方法（其他方法不一定存在，但是onCreate方法一定会有），
		(1)声明一个透明的广告的Activity
			为什么设置透明背景的Activity?
				就是为了使得弹出来的广告与浏览器融为一体，让用户感觉是浏览器弹出的广告，
				也是恶意广告程序为了防止自身被卸载掉的一些通用隐藏手段。
				这里演示的注入广告是通过Hook指定的Activity中的onCreate方法来启动一个广告Activity。
				如果启动的Activity带有恶意性，如将Activity做得与原Activity一模一样的钓鱼Activity，
				那么对于移动设备用户来说是极具欺骗性的。
			<!-- 透明无动画的广告Activity -->
			<activity
				android:name="com.example.hookad.MainActivity"
				android:theme="@android:style/Theme.Translucent.NoTitleBar" >
				<intent-filter>
					<action android:name="android.intent.action.VIEW" />
					<category android:name="android.intent.category.DEFAULT" />
					<!-- 广告的action,方便无context时启动  -->
					<action android:name="com.example.hook.AD" />
				</intent-filter>
			</activity>
		(2)找到浏览器主页的Activity名称
			使用adb shell下使用dumpsys activity命令找到浏览器主页的Activity名称为
				com.android.browser.BrowserActivity
		(3)关键hook代码
			// 执行Hook前的onCreate方法，保证浏览器正常启动
			Object result =  old.invoke(object, args);
			// 没有Context。所以执行一个shell 启动我们的广告Activity
			CMD.run("am start -a com.example.hook.AD");
			