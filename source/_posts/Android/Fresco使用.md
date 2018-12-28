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