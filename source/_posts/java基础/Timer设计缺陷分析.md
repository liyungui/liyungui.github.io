---
title: Timer设计缺陷分析
date: 2019-07-17 14:41:53
categories:
  - Java
tags: 
	- Java
---

# 背景

APP模块中使用Timer需要实现一个10秒一次的心跳

```java
mHeartBeatTimer = new Timer();
mHeartBeatTimerTask = new TimerTask() {
	@Override
    public void run() {
		try {
			//直接在Timer线程进行API请求，未开启线程
 		} catch (Exception e) {
			ExceptionUtil.handle(e);
		}
	}
};
mHeartBeatTimer.schedule(mHeartBeatTimerTask, 0, 10 * 1000);
```

上线后发现存在心跳丢失问题。

排查bugly发现没有任何异常和崩溃，初步怀疑是Timer的问题。

# Timer缺陷

下面来自《Java并发编程实战》：

```
1.Timer在执行所有定时任务时只会创建一个线程。
	如果某个任务的执行时间长度大于其周期时间长度，那么就会导致这一次的任务还在执行，而下一个周期的任务已经需要开始执行了，
	当然在一个线程内这两个任务只能顺序执行，有两种情况：对于之前需要执行但还没有执行的任务，
		scheduleAtFixedRate，任务快速调用。当前任务执行完马上执行那些任务（按顺序来），
		schedule，任务丢失。干脆把那些任务丢掉，不去执行它们。
2.如果TimerTask抛出了一个未检出的异常，那么Timer线程就会被终止掉，
之前已经被调度但尚未执行的TimerTask就不会再执行了，新的任务也不能被调度了。
```

# Timer源码分析

```java
public class Timer {
	//任务队列。
	//内部是一个数组，按任务执行时间排序
	//存放Timer的TimerTask；Timer生产，TimerThread消费
	private final TaskQueue queue = new TaskQueue();
	//Thread子类。run()中死循环 检查和执行 任务队列的任务
	private final TimerThread thread = new TimerThread(queue);
	
	//构造方法。设置线程名称和Daemon，开启线程
	public Timer(String name, boolean isDaemon) {
        thread.setName(name);
        thread.setDaemon(isDaemon);
        thread.start();//开启
    }
    
    public void schedule(TimerTask task, Date firstTime, long period) {
    	//period设置为负值
        sched(task, firstTime.getTime(), -period);
    }
    
    public void scheduleAtFixedRate(TimerTask task, Date firstTime,
                                    long period) {
        if (period <= 0)
            throw new IllegalArgumentException("Non-positive period.");
        sched(task, firstTime.getTime(), period);
    }
    
    private void sched(TimerTask task, long time, long period) {
        if (time < 0)
            throw new IllegalArgumentException("Illegal execution time.");

        // 限制period最大值
        if (Math.abs(period) > (Long.MAX_VALUE >> 1))
            period >>= 1;

        synchronized(queue) {
            if (!thread.newTasksMayBeScheduled)
                throw new IllegalStateException("Timer already cancelled.");

			//设置task属性
            synchronized(task.lock) {
                if (task.state != TimerTask.VIRGIN)
                    throw new IllegalStateException(
                        "Task already scheduled or cancelled");
                task.nextExecutionTime = time;
                task.period = period;
                task.state = TimerTask.SCHEDULED;
            }

			//将task加入队列
            queue.add(task);
            if (queue.getMin() == task)
                queue.notify();
        }
    }
```

```java
class TimerThread extends Thread {
	//用来标识是否可以添加新任务
    boolean newTasksMayBeScheduled = true;
    private TaskQueue queue;

    TimerThread(TaskQueue queue) {
        this.queue = queue;
    }

    public void run() {
        try {
            mainLoop();
        } finally {
            // Someone killed this Thread, behave as if Timer cancelled
            synchronized(queue) {
                newTasksMayBeScheduled = false;
                queue.clear();  // Eliminate obsolete references
            }
        }
    }

    private void mainLoop() {
        while (true) {
            try {
                TimerTask task;
                boolean taskFired;//任务是否过期(执行时间<=现在时间)
                synchronized(queue) {
                    // 死循环，等待任务队列非空
                    while (queue.isEmpty() && newTasksMayBeScheduled)
                        queue.wait();
                    if (queue.isEmpty())
                        break; // 任务队列为空，且不可添加新任务，结束TimerThread线程
                    // 任务队列非空，检查和执行第一个任务
                    long currentTime, executionTime;
                    task = queue.getMin();
                    synchronized(task.lock) {
                        if (task.state == TimerTask.CANCELLED) {
                            queue.removeMin();
                            continue;  // 该任务已取消，直接从队列中移除，等待下一任务
                        }
                        currentTime = System.currentTimeMillis();
                        executionTime = task.nextExecutionTime;
                        //任务已过期
                        if (taskFired = (executionTime<=currentTime)) {
                            if (task.period == 0) { // 不需要重复执行，直接移除
                                queue.removeMin();
                                task.state = TimerTask.EXECUTED;
                            } else { // 需要重复执行，修改task下一次执行时间，并刷新任务队列排序
                                queue.rescheduleMin(
                                  task.period<0 ? currentTime - task.period
                                                : executionTime + task.period);
                            }
                        }
                    }
                    if (!taskFired) // Task hasn't yet fired; wait
                        queue.wait(executionTime - currentTime);
                }
                if (taskFired)  // 任务已过期，立即执行
                    task.run();
            } catch(InterruptedException e) {//捕获异常
            }
        }
    }
}
```

- Timer在执行定时任务时只创建一个线程，如果任务耗时超过了两个任务的间隔时间，会发生一些缺陷
	- schedule **Timer任务丢失**	
		- period<0，下一次执行时间 = currentTime - task.period；
		- 任务被重置。从现在开始，period周期间隔后执行一次任务。
		- 那么之前预想在period这个间隔内存在的任务执行就没了，也就是 **任务丢失** 问题
	- scheduleAtFixedRate **Timer任务快速调用**
		- period>0，下一次执行时间 = executionTime + task.period；
		- 下一次任务还是按原来的算。从原来应该的执行时间开始，period周期间隔后执行一次任务。
		- 如果这时executionTime + task.period还先于currentTime，那么下一个任务就会马上执行，也就是 **任务快速调用** 问题。
- TimerTask异常导致 **Timer线程异常结束**
	- TimerThread run方法的死循环只捕获了 **InterruptedException**  异常
		- 当前线程可以被中断，被操作系统挂到一边休息，然后又回来继续执行
		- 其它异常，那么整个循环就挂掉，导致线程结束

- Timer执行周期任务时 **依赖系统时间** ,修改系统时间容易导致任务被挂起（如果当前时间小于执行时间）

# 总结

使用Timer实现定时发心跳包可能会有问题

如果Timer线程在执行过程中被中断了，那么调用schedule的就很有可能导致心跳包没有发出去，而调用scheduleAtFixedRate的又可能会导致Timer线程没有占用CPU时心跳包没发出去，某一时刻又快速地发送好几个心跳包。

因此在Android中如果需要一个严格准时的定时操作，一般使用 **AlarmManager** 实现。

# 参考&扩展

- [Java中的Timer源码分析及缺陷](https://blog.csdn.net/u012619640/article/details/50749715)



