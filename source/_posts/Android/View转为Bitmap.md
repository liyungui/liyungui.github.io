---
title: View转为Bitmap
date: 2018-06-07 15:54:53
tags:
	- View
	- Bitmap
	- Canvas
---

# 方法一:view.getDrawingCache() #

适用于View显示在界面上的情况。可以被完全遮挡住，只要android:visibility="visible"就可以

	public Bitmap convertViewToBitmap(View view){
	
		view.setDrawingCacheEnabled(true); ////启用DrawingCache
		
		view.buildDrawingCache(); //创建位图
		
		Bitmap bitmap=Bitmap.createBitmap(view.getDrawingCache()); ////创建一个DrawingCache的拷贝，因为DrawingCache得到的位图在禁用后会被回收
		
		view.setDrawingCacheEnabled(false);  //禁用DrawingCahce否则会影响性能

		return bitmap;
	
	}

## 返回的Bitmap为null或生成Bitmap全黑色 ##

主要原因是drawingCache的值大于系统给定的值，buildDrawingCache()失败

	if (width <= 0 || height <= 0 ||(width * height * (opaque && !translucentWindow ? 2 : 4) > ViewConfiguration.get(mContext).getScaledMaximumDrawingCacheSize())) {   
         destroyDrawingCache();   
         return;   
  	}  

解决方案：

	public static Bitmap convertViewToBitmap(View view){
		view.measure(MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED), MeasureSpec.makeMeasureSpec(0, MeasureSpec.UNSPECIFIED));
		view.layout(0, 0, view.getMeasuredWidth(), view.getMeasuredHeight());
		view.buildDrawingCache();
		Bitmap bitmap = view.getDrawingCache();
		return bitmap;
	}


# 方法二:View.draw(Canvas canvas) #

从源码中可以看到buildDrawingCache就是获得View的Canvas然后画到bitmap上，直接返回对应的bitmap。有些同学就直接将View画到bitmap

**个人不推荐使用**。因为系统buildDrawingCache考虑的因素很多，比如透明磁，大小 ，图片质量等；还有重新定位到当前可显示的区域(这点很重要，如果有可滚动的控件，不重定位是无法正确得到Bitmap的，比如ViewPager第二页，手动draw就会出问题)

	public static Bitmap convertViewToBitmap(View view) {  
	    Bitmap bitmap= Bitmap.createBitmap(view.getWidth(), view.getHeight(), HDConstantSet.BITMAP_QUALITY);  
	    Canvas canvas = new Canvas(bitmap);  
	    view.draw(canvas);  
	    return bitmap;  
	}
	
	public static Bitmap loadBitmapFromView(View v) {
     Bitmap b = Bitmap.createBitmap( v.getLayoutParams().width, v.getLayoutParams().height, Bitmap.Config.ARGB_8888);                
     Canvas c = new Canvas(b);
     v.layout(0, 0, v.getLayoutParams().width, v.getLayoutParams().height);
     v.draw(c);
     return b;
}


## View没有显示在界面上的情况 ##

通过java代码创建的或者inflate创建的View，是获取不到Bitmap的。

因为View在添加到容器中之前并没有得到实际的大小，需要先指定View的大小

	public static Bitmap convertViewToBitmap(View view) {  
		layoutView(view);//必须measure和layout。否则宽高都为0，报错 java.lang.IllegalArgumentException: width and height must be > 0
	    Bitmap bitmap= Bitmap.createBitmap(view.getWidth(), view.getHeight(), Bitmap.Config.ARGB_8888);  
	    Canvas canvas = new Canvas(bitmap);  
	    view.draw(canvas);  
	    return bitmap;  
	}

    private void layoutView(View v) {
		DisplayMetrics metric = new DisplayMetrics();
        getWindowManager().getDefaultDisplay().getMetrics(metric);
        int width = metric.widthPixels;     // 屏幕宽度（像素）
        int height = metric.heightPixels;   // 屏幕高度（像素）
        v.layout(0, 0, width, height);
        int measuredWidth = View.MeasureSpec.makeMeasureSpec(width, View.MeasureSpec.EXACTLY);
        int measuredHeight = View.MeasureSpec.makeMeasureSpec(10000, View.MeasureSpec.AT_MOST);
        v.measure(measuredWidth, measuredHeight);
        v.layout(0, 0, v.getMeasuredWidth(), v.getMeasuredHeight());
    }



