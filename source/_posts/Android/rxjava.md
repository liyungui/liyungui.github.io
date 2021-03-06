---
title: RxJava
date: 2018-04-26 14:12:33
categories:
  - Android
tags: RxJava
---

# RxJava是什么 #

**异步**

**响应式编程**

[GitHub主页](https://github.com/ReactiveX/RxJava)上的自我介绍是 "a library for composing asynchronous and event-based programs using observable sequences for the Java VM"（一个在 Java VM 上使用可观测的序列来组成异步的、基于事件的程序的库）

# RxJava 好在哪 #

一个词：**逻辑简洁**。不是代码简洁(代码量少)

比 `AsyncTask` 和 `Handler` 都更加简洁

链式调用，没有任何嵌套。把任何复杂逻辑都能穿成一条线的简洁

# 引入依赖 #

	compile "io.reactivex:rxjava:1.3.8"
	compile "io.reactivex:rxandroid:1.0.1"

# 响应式编程

响应式编程，用一个字来概括就是**流(Stream)**。

Stream 就是一个按时间排序的 **Events** 序列,它可以放射三种不同的 Events

- (某种类型的)**Value**
- Error 或者 一个 ” Completed” Signal

分别为 Value、Error、”Completed”定义事件处理函数，我们将会异步地捕获这些 Events。

基于观察者模式，事件流将从上往下，从订阅源传递到观察者。

# 原理简析 #

## 观察者模式--四个基本概念 ##

**生产消费者模型** 就是一个典型的观察者模式

### 被观察者/可观察者(`Observable`) ###

`View` 是**被观察者/可观察者**(`Observable`)

**产生事件**：决定什么时候触发事件以及触发怎样的事件

### 观察者(`Observer`) ###

`OnClickListener` 是**观察者**(`Observer`)

**消费事件**：决定事件触发的时候将有怎样的行为

### 订阅(`Subscribe`) ###

二者通过 `setOnClickListener()` 方法达成**注册**(Register)或者称为**订阅**(`Subscribe`)关系，从而 Observable 可以在需要的时候发出事件来通知 Observer。

### 事件 ###

订阅 `onClick() 事件`

## RxJava--扩展的观察者模式 ##

RxJava 作为一个工具库，使用的就是**通用形式的观察者模式**

与传统观察者模式不同，RxJava 的事件回调方法除了普通事件 `onNext()` (相当于 `onClick() / onEvent()`)之外，还定义了两个特殊的事件：`onCompleted()` 和 `onError()`。

{% asset_img rxjava.jpg %}

### onCompleted() ###

事件队列完结。

RxJava 不仅把每个事件单独处理，还会把它们看做一个队列。

RxJava 规定，当不会再有新的事件发出时，需要触发 onCompleted() 方法作为标志。

### onError() ###

事件队列异常。

在事件处理过程中出异常时，onError() 会被触发，同时队列自动终止，不允许再有事件发出。

**所有错误(包括 `Subscriber.onNext` 中的错误)都会回调 `Subscriber.onError()`**

在一个正确运行的事件序列中, onCompleted() 和 onError() 有且只有一个，并且是事件序列中的最后一个。

需要注意的是，onCompleted() 和 onError() 二者也是互斥的，即在队列中调用了其中一个，就不应该再调用另一个。

#### 错误处理	

	private void rxjava(Person person) {
        Observable.just(person)
                .map(new Func1<Person, String>() {
                    @Override
                    public String call(Person person) {
                        return person.name;//NPE会回调onError
                    }
                })
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread())
                .subscribe(new Subscriber<String>() {
                    @Override
                    public void onCompleted() {

                    }

                    @Override
                    public void onError(Throwable e) {
                        Log.e("lyg", "onError", e);
                    }

                    @Override
                    public void onNext(String s) {
                        Toast.makeText(MainActivity.this, s.concat(" haha"), Toast.LENGTH_SHORT).show();//NPE会回调onError
                    }
                });
    }
    
    rxjava(null);//调用
    
    错误日志
    	E/lyg: onError
         java.lang.NullPointerException: Attempt to read from field 'java.lang.String com.example.test.MainActivity$Person.name' on a null object reference
             at com.example.test.MainActivity$3.call(MainActivity.java:47)
             ......
             Caused by: rx.exceptions.OnErrorThrowable$OnNextValue: OnError while emitting onNext value: null
             at rx.internal.operators.OnSubscribeMap$MapSubscriber.onNext(OnSubscribeMap.java:73)

		
	如果将map 改为 return null; 即map中不触发NPE，让onNext触发NPE，也会回调onError
		E/lyg: onError
         java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.String java.lang.String.concat(java.lang.String)' on a null object reference
             at com.example.test.MainActivity$2.onNext(MainActivity.java:63)

# 造轮子-框架基本实现 #
框架内部实现有点复杂，代码逻辑有点绕。

既然用拆轮子的方式来分析源码比较难啃，不如换种方式，以**造轮子**的方式来分析

注意：以下是 核心代码，将与性能、兼容性、扩展性有关的代码剔除了。

## Observer ##

### interface `Observer<T>` ###

	public interface Observer<T>{
		void onNext(T t);
		void onCompleted();
	    void onError(Throwable e);
	}

`Observer` 总是会先被转换成一个 `Subscriber` 再使用

### abstract class `Subscriber<T>` ###

	public abstract class Subscriber<T> implements Observer<T>, Subscription{
		public void onStart() {
        	// do nothing by default
    	}
		public final void unsubscribe() {
	        subscriptions.unsubscribe();
	    }
	}
	public interface Subscription {
		void unsubscribe();
		boolean isUnsubscribed();
	}

#### onStart() ####

- subscribe()后立即执行(还未发送事件)，可以用于做一些准备工作
- 总是在 subscribe() 所发生的线程被调用，而不能指定线程
- 要在指定的线程来做准备工作，可以使用 `Observable.doOnSubscribe()`。 原理参考 `线程控制 Scheduler`部分

#### unsubscribe() ####

- 用于取消订阅
- 调用这个方法前，可以先使用 `isUnsubscribed()` 判断一下状态
- **很重要**。 解除 `Observable` 对 `Subscriber` 的引用关系，避免内存泄露

## Observable ##

### class `Observable<T>`

一个大而杂的类，拥有很多工厂方法和各式各样的操作符

每个Observable里面有一个**OnSubscribe**对象，OnSubscribe只有一个方法（void call(Subscriber<? super T> subscriber);），用来**产生数据流**，这是典型的**命令模式**。

`OnSubscribe.call(subscriber)`方法 命名有意思：

当 `Observable` 被订阅`subscribe(subscriber)`的时候，该方法会被调用（调用时传入subscriber）

```java
public class Observable<T> {
    final OnSubscribe<T> onSubscribe;

    private Observable(OnSubscribe<T> onSubscribe) {
        this.onSubscribe = onSubscribe;
    }

    public static <T> Observable<T> create(OnSubscribe<T> onSubscribe) {
        return new Observable<T>(onSubscribe);
    }

    public Subscription subscribe(Subscriber<? super T> subscriber) {
        subscriber.onStart();
        onSubscribe.call(subscriber);
        return subscriber; //将传入的 Subscriber 作为 Subscription 返回。是为了方便 unsubscribe().
    }

    public interface OnSubscribe<T> {
        void call(Subscriber<? super T> subscriber);
    }
}
```

#### 订阅 observable.subscribe(observer)

subscribe() 这个方法有点怪：它看起来是 `observalbe` 订阅了 `observer / subscriber`，看起来就像 『杂志订阅了读者』 一样颠倒了对象关系

这是为了 流式 API 的设计

将传入的 Subscriber 作为 Subscription 返回。这是为了方便 unsubscribe().

## 实践

```java
Observable.create(new Observable.OnSubscribe<String>() {
    @Override
    public void call(Subscriber<? super String> subscriber) {
        subscriber.onNext("Hello");
        subscriber.onNext("Hi");
        subscriber.onNext("Aloha");
        subscriber.onCompleted();
    }
})
.subscribe(new Subscriber<String>() {
    @Override
    public void onCompleted() {

    }
    @Override
    public void onError(Throwable t) {

    }
    @Override
    public void onNext(String var1) {
        System.out.println(var1);
    }
});
```

{% asset_img subscriber.jpg %}

# 造轮子-操作符

RxJava之所以强大好用，与其拥有丰富灵活的操作符是分不开的。

那么我们就试着为这个框架添加一个最常用的操作符：map()

map()的实现是lift()

RxJava操作符的实现，每调用一次操作符，就相当于在上层数据源和下层观察者之间桥接了一个新的Observable

桥接的Observable内部会实例化有新的OnSuscribe和Subscriber。新OnSuscribe负责接受目标Subscriber传来的订阅请求，并调用原Observable.OnSubscribe的subscribe方法。原Observable.OnSubscribe将Event往下发送给桥接Observable.Subscriber，桥接Observable.Subscriber将Event做相应处理后转发给目标Subscriber

**实质：对事件序列的处理和再发送**

**有点像一种代理机制，通过事件拦截和处理实现事件序列的变换。** 

订阅：新Observable.OnSubscribe调用原始OnSubscribe

发送事件： 新Observable.Subscriber 接收原始的 Observable 发出的事件，并在处理后发送给 Subscriber

{% asset_img lift.jpg %}

## lift()

```java
public <R> Observable<R> lift(Operator<? extends R, ? super T> operator) {
    return Observable.create(new OnSubscribe<R>() {
        @Override
        public void call(Subscriber subscriber) {
            Subscriber newSubscriber = operator.call(subscriber);
            newSubscriber.onStart();
            onSubscribe.call(newSubscriber);//原始 Observable 中的原始 OnSubscribe
        }
    });
}
```

- 生成一个新的 Observable 并返回。 

- 一个新的 Observable 意味着着 一个新的 OnSubscribe 和一个新的 Observer

- 新 Observable subscribe() 时，触发 新 onSubscribe.call(subscriber)
	- 在这个 call() 方法里
		- 新 OnSubscribe 利用 operator.call(subscriber) 生成了一个新的 Subscriber
		- Operator 就是在这里，通过自己的 call() 方法将新 Subscriber 和原始 Subscriber 进行关联，并插入自己的『变换』代码以实现变换
		- 然后利用这个新 Subscriber 向原始 Observable 进行订阅。 onSubscribe.call(newSubscriber)

## 实践

举一个具体的 Operator 的实现。下面这是一个将事件中的 Integer 对象转换成 String 的例子

	observable.lift(new Observable.Operator<String, Integer>() {
	    @Override
	    public Subscriber<? super Integer> call(final Subscriber<? super String> subscriber) {
	        // 将事件序列中的 Integer 对象转换为 String 对象
	        return new Subscriber<Integer>() {
	            @Override
	            public void onNext(Integer integer) {
	                subscriber.onNext("" + integer);
	            }
	        };
	    }
	});

RxJava不建议开发者自定义 Operator 来直接使用 lift()，而是建议尽量使用已有的 lift() 包装方法（如 map() flatMap() 等）进行组合来实现需求，因为直接使用 lift() 非常容易发生一些难以发现的错误

# 造轮子-线程控制

RxJava 的默认规则中，遵循的是**线程不变原则**。即不指定线程的情况下，事件的发出和消费都是在同一个线程的

所以，以上实现的只是一个同步的观察者模式

**观察者模式本身的目的就是『后台处理，前台回调』的异步机制**

而要实现异步，则需要用到 RxJava 的另一个概念： **Scheduler** 

## 自定义Scheduler

先来自定义一个简单的Scheduler和Worker。

线程切换的关键是 Worker.schedule()，因为它会把传过来的任务放入线程池(根据实现获取不同线程)执行

```java
public class Scheduler {
    final Executor executor;
    public Scheduler(Executor executor) {
        this.executor = executor;
    }
    
    //为了达到高仿效果，我们也提供相应的工厂方法。
    private static final Scheduler ioScheduler = new Scheduler(Executors.newSingleThreadExecutor());
    public static Scheduler io() {
        return ioScheduler;
    }
    
    public Worker createWorker() {
        return new Worker(executor);
    }
    
    public static class Worker {
        final Executor executor;
        public Worker(Executor executor) {
            this.executor = executor;
        }
      	// 这里接受的是Runnable而不是Action0，
      	// 其实这没什么关系，主要是懒得自定义函数式接口了。
        public void schedule(Runnable runnable) {
            executor.execute(runnable);
        }
    }
}
```

## 实现subscribeOn

subscribeOn是作用于上层OnSubscribe的，可以让OnSubscribe的call方法在新线程中执行。

```java
public Observable<T> subscribeOn(Scheduler scheduler) {
    return Observable.create(new OnSubscribe<T>() {
        @Override
        public void call(Subscriber<? super T> subscriber) {
            subscriber.onStart();
            // 将事件的生产切换到新的线程。
            scheduler.createWorker().schedule(new Runnable() {
                @Override
                public void run() {
                    Observable.this.onSubscribe.call(subscriber);
                }
            });
        }
    });
}
```

## 实现observeOn

subscribeOn是作用于下层Subscriber的，可以让下层Subscriber的事件处理方法在新线程中执行。

```java
public Observable<T> observeOn(Scheduler scheduler) {
    return Observable.create(new OnSubscribe<T>() {
        @Override
        public void call(Subscriber<? super T> subscriber) {
            subscriber.onStart();
            Scheduler.Worker worker = scheduler.createWorker();
            Observable.this.onSubscribe.call(new Subscriber<T>() {
                @Override
                public void onCompleted() {
                    worker.schedule(new Runnable() {
                        @Override
                        public void run() {
                            subscriber.onCompleted();
                        }
                    });
                }
                @Override
                public void onError(Throwable t) {
                    worker.schedule(new Runnable() {
                        @Override
                        public void run() {
                            subscriber.onError(t);
                        }
                    });
                }
                @Override
                public void onNext(T var1) {
                    worker.schedule(new Runnable() {
                        @Override
                        public void run() {
                            subscriber.onNext(var1);
                        }
                    });
                }
            });
        }
    });
}
```

## 在Android中切换线程

切换到Android主线程

```java
private AndroidSchedulers() {
	...
	//Scheduler的具体实现类：LooperScheduler
	mainThreadScheduler = new LooperScheduler(Looper.getMainLooper());
	...
}
/** A {@link Scheduler} which executes actions on the Android UI thread. */
public static Scheduler mainThread() {
    return getInstance().mainThreadScheduler;
}
```
LooperScheduler的代码很清晰，内部持有一个Handler，用于线程的切换。在Worker的schedule(Action0 action,...)方法中，将action通过Handler切换到所绑定的线程中执行。

# 内置Scheduler

- `Schedulers.immediate()`:在当前线程立即执行任务，相当于不指定线程。这是默认的 Scheduler。如果当前线程有任务在执行，则会将其暂停，等插入进来的任务执行完之后，再将未完成的任务接着执行
- Schedulers.trampoline()：RxJava2废弃了RxJava1中的Schedulers.immediate( )，作为替代者
- `Schedulers.newThread()`: 总是启用新线程，并在新线程执行操作。
- `Schedulers.io()`: I/O 密集操作（读写文件、读写数据库、网络信息交互等）所使用的 Scheduler。行为模式和 newThread() 差不多，区别在于 io() 的内部实现是是用一个**无数量上限的线程池**，可以复用空闲的线程，因此多数情况下 io() 比 newThread() 更有效率。不要把计算工作放在 io() 中，可以避免创建不必要的线程。每个线程设置了一个**60s的保活**时间防止被结束（60s内做频繁操作时，io调度器线程池不起作用）
- `Schedulers.computation()`: 计算所使用的 Scheduler。这个计算指的是 CPU 密集型计算，即不会被 I/O 等操作限制性能的操作，例如图形的计算。这个 Scheduler 使用的**固定的线程池**，大小为 CPU 核数。不要把 I/O 操作放在 computation() 中，否则 I/O 操作的等待时间会浪费 CPU。
- Schedulers.single()：**线程单例**，所有的任务都在这一个线程中执行，当此线程中有任务执行时，其他任务将会按照先进先出的顺序依次执行。
- Schedulers.from(@NonNull Executor executor)：指定一个线程调度器，由此调度器来控制任务的执行策略。
- `AndroidSchedulers.mainThread()`: 在 Android 主线程运行。Android专用的

# 线程控制API

`subscribeOn()`  指定被观察者`Observable`的线程/事件产生的线程

`observeOn()`  指定观察者`Subscriber`的线程/事件消费的线程

	Observable.just(1, 2, 3, 4)
	    .subscribeOn(Schedulers.io()) // 指定 subscribe() 发生在 IO 线程
	    .observeOn(AndroidSchedulers.mainThread()) // 指定 Subscriber 的回调发生在主线程
	    .subscribe(new Action1<Integer>() {
	        @Override
	        public void call(Integer number) {
	            Log.d(tag, "number:" + number);
	        }
	    });

## observeOn() delayError的坑

`observeOn(Scheduler scheduler, boolean delayError)` delayError默认为false，onNext未消费时，直接丢弃，发射OnEror事件，导致一些偶发bug
	
实例：为了更好的用户体验，首先展示缓存数据，加载网络数据成功，展示网络数据

	Observable<List<Feed>> fromNetwork = ...
	Observable<List<Feed>> fromCache = ...
	
	Observable<List<Feed>> observable = Observable.concat(fromCache, fromNetwork)
		.subscribeOn(Schedulers.io())       
		.observeOn(AndroidSchedulers.mainThread());
		.subscribe(...);
		
	bug：页面有时候会显示空白，即直接执行了OnEror

## 原理

`subscribeOn()` 和 `observeOn()` 的内部实现，是 `lift()`

具体看图（不同颜色的箭头表示不同的线程）：

{% asset_img subscribeOn.jpg %}

{% asset_img observeOn.jpg %}

subscribeOn() 和 observeOn() 都做了线程切换的工作（图中的 "schedule..." 部位）。

不同的是:

- subscribeOn() 的线程切换发生在 OnSubscribe 中
	- 即在它通知上一级 OnSubscribe 时，事件还没有开始发送，因此 subscribeOn() 的线程控制可以从事件发出的开端就造成影响；
- observeOn() 的线程切换则发生在它内建的 Subscriber 中
	- 即发生在它即将给下一级 Subscriber 发送事件时，因此 observeOn() 控制的是它后面的线程

## 多个 subscribeOn() 和 observeOn() 混合使用，线程调度

{% asset_img multi_schedule.jpg %}

- 图中共有 5 处含有对事件的操作。
- ①和②两处受第一个 subscribeOn() 影响，运行在红色线程；
- ③和④处受第一个 observeOn() 的影响，运行在绿色线程；
- ⑤处受第二个 onserveOn() 影响，运行在紫色线程；
- 第二个 subscribeOn() ，由于在通知过程中线程就被第一个 subscribeOn() 截断，因此对整个流程并没有任何影响。**当使用多个 subscribeOn() 的时候，只有第一个 subscribeOn() 起作用**。

## 延伸：doOnSubscribe()

**超过一个的 subscribeOn() 对事件处理的流程没有影响，但在流程之前却是可以利用的**

`Observable.doOnSubscribe()` 和 `Subscriber.onStart()` 同样是在 subscribe() 调用后而且在事件发送前执行，但区别在于它**可以指定线程**。

- 默认情况下， doOnSubscribe() 执行在 subscribe() 发生的线程；
- 如果在 doOnSubscribe() 之后有 subscribeOn() 的话，它将执行在离它最近的 subscribeOn() 所指定的线程

		Observable.create(onSubscribe)
		    .subscribeOn(Schedulers.io())
		    .doOnSubscribe(new Action0() {
		        @Override
		        public void call() {
		            progressBar.setVisibility(View.VISIBLE); // 需要在主线程执行
		        }
		    })
		    .subscribeOn(AndroidSchedulers.mainThread()) // 指定主线程
		    .observeOn(AndroidSchedulers.mainThread())
		    .subscribe(subscriber);

# 创建

## API

### `create()` ###

- 最基本的创造Observable的方法

		Observable observable = Observable.create(new Observable.OnSubscribe<String>() {
		    @Override
		    public void call(Subscriber<? super String> subscriber) {
		        subscriber.onNext("Hello");
		        subscriber.onNext("Hi");
		        subscriber.onNext("Aloha");
		        subscriber.onCompleted();
		    }
		});


### `just(T...)` ###

- 将传入的参数依次发送出来

		Observable observable = Observable.just("Hello", "Hi", "Aloha");

示例代码：try-catch代码块，子线程执行网络耗时操作，如果出现异常将异常抛出到主线程

	Observable
        .just(true)
        .map(new Func1<Boolean, Exception>() {
            @Override
            public Exception call(Boolean aBoolean) {
                try {
                    Log.d("lyg", "call on Thread " + Thread.currentThread().getName());
                    getConnection().publish(subject, data);
                    throw new Exception("test");
                } catch (Exception e) {
                    return e;
                }
            }
        })
        .subscribeOn(Schedulers.io())
        .observeOn(AndroidSchedulers.mainThread())
        .doOnNext(new Action1<Exception>() {
            @Override
            public void call(Exception e) {
                Log.d("lyg", " Exception on Thread " + Thread.currentThread().getName());
                if (e != null) {
                    callBack.onError(e);
                }
            }
        })
        .subscribe();

	输出
		
		07-20 13:40:32.151 5952-6631/com.zy.course.dev D/lyg: call on Thread RxCachedThreadScheduler-5
		07-20 13:40:32.389 5952-5952/com.zy.course.dev D/lyg:  Exception on Thread main

### `from(T[]) / from(Iterable<? extends T>)` ###

- 将传入的数组或 Iterable 拆分成具体对象后，依次发送出来。 

		tring[] words = {"Hello", "Hi", "Aloha"};
		Observable observable = Observable.from(words); 


### empty()/never() ###

返回一个不向Observer发送任何条目而立即调用onCompleted()方法的Observable. 因此该方法不会调用onNext()和onError()

	Observable
        .empty()
        .observeOn(AndroidSchedulers.mainThread())
        .doOnCompleted(new Action0() {
            @Override
            public void call() {
                Log.e("Observer.empty()", "doOnCompleted");
            }
        })
        .subscribe();

### error(Throwable exception)

返回一个不向Observer发送任何条目而立即调用onError()方法的Observable.

### never() ###

返回一个不向Observer发送任何事件的Observable。一般仅用来测试

### timer(long delay, TimeUnit unit)

定时触发一次任务

### interval(long initialDelay, long period, TimeUnit unit) ###

轮询循环

默认使用 Schedulers.computation

	interval(initialDelay, period, unit, Schedulers.computation());

实例：10秒一次心跳请求

	mSubscription = Observable.interval(0, 10, TimeUnit.SECONDS)
        .observeOn(Schedulers.io())
        .doOnNext(new Action1<Long>() {
            @Override
            public void call(Long aLong) {
				//网络请求
                NetService.getInstance().getBusinessService().liveHeartBeat(mClazzPlanId)
                        .subscribeOn(Schedulers.io())
                        .observeOn(AndroidSchedulers.mainThread())
                        .subscribe(new SszSubscriber<LiveHeartBeatResultBean>(mCommandReceiver) {
                            @Override
                            protected void onSuccess(@NonNull LiveHeartBeatResultBean bean) {
                                ...
                            }
                        });
            }
        })
        .subscribe(new Observer<Long>() {

            @Override
            public void onCompleted() {
            }

            @Override
            public void onError(Throwable e) {
            }

            @Override
            public void onNext(Long aLong) {
            }
        });

	mSubscription.unsubscribe();//取消轮询

### `defer(Func0<Observable<T>> observableFactory)`

**延迟：**在观察者订阅之前不创建这个Observable，为每一个观察者创建一个新的Observable(factory function决定如何创建)

特别适用的场景就是需要观察从头消息

### repeat(final long count)

创建一个重复发出特定的数据项或序列的Observable

### range(int start, int count)

创建一个发出指定范围的整数序列的Observable

# 变换 #

**将事件序列中的对象或整个序列，转换成不同的事件或事件序列**

## API ##

```java
public final <R> Observable<R> map(Func1<? super T, ? extends R> func) {}
public final <R> Observable<R> flatMap(Func1<? super T, ? extends Observable<? extends R>> func) {}
```
###  map() ###

- **同步**
- 闭包函数返回的是 结果集
- 只能**一对一**的转换
	- map返回的是结果集，不能直接使用from/just再次进行事件分发。只能for遍历。
		- RxJava 目的之一就是 剔除嵌套结构
	- 执行流程：原Observable发射数据，映射，观察者onNext()

### flatMap() ###

- **异步**
- 闭包函数返回的是 结果集的**Observable**
- 可以一对多和多对多的转换
	- flatMap返回的是结果集Observable，可以直接使用from/just再次进行事件分发。
	- 执行流程：将所有发射数据映射汇总到新Observable，新Observable再组织发射(一般利用from/just进行分发，一一执行观察者的onNext()）

**flatMap() 的原理：**

1. 使用传入的事件对象创建一个 Observable 对象；
2. 并不发送这个 Observable, 而是将它激活，于是它开始发送事件；
3. 每一个创建出来的 Observable 发送的事件，都被汇入同一个 Observable ，而这个 Observable 负责将这些事件统一交给 Subscriber 的回调方法。

把事件拆成了两级，通过一组新创建的 Observable 将初始的对象『铺平』之后通过统一路径分发了下去。

### map和flatMap使用场景

- 将一个类型对象**同步**处理成另一个类型，推荐用map，否则的话就用flatMap。
- 需要在处理中加入容错的机制，推荐用flatMap。
	
	```
	flatMap的闭包返回值是一个Observable，
	所以我们可以在这个闭包的call中通过Observable.create的方式来创建Observable，
	而create方法是可以控制数据流下端的Subscriber的，
	即可以调用onNext/onCompete/onError方法。
	如果出现异常，我们直接调用subscribe.onError即可
	```

**实例：**将一个File[] jsonFile中每个File转换成String

```java
Observable.from(jsonFile)
	.map(new Func1<File, String>() {
	    @Override public String call(File file) {
	        try {
	            return new Gson().toJson(new FileReader(file), Object.class);
	        } catch (FileNotFoundException e) {
	            // get Exception. What to do ?
	        }
	        return null; // Not good :(
	    }
	});
	
Observable.from(jsonFile)
	.flatMap(new Func1<File, Observable<String>>() {
	    @Override public Observable<String> call(final File file) {
	        return Observable.create(new Observable.OnSubscribe<String>() {
	            @Override public void call(Subscriber<? super String> subscriber) {
	                try {
	                    String json = new Gson().toJson(new FileReader(file), Object.class);
	                    subscriber.onNext(json);
	                    subscriber.onCompleted();
	                } catch (FileNotFoundException e) {
	                    subscriber.onError(e);
	                }
	            }
	        });
	    }
	});
```
### map和flatMap实例

**实例1：**执行流程的不同

	Observable.just("a", "b", "c")
        //使用map进行转换，参数1：转换前的类型，参数2：转换后的类型
        .map(new Func1<String, String>() {
            @Override
            public String call(String i) {
                String name = i;
                Log.i("tag","map--1----"+i);
                return name;
            }
        })
        .subscribe(new Action1<String>() {
            @Override
            public void call(String s) {
                Log.i("tag","map--2----"+s);
               tv.setText(s);
            }
        });
    logcat信息
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--1----a
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--2----a
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--1----b
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--2----b
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--1----c
    11-23 10:24:31.350 12902-12902/com.example.seele.retrofit I/tag: map--2----c

	--------------------------------------------------------------------------------

 	Observable.just("a", "b", "c")
        .flatMap(new Func1<String, Observable<String>>() {
            @Override
            public Observable<String> call(String s) {
                Log.i("tag", "map--1----" + s);
                return Observable.just(s + "!!!");
            }
        })
        .subscribeOn(Schedulers.newThread())
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe(new Action1<String>() {
            @Override
            public void call(String s) {
                Log.i("tag", "map--2----" + s);
                tv.setText(s);
            }
        });
	logcat信息：
	11-23 10:53:51.320 14442-14527/? I/tag: map--1----a
	11-23 10:53:51.320 14442-14527/? I/tag: map--1----b
	11-23 10:53:51.320 14442-14527/? I/tag: map--1----c
	11-23 10:53:51.340 14442-14442/? I/tag: map--2----a!!!
	11-23 10:53:51.340 14442-14442/? I/tag: map--2----b!!!
	11-23 10:53:51.340 14442-14442/? I/tag: map--2----c!!!

**实例2：**打印出一组学生的名字。每个学生只有一个名字

	Student[] students = ...;
	Observable.from(students)
	    .map(new Func1<Student, String>() {
	        @Override
	        public String call(Student student) {
	            return student.getName();
	        }
	    })
	    .subscribe(new Subscriber<String>() {
		    @Override
		    public void onNext(String name) {
		        Log.d(tag, name);
		    }
		    ...
		});

`map()` 方法将参数中的 `Student` 对象转换成一个 `String` 对象后返回，而在经过 map() 方法后，事件的参数类型也由 Student 转为了 String

**实例3：**打印出一组学生所修的所有课程的名称。每个学生有多个课程，把一个 Student 转化成多个 Course

	Student[] students = ...;
	Observable.from(students)
        .map(new Func1<Student, List<Course>>() {
            @Override
            public List<Course> call(Student student) {
                //返回coursesList
                return student.getCoursesList();
            }
        })
        .subscribe(new Action1<List<Course>>() {
            @Override
            public void call(List<Course> courses) {
                //遍历courses，输出cuouses的name
                for (int i = 0; i < courses.size(); i++) {
                    Log.i(TAG, courses.get(i).getName());
                }
            }
        })
	
	--------------------------------------------------------------------------------

	Observable.from(students)
	    .flatMap(new Func1<Student, Observable<Course>>() {
	        @Override
	        public Observable<Course> call(Student student) {
	            return Observable.from(student.getCourses());
	        }
	    })
	    .subscribe(new Subscriber<Course>() {
		    @Override
		    public void onNext(Course course) {
		        Log.d(tag, course.getName());
		    }
		    ...
		});

**实例4：** 合并两个网络请求。账号密码登录返回token，再用token请求返回user对象

	//登录，获取token
	@GET("/login")
	public Observable<String> login(   
	    @Query("username") String username,
	    @Query("password") String password);
	//根据token获取用户信息
	@GET("/user")
	public Observable<User> getUser(
	    @Query("token") String token);
	
	service.login("11111", "22222")
		.flatMap(new Func1<String, Observable<User>>() {  //得到token后获取用户信息
		    @Override
		    public Observable<User> onNext(String token) {
		        return service.getUser(token);
		    })
		.subscribeOn(Schedulers.newThread())//请求在新的线程中执行请求
		.observeOn(Schedulers.io())         //请求完成后在io线程中执行
		.doOnNext(new Action1<User>() {      //保存用户信息到本地
		     @Override
		     public void call(User userInfo) {
		         saveUserInfo(userInfo);
		     }
		 })
		.observeOn(AndroidSchedulers.mainThread())//在主线程中执行
		.subscribe(new Observer<User>() {
		    @Override
		    public void onNext(User user) {
		        //完成一次完整的登录请求
		        userView.setUser(user);
		    }
		 
		    @Override
		    public void onCompleted() {
		  
		    }
		 
		    @Override
		    public void onError(Throwable error) {
		        //请求失败
		    }
		});

### buffer()

定期从Observable收集数据到一个集合，并将这些数据项打包发出，而不是一次发出一个

### groupBy()

将Observable分拆为一组Observable，将原始Observable发出的数据按Key分组，每一个Observable发出一组不同的数据项

### scan() 

— 对Observable发出的每一项数据应用一个函数，然后按顺序依次发出这些值

### window()

— 定期将来自Observable的数据分拆成一些Observable窗口，然后发出这些窗口，而不是每次发出一项。类似于Buffer，但Buffer发出的是数据，Window发出的是Observable，每一个Observable发出原始Observable的数据的一个子集

### cast()

 — 在发出数据之前强制将Observable发出的所有数据转换为指定类型 

### throttleFirst() ###

在每次事件触发后的一定时间间隔内丢弃新的事件。常用作去抖动过滤，例如按钮的点击监听器，再也不怕用户手抖点开两个重复的界面啦。

	RxView.clickEvents(button) .throttleFirst(500, TimeUnit.MILLISECONDS).subscribe(subscriber);

## compose:对 Observable 整体的变换 ##

**lift() 是针对事件项和事件序列的，而 compose() 是针对 Observable 自身进行变换**

假设在程序中有多个 Observable ，并且他们都需要应用一组相同的 lift() 变换。

	public class LiftAllTransformer implements Observable.Transformer<Integer, String> {
	    @Override
	    public Observable<String> call(Observable<Integer> observable) {
	        return observable
	            .lift1()
	            .lift2()
	            .lift3()
	            .lift4();
	    }
	}
	...
	Transformer liftAll = new LiftAllTransformer();
	observable1.compose(liftAll).subscribe(subscriber1);
	observable2.compose(liftAll).subscribe(subscriber2);
	observable3.compose(liftAll).subscribe(subscriber3);

使用 `compose()` 方法，`Observable` 可以利用传入的 `Transformer` 对象的 `call()` 方法直接对自身进行处理

# 过滤

选择性的过滤从Observable发射的数据

## API

	debounce() 防反跳，去抖 - 如果在特定的时间跨度已经过去而没有发出新数据项，则从Observable发出一个数据项
	throttleFirst() 节流 - 在特定的时间跨度内，只发出该时间跨度内的第一个数据项
	sample 抽样检查 — 在特定的时间跨度内只发出最新的数据。定期发射最新的数据，等于就是数据抽样，
	distinct() 有区别的，去重 — 抑制Observable发出的重复数据
	elementAt() — 取值取特定位置的那一项数据
	ignoreElements() 忽略所有的数据 — 不从Observable发出任何数据项，但保留终止通知(onError或 onCompleted)
	filter() 过滤 — 过滤掉没有通过断言测试的数据项，只发射通过测试的
	first() — 只从Observable发出第一个数据项满足条件的第一个数据项
	last() — 只发出Observable发出最后一条数据
	skip() — 跳过由Observable发出的前n个数据项
	skipLast() — 跳过由Observable发出的最末n个数据项
	take() — 只发出由Observable发出的前n项数据
	takeLast() — 只发出由Observable发出的最后n项数据

# 组合

将多个Observable组合成一个单一的Observable

## API

	merge - 合并后发射的数据是无序的
	startWith(T...) - 在源Observable发射的数据前插入数据
	concat - 按顺序发射(发射完一个Observable,然后另一个)
	zip - 通过指定的函数将多个Observable的发射组合在一起，并根据此函数的结果为每个组合发出单个数据项
	combineLatest - 通过指定的函数组合每个Observable发出的最新项，并基于此函数的结果发射事件
	switch（切换） - 将一个发出Observable的Observable转换为另一个Observable，并逐个发射原来Observable最近发射的数据
	join - 当在根据由另一Observable发射的项目定义的时间窗期间发出来自一个Observable的项目时，就将两个Observable发射的数据组合成一个并发射

{% asset_img comnineLatest.png %}

	String[] letters = new String[]{"A", "B", "C", "D", "E", "F", "G", "H"};
	Observable<String> letterSequence = Observable.interval(120, TimeUnit.MILLISECONDS)
	        .map(new Func1<Long, String>() {
	            @Override
	            public String call(Long position) {
	                return letters[position.intValue()];
	            }
	        }).take(letters.length);
	
	Observable<Long> numberSequence = Observable.interval(200, TimeUnit.MILLISECONDS).take(5);
	
	Observable.zip(letterSequence, numberSequence, new Func2<String, Long, String>() {
	    @Override
	    public String call(String letter, Long number) {
	        return letter + number;
	    }
	}).subscribe(new Observer<String>() {
	    @Override
	    public void onCompleted() {
	        System.exit(0);
	    }
	
	    @Override
	    public void onError(Throwable e) {
	        System.out.println("Error:" + e.getMessage());
	    }
	
	    @Override
	    public void onNext(String result) {
	        System.out.print(result + " ");
	    }
	});
	输出
		A0 B1 C2 D3 E4

## zip

将多个Observable的发射组合在一起

在user界面，既要请求user基本信息，又要列举user下的event数据

```java
public interface GitHubUser {
  @GET("users/{user}")
  Observable<JsonObject> getUser(@Path("user") String user);
}
 
public interface GitHubEvents {
  @GET("users/{user}/events")
  Observable<JsonArray> listEvents(@Path("user") String user);
}

Observable.zip(userObservable, eventsObservable, new Func2<JsonObject, JsonArray, UserAndEvents>() {
  @Override
  public UserAndEvents call(JsonObject jsonObject, JsonArray jsonElements) {
    return new UserAndEvents(jsonObject, jsonElements);
  }
});

public class UserAndEvents {
  public UserAndEvents(JsonObject user, JsonArray events) {
    this.events = events;
    this.user = user;
  }
 
  public JsonArray events;
  public JsonObject user;
}
```
# 错误处理
从Observable的错误通知中恢复

## API

	retry() 重试 — 如果Observable发射了一个onError通知，重新订阅它，希望它将完成并没有错误
	retryWhen()

实例：实现接口错误重试机制

	NetService.getInstance().doVote(voteId, choice)
        .retryWhen(new RetryWithDelay(9, 3000))
        .subscribeOn(Schedulers.io())
        .observeOn(AndroidSchedulers.mainThread())
        .subscribe()

	public class RetryWithDelay implements Func1<Observable<? extends Throwable>, Observable<?>> {
	    private final int maxRetries;
	    private final int retryDelayMillis;
	    private int retryCount;
	
	    public RetryWithDelay(int maxRetries, int retryDelayMillis) {
	        this.maxRetries = maxRetries;
	        this.retryDelayMillis = retryDelayMillis;
	    }
	
	    @Override
	    public Observable<?> call(Observable<? extends Throwable> attempts) {
	        return attempts
	                .flatMap(new Func1<Throwable, Observable<?>>() {
	                    @Override
	                    public Observable<?> call(Throwable throwable) {
	                        if (++retryCount <= maxRetries) {
	                            // When this Observable calls onNext, the original Observable will be retried (i.e. re-subscribed).
	                            LogUtil.i("OkHttp", "get error, it will try after " + retryDelayMillis + " millisecond, retry count " + retryCount);
	                            return Observable.timer(retryDelayMillis, TimeUnit.MILLISECONDS);
	                        }
	                        // Max retries hit. Just pass the error along.
	                        return Observable.error(throwable);
	                    }
	                });
	    }
	}

	服务器关闭开始测试

# Do #

Rxjava do系列操作符有多个，如doOnNext，doOnSubscribe，doOnUnsubscribe，doOnCompleted，doOnError，doOnTerminate和doOnEach

do系列的作用是side effect, 不改变数据流。 如当onNext发生时，doOnNext会先被调用，经常用来做数据修正/转换。

doOnEach操作符，他接收的是一个Observable参数，相当于doOnNext，doOnError，doOnCompleted综合体

	final SimpleDateFormat sDateFormat = new SimpleDateFormat("yyyy-MM-dd    hh:mm:ss");
    Observable.create(new Observable.OnSubscribe<Person>() {
        @Override
        public void call(Subscriber<? super Person> subscriber) {
            String date = sDateFormat.format(new Date());
            System.out.println(date + " call " + Thread.currentThread().getName());
            Person person = new Person(201);
            subscriber.onNext(person);
        }
    })
    .subscribeOn(Schedulers.io()) //指定耗时进程
    .observeOn(Schedulers.newThread()) //指定doOnNext执行线程是新线程
    .doOnNext(new Action1<Person>() {
        @Override
        public void call(Person person) {
            String date = sDateFormat.format(new Date());
            System.out.println(date + " call " + Thread.currentThread().getName());
            person.age = 301;
            try {
                Thread.sleep(2000);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    })
    .observeOn(AndroidSchedulers.mainThread())//指定最后观察者在主线程.
    .subscribe(new Action1<Person>() {
        @Override
        public void call(Person person) {
            String date = sDateFormat.format(new Date());
            System.out.println(date + " call " + Thread.currentThread().getName());
            Log.d(TAG, "call: " + person.age);
        }
    });

执行结果：

	03-01 14:49:29.897 23442-24145/com.example.myrxlearn I/System.out: 2016-03-01    02:49:29 call RxCachedThreadScheduler-2
	03-01 14:49:29.907 23442-24144/com.example.myrxlearn I/System.out: 2016-03-01    02:49:29 call RxNewThreadScheduler-2
	03-01 14:49:31.907 23442-23442/com.example.myrxlearn I/System.out: 2016-03-01    02:49:31 call main

直到doOnNext里的方法在新线程执行完毕，subscribe里的call才有机会在主线程执行

非阻塞I/O操作

	Schedulers.io().createWorker().schedule(new Action0() {
        @Override
        public void call() {
            try {
                Thread.sleep(2000);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    });
    
    把耗时操作放在一个新worker中
    不需要用observeOn指定doOnNext执行线程是新线程



执行结果：

	03-01 14:55:02.307 30368-30406/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call RxCachedThreadScheduler-1
	03-01 14:55:02.307 30368-30406/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call RxCachedThreadScheduler-1
	03-01 14:55:02.347 30368-30368/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call main
	
# 异常

	Exceptions.propagate(e);
	                                                         
# 实例

封装Nats业务，connect() -- subject()/publish()/request()

	//返回单例Connection
	private Observable<Connection> connect() {
        return Observable.just(mConnection)
                .map(new Func1<Connection, Connection>() {
                    @Override
                    public Connection call(Connection connection) {
                        try {
                            if (mConnection == null) {
                                synchronized (NATSManager.class) {
                                    if (mConnection == null) {
                                        mConnection = Nats.connect(url, getOptions());//耗时操作
                                        if (mConnection != null) {
                                            throw new Exception("mConnection is null");
                                        }
                                    }
                                }
                            }
                        } catch (Exception e) {
                            Exceptions.propagate(e);
                        }
                        return mConnection;
                    }
                })
                .subscribeOn(Schedulers.io())
                .observeOn(AndroidSchedulers.mainThread());
    }
    
	public void request(final String subject, final byte[] data, final long timeout, final RequestCallBack callBack) {
        connect().map(new Func1<Connection, Message>() {
            @Override
            public Message call(Connection connection) {
                try {
                    return mConnection.request(subject, data, timeout);//耗时操作
                } catch (Exception e) {
                    Exceptions.propagate(e);
                    return null;
                }
            }
        }).subscribe(new Subscriber<Message>() {});
    }
	    
# 问题

## Scheduler.io导致OOM

线程超限导致OOM

华为在线程限制上非常严苛

通过Fabric任务栈可以发现，Crash爆发时，线程数量都在400+，而且有大量RxIoSchedule线程处于wait状态，可以推断出RxJava调度器Scheduler.io中维护的线程池没起作用

参考 [华为手机6.0线程OOM分析](https://www.jianshu.com/p/cc93e5a4a880)
### 验证

for循环用Rxjava在IO调度器中创建大量线程模仿网络请求，

```java
private void sendData(final int num) {
    Observable.create(new Observable.OnSubscribe<Integer>() {
      @Override public void call(Subscriber<? super Integer> subscriber) {
        try {
          Thread.sleep(400);
        } catch (InterruptedException e) {
          e.printStackTrace();
        }

        subscriber.onNext(num);
        subscriber.onCompleted();
      }
    })
    .subscribeOn(Schedulers.io())
    .observeOn(AndroidSchedulers.mainThread())
    .subscribe(new Observer<Integer>() {
      @Override public void onNext(Integer num) {
        Log.d(TAG, "current_tread == " + Thread.currentThread().getId());
      }

      @Override public void onCompleted() {
        Log.d(TAG, "work_num == " + num);
      }

      @Override public void onError(Throwable e) {
      }
    });
  }
```
当for循环超过600时，OOM，IO调度器的线程池失效了

### 原因

看Scheduler.io的原码发现，里面的线程池是一个可以**自增、无上限的线程池**，而且每个线程设置了一个**60s的保活**时间防止被结束。

也就是说：在60s内做频繁操作时，io调度器线程池并没有约束线程数且会不断开新线程。

### 解决方案

在这种密集频繁的操作时，自己指定一个Executor作为调度器。

# 背压 Backpressure

参考

- [关于RxJava最友好的文章——背压](https://juejin.im/post/582d413c8ac24700619cceed#heading-10) 背压的原理和解决，版本RxJava1

- [RxJava 系列-2：背压和 Flowable](https://juejin.im/post/5b759b9cf265da283719d187) 侧重背压的解决，版本RxJava2

**深入运用RxJava必须理解的一个概念**

背压最初用在流体力学中，指的是后端的压力， 用于描述系统排出的流体在出口处或二次侧受到的与流动方向相反的压力

响应式编程中，被观察者产生事件的速度快于观察者处理速度，事件堆积，最终挤爆你的内存，导致程序崩溃

```java
Observable.interval(10, TimeUnit.SECONDS)
	.observeOn(Schedulers.newThread())
    //观察者处理每50s才处理一个事件
    .subscribe(new Action1<Long>() {
          @Override
          public void call(Long aLong) {
          	Log.w("TAG","onNext " + aLong + " " + Thread.currentThread().getName());
              try {
                  Thread.sleep(50000);
              } catch (InterruptedException e) {
                  e.printStackTrace();
              }
          }
      });
 
 log打印间隔为50s，华为手机上是发射四次事件左右就会抛出MissingBackpressureException
 
04-01 18:34:43.614 17478-17682/com.zy.course.dev I/lyg: onNext 0 RxNewThreadScheduler-1
04-01 18:35:33.616 17478-17682/com.zy.course.dev I/lyg: onNext 1 RxNewThreadScheduler-1
04-01 18:36:23.617 17478-17682/com.zy.course.dev I/lyg: onNext 2 RxNewThreadScheduler-1
04-01 18:37:13.618 17478-17682/com.zy.course.dev I/lyg: onNext 3 RxNewThreadScheduler-1
04-01 18:38:03.629 17478-17682/com.zy.course.dev E/lyg: onError
                                                        rx.exceptions.MissingBackpressureException
```
被观察者发送事件的速度是观察者处理速度的5倍

抛出MissingBackpressureException


**背压**是指在**异步**场景中，被观察者发送事件速度远快于观察者的处理速度的情况下，一种告诉上游的被观察者降低发送速度的**策略**

简而言之，**背压是流速控制的一种策略**。

## 响应式拉取（reactive pull）

RxJava的观察者模型中，被观察者是主动的推送数据给观察者，观察者是被动接收的。而响应式拉取则反过来，观察者主动从被观察者那里去拉取数据，而被观察者变成被动的等待通知再发送数据

{% asset_img 背压.png %}

观察者可以根据自身实际情况按需拉取数据，而不是被动接收（也就相当于告诉上游观察者把速度慢下来），最终实现了上游被观察者发送事件的速度的控制，实现了背压的策略

```java
class MySubscriber extends Subscriber<T> {
    @Override
    public void onStart() {
    //一定要在onStart中通知被观察者先发送一个事件
      request(1);
    }
 
    @Override
    public void onCompleted() {
        ...
    }
 
    @Override
    public void onError(Throwable e) {
        ...
    }
 
    @Override
    public void onNext(T n) {
        ...
        ...
        //处理完毕之后，在通知被观察者发送下一个事件
        //取消这种backpressure 策略，调用quest(Long.MAX_VALUE)即可
        request(1);
    }
}

Observable.range(1,100000)
	.observeOn(Schedulers.newThread())
    .subscribe(MySubscriber);
``` 

实际上，在上面的代码中，可以不需要调用request(n)方法去拉取数据，程序依然能完美运行

这是因为range --> observeOn,这一段过程本身就是响应式拉取数据，**observeOn操作符内部有一个缓冲区**，Android环境下长度是16，它会告诉range最多发送16个事件，充满缓冲区即可。

上面在观察者中使用request(n)这个方法可以使背压的策略表现得更加直观，更便于理解

## Hot and Cold Observables

上面展示异常情况的代码中，使用的是interval操作符，但是在使用背压时使用了range操作符，这是因为interval操作符本身并不支持背压策略

**在1.0中，部分不支持背压；2.0中，已全部支持背压**

到底什么样的Observable是支持背压的呢？

- **Cold Observables**：在订阅之后才开始发送事件的Observable（每个Subscriber都能接收到完整的事件）
	- **常用**
	- 部分不支持背压
		- **interval，timer**等操作符创建的Observable
- **Hot Observables**:创建了Observable之后，（不管是否订阅）就开始发送事件的Observable
	- **特殊需求才用** 
	- 不支持背压

## 流速控制操作符

不支持背压的Observevable通过操作符做流速控制

### 过滤（抛弃）

Sample，ThrottleFirst.... 

### 缓存

buffer，window...

### 两个特殊操作符

**onBackpressurebuffer**：把observable发送出来的事件做**缓存**，当request方法被调用的时候，给下层流发送一个item(如果给这个缓存区设置了大小，那么超过了这个大小就会抛出异常)。

**onBackpressureDrop**：将observable发送的事件**抛弃**掉，直到subscriber再次调用request（n）方法的时候，就发送给它这之后的n个事件。

# 参考&扩展

- [一起来造一个RxJava，揭秘RxJava的实现原理](https://www.ctolib.com/topics-116009.html#articleHeader0)





