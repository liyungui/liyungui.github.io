---
title: Android端架构_MVP-Clean架构
date: 2019-08-16 11:46:01
categories:
  - Android
tags: 
	- 架构
---

# Activity跳转

Activity跳转是如何实现的

`BaseActivity` 持有 `Navigator`，Activity A 调用 Navigator 相应的跳转方法。

每个Activity 都需要提供启动自己的Intent，而不是由Navigator构造

```java
public class Navigator {
  public void navigateToUserList(Context context) {
    if (context != null) {
      Intent intentToLaunch = UserListActivity.getCallingIntent(context);
      context.startActivity(intentToLaunch);
    }
  }
}

public class UserListActivity extends BaseActivity {
  public static Intent getCallingIntent(Context context) {
    return new Intent(context, UserListActivity.class);
  }
}    
```  