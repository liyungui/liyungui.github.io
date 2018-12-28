---
title: Android ORM框架
date: 2018-12-21 09:01:53
categories:
  - 数据库
tags:
  - ORM
---


|orm|原理|特性|Module定义|初始化灵活|配置数据库|
| --- | --- | --- |--- |--- |--- |
|OrmLite|注解反射|OrmLiteSqliteOpenHelper创建数据库|@DatabaseTable(tableName = "accounts")|√|OrmLiteSqliteOpenHelper创建数据库时|
|SugarORM|注解反射|实践中提示找不到表|直接继承特定类/@Table注解|提供application|meta-data|
|Active Android|注解反射||×直接继承特定类|提供application/自定义初始化|meta-data|
|Realm |注解反射|基于C++，直接运行在设备硬件上，高性能|×直接继承特定类|√|代码灵活配置|
|xutils的dbutils|注解反射|可继承父类字段，泛框架，apk体积大|可继承父类字段|√|代码灵活配置|
|GreenDAO|代码模板生成|Java工程生成dao，高性能，繁琐不灵活|无法继承父类字段，可继承接口方法|√||
|DBFlow |注解apt预编译|apt预编译，高性能，无缝支持多个数据库|直接继承特定类/实现Model接口|application中/其他Context(Activity)中初始化也将只有Application的context|static final字段|
|SQLBrite ||响应式数据库||||

## 1. OrmLite 注解反射 ##

OrmLite 是 Java ORM。支持JDBC连接，Spring以及Android平台。

语法中广泛使用了注解（Annotation）。

## 2. SugarORM 注解反射 ##

	http://satyan.github.io/sugar/getting-started.html

SugarORM 是 Android 平台专用ORM。提供简单易学的APIs。可以很容易的处理1对1和1对多的关系型数据，并通过3个函数save(), delete() 和 find() (或者 findById()) 来简化CRUD基本操作。

github开源的jar包导入Android studio 识别出错，eclipse使用正常

### 配置 ###

通过AndroidManifest.xml meta-data标签配置 数据库名称、版本

### 初始化 ###

1. AndroidManifest.xml application 是 `com.orm.SugarApp`或它的子类

### Moudle ###

1. Moudle 必须含有 default constructor.
2. Moudle 两种定义方式

		直接 extends SugarRecord
		@Table注解，同时 Moudle 必须含有 private Long id field

## 3. GreenDAO 代码模板生成##

**快**：当性能很重要时（数据访问频繁），GreenDao是一个很快的解决方案，它能够支持数千条记录的CRUD每秒，和OrmLite相比，GreenDAO要快几乎4.5倍。

**小**：GreenDAO小于100KB，所以对于应用程序APK的大小影响很小。

**繁**：必须使用Java工程（代码模板）生成dao，学习成本高

**死**：生成的dao固定，不方便修改。增加功能需要重新运行Java工程生成dao，这同时导致我们添加到dao类的自定义方法（非模板生成）被覆盖

## 4. Active Android 注解反射##

### 配置 ###

通过AndroidManifest.xml meta-data标签配置 数据库名称、版本

### 初始化 ###

1. AndroidManifest.xml application 是 `com.activeandroid.app.Application`或它的子类

2. 自定义初始化

		ActiveAndroid.initialize(this);//方法一
	
		Configuration dbConfiguration = new Configuration.Builder(this).setDatabaseName("xxx.db").create();
        ActiveAndroid.initialize(dbConfiguration);//方法二

### Moudle ###

1. Moudle 必须含有 default constructor.
2. Moudle 一种定义方式

		extends  Model

## 5. Realm 注解反射 ##

	https://realm.io/
	http://www.tuicool.com/articles/V7ZFvuB Realm for Android快速入门教程
	
基于C++编写，直接运行在你的设备硬件上（不需要被解释），因此运行很快。

开源跨平台

### 创建一个Realm ###

一个Realm相当于一个SQLite数据库。它有一个与之对应的文件，一旦创建将持久保存在安卓的文件系统中。

要创建一个新的Realm，你可以在任意Activity中调用静态方法Realm.getInstance。

	Realm myRealm = Realm.getInstance(context); //创建default.realm的Realm文件
	
	Realm myOtherRealm = Realm.getInstance(
                new RealmConfiguration.Builder(context)
                        .name("myOtherRealm.realm")
                        .build()
	);//自定义文件名的realm文件

### 创建一个RealmObject ###

继承RealmObject

### Realm实战总结 ###

	Realm实战总结---Android http://blog.csdn.net/javine/article/details/51016754

1. model类必须extends RealmObject,所有属性必须用private修饰

2. model中支持基本数据结构：boolean, byte, short, ìnt, long, float, double, String, Dateand byte[]

3. 若要使用List必须用RealmList<T>，或者继承RealmList

4. 与Retrofit2.*一起使用，通过Gson来解析Json数据并直接生成RealmObject，可参考如下写法：

		Gson gson = new GsonBuilder()  
        .setExclusionStrategies(new ExclusionStrategy() {  
            @Override  
            public boolean shouldSkipField(FieldAttributes f) {  
                return f.getDeclaringClass().equals(RealmObject.class);//跳过RealmObject类型字段不解析  
            }  
  
            @Override  
            public boolean shouldSkipClass(Class<?> clazz) {  
                return false;  
            }  
        })  
        .create();  
  
		// Configure Retrofit to use the proper GSON converter  
		RestAdapter restAdapter = new RestAdapter.Builder()  
		    .setEndpoint("https://api.github.com")  
		    .addConverterFactory(GsonConverterFactory.create(gson))  
		    .build();  
		  
		GitHubService service = restAdapter.create(GitHubService.class);
		
5. 使用@PrimaryKey 注释的成员变量，在保存时不能为null，但在执行保存的transaction之前可以是null。

6. 以PrimaryKey为索引，如果要保存的数据中的primaryKey是新的则保存一条新数据，否则更新原有数据

### realm 坑 ###

	http://www.open-open.com/lib/view/open1453185177792.html 为什么我不再使用Realm

1. 必须直接继承自RealmObject。这阻碍我们利用数据模型中的任意类型的继承。所有属性必须用private修饰

2. 不能定义除setters 和 getters之外的实例方法。如果你想重写equals 或者toString`那么你就别想了。这样导致的另外一个后果就是我们只能局限于使用标记接口模式（marker interfaces） (注解也是可以的 )。

3. setters 和 getters方法只是为Realm替换自己实现的代理方法。它不能操作数据，跑出异常，或者打印日志。

4. 必须保证存在一个空的构造函数。如果你想用一个builder 或者工厂方法来作为实例化的唯一途径，那么这种限制就成了一个问题。

5. 数据类型限制。所有的基本数据类型以及它们的封装类型都能支持，包括String, Date, 和byte[]`。但是对于其它类型，为了被持久化，必须继承自RealmObject。Lists可以用RealmList来支持。如果我们想使用枚举而不是int，是没有办法的（使用@IntDef注解）。我们还不能使用集合类型，比如Set和Map。

### Realm多线程中的那些坑 ###
	Realm多线程中的那些坑... http://blog.csdn.net/javine/article/details/51040110
1. RealmObject自带线程保护功能，只能在创建它的线程中访问，在子线程中不能访问。
	
	也就是说，如果你在主线程中new了一个RealmObject对象 user，那么在子线程中是访问不了user对象的。要想在子线程中访问，必须先将user存入Ream中，然后在子线程中query出来。

2. 如果Realm关闭，所有查询得到的RealmObject都不能使用了。

	如果想在子线程中去查询数据，然后在主线程中使用是无法做到的。所以Realm提供的异步查询就很重要了...

3. 如果想在Realm.close()之后继续操作查询得到的对象，只能复制一份数据传出来。

	Realm开发者是为了它的一个特色功能Auto-Update，即自动更新查询到的数据，
	特意让查询得到的数据与数据库中的数据保持了同步，所以Realm一关，外面的数据也用不了。
	而且，这个Auto-update暂时还无法关闭，stackOverFlow上有说以后可能会提供关闭这个功能的方法。

4. 如果直接修改或删除query得到的数据，必须在transaction中完成...

	也就是说，你根本不能把query返回的对象，当成普通对象去赋值或删除，如果想要直接操作...ok，把对象copy一份传出来...

### 初次使用Realm踩到的坑 ###
	初次使用Realm踩到的坑 http://www.jianshu.com/p/92c6337f3129
1. Realm对象只能在创建它的线程中使用

	按照以前的思路, 我在自己的 Application 类中添加了一个静态字段以及一个方法用来全局获取到数据库

		public class MyApp extends Application {
		    private static Realm mRealm;
		
		    @Override
		    public void onCreate() {
		        super.onCreate();
		
		        RealmConfiguration configuration = new RealmConfiguration.Builder(this).build();
		        Realm.setDefaultConfiguration(configuration);
		        mRealm = Realm.getDefaultInstance();
		    }
		
		    public static Realm getRealm() {
		        return mRealm;
		    }
		}
	一旦在不是创建 Application 的线程中使用就会抛出异常:

		Caused by: java.lang.IllegalStateException: Realm access from incorrect thread. Realm objects can only be accessed on the thread they were created.

正确的做法是在需要的时候再使用 Realm.getDefaultInstance() 获取到Realm实例

## 6. SQLBrite 响应式数据库 ##

Square 的 Jake Wharton 大神的，响应式数据库

关注如何在数据变化时更简便的获取到通知。当你不想用ContentProvider，只想简单监听SQLite表增删改的数据变更时可以试试它

## 7. xutils的dbutils 注解反射 ##

xutils框架太泛，包含网络请求、图片加载、view注入等，太泛不精，怕出现问题

优势：支持Module继承

## 8. DBFlow 注解预编译 ##

	https://github.com/Raizlabs/DBFlow

注解 + apt预编译，高性能。

### Module ###

1. 直接 extends BaseModel，不灵活
2. implement Model，麻烦