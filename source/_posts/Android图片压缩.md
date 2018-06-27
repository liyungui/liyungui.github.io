---
title: Android图片压缩
date: 2018-06-11 15:03:18
tags: 图片
---

# 内存大小 #

**色彩模式**是数字世界中表示颜色的一种算法，在Bitmap里用Config来表示。

颜色默认是 RGB，三原色各占8位，共计24位，即3个字节

	颜色值0-255，8位刚好能标示一种颜色

BitmapFactory.Options 设置图像的色彩模式，共有4种取值

	ARGB_8888，表示一个像素点的透明度以及三原色各占8位，共计32位，即4个字节
    ALPHA_8，表示一个像素点只有透明度，没有三原色，此时，一个像素点占8位，即1个字节
    ARGB_4444，表示一个像素点的透明度以及三原色各占4位，共计16位，即2个字节
    RGB_565，这种色彩模式不能表示透明度，红绿蓝三色各占5、6、6位，共计16位，即2个字节

Bitmap的计算方式

	memory=scaledWidth*scaledHeight*每个像素所占字节数

		scaledWidth :  widthtargetDensity/density+0.5
		scaledHeight： heighttargetDensity/density+0.5

			targetDensity表示手机的像素密度,这个值一般跟手机相关,
			density表示decodingBitmap 的 density,这个值一般跟图片放置的目录有关(hdpi/xxhdpi)

**Bitmap获取内存占用大小的API**

- getByteCount()：API12 加入，代表存储 Bitmap 的像素需要的最少内存。
- getAllocationByteCount()：API19 加入，代表在内存中为 Bitmap 分配的内存大小，代替了 getByteCount() 方法。


两者的区别:

在不复用 Bitmap 时，getByteCount() 和 getAllocationByteCount 返回的结果是一样的。

在通过复用 Bitmap 来解码图片时，那么 getByteCount() 表示新解码图片占用内存的大小，getAllocationByteCount() 表示被复用 Bitmap真实占用的内存大小（即 mBuffer 的长度）。

早期的Android平台下,对一张图片进行多次质量压缩,会得到一张**变绿**的图片

假设客户端需要加载一张图片，图片尺寸为3000*3000（像素）,如果客户端显示原图，按一个像素四个字节算(argb)， 

3000 * 3000 * 4 / 1024 / 1024 = 34 M，

客户端一个应用程序的运行内存就16M,你一下显示一个30多M的图片，直接 OOM crash了。

# 图片压缩方式 #

## 质量压缩 ##

不会改变图像的宽高，降低图像的质量，从而降低存储大小

	bitmap.compress(Bitmap.CompressFormat.JPEG, 100, outputStream);

		压缩格式,它有JPEG、PNG、WEBP三种选择，JPEG是有损压缩，PNG是无损压缩，WEBP是Google推出的图像格式(会存在兼容性的问题).一般会选择JPEG
		quality：0~100可选，数值越大，质量越高，图像越大。

## 尺寸压缩 ##

尺寸压缩本质上就是一个重新采样的过程，放大图像称为上采样，缩小图像称为下采样

Android提供了两种图像采样方法，邻近采样和双线性采样。

**采样效果 从低到高依次：**

### 邻近采样 ###

采用邻近点插值算法，用一个像素点代替邻近的像素点

	BitmapFactory.Options options = new BitmapFactory.Options();
	options.inSampleSize = 2
	Bitmap bitmap = BitmapFactory.decodeFile("/sdcard/test.png");
	Bitmap compress = BitmapFactory.decodeFile("/sdcard/test.png", options);

	options.inSampleSize = 2;一个像素点会代替原来的2个像素点
		注意这里的2个像素点仅仅指水平方向或者竖直方向上的。
		即原来2x2的像素,压缩后仅使用一个像素点来代替

**压缩前红绿相间的图片,经过压缩后,完全变成了绿色**.这时因为邻近点插值算法直接选择其中一个像素作为生成像素,另外一个像素直接抛弃,这样才会造成图片变成纯绿色的情况。

邻近采样的方法有些**暴力**,Android平台提供了另一种尺寸压缩方案

### 双线性采样 ###

采用双线性插值算法，相比邻近采样简单粗暴的选择一个像素点代替其他像素点，双线性采样参考源像素相应位置周围2x2个点的值，根据相对位置取对应的权重，经过计算得到目标图像。

	Bitmap bitmap = BitmapFactory.decodeFile("/sdcard/test.png");
	Bitmap compress = Bitmap.createScaledBitmap(bitmap, bitmap.getWidth()/2, bitmap.getHeight()/2, true);
	
	或者
	Bitmap bitmap = BitmapFactory.decodeFile("/sdcard/test.png");
	Matrix matrix = new Matrix();
	matrix.setScale(0.5f, 0.5f);
	bm = Bitmap.createBitmap(bitmap, 0, 0, bit.getWidth(), bit.getHeight(), matrix, true);


压缩后的图片不会像邻近采样那般只有纯粹的一种颜色,而是参考了像素源周围2x2个点的像素，并取其权重得到目标图像。

双线性采样相比邻近采样而言,图片的保真度会高些,但压缩的速率不及前者,因为前者不需要计算直接选择了其中一个像素作为生成像素。

#### 二次采样 ####

**`二次采样`** 二次设置图片采样比率，达到减小加载图片所需内存空间

步骤： 

	第一次采样：
		第一次解码,只获取图片的尺寸(不会占用太多内存)，不进行实际的Bitmap创建。
	
	计算采样率：根据图片宽高，以及客户端希望图片加载后的尺寸

	第二次采样：
		
		给BitmapFactory设置采样率，加载Bitmap到内存

`BitmapFactory.Options` 参数说明

	In开头的：用于给解码器传递参数 
	
		inSampleSize 

	Out开头的：用于从解码器获取结果

		options.outMimeType; // 图片类型 "image/png"

		
代码实例：

	public static Bitmap decodeSampledBitmapFromResource(Resources res, int resId,
	        int reqWidth, int reqHeight) {
	    final BitmapFactory.Options options = new BitmapFactory.Options();
	    options.inJustDecodeBounds = true; //是否只加载图片的边框
	    BitmapFactory.decodeResource(res, resId, options); //加载图片，此时加载只能够获取到图片的边框
	
	    // 计算inSampleSize
	    options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);
	
	    options.inJustDecodeBounds = false;
	    // 加载压缩版图片
	    return BitmapFactory.decodeResource(res, resId, options);
	}


	//google推荐算法：以对角线的方式进行缩放比率的计算
	public static int calculateInSampleSize(BitmapFactory.Options options, int reqWidth, int reqHeight) {
        // 图片原始宽高
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;

        //只有当请求的宽度、高度 > 0时，进行缩放。否则，图片不进行缩放
        if(reqHeight > 0 && reqWidth > 0){
            if (height > reqHeight || width > reqWidth) {

                final int halfHeight = height / 2;
                final int halfWidth = width / 2;

				//计算一个最大的缩放比例（采样比率，2的n次幂），保证缩放后的宽高大于要求的宽高
                while ((halfHeight / inSampleSize) > reqHeight && (halfWidth / inSampleSize) > reqWidth) {
                    inSampleSize *= 2;
                }
            }
        }
        return inSampleSize;
    }

特别注意：

二次采样后获得的图片宽高并不是完全吻合控件宽高，还是需要设置ScaleType来适应

二次采样只是为了解决图片OOM

### 双立方／双三次采样 (Android原生不支持) ###

双立方／双三次采样使用的是双立方／双三次插值算法。双立方／双三次插值算法参考了源像素某点周围 4x4 个像素。

双立方/双三次插值算法经常用于图像或者视频的缩放，它能比双线性内插值算法保留更好的细节质量。

双立方／双三次插值算法在平时的软件中是很常用的一种图片处理算法，但是这个算法有一个缺点就是计算量会相对比较大，是前三种算法中计算量最大的，软件 photoshop 中的图片缩放功能使用的就是这个算法。

### Lanczos 采样 (原生不支持) ###

Lanczos 采样和 Lanczos 过滤是 Lanczos 算法的两种常见应用，它可以用作低通滤波器或者用于平滑地在采样之间插入数字信号，Lanczos 采样一般用来增加数字信号的采样率，或者间隔采样来降低采样率。

采样效果对比参考：腾讯音乐技术团队[Android中图片压缩分析（下）](https://mp.weixin.qq.com/s/H9Tz1n4O2-Aawgu7p-XL5w)。总的来说，上采样和对二值化图片(黑白)的处理表现差异特别明显


    