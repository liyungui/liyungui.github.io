---
title: View.post不靠谱
date: 2019-07-10 18:36:53
categories: 
	- Android
tags: 
	- Android
---

# 背景

有时候，我们会用 View.post() 方法，来将一个 Runnable 发送到主线程去执行。这一切，看似很美好，它最终会通过一个 Handler.post() 方法去执行，又避免我们重新定义一个 Handler 对象。

但是，在 Android 7.0（Api level 24） 上，View.post() 将不再那么靠谱了，你post() 出去的 Runnable ，可能永远也不会有机会得到执行。

# post 在 7.0 的差异

在 Api23 及以下，`executeAction()` 是会被**循环调用**（一个 VSync 的间隔），基本上其内的 mActions 中，只要有未执行的 Runnable 立刻就会被消费掉

在 Api24 及以上，`executeActions()` 只在 `dispatchAttachedToWindow()` 中才有机会被**调用一次**，而 `View.dispatchAttachedToWindow()` 只有在这个 View 通过 addView() 方法，或者原本写在页面布局的 xml 中（实际上也是调用的 addView()），加入到一个 ViewGroup 的时候，才会被调用到

# 总结

View.post() 方法，在不同版本的差异，根本原因还是在于 Api23 和 Api24 中，`executeActions()` 方法的调用时机不同，导致 View 在没有 mAttachInfo 对象的时候，表现不一样了。

所以我们在使用的过程中需要慎用，区分出实际使用的场景，一般规范自己的代码即可：

- 动态创建的 View ，如果视条件去决定是否加入到根布局中，则不要使用它来调用 post() 方法。
- 尽量避免使用 View.post() 方法，可以直接使用 Handler.post() 方法来替代。

# 参考&扩展

- [View.post() 不靠谱的地方你知道吗？](https://www.cnblogs.com/plokmju/p/7481727.html)
