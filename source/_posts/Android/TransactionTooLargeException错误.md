---
title: TransactionTooLargeException错误
date: 2019-09-02 17:54:53
categories:
	- Android
tags:
	- Android
---

# 表现

	TransactionTooLargeException: data parcel size 587588  bytes

# 原因

**Binder传递数据量过大**	

进程内Binder缓冲区最大上限1M（进程内所有线程共享这块空间，实际上操作的线程内，数据超过200K都可能挂掉）

在6.0的源码 `/frameworks/base/core/jni/android_util_Binder.cpp`v中的 `signalExceptionForError` 函数里，对于 `FAILED_TRANSACTION` 这种错误的分支里，丢出了异常，不过还是有让人困惑的地方：传递的数据超过200K就要报错

## Activity状态Bundle

```java
protected void onSaveInstanceState(Bundle outState) {}
```

## Activity跳转Intent

通过Intent传递数据，具体的大小限制不同版本的系统不同，比较普遍的一个看法是不能超过1MB，因为官方文档里有这样的说明：

```
The Binder transaction failed because it was too large.

During a remote procedure call, the arguments and the return value of the call are transferred as Parcel objects stored in the Binder transaction buffer. If the arguments or the return value are too large to fit in the transaction buffer, then the call will fail and TransactionTooLargeException will be thrown.

The Binder transaction buffer has a limited fixed size, currently 1Mb, which is shared by all transactions in progress for the process. Consequently this exception can be thrown when there are many transactions in progress even when most of the individual transactions are of moderate size.
```

# 解决方案

## 压缩数据量

## 使用其他方式传递数据

- 文件
- EventBus

# 参考&扩展

- [Android TransactionTooLargeException 解析，思考与监控方案](https://www.jianshu.com/p/044e2c318306)