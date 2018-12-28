---
title: Android动画
date: 2018-12-14 16:22:53
tags: 
	- 动画
---

# 常见问题

## setVisibility(INVISIBLE)无效

setVisibility(INVISIBLE)隐藏view，但是还是在界面上没有消失

解决方案：**clearAnimation()**

View的clearAnimation()源码

```java
public void clearAnimation() {
    if (mCurrentAnimation != null) {
        mCurrentAnimation.detach();
    }
    mCurrentAnimation = null;
    invalidateParentIfNeeded();
}
```

主要是把mCurrentAnimation这个变量置空
