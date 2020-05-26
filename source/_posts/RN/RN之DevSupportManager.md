---
title: RN之DevSupportManager
date: 2018-07-27 10:31:15
tags:
	- RN
---

# DevSupportManager

```java
/**
 * 开发调试功能的接口类
 * 开发模式使用DevSupportManagerImpl 
 * 生成模式使用DisabledDevSupportManager
 */
public interface DevSupportManager extends NativeModuleCallExceptionHandler {}
```

# 异常处理

## DevSupportManagerImpl

```java
public class DevSupportManagerImpl
    implements DevSupportManager, PackagerCommandListener, DevInternalSettings.Listener {
  @Override
  public void handleException(Exception e) {
    if (mIsDevSupportEnabled) {

      for (ExceptionLogger logger : mExceptionLoggers) {
        logger.log(e);
      }

    } else {
      //类构造函数中初始化的，原样抛出RuntimeException
      mDefaultNativeModuleCallExceptionHandler.handleException(e);
    }
  }
}  
```

## DisabledDevSupportManager

```java
public class DisabledDevSupportManager implements DevSupportManager {
  @Override
  public void handleException(Exception e) {
    mDefaultNativeModuleCallExceptionHandler.handleException(e);
  }
}
```