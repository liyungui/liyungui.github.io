---
title: MVVM布局嵌套dataBinding
date: 2019-01-14 09:09:56
categories:
  - 编程思想
tags:
  - 编程思想
---

## common_title _layout.xml ##

	<layout>
	    <data>
	        <variable
	            name="titleVM"
	            type="com.xuehu365.xuehu.viewmodel.CommonTitleVM" />
	    </data>
	
	    <RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
	        android:layout_width="match_parent"
	        android:layout_height="@dimen/activity_title_height">
	        <ImageView
	            android:id="@+id/ivBack"
	            android:layout_width="wrap_content"
	            android:layout_height="match_parent"
	            android:paddingLeft="@dimen/activity_horizontal_padding"
	            android:paddingRight="@dimen/activity_horizontal_padding"
	            android:src="@drawable/icon_fanhui" />
	        <TextView
	            android:layout_width="wrap_content"
	            android:layout_height="wrap_content"
	            android:layout_centerInParent="true"
	            android:text="@{titleVM.title}"
	            android:textColor="@color/c32"
	            android:textSize="18dp" />
	        <TextView
	            android:id="@+id/tvMenu"
	            android:layout_width="wrap_content"
	            android:layout_height="wrap_content"
	            android:layout_alignParentRight="true"
	            android:layout_centerVertical="true"
	            android:paddingLeft="@dimen/activity_horizontal_padding"
	            android:paddingRight="@dimen/activity_horizontal_padding"
	            android:text="@{titleVM.menu}"
	            android:textColor="@color/c66"
	            android:textSize="15dp" />
	    </RelativeLayout>
	</layout>

## fragment_mine.xml ##

	<layout>
	    <LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
	        android:layout_width="match_parent"
	        android:layout_height="match_parent"
	        android:background="@color/white"
	        android:orientation="vertical">
	
	        <include
	            android:id="@+id/title"
	            layout="@layout/common_title_layout_vm" />
	
	        <ImageView
	            android:layout_width="match_parent"
	            android:layout_height="0.5dp"
	            android:layout_alignParentBottom="true"
	            android:background="@color/divider_color_light" />
	
	        <com.xuehu365.xuehu.ui.widget.CustomWebView
	            android:id="@+id/mineFragmentWebview"
	            android:layout_width="match_parent"
	            android:layout_height="match_parent" />
	    </LinearLayout>
	</layout>

## MineFragment ##

	View inflate = inflater.inflate(R.layout.fragment_mine, container, false);
    bind = DataBindingUtil.bind(inflate);
    bind.title.setTitleVM(new CommonTitleVM("我在学乎", "设置", false)); 
	//bind.title，通过id找view找到导航标题。public final CommonTitleLayoutVmBinding title