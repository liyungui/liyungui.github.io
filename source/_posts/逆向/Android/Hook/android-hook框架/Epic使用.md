---
title: Epic使用
date: 2020-08-30 14:16:53
tags:
	- Hook
---

# 特性

- 以 Java 方法为粒度的运行时 Hook 框架
- 不需要root
- 支持 Android 4.0~10.0

# 使用

`implementation 'me.weishu:epic:0.6.0'`

## MethodHookParam

```
thisObject; //静态方法返回null
args; //参数列表；下标从0开始
getResult(); //获取方法返回结果
setResult(); //设置方法返回结果
getThrowable(); //捕获异常；没有返回null
setThrowable(); //抛出异常
```

# 参考&扩展

- [Epic github](https://github.com/tiann/epic/blob/master/README_cn.md)




