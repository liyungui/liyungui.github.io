---
title: Dagger2
date: 2019-08-10 20:25:53
categories:
  - Android
tags:
  - Android
---

# 概述

Dagger2 是一个依赖注入框架

是Dagger的升级版，agger由Square公司开源；Dagger2 由 Google接手维护

是首个使用生成代码实现完整依赖注入的框架，极大减少了使用者的编码负担。

Dagger 得名于树状结构的依赖。能更准确地记住这是个依赖图，实际上是**有向无环图**，DAG（Directed Acyclic Graph）有向无环图，因此取名为 **DAGger**

# 为什么要依赖注入

因为依赖注入是实现控制反转(IOC)的最常用方式。更多关于IOC的信息，参考IOC文章。

# Dagger2 原理

{% asset_img Dagger.png %}

## Inject

依赖提供者，注解依赖实例构造方法

依赖消费者，注解依赖实例对象

## Component

通过Inject，目标类中所依赖的其他类与其他类的构造函数之间有了一种无形的联系。

但是要想使它们之间产生直接的关系，还得需要一个桥梁来把它们之间连接起来。那这个桥梁就是Component了

Component 是一个 **桥梁** ，一个 **容器** ，一个 **注入器** (Injector)

主要工作：把目标类依赖的实例注入到目标类中，来初始化目标类中的依赖

调用Component的 `injectXXX(Object)`方法开始注入。(injectXXX方法名字是官方推荐的命名)

Component工作流程：

- 查找目标类中用Inject注解标注的属性，
- 查找该属性对应的用Inject标注的构造函数
- 初始化该属性的实例
- 把实例赋值给目标类的属性。

因此我们也可以给Component叫另外一个名字

{% asset_img Component.png %}

## Module 和 Provides

**解决第三方类库依赖**

无法把Inject注解加入第三方类库的类中。

把封装第三方类库的代码放入 Module 中。所以 **Module其实是一个简单工厂模式，Module里面的方法基本都是创建类实例的方法** 。

```java
@Module
public class ModuleClass{
	//A是第三方类库中的一个类
	A provideA(){
	   return A();
	}
}   
```

# 配置依赖 

	compile 'com.google.dagger:dagger:2.24'
	annotationProcessor 'com.google.dagger:dagger-compiler:2.24'
	compile 'com.google.dagger:dagger-android:2.24'
	compile 'com.google.dagger:dagger-android-support:2.24' // if you use the support libraries
	annotationProcessor 'com.google.dagger:dagger-android-processor:2.24'

# 简单依赖注入

实例：在MainActivity中创建User对象。

## Module -- 构建依赖（依赖提供者）

```java
@Module
public class UserModule {
    @Provides
    User provideUser() {
        return new User();
    }
}
```

@Module这是一个Module，@Provides这是一个提供依赖的方法
	
## Component -- injector（连接 依赖提供者和依赖消费者）

```java
@Component(modules = UserModule.class)
public interface UserComponent {
	void inject(MainActivity activity);
}
```

	inject方法需要一个真正消耗依赖的类型对象(而不可以写成其父类)作为参数。
	因为dagger2在编译时生成依赖注入的代码，会到inject方法的参数类型中寻找可以注入的对象
	dagger2会自动生成类实现该接口

## 使用依赖注入

```java
public class MainActivity extends AppCompatActivity {
 	@Inject
 	User mUser;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        UserComponent userComponent = DaggerUserComponent.builder().userModule(new UserModule()).build();
        userComponent.inject(this);
        
        TextView viewById = (TextView) findViewById(R.id.textView);
        viewById.setText(mUser.name);
	}
}
```
	
@Inject标识被注入的对象User（注意User不能为private，否则会报错）
	
	Error:(12, 18) 错误: Dagger does not support injection into private fields
	注: Generating a MembersInjector or Factory for com.example.test2.MainActivity. Prefer to run the dagger processor over that class instead.

通过类 `DaggerActivityComponent` 创建component，调用其inject方法完成注入

	DaggerUserComponent 是dagger2自动生成，实现了我们提供的 UserComponent 接口。
	目录在build/generated/sources/apt/下 （可对生成的文件加断点调试，理解整个过程）
	
# Dagger2 调试

Dagger2实现原理：**注解 + 编译时处理**，为了性能考虑，没有使用反射

build后生成的代码目录在 `build/generated/sources/apt/` 下，可对生成的文件加断点调试，理解整个过程

比如 DaggerUserComponent 是dagger2自动生成，实现了我们提供的 UserComponent 接口。

# 构建依赖(依赖提供者)两种方法

## @Inject 类构造方法

```java
public class User {
    @Inject
    public User() {
    }
}
```
	
每个类只能有一个构造方法有@inject注解。否则报错 `Types may only contain one @Inject constructor.`

不够灵活，只能注解一个构造方法。
		
## @Module 和 @Provides

**解决第三方类库类实例问题**

**工厂模式**

```java
@Module
public class UserModule {
    @Provides
    User provideUser() {
        return new User();
    }
}
```

## 总结

两种方法必选其一，编译期才能生成构造User对象的方法。否则会报错（注入依赖失败）

	Error:(7, 10) 错误: com.example.test2.User cannot be provided without an @Inject constructor or from an @Provides- or @Produces-annotated method.
	com.example.test2.MainActivity.user
	[injected field of type: com.example.test2.User user]

@Inject 不够灵活。一个依赖提供者类只能有一个@Inject注解的构造方法，不能提供接口和三方库中类的依赖

@Module非常灵活，能提供接口和三方库中类的依赖

@Module优先级也高于@inject（@Module中找到了依赖就不会到@ Inject中找）

dagger会自动查找并注入依赖类的依赖（如果能找到依赖提供者），比如上面 ShoppingCar依赖的User

# 注入依赖三种方法

## @inject 配合Component接口实现类的inject方法。

inject方法一调用就 **马上生成依赖对象**

	@Inject
	User mUser;//不可私有，否则注入失败
	
	protected void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.activity_main);
		
	    UserComponent userComponent = DaggerUserComponent.builder().userModule(new UserModule()).build();
	    userComponent.inject(this);
	    viewById.setText(mUser.name);
	}

## 调用Component接口实现类的 返回依赖对象的方法

**使用时生成依赖对象**

**科学，推荐使用**

```java
@Component(modules = UserModule.class)
public interface UserComponent {
    void inject(MainActivity activity);//如果User对象不需要直接注入到其他类中(即UserComponent是其他Component的依赖Component)可以不需要inject方法
    User user();//调用该方法返回User对象
}

UserComponent userComponent = DaggerUserComponent.builder().userModule(new UserModule()).build();
viewById.setText(userComponent.user().name);
```

## @inject Lazy泛型

**使用时生成依赖对象**

	@Inject
	Lazy<User> mUser;//不可私有，否则注入失败
	
	protected void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    setContentView(R.layout.activity_main);
		
	    UserComponent userComponent = DaggerUserComponent.builder().userModule(new UserModule()).build();
	    userComponent.inject(this);
	    viewById.setText(mUser.get().name);//通过get方法得到User对象
	}

# 注入依赖的步骤

注入依赖的步骤，其实是一个递归的过程

- 步骤1：查找Module中是否存在创建该类的方法。
- 步骤2：若Module中找到，查看该方法是否存在参数
    - 步骤2.1：若存在参数，则按从**步骤1**开始依次初始化每个参数
    - 步骤2.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
- 步骤3：若Module中未找到，则查找Inject注解的构造函数
- 步骤4：若找到Inject注解的构造函数，看构造函数是否存在参数
    - 步骤4.1：若存在参数，则从**步骤1**开始依次初始化每个参数
    - 步骤4.2：若不存在参数，则直接初始化该类实例，一次依赖注入到此结束
- 步骤5：若找不到Inject注解的构造函数，报错
	    
# @Qualifier 限定符

解决 **依赖迷失** 问题(同一纬度/优先级 的 依赖提供者 依靠类型无法确定依赖唯一性)

即：当 `@Provides` 返回一种类型的方法有多个(两个及以上)，需要@Qualifier来区分。否则报错 。比如：String依赖无法确定唯一性，`java.lang.String is bound multiple times:`

Module类 和 目标类 同时使用 @Qualifier 限定符，解决依赖迷失

@Qualifier 不能用于构造方法。否则报错 `@Qualifier annotations are not allowed on @Inject constructors.`

## @Named
			
```java
@Qualifier
@Documented
@Retention(RUNTIME)
public @interface Named {
    /** The name. */
    String value() default "";
}
```

## 自定义@Qualifier

```java
@Qualifier
@Documented
@Retention(RetentionPolicy.RUNTIME)
public @interface UserRole {
    String value() default "";
}
```

## 使用

```java
@Module
public class UserModule {
    @UserRole("admin")
    @Provides
    User provideAdminUser() {
        return new User("admin");
    }

    @UserRole("teacher")
    @Provides
    User provideTeacherUser() {
        return new User("teacher");
    }
}

目标类
@UserRole("admin")
@Inject
User mAdminUser;

@UserRole("teacher")
@Inject
User mTeacherUser;
```

# Component 划分方式

假如一个app中只有一个Component，那这个Component职责太多过于庞大，导致是很难维护、并且变化率是很高。所以需要划分为粒度小的Component。

划分粒度也不能太小了，定义过多的Component，管理、维护非常困难

合适划分的规则这样的：

- 一个**全局**的Component(可以叫ApplicationComponent),负责管理整个app的全局类实例（全局类实例整个app都要用到的类的实例，这些类基本都是单例的）
- 每个**页面**对应一个Component。比如一个Activity页面定义一个Component，一个Fragment定义一个Component。有些页面之间的依赖的类是一样的，可以公用一个Component。

## 创建单例依赖的方法

1. 在Module中定义创建全局类实例的方法（因为Module中找到了创建实例方法，就不会到Inject维度找了）
2. ApplicationComponent管理Module
3. 保证ApplicationComponent只有一个实例（在app的Application中实例化ApplicationComponent）

# Component 组织方式

按照上面的规则划分为不同的Component，全局类实例也创建了单例模式。问题来了其他的Component想要把全局的类实例注入到目标类中该怎么办呢？

这就涉及到**类实例共享**的问题了。

因为Component有管理创建类实例的能力，因此只要能很好的组织Component之间的关系，问题就好办了。

具体的组织方式分为以下3种：

## 依赖方式

一个Component依赖于一个或多个Component

Component中的 **dependencies** 属性就是依赖方式的具体实现

### 关键

- 高层Component 的 dependencies  属性 **依赖** 低层Component
- 低层Component 提供一个方法 返回依赖实例。(目的：**显式暴露依赖**)
- 使用：
	- 先初始化 低层Component
	- 低层Component 作为参数初 始化高层Component
	- 调用高层Component.inject() 注入 高层对象

### 优缺点

- 高层Component只能使用低层Component显式暴露出来的依赖
	- 低层Component 需要写 抽象方法暴露依赖

### 实例

实例：MainActivity 依赖 User，User 依赖 ShoppingCart

低层

```java
@Module
public class ShoppingCartModule {
    @Provides
    ShoppingCart provideShoppingCart() {
        return new ShoppingCart();
    }
}
```

```java
@Component(modules = ShoppingCartModule.class)
public interface ShoppingCartComponent {
    //void inject(MainActivity mainActivity);//不需要直接注入到目标类中(即ShoppingCartComponent是其他Component的依赖Component)就不需要inject方法。有的话会报错找不到依赖
    ShoppingCart offerShoppingCart();//新增一个方法提供依赖对象。低层 Component 需要一个方法提供依赖对象
}
```

高层

```java
@Module
public class UserModule {
    @Provides
    User provideUser(ShoppingCart shoppingCart) {
        return new User(shoppingCart);
    }
}
```

```java
@Component(modules = UserModule.class, dependencies = ShoppingCartComponent.class)
public interface UserComponent {
    void inject(MainActivity activity);
}
```

使用

```java
public class MainActivity extends AppCompatActivity {
    @Inject
    User mUser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ShoppingCartComponent shoppingCartComponent = DaggerShoppingCartComponent.builder().shoppingCartModule(new ShoppingCartModule()).build();
        UserComponent userComponent = DaggerUserComponent.builder().userModule(new UserModule()).shoppingCartComponent(shoppingCartComponent).build();
        userComponent.inject(this);
        ((TextView) findViewById(R.id.text)).setText(mUser.name + " " + mUser.mShoppingCart.total);
    }
}
```

**Component接口的inject方法** 参数类型必须是真实使用注入依赖的类对象。而且**一个类对象只能对应一个inject方法**。

	比如 UserComponent 的inject(MainActivity activity)，ShoppingCarComponent 的 inject(MainActivity activity) 就会报错，两个inject指向同一个对象
		Error:(7, 10) 错误: com.example.test2.User cannot be provided without an @Inject constructor or from an @Provides- or @Produces-annotated method.
		com.example.test2.MainActivity.user
		[injected field of type: com.example.test2.User user]
	其实是有提供依赖的，真正的原因就是两个inject指向MainActivity activity这同一个对象。
	app\build\generated\source\apt\目录下会生成 MainActivity_MembersInjector.java

**UserComponent必须初始化依赖的shoppingCartComponent和userModule，否则会报错**

	Caused by: java.lang.IllegalStateException: shoppingCartComponent must be set 
		at com.example.testdagger2. DaggerUserComponent$Builder.build(DaggerUserComponent.java:55)

## 包含方式(继承方式)

一个Component包含一个或多个Component的，被包含的Component还可以继续包含其他的Component。

这种方式特别像Activity与Fragment的关系。

**推荐使用，实际使用更加广泛**

**SubComponent** 就是包含方式的具体实现。子Component，可以理解为 **继承或者拓展**(比较好理解)

### 优缺点

- @Subcomponent注解不会在编译后生成Dagger前缀的容器类，而是体现在父@Component的**私有内部类**，并且如何在父@Component中构建@Subcomponent都需要我们自己写(既然是继承关系，完全可以自动生成吧？)
- 父@Component的依赖是完全暴露
	- 不需要像依赖方式一样，在Component中显示声明暴露

### 建造者模式 写法

官方推荐写法

建造者模式套路(不熟悉的可以参照生成的Dagger前缀的容器类)：

- builder()生成Builder对象
- 传入@Module对象
- 调用Builder对象的build()方法生成@Component实例

#### 关键

- 包含者Subcomponent，改造成 **标准的建造者**
	- 定义一个内部接口。(标准的建造者。接口名一般是 Builder；)
		- 用@Subcomponent.Builder注解
		- 接口提供方法构建 Subcomponent
- 被包含者Module 的 subcomponents 属性 把实例共享/暴露给 包含者Subcomponent
	- 目的：定义 **继承关系** 。把父Component的**依赖全部暴露**给Subcomponent 
- 被包含者Component 提供一个方法 返回 包含者的建造者Subcomponent.Builder
	- 目的：定义 **继承关系** 。
	- 通过这个方法父Component可以生成自己的私有内部类Subcomponent
- 使用：
	- 先初始化 被包含者Component
	- 被包含者Component 使用包含者的建造者 构造 包含者Subcomponent
	- 调用包含者Subcomponent.inject() 注入 包含者对象

#### 编译过程

- 父Component 在检测到 子Component.Builder 返回值方法
- 检测子Component类与其内部类的注解
- 如果是@Subcomponent注解，会在父Component的实现类里维护子Component类与其内部类的实现类
- 如果子Component使用了父Component的依赖，则检测父Module有没有注解开放“权限”。

#### 实例

实例：MainActivity 依赖 User，User 包含 ShoppingCart

被包含者

```java
@Module(subcomponents = UserComponent.class)
public class ShoppingCartModule {
    @Provides
    ShoppingCart provideShoppingCart() {
        return new ShoppingCart();
    }
}
```

```java
@Component(modules = ShoppingCartModule.class)
public interface ShoppingCartComponent {
    UserComponent.Builder buildUserComponent();
}
```

包含者

```java
@Module
public class UserModule {
    @Provides
    User provideUser(ShoppingCart shoppingCart) {
        return new User(shoppingCart);
    }
}
```

```java
@Subcomponent(modules = UserModule.class)
public interface UserComponent {
    void inject(MainActivity activity);

    @Subcomponent.Builder
    interface Builder {
        UserComponent build();
    }
}
```

使用

```java
public class MainActivity extends AppCompatActivity {
    @Inject
    User mUser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ShoppingCartComponent shoppingCartComponent = DaggerShoppingCartComponent.builder().shoppingCartModule(new ShoppingCartModule()).build();
        UserComponent userComponent = shoppingCartComponent.buildUserComponent().build();
        userComponent.inject(this);
        ((TextView) findViewById(R.id.text)).setText(mUser.name + " " + mUser.mShoppingCart.total);
    }
}
```

### 抽象工厂方法模式 写法

抽象工厂方法写法 则 相对简单粗暴

- 包含者Subcomponent
- 被包含者Component 提供一个方法 返回 包含者Subcomponent
	- 抽象工厂方法
	- 目的：定义 **继承关系**
- 使用：
	- 先初始化 被包含者Component
	- 被包含者Component 利用抽象工厂方法 构造 包含者Subcomponent
	- 调用包含者Subcomponent.inject() 注入 包含者对象

被包含者

```java
@Module
public class ShoppingCartModule {
    @Provides
    ShoppingCart provideShoppingCart() {
        return new ShoppingCart();
    }
}
```

```java
@Component(modules = ShoppingCartModule.class)
public interface ShoppingCartComponent {
    UserComponent buildUserComponent();
}
```

包含者

```java
@Module
public class UserModule {
    @Provides
    User provideUser(ShoppingCart shoppingCart) {
        return new User(shoppingCart);
    }
}
```

```java
@Subcomponent(modules = UserModule.class)
public interface UserComponent {
    void inject(MainActivity activity);
}
```

使用

```java
public class MainActivity extends AppCompatActivity {
    @Inject
    User mUser;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        ShoppingCartComponent shoppingCartComponent = DaggerShoppingCartComponent.builder().shoppingCartModule(new ShoppingCartModule()).build();
        UserComponent userComponent = shoppingCartComponent.buildUserComponent();
        userComponent.inject(this);
        ((TextView) findViewById(R.id.text)).setText(mUser.name + " " + mUser.mShoppingCart.total);
    }
}
```

### 两种写法 总结

建造者模式 写法

- 官方推荐
- 继承关系的声明更加显式。有两处
	- 父Module 的 subcomponents 属性
	- 父Component 提供一个方法 返回 建造者Subcomponent.Builder 

抽象工厂方法模式 写法

- 简单粗暴
- 继承关系的声明不那么显式。
	- 父Component 提供一个方法 返回 Subcomponent

## 继承方式

官网没有提到该方式，因为该方式不是解决类实例共享的问题，而是为了更好 **管理维护** Component，把一些Component共有的方法抽象到一个父类中，然后子Component继承。

属于 Java中继承的使用

# @Scope

真正用处就在于 **可读性和管理Component**。并**没有实现真正功能**(单例，Activity生命周期绑定这些都靠Component组织方式来实现)

- 可读性提高。
	- 如用 `@Singleton` 标注全局类，立马就能明白这类是全局单例类。
- 更好的管理Component与Module之间的匹配关系
	- 编译器会检查 Component管理的Modules，若发现两者标注的Scope注解不一样，就会报错。
- 更好的管理Component间的组织方式
	- 有必要用自定义的不同Scope注解标注Component，通过Scope命名更好的体现出Component之间的组织方式。

自定义Scope注解最好使用上，虽然不使用也是可以让项目运行起来的，但是加上好处多

# 使用Dagger2的好处

最后，可以总结一下 使用Dagger2的好处

## 增加开发效率、省去重复的简单体力劳动

## 更好的管理类实例

ApplicationComponent管理整个app的全局类实例，生命周期与app的生命周期一样

每个页面对应自己的Component，页面Component管理着自己页面所依赖的所有类实例

因为Component，Module，整个app的类实例结构变的很清晰。

## 解耦

通过工厂模式Module创建类实例，这样即使类的构造函数发生变化，只需要修改Module即可

解耦还有个好处，就是**方便测试**，若需要替换为网络测试类，只需要修改相应的Module即可

# Spring IoC 和 Dagger2

## Spring IoC

实现原理：**注解 + 反射**，涉及动态生成类

用起来**非常好上手**

提供依赖的，用@Component注解，需要依赖的地方 用@Autowired注解，配置文件加上component-scan就差不多了。 

因为接口可能有多个实现，也有@qualifier提供过滤 

## Dagger2

实现原理：**注解 + 编译时处理**，为了性能考虑，没有使用反射

**不好上手**
 
提供依赖的类用@Module注解 能提供的依赖用@Provide注解,需要依赖的地方 用@Inject注解， 
最终要靠手动调用@Compoent的inject方法完成依赖的注入。 
 
# 参考&扩展

- [github](https://github.com/google/dagger)
- [使用dagger2进行依赖注入](http://www.tuicool.com/articles/viQz2uF)
- [Android Dagger2 从零单排(四) Dependencies与SubComponent](https://www.jianshu.com/p/b989e2cb88f6)
- [dagger2系列 - 基础框架篇](https://www.jianshu.com/p/cd2c1c9f68d4) - 基础框架篇
- [dagger2系列 - 重点概念讲解、融合篇](https://www.jianshu.com/p/1d42d2e6f4a5) - 细节完善
- [dagger2系列 - 终结篇](https://www.jianshu.com/p/65737ac39c44) - 实践总结
- [Dagger2 学习笔记](http://blog.csdn.net/wangkai0681080/article/details/50868355) - spring ioc 和 Dagger2 使用对比
