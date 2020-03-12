---
title: pcm 转 amr
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

[pcm 转 amr](http://blog.csdn.net/honeybaby201314/article/details/50379040)

[Android中Pcm文件转Amr文件](https://www.zybuluo.com/DevWiki/note/115307)

Android系统自带的AmrInputStream类可以转换pcm到amr

# 思路一、反射调用 #

- 通过Android系统自带的AmrInputStream类转换，因为它被隐藏了，只有通过反射来操作。
- 手动加上 `amr文件头`，`byte[] header = new byte[]{0x23, 0x21, 0x41, 0x4D, 0x52, 0x0A};`

## 代码实现 ##

	 /**
	 * 通过反射调用android系统自身AmrInputStream类进行转换
	 * @param inPath 源文件
	 * @param outPath 目标文件
	 */
	public void systemPcm2Amr(String inPath,String outPath){
		try {
			FileInputStream fileInputStream = new FileInputStream(inPath);
			FileOutputStream fileoutputStream = new FileOutputStream(outPath);
			// 获得Class
			Class<?> cls = Class.forName("android.media.AmrInputStream");
			// 通过Class获得所对应对象的方法
			Method[] methods = cls.getMethods();
			// 输出每个方法名
			byte[] header = new byte[]{0x23, 0x21, 0x41, 0x4D, 0x52, 0x0A};
			fileoutputStream.write(header);
			Constructor<?> con = cls.getConstructor(InputStream.class);
			Object obj = con.newInstance(fileInputStream);
			for (Method method : methods) {
				Class<?>[] parameterTypes = method.getParameterTypes();
				if ("read".equals(method.getName())
						&& parameterTypes.length == 3) {
					byte[] buf = new byte[1024];
					int len = 0;
					while ((len = (int) method.invoke(obj, buf, 0, 1024)) > 0) {
						fileoutputStream.write(buf, 0, len);
					}
					break;
				}
			}
			for (Method method : methods) {
				if ("close".equals(method.getName())) {
					method.invoke(obj);
					break;
				}
			}
			fileoutputStream.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

## 注意 ##

查看源码可知，AmrInputStream 转码默认 PCM 的采样率是 8000 Hz，所以要**保证录制时采样率是8000Hz**，否则amr音频会有快放和慢放的效果

	public class AmrInputStream extends InputStream {      
	    ... 
	    // frame is 20 msec at 8.000 khz  
	    private final static int SAMPLES_PER_FRAME = 8000 * 20 / 1000;  

在华为机型上，反射调用特别的慢，容易AR

# 思路二、复制类文件到工程 #

不用反射，更加高效

工程下新建包 `android.media`。因为调用Android自带的Pcm转amr的库:media_jni.so需要这个包名

复制AmrInputStream类到该包下

	public final class AmrInputStream extends InputStream {
	    static {
	        System.loadLibrary("media_jni");
	    }
	    private final static String TAG = "AmrInputStream";
	    // frame is 20 msec at 8.000 khz
	    private final static int SAMPLES_PER_FRAME = 8000 * 20 / 1000;
	    // pcm input stream
	    private InputStream mInputStream;
	    // native handle
	    private int mGae;
	    // result amr stream
	    private byte[] mBuf = new byte[SAMPLES_PER_FRAME * 2];
	    private int mBufIn = 0;
	    private int mBufOut = 0;
	    // helper for bytewise read()
	    private byte[] mOneByte = new byte[1];
	    /**
	     * Create a new AmrInputStream, which converts 16 bit PCM to AMR
	     * @param inputStream InputStream containing 16 bit PCM.
	     */
	    public AmrInputStream(InputStream inputStream) {
	        mInputStream = inputStream;
	        mGae = GsmAmrEncoderNew();
	        GsmAmrEncoderInitialize(mGae);
	    }
	    @Override
	    public int read() throws IOException {
	        int rtn = read(mOneByte, 0, 1);
	        return rtn == 1 ? (0xff & mOneByte[0]) : -1;
	    }
	    @Override
	    public int read(byte[] b) throws IOException {
	        return read(b, 0, b.length);
	    }
	    @Override
	    public int read(byte[] b, int offset, int length) throws IOException {
	        if (mGae == 0) throw new IllegalStateException("not open");
	        // local buffer of amr encoded audio empty
	        if (mBufOut >= mBufIn) {
	            // reset the buffer
	            mBufOut = 0;
	            mBufIn = 0;
	            // fetch a 20 msec frame of pcm
	            for (int i = 0; i < SAMPLES_PER_FRAME * 2; ) {
	                int n = mInputStream.read(mBuf, i, SAMPLES_PER_FRAME * 2 - i);
	                if (n == -1) return -1;
	                i += n;
	            }
	            // encode it
	            mBufIn = GsmAmrEncoderEncode(mGae, mBuf, 0, mBuf, 0);
	        }
	        // return encoded audio to user
	        if (length > mBufIn - mBufOut) length = mBufIn - mBufOut;
	        System.arraycopy(mBuf, mBufOut, b, offset, length);
	        mBufOut += length;
	        return length;
	    }
	    @Override
	    public void close() throws IOException {
	        try {
	            if (mInputStream != null) mInputStream.close();
	        } finally {
	            mInputStream = null;
	            try {
	                if (mGae != 0) GsmAmrEncoderCleanup(mGae);
	            } finally {
	                try {
	                    if (mGae != 0) GsmAmrEncoderDelete(mGae);
	                } finally {
	                    mGae = 0;
	                }
	            }
	        }
	   }
	    @Override
	    protected void finalize() throws Throwable {
	        if (mGae != 0) {
	            close();
	            throw new IllegalStateException("someone forgot to close AmrInputStream");
	        }
	    }
	    //
	    // AudioRecord JNI interface
	    //
	    private static native int GsmAmrEncoderNew();
	    private static native void GsmAmrEncoderInitialize(int gae);
	    private static native int GsmAmrEncoderEncode(int gae,
	           byte[] pcm, int pcmOffset, byte[] amr, int amrOffset) throws IOException;
	    private static native void GsmAmrEncoderCleanup(int gae);
	    private static native void GsmAmrEncoderDelete(int gae);
	}

复制AmrEncoder类

	public class AmrEncoder {
	    public static void pcm2Amr(String pcmPath , String amrPath) {
	        FileInputStream fis;
	        try {
	            fis = new FileInputStream(pcmPath);
	            pcm2Amr(fis, amrPath);
	            fis.close();
	        } catch (FileNotFoundException e1) {
	            e1.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }
	    }
	    public static void pcm2Amr(InputStream pcmStream, String amrPath) {
	        try {
	            AmrInputStream ais = new AmrInputStream(pcmStream);
	            OutputStream out = new FileOutputStream(amrPath);
	            byte[] buf = new byte[4096];
	            int len = -1;
	            /*
	             * 下面的AMR的文件头,缺少这几个字节是不行的
	             */
	            out.write(0x23);
	            out.write(0x21);
	            out.write(0x41);
	            out.write(0x4D);
	            out.write(0x52);
	            out.write(0x0A);   
	            while((len = ais.read(buf)) >0){
	                out.write(buf,0,len);
	            }
	            out.close();
	            ais.close();
	        } catch (FileNotFoundException e) {
	            e.printStackTrace();
	        } catch (IOException e) {
	            e.printStackTrace();
	        }       
	    }
	}