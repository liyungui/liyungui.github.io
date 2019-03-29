---
title: InputMethodManager 导致的内存泄露及解决方案
date: 2019-03-01 14:15:53
categories:
  - Android
tags:
  - 性能优化
---

[Issue 171190:	InputMethodManager leaks the last focused view](https://code.google.com/p/android/issues/detail?id=171190) `Repro steps` are very easy:

# 泄露实例 #

[Android InputMethodManager 导致的内存泄露及解决方案](http://www.jianshu.com/p/aa2555628b17)

![](https://pic4.zhimg.com/c55242f458e266f3e2cfb7d112411167_b.png)

并且还给出了参考链接，这是Android输入法的一个bug，在15<=API<=23中都存在。

`InputMethodManager.sInstance` --> `InputMethodManager.mNextServedView`

LeakCanary之所以能够显示参考链接是因为它有一个针对SDK已知内存泄露的列表，放在AndroidExcludedRefs.java中，比如输入法的这个。

![](https://pic4.zhimg.com/2b97881206ab6a8556946b9a016e078f_b.png)

# 泄露原因 #

分析原因比较透彻的是这篇文章：[InputMethodManager内存泄露现象及解决](http://blog.csdn.net/sodino/article/details/32188809)

# 解决方案 #

## 方案一 ##

改善方案可以参考Leaknary给出的方案：[InputMethodManager内存泄露修正方案](https://gist.github.com/pyricau/4df64341cc978a7de414)

在退出使用InputMethodManager的Activity时，调用fixFocusedViewLeak方法即可解决。

## 方案二、简单方案 ##

[Android Memory Leaks InputMethodManager Solved](https://medium.com/@amitshekhar/android-memory-leaks-inputmethodmanager-solved-a6f2fe1d1348#.j686ef3a0) `Simple solution` to solve this. 

After some observations we realize that if any other activity is being called after that the finish of main activity the things is going perfect , no more Memory Leaks by InputMethodManager.

	public class DummyActivity extends FragmentActivity {
	    @Override
	    protected void onCreate(@Nullable Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        new Handler().postDelayed(new Runnable() {
	            @Override
	            public void run() {
	                finish();
	            }
	        }, 100);
	    }
	}

	可以把Activity设为透明，这样退出时不会出现短暂白屏