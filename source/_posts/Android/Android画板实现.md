---
title: Android画板实现
date: 2018-11-14 17:54:53
tags:
	- View
	- Canvas
---

# 原理

使用Canvas

绘制图形有两种方式：

- 直接画，drawXXX: drawLine,drawCircle
- 通过path画，drawPath(Path path, Paint paint)

## 贝塞尔曲线

三要素：起点，终点，控制点(决定曲线的弯曲程度)

- 一阶：起点，终点，没有控制点
- 二阶：起点，终点，一个控制点
- 二阶：起点，终点，两个控制点

# 两种实现方式

- 自定义View
	- 复写onDraw(Canvas canvas)
	- 复写onTouchEvent(MotionEvent event)
- 使用ImageView
	- 用Canvas绘制一张空的Bitmap，通过ImageView的setImageBitmap()方法加载这个Bitmap
	- setOnTouchListener()

## 自定义View

完整实现即用的是自定义View

## 使用ImageView实现绘制直线

不断绘制直线(折现)。

可以使用二阶贝塞尔曲线绘制(以起点和终点的中点作为控制点)，效果更加平滑

	private void showImage() {
        // 创建一张空白图片
        mBitmap = Bitmap.createBitmap(720, 1280, Bitmap.Config.ARGB_8888);
        // 创建一张画布
        canvas = new Canvas(mBitmap);
        // 画布背景为白色
        canvas.drawColor(Color.WHITE);
        // 创建画笔
        paint = new Paint();
        // 画笔颜色为蓝色
        paint.setColor(Color.BLUE);
        // 宽度5个像素
        paint.setStrokeWidth(5);
        // 先将白色背景画上
        canvas.drawBitmap(mBitmap, new Matrix(), paint);
        img.setImageBitmap(mBitmap);//展示白色背景图

        img.setOnTouchListener(new View.OnTouchListener() {
            int startX;
            int startY;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        // 获取手按下时的坐标
                        startX = (int) event.getX();
                        startY = (int) event.getY();
                        break;
                    case MotionEvent.ACTION_MOVE:
                        // 获取手移动后的坐标
                        int endX = (int) event.getX();
                        int endY = (int) event.getY();
                        // 在开始和结束坐标间画一条线
                        canvas.drawLine(startX, startY, endX, endY, paint);
                        // 刷新开始坐标
                        startX = (int) event.getX();
                        startY = (int) event.getY();
                        img.setImageBitmap(mBitmap);
                        break;
                }
                return true;
            }
        });
    }
    
#	完整实现

功能：

- 支持撤销（undo）；
- 支持反撤销（redo）；
- 支持橡皮擦（eraser）；
- 支持清除功能（clear）；
- 支持保存为图像（save）。
	
[GitHub](https://github.com/wensefu/android-palette)

## 原理分析

### 思路

- 绘制：考虑到性能问题，使用了双缓冲绘图技术。
- 撤销功能：在画轨迹时，记录每一步的轨迹和画笔属性，每次撤销时把最后一步删除，然后重绘；
- 反撤销功能：撤销时把撤销的轨迹和画笔属性保存在另一个列表里，反撤销时从这个列表里取出来放到记录绘制信息的列表里，然后重绘；
- 橡皮擦功能：应用到android的图象混合（Xfermode）知识
- 清除功能：清除屏上的像素记录即可；

### android的图象混合（Xfermode）

图象混合本质上用一句话解释就是：

	按照某种算法将画布上你将要绘制的区域的每个像素的ARGB和你将要在这个区域绘制的ARGB进行组合变换。

Xfermode有三个子类，两个在API 16上已经过时了，现在最常用的是PorterDuffXfermode，目前支持18种图像混合算法，分别产生不同的混合效果，做橡皮擦功能用到了CLEAR算法(PorterDuff.Mode.CLEAR,将绘制区域的所有像素点ARGB全部置0，显示activity的背景色，没设置默认为黑色背景)，其他算法的效果大家有兴趣可以参考google官方的介绍

需要注意的是，Xfermode的某些算法不支持硬件加速

### android双缓冲绘图技术

所谓缓冲，简单地说就是将**多个将要执行的独立的任务集结起来**，一起提交。

打个比方，现实生活中，你现在要将很多砖从A处搬到B处，原始的方法是徒手一次搬几块，这就是没有使用“缓存”的方法。你也可以用一辆拖车，先把砖搬到拖车上，再把拖车拉到B处，这就是使用了“缓存”的方法。

每个canvas都有对应的一个bitmap，绘图的过程实际上就是往这个bitmap上写入ARGB信息，然后把这些信息交给GPU进行显示。这里面其实已经包含了一次缓冲的过程(**显示缓冲**)。

绘图时的双缓冲其实就是再增加一个canvas，把想要绘制的内容先绘制到这个增加的canvas对应的bitmap上，写完后再把这个bitmap的ARGB信息一次提交给上下文的canvas去绘制。

双缓冲技术在绘制数据量较大时在性能上有明显的提升，画板程序之所以用到了双缓存，也是基于提高绘制效率的考虑。


#### 显示缓冲的验证

	@Override
    protected void onDraw(Canvas canvas) {
        canvas.drawRect(rect,mPaint);
        try {
            TimeUnit.MILLISECONDS.sleep(2000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        canvas.drawCircle(cx,cy,100,mPaint);
    }
    两个几乎同时一起显示出来的。
    这就说明必须要等onDraw方法执行完成之后，才会把数据交给GPU去处理展示。
    这就是android绘图当中的第一道缓冲，即显示缓冲区。

#### 双缓冲

- 再创建一个Canvas和对应的Bitmap
- 在onDraw方法里默认的Canvas通过drawBitmap画bitmap从而实现双缓冲。

用代码简单的表述是这样的：

	private void init(){
	    Bitmap bufferBm = Bitmap.create(getWidth,getHeight,Bitmap.Config.ARGB_8888);
	    Canvas bufferCanvas = new Canvas(bufferBm);
	}
	
	private void drawSomething(){
	    bufferCanvas.drawRect();
	    bufferCanvas.drawCircle();
	    ...
	    invalidate();
	}
	
	@Override
	protected void onDraw(Canvas canvas) {
	    canvas.drawBitmap(bufferBm,0,0,null);
	}

{% asset_img 双缓冲.png %}

#### 双缓冲绘图的优缺点及适用场景

使用双缓冲会增加内存消耗。

- 在绘制数据量较小时，不使用双缓冲，GPU的负荷更低，即绘制性能更高；
- 在绘制数据量较大时，使用双缓冲绘图，绘制性能明显高于不使用双缓冲的情况；

**实例验证：自定义View,每次点击在点击处画一个圆**

实验之前，先打开开发者选项里的”GPU呈现模式分析“，设置为“在屏幕上显示为条形图”

不用双缓冲的代码：

	public class MyView extends View{
	
	    private Paint mPaint;
	    private List<Point> mPoints;
	
	    public MyView(Context context) {
	        super(context);
	    }
	
	    public MyView(Context context, AttributeSet attrs) {
	        super(context, attrs);
	        mPaint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.DITHER_FLAG);
	        mPaint.setStyle(Paint.Style.FILL);
	        mPaint.setColor(Color.GREEN);
	        setBackgroundColor(Color.WHITE);
	        mPoints = new ArrayList<>();
	    }
	
	    @Override
	    public boolean onTouchEvent(MotionEvent event) {
	        int action = event.getAction();
	        switch (action){
	            case MotionEvent.ACTION_DOWN:
	                mPoints.add(new Point((int)event.getX(),(int)event.getY()));
	                break;
	            case MotionEvent.ACTION_UP:
	                invalidate();
	                break;
	        }
	        return true;
	    }
	
	    @Override
	    protected void onDraw(Canvas canvas) {
	        for (Point p : mPoints) {
	            canvas.drawCircle(p.x,p.y,50,mPaint);
	        }
	    }
	}

双缓冲代码如下：

	public class MyView extends View{
	
	    private Paint mPaint;
	    private Canvas mBufferCanvas;
	    private Bitmap mBufferBitmap;
	
	    public MyView(Context context) {
	        super(context);
	    }
	
	    public MyView(Context context, AttributeSet attrs) {
	        super(context, attrs);
	        mPaint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.DITHER_FLAG);
	        mPaint.setStyle(Paint.Style.FILL);
	        mPaint.setColor(Color.GREEN);
	        setBackgroundColor(Color.WHITE);
	    }
	
	    @Override
	    public boolean onTouchEvent(MotionEvent event) {
	        int action = event.getAction();
	        switch (action){
	            case MotionEvent.ACTION_DOWN:
	                if (mBufferBitmap == null) {
	                    mBufferBitmap = Bitmap.createBitmap(getWidth(),getHeight(), Bitmap.Config.ARGB_8888);
	                    mBufferCanvas = new Canvas(mBufferBitmap);
	                }
	                mBufferCanvas.drawCircle((int)event.getX(),(int)event.getY(),50,mPaint);
	                break;
	            case MotionEvent.ACTION_UP:
	                invalidate();
	                break;
	        }
	        return true;
	    }
	
	    @Override
	    protected void onDraw(Canvas canvas) {
	        if (mBufferBitmap == null) {
	            return;
	        }
	        canvas.drawBitmap(mBufferBitmap,0,0,null);
	    }
	}

## 关键代码

非常简短，只有200来行

	package com.shensz.course.module.main.screen.liveroom.component;
	
	import android.content.Context;
	import android.content.res.Resources;
	import android.graphics.Bitmap;
	import android.graphics.Canvas;
	import android.graphics.Color;
	import android.graphics.Paint;
	import android.graphics.Path;
	import android.graphics.PorterDuff;
	import android.graphics.PorterDuffXfermode;
	import android.graphics.Xfermode;
	import android.support.annotation.Nullable;
	import android.util.AttributeSet;
	import android.util.DisplayMetrics;
	import android.util.TypedValue;
	import android.view.MotionEvent;
	import android.view.View;
	
	import java.util.ArrayList;
	import java.util.List;
	
	public class PaletteView extends View {
	
	    private Paint mPaint;
	    private Path mPath;
	    private float mLastX;
	    private float mLastY;
	    private Bitmap mBufferBitmap;
	    private Canvas mBufferCanvas;
	
	    private static final int MAX_CACHE_STEP = 20;
	
	    private List<DrawingInfo> mDrawingList;
	    private List<DrawingInfo> mRemovedList;
	
	    private Xfermode mXferModeClear;
	    private Xfermode mXferModeDraw;
	    private int mDrawSize;
	    private int mEraserSize;
	    private int mPenAlpha = 255;
	
	    private boolean mCanEraser;
	
	    private Callback mCallback;
	
	    public enum Mode {
	        DRAW,
	        ERASER
	    }
	
	    private Mode mMode = Mode.DRAW;
	
	
	    public PaletteView(Context context) {
	        super(context);
	        init();
	    }
	
	    public PaletteView(Context context, @Nullable AttributeSet attrs) {
	        super(context, attrs);
	        init();
	    }
	
	    public PaletteView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
	        super(context, attrs, defStyleAttr);
	        init();
	    }
	
	    public interface Callback {
	        void onUndoRedoStatusChanged();
	    }
	
	    public void setCallback(Callback callback) {
	        mCallback = callback;
	    }
	
	    public static class DimenUtils {
	
	        private static final Resources sResource = Resources.getSystem();
	
	        public static float dp2px(float dp) {
	            DisplayMetrics dm = sResource.getDisplayMetrics();
	            return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, dp, dm);
	        }
	
	        public static int dp2pxInt(float dp) {
	            return (int) dp2px(dp);
	        }
	
	        public static float sp2px(float sp) {
	            DisplayMetrics dm = sResource.getDisplayMetrics();
	            return TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, sp, dm);
	        }
	
	        public static int sp2pxInt(float sp) {
	            return (int) sp2px(sp);
	        }
	
	
	    }
	
	    private void init() {
	        setDrawingCacheEnabled(true);
	        mPaint = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.DITHER_FLAG);
	        mPaint.setStyle(Paint.Style.STROKE);
	        mPaint.setFilterBitmap(true);
	        mPaint.setStrokeJoin(Paint.Join.ROUND);
	        mPaint.setStrokeCap(Paint.Cap.ROUND);
	        mDrawSize = DimenUtils.dp2pxInt(3);
	        mEraserSize = DimenUtils.dp2pxInt(30);
	        mPaint.setStrokeWidth(mDrawSize);
	        mPaint.setColor(0XFF000000);
	        mXferModeDraw = new PorterDuffXfermode(PorterDuff.Mode.SRC);
	        mXferModeClear = new PorterDuffXfermode(PorterDuff.Mode.CLEAR);
	        mPaint.setXfermode(mXferModeDraw);
	    }
	
	    private void initBuffer() {
	        mBufferBitmap = Bitmap.createBitmap(getWidth(), getHeight(), Bitmap.Config.ARGB_8888);
	        mBufferCanvas = new Canvas(mBufferBitmap);
	    }
	
	    private abstract static class DrawingInfo {
	        Paint paint;
	
	        abstract void draw(Canvas canvas);
	    }
	
	    private static class PathDrawingInfo extends DrawingInfo {
	
	        Path path;
	
	        @Override
	        void draw(Canvas canvas) {
	            canvas.drawPath(path, paint);
	        }
	    }
	
	    public Mode getMode() {
	        return mMode;
	    }
	
	    public void setMode(Mode mode) {
	        if (mode != mMode) {
	            mMode = mode;
	            if (mMode == Mode.DRAW) {
	                mPaint.setXfermode(mXferModeDraw);
	                mPaint.setStrokeWidth(mDrawSize);
	            } else {
	                mPaint.setXfermode(mXferModeClear);
	                mPaint.setStrokeWidth(mEraserSize);
	            }
	        }
	    }
	
	    public void setEraserSize(int size) {
	        mEraserSize = size;
	    }
	
	    public void setPenRawSize(int size) {
	        mDrawSize = size;
	        if (mMode == Mode.DRAW) {
	            mPaint.setStrokeWidth(mDrawSize);
	        }
	    }
	
	    public void setPenColor(int color) {
	        mPaint.setColor(color);
	    }
	
	    private void reDraw() {
	        if (mDrawingList != null) {
	            mBufferBitmap.eraseColor(Color.TRANSPARENT);
	            for (DrawingInfo drawingInfo : mDrawingList) {
	                drawingInfo.draw(mBufferCanvas);
	            }
	            invalidate();
	        }
	    }
	
	    public int getPenColor() {
	        return mPaint.getColor();
	    }
	
	    public int getPenSize() {
	        return mDrawSize;
	    }
	
	    public int getEraserSize() {
	        return mEraserSize;
	    }
	
	    public void setPenAlpha(int alpha) {
	        mPenAlpha = alpha;
	        if (mMode == Mode.DRAW) {
	            mPaint.setAlpha(alpha);
	        }
	    }
	
	    public int getPenAlpha() {
	        return mPenAlpha;
	    }
	
	    public boolean canRedo() {
	        return mRemovedList != null && mRemovedList.size() > 0;
	    }
	
	    public boolean canUndo() {
	        return mDrawingList != null && mDrawingList.size() > 0;
	    }
	
	    public void redo() {
	        int size = mRemovedList == null ? 0 : mRemovedList.size();
	        if (size > 0) {
	            DrawingInfo info = mRemovedList.remove(size - 1);
	            mDrawingList.add(info);
	            mCanEraser = true;
	            reDraw();
	            if (mCallback != null) {
	                mCallback.onUndoRedoStatusChanged();
	            }
	        }
	    }
	
	    public void undo() {
	        int size = mDrawingList == null ? 0 : mDrawingList.size();
	        if (size > 0) {
	            DrawingInfo info = mDrawingList.remove(size - 1);
	            if (mRemovedList == null) {
	                mRemovedList = new ArrayList<>(MAX_CACHE_STEP);
	            }
	            if (size == 1) {
	                mCanEraser = false;
	            }
	            mRemovedList.add(info);
	            reDraw();
	            if (mCallback != null) {
	                mCallback.onUndoRedoStatusChanged();
	            }
	        }
	    }
	
	    public void clear() {
	        if (mBufferBitmap != null) {
	            if (mDrawingList != null) {
	                mDrawingList.clear();
	            }
	            if (mRemovedList != null) {
	                mRemovedList.clear();
	            }
	            mCanEraser = false;
	            mBufferBitmap.eraseColor(Color.TRANSPARENT);
	            invalidate();
	            if (mCallback != null) {
	                mCallback.onUndoRedoStatusChanged();
	            }
	        }
	    }
	
	    public Bitmap buildBitmap() {
	        Bitmap bm = getDrawingCache();
	        Bitmap result = Bitmap.createBitmap(bm);
	        destroyDrawingCache();
	        return result;
	    }
	
	    private void saveDrawingPath() {
	        if (mDrawingList == null) {
	            mDrawingList = new ArrayList<>(MAX_CACHE_STEP);
	        } else if (mDrawingList.size() == MAX_CACHE_STEP) {
	            mDrawingList.remove(0);
	        }
	        Path cachePath = new Path(mPath);
	        Paint cachePaint = new Paint(mPaint);
	        PathDrawingInfo info = new PathDrawingInfo();
	        info.path = cachePath;
	        info.paint = cachePaint;
	        mDrawingList.add(info);
	        mCanEraser = true;
	        if (mCallback != null) {
	            mCallback.onUndoRedoStatusChanged();
	        }
	    }
	
	    @Override
	    protected void onDraw(Canvas canvas) {
	        super.onDraw(canvas);
	        if (mBufferBitmap != null) {
	            canvas.drawBitmap(mBufferBitmap, 0, 0, null);
	        }
	    }
	
	    @SuppressWarnings("all")
	    @Override
	    public boolean onTouchEvent(MotionEvent event) {
	        if(!isEnabled()){
	            return false;
	        }
	        final int action = event.getAction() & MotionEvent.ACTION_MASK;
	        final float x = event.getX();
	        final float y = event.getY();
	        switch (action) {
	            case MotionEvent.ACTION_DOWN:
	                mLastX = x;
	                mLastY = y;
	                if (mPath == null) {
	                    mPath = new Path();
	                }
	                mPath.moveTo(x,y);
	                break;
	            case MotionEvent.ACTION_MOVE:
	                //这里终点设为两点的中心点的目的在于使绘制的曲线更平滑，如果终点直接设置为x,y，效果和lineto是一样的,实际是折线效果
	                mPath.quadTo(mLastX, mLastY, (x + mLastX) / 2, (y + mLastY) / 2);
	                if (mBufferBitmap == null) {
	                    initBuffer();
	                }
	                if (mMode == Mode.ERASER && !mCanEraser) {
	                    break;
	                }
	                mBufferCanvas.drawPath(mPath,mPaint);
	                invalidate();
	                mLastX = x;
	                mLastY = y;
	                break;
	            case MotionEvent.ACTION_UP:
	                if (mMode == Mode.DRAW || mCanEraser) {
	                    saveDrawingPath();
	                }
	                mPath.reset();
	                break;
	        }
	        return true;
	    }
	}

# [Android电子白板](https://blog.csdn.net/u013491946/article/details/77983405)

基本思路是在画板上确认两个点，一个起点，一个终点，根据选择的图形样式，拖动的时候有预览图形，松开时图形定下来显示到画板上。

功能

- 曲线，直线，矩形，正方形，圆，椭圆
- 橡皮檫功能，
- 筛选相册图片显示到画板

利用canvas.drawXXX 实现图形绘制