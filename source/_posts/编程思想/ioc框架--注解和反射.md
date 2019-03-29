---
title: 分层架构与 M-V-X
date: 2019-01-14 08:58:53
categories:
  - 编程思想
tags:
  - 编程思想
---

ioc框架--注解和反射
来自张鸿洋博客 http://blog.csdn.net/lmj623565791/article/details/39269193
IoC，控制反转（Inversion of Control，英文缩写为IoC）
1.为什么要ioc
	一个类里面需要用到很多个成员变量，传统的写法，你要用这些成员变量，那么你就new 出来用呗~~
	IoC的原则是：不要new，这样耦合度太高；你配置个xml文件，里面标明哪个类，里面用了哪些成员变量，等待加载这个类的时候，我帮你注入（new）进去；
	所以，在现代软件分层开发中，每一层要一个包放接口，一个包放实现类
		而ioc只要声明了成员变量+写个配置文件，有人帮你new；
		此时，在类中就可以把需要使用到的成员变量都声明成接口，
		然后你会发现，当实现类发生变化的时候，或者切换实现类，你只要在配置文件里面做个简单的修改。
		如果你用的就是实实在在的实现类，现在换实现类，你需要找到所有声明这个实现类的地方，逐个手动修改类名
	有人说，写个配置文件多麻烦。于是又出现了另一种方案。
	注解--在需要注入的成员变量上面加个注解
2.如何注入
	配置文件/注解 是如何实现注入的？
	其实就是把字符串类路径变成类。这就需要用到反射了。
3.注入框架实现--xUtils
	使用实例
		@ContentView(value = R.layout.activity_main)  
		public class MainActivity extends BaseActivity {  
			@ViewInject(R.id.id_btn)  
			private Button mBtn1;  
			@ViewInject(R.id.id_btn02)  
			private Button mBtn2; 
			public void onCreate(Bundle savedInstanceState) {
				super.onCreate(savedInstanceState);								
				ViewUtils.inject(this);	
			}
		}	
	实现	
		@Target(ElementType.TYPE)  
		@Retention(RetentionPolicy.RUNTIME)  
		public @interface ContentView  
		{  
			int value();  
		} 
		@Target(ElementType.FIELD)  
		@Retention(RetentionPolicy.RUNTIME)  
		public @interface ViewInject  
		{  
			int value();  
		}
		public static void inject(Activity activity) { 
			injectContentView(activity);  
			injectViews(activity);  
		} 
		(1)注入主布局文件的代码
			private static void injectContentView(Activity activity) {  
				Class<? extends Activity> clazz = activity.getClass();  
				// 查询类上是否存在ContentView注解  
				ContentView contentView = clazz.getAnnotation(ContentView.class);  
				if (contentView != null)// 存在  
				{  
					int contentViewLayoutId = contentView.value();  
					try  
					{  
						Method method = clazz.getMethod("setContentView", int.class);  
						method.setAccessible(true);  
						method.invoke(activity, contentViewLayoutId);  
					} catch (Exception e)  
					{  
						e.printStackTrace();  
					}  
				}  
			} 
			通过传入的activity对象，获得它的Class类型，判断如果该类写了ContentView这个注解，读取它的value，然后得到setContentView这个方法，使用invoke进行调用；
		(2)注入Views	
			private static void injectViews(Activity activity) {  
				Class<? extends Activity> clazz = activity.getClass();  
				Field[] fields = clazz.getDeclaredFields();  
				// 遍历所有成员变量  
				for (Field field : fields)  
				{   
					ViewInject viewInjectAnnotation = field.getAnnotation(ViewInject.class);  
					if (viewInjectAnnotation != null){  
						int viewId = viewInjectAnnotation.value();  
						if (viewId != -1){  
							Log.e("TAG", viewId+"");  
							// 初始化View  
							try {  
								Method method = clazz.getMethod("findViewById", int.class);  
								Object resView = method.invoke(activity, viewId);  
								field.setAccessible(true);  
								field.set(activity, resView);  
							} catch (Exception e) {  
								e.printStackTrace();  
							}  
						}  
					}  
				}  		  
			} 
			遍历类中声明的所有属性，找到存在ViewInject注解的属性并获取其value，然后去调用findViewById方法，最后把值设置给field