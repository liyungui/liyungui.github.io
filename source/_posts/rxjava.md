---
title: rxjava
date: 2018-04-26 14:12:33
tags: rxjava
---

# RxJava是什么 #

一个词：**异步**

[GitHub主页](https://github.com/ReactiveX/RxJava)上的自我介绍是 "a library for composing asynchronous and event-based programs using observable sequences for the Java VM"（一个在 Java VM 上使用可观测的序列来组成异步的、基于事件的程序的库）

# RxJava 好在哪 #

一个词：**逻辑简洁**。不是代码简洁(代码量少)

比 `AsyncTask` 和 `Handler` 都更加简洁

链式调用，没有任何嵌套。把任何复杂逻辑都能穿成一条线的简洁

# 引入依赖 #

	compile "io.reactivex:rxjava:1.3.8"

# 原理简析 #

## 观察者模式--四个基本概念 ##

**生产消费者模型** 

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

在一个正确运行的事件序列中, onCompleted() 和 onError() 有且只有一个，并且是事件序列中的最后一个。

需要注意的是，onCompleted() 和 onError() 二者也是互斥的，即在队列中调用了其中一个，就不应该再调用另一个。

# 基本实现API #

## 创建 Observer ##

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

## 创建 Observable ##

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

`OnSubscribe` 会被存储在返回的 `Observable` 对象中

`OnSubscribe.call(subscriber)`方法 命名有意思：

当 `Observable` 被 订阅`subscribe()`的时候，该方法会被调用。回调时传入 Observable 对应的 Observer

注意：**一个 Observable 总是对应着 一个 OnSubscribe 和一个 Observer**

### `just(T...)` ###

- 将传入的参数依次发送出来

		Observable observable = Observable.just("Hello", "Hi", "Aloha");

### `from(T[]) / from(Iterable<? extends T>)` ###

- 将传入的数组或 Iterable 拆分成具体对象后，依次发送出来。 

		tring[] words = {"Hello", "Hi", "Aloha"};
		Observable observable = Observable.from(words);

## 订阅 observable.subscribe(observer) ##

subscribe() 这个方法有点怪：它看起来是 `observalbe` 订阅了 `observer / subscriber`，看起来就像 『杂志订阅了读者』 一样颠倒了对象关系

这是为了 流式 API 的设计

	// 注意：这是 subscribe() 的核心代码，将与性能、兼容性、扩展性有关的代码剔除了。
	public Subscription subscribe(Subscriber subscriber) {
	    subscriber.onStart();
	    onSubscribe.call(subscriber);
	    return subscriber;
	}

- 将传入的 Subscriber 作为 Subscription 返回。这是为了方便 unsubscribe().

{% asset_img subscriber.jpg %}

RxJava 的默认规则中，遵循的是**线程不变原则**。即不指定线程的情况下，事件的发出和消费都是在同一个线程的

所以，以上实现的只是一个同步的观察者模式

**观察者模式本身的目的就是『后台处理，前台回调』的异步机制**

而要实现异步，则需要用到 RxJava 的另一个概念： Scheduler 

## 线程控制 Scheduler ##

### 内置Scheduler ###

- `Schedulers.immediate()`:直接在当前线程运行，相当于不指定线程。这是默认的 Scheduler。
- `Schedulers.newThread()`: 总是启用新线程，并在新线程执行操作。
- `Schedulers.io()`: I/O 操作（读写文件、读写数据库、网络信息交互等）所使用的 Scheduler。行为模式和 newThread() 差不多，区别在于 io() 的内部实现是是用一个无数量上限的线程池，可以重用空闲的线程，因此多数情况下 io() 比 newThread() 更有效率。不要把计算工作放在 io() 中，可以避免创建不必要的线程。
- `Schedulers.computation()`: 计算所使用的 Scheduler。这个计算指的是 CPU 密集型计算，即不会被 I/O 等操作限制性能的操作，例如图形的计算。这个 Scheduler 使用的固定的线程池，大小为 CPU 核数。不要把 I/O 操作放在 computation() 中，否则 I/O 操作的等待时间会浪费 CPU。
- `AndroidSchedulers.mainThread()`: 在 Android 主线程运行。Android专用的

### 线程控制 ###

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

### Scheduler原理 ###

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

### 多个 subscribeOn() 和 observeOn() 混合使用，线程调度 ###

{% asset_img multi_schedule.jpg %}

- 图中共有 5 处含有对事件的操作。
- ①和②两处受第一个 subscribeOn() 影响，运行在红色线程；
- ③和④处受第一个 observeOn() 的影响，运行在绿色线程；
- ⑤处受第二个 onserveOn() 影响，运行在紫色线程；
- 第二个 subscribeOn() ，由于在通知过程中线程就被第一个 subscribeOn() 截断，因此对整个流程并没有任何影响。**当使用多个 subscribeOn() 的时候，只有第一个 subscribeOn() 起作用**。

### 延伸：doOnSubscribe() ###

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


# 变换 #

**将事件序列中的对象或整个序列，转换成不同的事件或事件序列**

## API ##

###  map() ###

**一对一的转化**

打印出一组学生的名字。每个学生只有一个名字

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

### flatMap() ###

**一对多的转化**

**flatMap() 返回的是 Observable 对象**

打印出一组学生所修的所有课程的名称。每个学生有多个课程，把一个 Student 转化成多个 Course

	Student[] students = ...;
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

**flatMap() 的原理：**

1. 使用传入的事件对象创建一个 Observable 对象；
2. 并不发送这个 Observable, 而是将它激活，于是它开始发送事件；
3. 每一个创建出来的 Observable 发送的事件，都被汇入同一个 Observable ，而这个 Observable 负责将这些事件统一交给 Subscriber 的回调方法。

把事件拆成了两级，通过一组新创建的 Observable 将初始的对象『铺平』之后通过统一路径分发了下去。

### throttleFirst() ###

在每次事件触发后的一定时间间隔内丢弃新的事件。常用作去抖动过滤，例如按钮的点击监听器，再也不怕用户手抖点开两个重复的界面啦。

	RxView.clickEvents(button) .throttleFirst(500, TimeUnit.MILLISECONDS).subscribe(subscriber);

## 变换的原理：lift() ##

**实质：对事件序列的处理和再发送**

	// 核心代码。
	public <R> Observable<R> lift(Operator<? extends R, ? super T> operator) {
	    return Observable.create(new OnSubscribe<R>() {
	        @Override
	        public void call(Subscriber subscriber) {
	            Subscriber newSubscriber = operator.call(subscriber);
	            newSubscriber.onStart();
	            onSubscribe.call(newSubscriber);//onSubscribe是原始 Observable 中的原始 OnSubscribe
	        }
	    });
	}

- 生成一个新的 Observable 并返回。 

- 一个新的 Observable 意味着着 一个新的 OnSubscribe 和一个新的 Observer

- 新 Observable subscribe() 时，触发 新 onSubscribe.call(subscriber)
	- 在这个 call() 方法里
		- 新 OnSubscribe 利用 operator.call(subscriber) 生成了一个新的 Subscriber
		- Operator 就是在这里，通过自己的 call() 方法将新 Subscriber 和原始 Subscriber 进行关联，并插入自己的『变换』代码以实现变换
		- 然后利用这个新 Subscriber 向原始 Observable 进行订阅。 onSubscribe.call(newSubscriber)

**有点像一种代理机制，通过事件拦截和处理实现事件序列的变换。** 新 Observable 像代理一样，负责接收原始的 Observable 发出的事件，并在处理后发送给 Subscriber

{% asset_img lift.jpg %}

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
    }).subscribeOn(Schedulers.io()) //指定耗时进程
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
    }).observeOn(AndroidSchedulers.mainThread())//指定最后观察者在主线程
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

不需要在用observeOn指定在新线程就可以实现

执行结果：

	03-01 14:55:02.307 30368-30406/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call RxCachedThreadScheduler-1
	03-01 14:55:02.307 30368-30406/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call RxCachedThreadScheduler-1
	03-01 14:55:02.347 30368-30368/com.example.myrxlearn I/System.out: 2016-03-01    02:55:02 call main

# retryWhen #

实现接口错误重试机制

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

# interval #

轮询

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