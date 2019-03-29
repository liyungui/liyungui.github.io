---
title: 面向切面编程AOP
date: 2019-01-14 08:56:53
categories:
  - 编程思想
tags:
  - 编程思想
---

[面向切面编程（AOP，Aspect-oriented programming）](http://www.jianshu.com/p/0fa8073fd144)

- 需要把程序逻辑分解成**『关注点』**（concerns，功能的内聚区域，多处代码中需要的逻辑，但没有一个单独的类来实现）
- **『关注点』**只被实现一次
- 不需要显式的修改就可以向代码中添加可执行的代码块（注入到需要该逻辑的地方）

# 概念 #

- Cross-cutting concerns（横切关注点）: 比如

	- 日志
	- 持久化
	- 性能监控
	- 数据校验
	- 缓存

- Advice（注入代码）: 注入到class文件中的代码。

- Joint point（注入点 / 连接点）: 程序中可能作为代码注入目标的特定的点，例如一个方法调用或者方法入口。

	- 方法。 类型有 before、after 和 around，分别表示在目标方法执行之前、执行后和完全替代目标方法执行的代码。 
	- class。增加字段或者接口。
	
- Pointcut（切入点）: 在何处注入何代码的表达式（给代码注入工具用）。例如，标记了自定义注解@DebguTrace的方法。

- Aspect（切面）: Pointcut 和 Advice 的组合看做切面。例如，一个pointcut和恰当的advice = 一个日志切面。

- Weaving（织入）: 注入代码（advices）到目标位置（joint points）的过程。

下面这张图简要总结了一下上述这些概念。
![](http://upload-images.jianshu.io/upload_images/30689-55846998f4f5b4ce.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

# 工具和库 #

- [AspectJ](https://eclipse.org/aspectj/): 一个 JavaTM 语言的面向切面编程的无缝扩展（适用Android）。

- [Javassist for Android](https://github.com/crimsonwoods/javassist-android): 知名 java 类库 Javassist（字节码操作库） 的 Android 平台移植版。

- [DexMaker](https://code.google.com/p/dexmaker/): Dalvik 虚拟机上，在编译期或者运行时生成代码的 Java API。

- [ASMDEX](http://asm.ow2.org/asmdex-index.html): 一个类似 ASM 的字节码操作库，运行在Android平台，操作Dex字节码。

# 为什么用 AspectJ #

- 功能强大
- 支持**编译期和加载时代码注入**
- 易于使用

# 使用 AspectJ #

[示例：](https://github.com/android10/Android-AOPExample)测量一个方法的性能（执行这个方法需要多长时间）。logcat 输出 @DebugTrace 注解标记的方法性能。[Jake Wharton’s Hugo Library](https://github.com/JakeWharton/hugo) 支持做同样的事情

## 依赖配置 ##

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

## 定义 DebugTrace注解 ##

注解周期声明在 class 文件上，以注解构造函数和方法

	@Retention(RetentionPolicy.CLASS)
	@Target({ ElementType.CONSTRUCTOR, ElementType.METHOD })
	public @interface DebugTrace {}

## Aspect 类 ##

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

## 测试 DebugTrace ##

	@DebugTrace
	  private void testAnnotatedMethod() {
	    try {
	      Thread.sleep(10);
	    } catch (InterruptedException e) {
	      e.printStackTrace();
	    }
	  }

## 输出结果 ##

	Gintonic --> testAnnotatedMethod --> [10ms]