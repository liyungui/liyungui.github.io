---
title: Java代码设置margin
date: 2018-08-31 18:22:53
tags: 
	- Android
	- View
---
	
api
	
	ViewGroup.MarginLayoutParams.setMargins(left, top, right, bottom)
	
	直接的子类有: 
		FrameLayout.LayoutParams, 		
		LinearLayout.LayoutParams and 
		RelativeLayout.LayoutParams.
		
创建一个MarginLayoutParams时,需要以View本身的布局参数对象为基础,否则可能丢失一些原本的布局属性. 

	/**
     * 设置某个View的margin
     *
     * @param view
     * @param leftPx
     * @param rightPx
     * @param topPx
     * @param bottomPx
     * @return
     */
    public static boolean setViewMargin(View view, int leftPx, int rightPx, int topPx, int bottomPx) {
        if (view == null) {
            return false;
        }

        ViewGroup.MarginLayoutParams marginParams = null;

        //获取view的margin设置参数
        ViewGroup.LayoutParams params = view.getLayoutParams();
        if (params instanceof ViewGroup.MarginLayoutParams) {
            marginParams = (ViewGroup.MarginLayoutParams) params;
        } else {
            //不存在时创建一个新的参数
            marginParams = new ViewGroup.MarginLayoutParams(params);
        }

        //设置margin
        marginParams.setMargins(leftPx, topPx, rightPx, bottomPx);
        view.setLayoutParams(marginParams);

        return true;
    }
	