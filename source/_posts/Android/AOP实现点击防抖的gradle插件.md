---
title: AOP实现点击防抖的gradle插件
date: 2019-06-16 18:10:53
tags: 
	- Android
category:
	- Android
---

# 为什么使用AOP

对旧代码零入侵

# 为什么选择 ASM 实现 AOP

因为ASM的语法更通俗易懂，并且与gradle的联动效果更好，能够非常方便的修改字节码

AspectJ在这些维度的比较上实在显得笨重。

# 支持的点击事件

 - View.OnClickListener
 - AdapterView.OnItemClickListener
 
# 使用

常规的集成

不需要配置混淆规则，因为纯字节码操作，没任何反射

## 设置防抖间隔时间

默认 300 milliseconds

`DebouncedPredictor.FROZEN_WINDOW_MILLIS = 400L`

## 忽略某些点击方法

推荐 在 gradle 中配置，会自动 添加 `@Debounce`注解

```
debounce {
  // enable log
  loggable = true
  // java bytecode descriptor: [class: [methods]]
  exclusion = ["com/smartdengg/clickdebounce/ClickProxy": ['onClick(Landroid/view/View;)V',
                                                           'onItemClick(Landroid/widget/AdapterView;Landroid/view/View;IJ)V']]
}
```

某些匿名内部类不太好在 gradle中配置，手动 添加 `@Debounce`注解

```java
this.setOnClickListener(new View.OnClickListener() {
    @Override
    @Debounced
    public void onClick(View v) {
	}
});
```

# 参考&扩展

[click-debounce](https://github.com/SmartDengg/click-debounce)