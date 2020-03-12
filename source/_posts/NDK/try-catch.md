---
title: try-catch
date: 2020-01-15 11:39:14
categories:
  - Android
tags:
  - NDK
---

# 捕获所有异常

```cpp
try {
    g_app->start();
    g_isStarted = true;
} catch (...) {
}
```

# NDK开启`try-catch`支持

`cannot use 'try' with exceptions disabled`

这是由于 DragonBonesCPP 库使用了 C++ 标准异常，而Android NDK r5 版本开始支持 C++ 异常控制，但是编译器的 C++ 异常控制特性支持默认是关闭的。

要打开它，可以这样做：

编辑 Android.mk 文件，使当前module支持：

```bash
LOCAL_CPP_FEATURES += exceptions
或者：

LOCAL_CPPFLAGS += -fexceptions
```

如果想偷懒，也可以编辑 Application.mk 文件，使所有module支持：

`APP_CPPFLAGS += -fexceptions`

# 参考&扩展

- [cannot use 'try' with exceptions disabled](https://www.cnblogs.com/zl1991/p/6604889.html)
