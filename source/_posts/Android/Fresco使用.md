---
title: Fresco使用
date: 2018-06-27 10:43:15
tags:
	- 图片
---

# SimpleDraweeView实现圆形图片  #

	LinearLayout.LayoutParams headPortraitQueueLayoutParams = new LinearLayout.LayoutParams(ResourcesManager.instance().dipToPx(20), ResourcesManager.instance().dipToPx(20));
    mQueueHeadPortrait = new SimpleDraweeView(context);
    mQueueHeadPortrait.setLayoutParams(headPortraitQueueLayoutParams);
    mQueueHeadPortrait.setHierarchy(buildGenericDraweeHierarchy());

	private GenericDraweeHierarchy buildGenericDraweeHierarchy() {
        RoundingParams roundingParams = new RoundingParams();
        roundingParams.setRoundAsCircle(true);//设置图像显示圆形，当我们同时设置图像显示为圆形图像和圆角图像时，只会显示为圆形图像
        roundingParams.setBorderColor(Color.parseColor("#E9E9E9"));//边框颜色
        roundingParams.setBorderWidth(2f);//边框宽度
        GenericDraweeHierarchyBuilder genericDraweeHierarchyBuilder = new GenericDraweeHierarchyBuilder(getResources());
        return genericDraweeHierarchyBuilder
                .setPlaceholderImage(ResourcesManager.instance().getDrawable(R.mipmap.ic_default_avatar_t))
                .setPlaceholderImageScaleType(ScalingUtils.ScaleType.CENTER_INSIDE)
                .setActualImageScaleType(ScalingUtils.ScaleType.CENTER_INSIDE)
                .setFailureImage(ResourcesManager.instance().getDrawable(R.mipmap.ic_default_avatar_t))
                .setFailureImageScaleType(ScalingUtils.ScaleType.CENTER_INSIDE)
                .setRoundingParams(roundingParams)//圆形圆角设置
                .build();
    }

- 宽高不支持wrap-content(图片无法显示)，需设置精确值
- GenericDraweeHierarchy不能共用(共用的话，所有图片都展示成最后一个view的图片)

# 常见问题

## 未初始化导致APP崩溃

使用之前，必须调用 `Fresco.initialize`初始化

大部分APP，为了优化启动速度，一般都会启用IntentService，异步线程执行初始化，很容易导致Fresco未初始化就使用，导致APP奔溃

## 重复初始化导致内存泄漏

APP主module初始化了Fresco，其他module(RN Udesk等)如果未经判断直接初始化Fresco，就会出问题

### 初始化源码

```java
  /** Initializes Fresco with the specified config. */
  public static void initialize(
      Context context,
      @Nullable ImagePipelineConfig imagePipelineConfig,
      @Nullable DraweeConfig draweeConfig) {
    if (FrescoSystrace.isTracing()) {
      FrescoSystrace.beginSection("Fresco#initialize");
    }
    if (sIsInitialized) {
      FLog.w(
          TAG,
          "Fresco has already been initialized! `Fresco.initialize(...)` should only be called "
              + "1 single time to avoid memory leaks!");
    } else {
      sIsInitialized = true;
    }
    ...初始化工作
  }
```

可以看到，Fresco的初始化实现，是有一个字段sIsInitialized记录是否已经初始化的，如果重复初始化，是会有警告日志输出到logcat的。但是还是执行了初始化的工作

### 错误姿势-RN
  
```java
react-native-0.48.4 FrescoModule.initialize 
没有判断，直接初始化Fresco
```

{% asset_img RN初始化Fresco.png %}

### 正确姿势-Udesk

```java
//UdeskUtil.java
public static void frescoInit(final Context context) {
    try {
    	//判断，防止重复初始化
        if (!Fresco.hasBeenInitialized()) {
            ...
            Fresco.initialize(context, config);
        }
    } catch (Exception e) {
        e.printStackTrace();
        Fresco.initialize(context);
    }
}
```

# 最佳实践建议

## clearMemoryCache

页面退出之前，建议强制调用 Fresco 框架的 clearMemoryCache 方法，通知 Fresco 清除内存缓存。可以保证 GC 及时地把这些图片内存给回收掉，避免整个 APP 的内存占用过高，经过实践验证这也很有效地解决了内存问题。

# 参考&扩展

- [京东 618：ReactNative 框架在京东无线端的实践](https://www.infoq.cn/article/jd-618-ReactNative-jingdong-practise)