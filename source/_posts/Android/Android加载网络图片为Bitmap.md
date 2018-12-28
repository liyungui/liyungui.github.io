---
title: Android加载网络图片为Bitmap
date: 2018-12-10 16:56:18
tags: 
	- 图片
	- Bitmap
---

# HttpURLConnection下载

- 注意二次采样，防止OOM

		options.inJustDecodeBounds = true;
		BitmapFactory.decodeResource(getResources(), R.id.myimage, options);
 		设置为true 时，返回的BitMap 将为 Null

- 读取网络图片常用的是decodeStream，但是如果需要读取两次，第二次读的时候流已经改变，读取的是null。可以用字节数组存储流，以后可以多次使用

代码：

	public static Observable<Bitmap> getHttpBitmap(String drawableUrl, final int reqWidth, final int reqHeight) {
        return Observable
                .just(drawableUrl)
                .filter(new Func1<String, Boolean>() {
                    @Override
                    public Boolean call(String s) {
                        if (TextUtils.isEmpty(s)) {
                            return false;
                        }
                        return true;
                    }
                })
                .map(new Func1<String, Bitmap>() {
                    @Override
                    public Bitmap call(String s) {
                        try {
                            HttpURLConnection conn = (HttpURLConnection) new URL(s).openConnection();
                            //设置超时时间为6000毫秒，conn.setConnectionTiem(0);表示没有时间限制
                            conn.setConnectTimeout(6000);
                            //连接设置获得数据流
                            conn.setDoInput(true);
                            //不使用缓存
                            conn.setUseCaches(false);
                            //此方法用于在预先不知道内容长度时启用没有进行内部缓冲的 HTTP请求正文的流
                            conn.setChunkedStreamingMode(51200); // 128K
                            conn.connect();
                            InputStream is = conn.getInputStream();
                            if (is != null) {
                                BitmapFactory.Options options = new BitmapFactory.Options();
                                options.inJustDecodeBounds = true;
                                byte[] data = inputStream2ByteArr(is);
                                BitmapFactory.decodeByteArray(data, 0, data.length, options);
                                options.inSampleSize = calculateInSampleSize(options, reqWidth, reqHeight);
                                options.inJustDecodeBounds = false;
                                //解析得到图片
                                return BitmapFactory.decodeByteArray(data, 0, data.length, options);
                            }
                            is.close();
                        } catch (Exception e) {
                            throw Exceptions.propagate(e);
                        }
                        return null;
                    }
                })
                .subscribeOn(Schedulers.io());
    }

    /**
     * 输入流转成字节数组(重复读取)
     *
     * @param inputStream
     * @return
     * @throws IOException
     */

    public static byte[] inputStream2ByteArr(InputStream inputStream) throws IOException {
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        byte[] buff = new byte[1024];
        int len = 0;
        while ((len = inputStream.read(buff)) != -1) {
            outputStream.write(buff, 0, len);
        }
        inputStream.close();
        outputStream.close();
        return outputStream.toByteArray();
    }

    /**
     * 计算options.InSampleSize值 此算法可根据需求改动
     *
     * @param options
     * @param reqWidth  期望宽
     * @param reqHeight 期望高
     * @return
     */

    public static int calculateInSampleSize(BitmapFactory.Options options, int reqWidth, int reqHeight) {
        // 源图片的高度和宽度
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;
        if (height > reqHeight || width > reqWidth) {
            // 计算出实际宽高和目标宽高的比率
            final int heightRatio = Math.round((float) height / (float) reqHeight);
            final int widthRatio = Math.round((float) width / (float) reqWidth);
            // 选择宽和高中最小的比率作为inSampleSize的值，这样可以保证最终图片的宽和高
            // 一定都会大于等于目标的宽和高。
            inSampleSize = heightRatio < widthRatio ? heightRatio : widthRatio;
        }
        return inSampleSize;
    }
    
# glide

	public  void getBitmap(Context context, String uri, final GlideLoadBitmapCallback callback) {
	    Glide.with(context)
	            .load(uri)
	            .asBitmap()
	            .centerCrop()
	            .override(150, 150)
	            .into(new SimpleTarget<Bitmap>() {
	                @Override
	                public void onResourceReady(Bitmap bitmap, GlideAnimation anim) {
	                    callback.getBitmapCallback(bitmap);
	                }
	            });
	}
