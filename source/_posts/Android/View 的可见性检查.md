---
title: View 的可见性检查
date: 2019-07-10 18:24:53
categories: 
	- Android
tags: 
	- Android
---

{% asset_img visibility.png %}

四种方法获取的结果如下：

```java
View5.getVisibility() = View.VISIBLE;
View5.isShown() = true; 
View5.getGlobalVisibleRect() = false;
View5.getLocalVisibleRect() =  false;
```

# View.getVisibility()

最基本的检查View可见性的方法

如果这个方法返回的是View.INVISIBLE或者View.GONE，那么这个View肯定是对用户不可见的。

# View.isShown()

- 递归
- 检查View以及它的parentView的Visibility == View.VISIBLE，
- 检查parentView == null
	- 也就是说所有的parentView都不能为null。否则就说明这个View根本没有被addView过

```java
/**
 * Returns the visibility of this view and all of its ancestors
 *
 * @return True if this view and all of its ancestors are {@link #VISIBLE}
 */
public boolean isShown() {
    View current = this;
    //noinspection ConstantConditions
    do {
        if ((current.mViewFlags & VISIBILITY_MASK) != VISIBLE) {
            return false;
        }
        ViewParent parent = current.mParent;
        if (parent == null) {
            return false; // We are not attached to the view root
        }
        if (!(parent instanceof View)) {
            return true;
        }
        current = (View) parent;
    } while (current != null);

    return false;
}
```

# View.getGlobalVisibleRect()

返回一个View是否可见的boolean值，同时还会将该View的可见区域left，top，right，bottom值保存在一个rect对象中

获得的rect坐标系的原点是屏幕的左上角

调用的是`getGlobalVisibleRect(Rect r, Point globalOffset)`

# View.getLocalVisibleRect()

获得的rect坐标系的原点是View自己的左上角

其也会调用`getGlobalVisibleRect()`

```java
public final boolean getLocalVisibleRect(Rect r) {
    final Point offset = mAttachInfo != null ? mAttachInfo.mPoint : new Point();
    if (getGlobalVisibleRect(r, offset)) {
        r.offset(-offset.x, -offset.y); // make r local
        return true;
    }
    return false;
}
```

- 先获取View的offset point（相对屏幕或者ParentView的偏移坐标），
- 再调用getGlobalVisibleRect(Rect r, Point globalOffset)方法来获取可见区域
- 最后再把得到的GlobalVisibleRect和Offset坐标做一个加减法，转换坐标系原点

View在屏幕中全部不可见时(图中view5)，两者的visibility都为false，且两者获取的rect值相同。由源码可以知道，getLocalVisibleRect()最终调用的是getGlobalVisibleRect()方法，并会减去View自身的便偏移坐标offset point，但只有当View可见时才会减去这个偏移坐标，要是不可见就直接返回了，所以此时两者获取出的rect值是相同的

# 注意

- `getGlobalVisibleRect()` `getLocalVisibleRect()`判断View的可见性时，一定要等View绘制完成后，再去调用这两个方法，否则无法得到对的结果，返回值的rect值都是0，visibility为false。这和获取View的宽高原理是一样的，如果View没有被绘制完成，那么View.getWidth和View.getHeight一定是等于0的
- `getGlobalVisibleRect()`只能检查出这个View在手机屏幕（或者说是相对它的父View）的位置，而不能检查出与其他兄弟View的相对位置:
比如有一个ViewGroup，下面有View1、View2这两个子View，View1和View2是平级关系。此时如果View2盖住了View1，那么用getGlobalVisibleRect方法检查View1的可见性，得到的返回值依然是true，得到的可见矩形区域rect也是没有任何变化的。

# 参考&扩展

- [View 的可见性检查还可以这样](https://www.jianshu.com/p/30b0ae304518)