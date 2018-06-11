---
title: Android资源文件res
date: 2018-06-11 11:08:38
tags: res
---

# 根据资源名获取资源id--getIdentifier() #

	int layoutId = getResources().getIdentifier("activity_main", "layout", getPackageName());

一般都是动态替换资源id时用到，可以有效避免定义资源Array。比如下例，动态展示连击1到连击9，超过9展示最佳连击

	getResources().getIdentifier(comboNum <= 9 ? "combo_" + comboNum : "combo_best", "drawable", getPackageName());