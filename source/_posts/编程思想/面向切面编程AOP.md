---
title: 面向切面编程AOP
date: 2019-01-14 08:56:53
categories:
  - 编程思想
tags:
  - 编程思想
---
# AOP和OOP

**纵向关系 OOP，横向角度 AOP**

举个例子：设计一个日志打印模块。

按 OOP 思想，我们会设计一个打印日志 LogUtils 类，然后在需要打印的地方引用即可。我们一般采用的分类方法都是使用类似生物学分类的方法，以「**继承」**关系为主线，我们称之为**纵向**

设计时只使用 OOP思想可能会带来三个问题：

1. 对象设计的时候一般都是纵向思维，如果这个时候考虑这些不同类对象的共性，不仅会增加设计的难度和复杂性，还会造成类的接口过多而难以维护（共性越多，意味着接口契约越多）。
2. 类是横跨并嵌入众多模块里的，在各个模块里分散得很厉害
3. 需要对现有的对象 动态增加 某种行为或责任时非常困难。

而AOP就可以很好地解决以上的问题。从横向的角度去观察这些对象，无需再去到处调用 LogUtils 了，声明哪些地方需要打印日志，这个地方就是一个切面，AOP 会在适当的时机为你把打印语句插进切面。

如果说 OOP 是把问题划分到单个模块的话，那么 AOP 就是把涉及到众多模块的某一类问题进行统一管理。AOP的目标是把这些功能集中起来，放到一个统一的地方来控制和管理。利用 AOP 思想，这样对业务逻辑的各个部分进行了隔离，从而降低业务逻辑各部分之间的耦合，提高程序的可重用性，提高开发效率。

OOP 与 AOP 之间是一个相互补充和完善的关系。

- 需要把程序逻辑分解成**『关注点』**（concerns，功能的内聚区域，多处代码中需要的逻辑，但没有一个单独的类来实现）
- **『关注点』**只被实现一次
- 不需要显式的修改就可以向代码中添加可执行的代码块（注入到需要该逻辑的地方）

# 应用场景

1. 参数校验和判空
2. 权限控制。比如Android API23+的权限控制
3. 无痕埋点
4. 安全控制。比如全局的登录状态流程控制
5. 日志记录
6. 事件防抖
7. 性能统计
8. 事务处理
9. 异常处理。替代防御性的 try-Catch。
10. 缓存
11. 软件破解
12. 热修复

# 概念 #

- Joint point（注入点/连接点）: 程序中可能作为代码注入目标的特定的点，例如一个方法调用或者方法入口。
	
- Pointcut（切入点）: 在何处注入何代码的表达式（给代码注入工具用）
	- 更精确的JPoint时机和位置
	- 时机：同一个方法，还分为call(调用该方法)和execution(该方法执行)
	- 位置：
		- before 目标方法执行之前
		- after 目标方法执行后
		- around 完全替代目标方法执行的代码。切记要 `joinPoint.proceed()`调用原方法

- Advice（注入代码）: 注入到class文件中的代码。

- Aspect（切面）: Pointcut 和 Advice 的组合看做切面。例如，一个pointcut和恰当的advice = 一个日志切面。

- Weaving（织入）: 注入代码（advices）到目标位置（joint points）的过程。

实例：接管 点击监听的onClick执行时逻辑

```java
@Aspect
public class ClickAspect {
    private static final String TAG = "ClickAspect";
    // 第一个*所在的位置表示的是返回值，*是通配，表示的是任意的返回值，
    // onClick()中的 .. 所在位置是方法参数的位置，.. 表示的是任意类型、任意个数的参数
    @Pointcut("execution(* android.view.View.OnClickListener.onClick(..))")
    public void clickMethod() {}

    @Around("clickMethod()")
    public void onClickMethodAround(ProceedingJoinPoint joinPoint) throws Throwable {
        Object[] args = joinPoint.getArgs();
        View view = null;
        for (Object arg : args) {
            if (arg instanceof View) {
                view = (View) arg;
            }
        }
        //获取View 的 string id
        String resEntryName = null;
        String resName = null;
        if (view != null) {
            // resEntryName: btn_activity_2  resName: com.sososeen09.aop_tech:id/btn_activity_2
            resEntryName = view.getContext().getResources().getResourceEntryName(view.getId());
            resName = view.getContext().getResources().getResourceName(view.getId());
        }
        joinPoint.proceed();
        Log.d(TAG, "after onclick: " + "resEntryName: " + resEntryName + "  resName: " + resName);
    }
}
```

运行项目，点击一个控件（设置了点击事件）之后，可以看到日志输出：

`./com.sososeen09.aop_tech D/ClickAspect: after onclick: resEntryName: btn_activity_3 resName: com.sososeen09.aop_tech:id/btn_activity_3`

```
@Pointcut("execution(* android.view.View.OnClickListener.onClick(..))")
public void clickMethod() {}

@Around("clickMethod()")
``` 

可以这样写，更简洁，不用自定义PointCut
   
`@Around("execution(* android.view.View.OnClickListener.onClick(..))")`

# 工具和库 #

{% asset_img AOP工具.png %}

|方法|优点|缺点|上手关键|
|---|---|---|---|
|APT|可以织入所有类|1. 需要使用 apt 编译器编译；2. 需要手动拼接代理的代码（可以使用 Javapoet 弥补）；3. 生成大量代理类|设计模式和解耦思想的灵活应用|
|AspectJ|功能强大，除了 hook 之外，还可以为目标类添加变量，接口。也有抽象，继承等各种更高级的玩法。|1. 不够轻量级；2. 定义的切点依赖编程语言，无法兼容Lambda语法；3. 无法织入第三方库；4. 会有一些兼容性问题，如：D8、Gradle 4.x等|复杂的语法，但掌握几个简单的，就能实现绝大多数场景|
|Javassist|1. 减少了生成子类的开销；2. 直接操作修改编译后的字节码，直接绕过了java编译器，所以可以做很多突破限制的事情，例如，跨 dex 引用，解决热修复中 CLASS_ISPREVERIFIED 问题。|运行时加入切面逻辑，产生性能开销。|1. 自定义 Gradle 插件；2. 掌握groovy 语言|
|ASM|小巧轻便、性能好，效率比Javassist高|学习成本高|需要熟悉字节码语法，ASM 通过树这种数据结构来表示复杂的字节码结构，并利用 Push 模型来对树进行遍历，在遍历过程中对字节码进行修改。|
|ASMDEX|可以织入所有类|学习成本高|需要对 class 文件比较熟悉，编写过程复杂。|
|DexMaker|同ASMDEX|同ASMDEX|同ASMDEX|
|Cglib|运行期生成子类拦截方法；没有接口也可以织入|1. 不能代理被final字段修饰的方法；2. 需要和 dexmaker 结合使用|--|
|xposed|能hook自己应用进程的方法，能hook其他应用的方法，能hook系统的方法|依赖三方包的支持，兼容性差，手机需要root|--|
|dexposed|只能hook自己应用进程的方法，但无需root|1. 依赖三方包的支持，兼容性差；2. 只能支持 Dalvik 虚拟机|--|
|epic|支持 Dalvik 和 Art 虚拟机|只适合在开发调试中使用，碎片化严重有兼容性问题|--|

# APT

Annotation Processing Tool 注解处理器

一种编译时处理注解的工具(javac的一个工具)。

简单来说就是在编译期，通过注解生成 .java 文件

## 代表框架

DataBinding、Dagger2、ButterKnife、EventBus3、DBFlow、AndroidAnnotation

## 为什么用APT

目前 Android **注解解析框架**主要有**两种**实现方法：

- 一种是**运行期通过反射**去解析当前类，注入相应要运行的方法。
- 另一种是在**编译期****生成类的代理类**，在运行期直接调用代理类的代理方法
	- APT就是这种。
	- 增加了代码量，但是不再需要用反射，也就无损性能

性能问题解决了，又带来新的问题了。我们在处理注解或元数据文件的时候，往往有自动生成源代码的需要。难道我们要手动拼接源代码吗？不不不，这不符合代码的优雅，JavaPoet 这个神器就是来解决这个问题的。


# AspectJ

目前最好、最方便、最火的 AOP 实现方式当属 AspectJ，它是一种几乎和 Java 完全一样的语言，而且完全兼容 Java。

- 功能强大
- 支持**编译期和加载时代码注入**
- 易于使用

编译时，所以无法编辑Android SDK类(比如LayoutInflater和ImageView)。因为这些类都不会打包到apk中，都是在手机系统framework.jar里面。

所以，xml布局中ImageView指定图片，是无法切到`setImageDrawable`方法执行的。最多只能切到自定义和第三方库中对`setImageDrawable`的调用

## AspectJ 框架选型

在 Android 上集成 AspectJ 是比较复杂的。

有很多库帮助我们完成这些工作，可以方便快捷接入 AspectJ。

|库|大小|兼容性|缺点|备注|
|---|---|---|---|---|
|Hugo|131kb|--|不支持AAR或JAR切入|--|
|gradle-android-aspectj-plugin|--|--|无法兼容databinding，不支持AAR或JAR切入|该库已经弃用|
|AspectJx（推荐）|44kb|会和有transform功能的插件冲突，如：retroLambda|在前两者基础上扩展支持AAR, JAR及Kotlin的应用|仅支持annotation的方式，不支持 *.aj 文件的编译|

## 实例

测量@DebugTrace注解标记的方法的性能(执行耗时)并在logcat输出。

[示例源码](https://github.com/android10/Android-AOPExample)

[Jake Wharton’s Hugo Library](https://github.com/JakeWharton/hugo) 支持做同样的事情

### 依赖配置

module 的 `build.gradle`

	import org.aspectj.bridge.IMessage
	import org.aspectj.bridge.MessageHandler
	import org.aspectj.tools.ajc.Main
	
	buildscript {
	  repositories {
	    mavenCentral()
	  }
	  dependencies {
	    classpath 'com.android.tools.build:gradle:2.1.0'
	    classpath 'org.aspectj:aspectjtools:1.8.1'
	  }
	}
	
	apply plugin: 'com.android.library'
	
	repositories {
	  mavenCentral()
	}
	
	dependencies {
	  compile 'org.aspectj:aspectjrt:1.8.1'
	}
	
	android {
	  compileSdkVersion 23
	  buildToolsVersion '23.0.2'
	
	  lintOptions {
	    abortOnError false
	  }
	}
	
	android.libraryVariants.all { variant ->
	  LibraryPlugin plugin = project.plugins.getPlugin(LibraryPlugin)
	  JavaCompile javaCompile = variant.javaCompile
	  javaCompile.doLast {
	    String[] args = ["-showWeaveInfo",
	                     "-1.5",
	                     "-inpath", javaCompile.destinationDir.toString(),
	                     "-aspectpath", javaCompile.classpath.asPath,
	                     "-d", javaCompile.destinationDir.toString(),
	                     "-classpath", javaCompile.classpath.asPath,
	                     "-bootclasspath", plugin.project.android.bootClasspath.join(
	        File.pathSeparator)]
	
	    MessageHandler handler = new MessageHandler(true);
	    new Main().run(args, handler)
	
	    def log = project.logger
	    for (IMessage message : handler.getMessages(null, true)) {
	      switch (message.getKind()) {
	        case IMessage.ABORT:
	        case IMessage.ERROR:
	        case IMessage.FAIL:
	          log.error message.message, message.thrown
	          break;
	        case IMessage.WARNING:
	        case IMessage.INFO:
	          log.info message.message, message.thrown
	          break;
	        case IMessage.DEBUG:
	          log.debug message.message, message.thrown
	          break;
	      }
	    }
	  }
	}

### 定义 DebugTrace注解

注解周期声明在 class 文件上，以注解构造函数和方法

	@Retention(RetentionPolicy.CLASS)
	@Target({ ElementType.CONSTRUCTOR, ElementType.METHOD })
	public @interface DebugTrace {}

### Aspect 类

Aspect 类负责管理注解的处理和代码织入。

	@Aspect
	public class TraceAspect {
	
	  private static final String POINTCUT_METHOD =
	      "execution(@org.android10.gintonic.annotation.DebugTrace * *(..))";
	
	  private static final String POINTCUT_CONSTRUCTOR =
	      "execution(@org.android10.gintonic.annotation.DebugTrace *.new(..))";
	
	  @Pointcut(POINTCUT_METHOD)
	  public void methodAnnotatedWithDebugTrace() {}
	
	  @Pointcut(POINTCUT_CONSTRUCTOR)
	  public void constructorAnnotatedDebugTrace() {}
	
	  @Around("methodAnnotatedWithDebugTrace() || constructorAnnotatedDebugTrace()")
	  public Object weaveJoinPoint(ProceedingJoinPoint joinPoint) throws Throwable {
	    MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
	    String className = methodSignature.getDeclaringType().getSimpleName();
	    String methodName = methodSignature.getName();
	
	    final StopWatch stopWatch = new StopWatch();
	    stopWatch.start();
	    Object result = joinPoint.proceed();
	    stopWatch.stop();
	
	    DebugLog.log(className, buildLogMessage(methodName, stopWatch.getTotalTimeMillis()));
	
	    return result;
	  }
	
	  /**
	   * Create a log message.
	   *
	   * @param methodName A string with the method name.
	   * @param methodDuration Duration of the method in milliseconds.
	   * @return A string representing message.
	   */
	  private static String buildLogMessage(String methodName, long methodDuration) {
	    StringBuilder message = new StringBuilder();
	    message.append("Gintonic --> ");
	    message.append(methodName);
	    message.append(" --> ");
	    message.append("[");
	    message.append(methodDuration);
	    message.append("ms");
	    message.append("]");
	
	    return message.toString();
	  }
	}

- `@Pointcut` **属性值声明的方法**（“org.android10.gintonic.annotation.DebugTrace” 注解的方法和构造函数）**注入@Pointcut注解的方法**

- `@Around` **@Around注解的方法**（“weaveJointPoint(ProceedingJoinPoint joinPoint)”）**替换属性值声明的方法**（@DebugTrace"注解的方法）

- `Object result = joinPoint.proceed();` 执行原来的方法

### 测试 DebugTrace ##

	@DebugTrace
	  private void testAnnotatedMethod() {
	    try {
	      Thread.sleep(10);
	    } catch (InterruptedException e) {
	      e.printStackTrace();
	    }
	  }

### 输出结果 ##

	Gintonic --> testAnnotatedMethod --> [10ms]
	
# AspectJ 语法

{% asset_img JPoint和Pointcut.png %}

{% asset_img Pointcut的Signature总览.png %}

{% asset_img Pointcut的Signature明细.png %}

{% asset_img Advice.png %}

{% asset_img JPoint高级用法.png %}

# Javassist

## 代表框架

热修复框架HotFix 、Savior（InstantRun）	

如何在合适的时机实现在 .class文件被转为 .dex 文件之前去做修改。

在 Gradle Transfrom 这个 api 出来之前，必须自定义一个 Gradle Task，插入到 predex 或者 dex 之前，在这个自定义的 Task 中使用 Javassist 对 class 字节码进行操作。

而 Transform 更为方便，执行时机正好是 class 被打包成dex之前。

# 参考&扩展

- [一文读懂 AOP | 你想要的最全面 AOP 方法探讨	](https://juejin.im/post/5c01533de51d451b80257752#heading-19)
- [AOP 之 AspectJ 全面剖析 in Android](https://www.jianshu.com/p/f90e04bcb326) AspectJ语法
	