---
title: DownloadManager使用
date: 2020-01-10 14:49:53
categories:
  - Android
tags:
	- Android
---

# 基本API

```java
enqueue(Request request) 开始任务
remove(long... ids) 移除任务；如果任务下载中，取消然后移除
query(Query query) 查询已开始的任务

Request设置文件存储路径：只支持外部存储
setDestinationUri(Uri uri)
setDestinationInExternalFilesDir
setDestinationInExternalPublicDir
```

# 基本流程

- 开始下载
- 注册广播接收器，接受下载完成广播事件
- 注销广播接收器

## 下载新版本的 apk ##

	public void downloadNewVersion() {
	    mDownloadManager = (DownloadManager) getSystemService(DOWNLOAD_SERVICE);
	    // apkDownloadUrl 是 apk 的下载地址
	    DownloadManager.Request request = new DownloadManager.Request(Uri.parse(apkDownloadUrl));
	    // 获取下载队列 id
	    enqueueId = mDownloadManager.enqueue(request);
	}

## 注册接收下载完成的广播 ##

	BroadcastReceiver receiver = new BroadcastReceiver() {
	    @Override
	    public void onReceive(Context context, Intent intent) {
	        long downloadCompletedId = intent.getLongExtra(
	                DownloadManager.EXTRA_DOWNLOAD_ID, 0);
	        // 检查是否是自己的下载队列 id, 有可能是其他应用的
	        if (enqueueId != downloadCompletedId) {
	            return;
	        }
	        DownloadManager.Query query = new DownloadManager.Query();
	        query.setFilterById(enqueueId);
	        Cursor c = mDownloadManager.query(query);
	        if (c.moveToFirst()) {
	            int columnIndex = c.getColumnIndex(DownloadManager.COLUMN_STATUS);
	            // 下载失败也会返回这个广播，所以要判断下是否真的下载成功
	            if (DownloadManager.STATUS_SUCCESSFUL == c.getInt(columnIndex)) {
	                // 获取下载好的 apk 路径
	                String uriString = c.getString(c.getColumnIndex(DownloadManager.COLUMN_LOCAL_FILENAME));
	                // 提示用户安装
	                promptInstall(Uri.parse("file://" + uriString));
	            }
	        }
	    }
	};

	// 注册广播, 设置只接受下载完成的广播
	registerReceiver(receiver, new IntentFilter(
	        DownloadManager.ACTION_DOWNLOAD_COMPLETE));

## 注销广播 ##

	@Override
	protected void onDestroy() {
		super.onDestroy();
	
		unregisterReceiver(mBroadcastReceiver);
	}

## 提示用户安装 ##

	private void promptInstall(Uri data) {
	    Intent promptInstall = new Intent(Intent.ACTION_VIEW)
	            .setDataAndType(data, "application/vnd.android.package-archive");
	    // FLAG_ACTIVITY_NEW_TASK 可以保证安装成功时可以正常打开 app
	    promptInstall.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
	    startActivity(promptInstall);
	}

# 最佳实践建议

## 服务化

最好在服务中进行下载，而且不要绑定Activity生命周期，保证下载完成

下载完成要及时的注销广播，停止服务

# 常见问题

## DownloadManager 某些型号手机被禁掉

用其他网络下载框架

## 解析apk包错误

mDownloadManager.getUriForDownloadedFile(enqueueId)返回的Uri是这种格式的 `content://downloads/my_downloads/83`, 这种格式的Uri启动intent会报解析程序包时出现问题。所以需要解析或直接指定绝对下载路径

## ERROR_UNKNOWN

Android 18之前，下载链接含有 [] 会导致这个问题

```
if(Build.VERSION.SDK_INT<=Build.VERSION_CODES.JELLY_BEAN_MR2){
    uri = uri.replace("[","%5B").replace("]","%5D");
}
```

方案来自 [stackoverflow](http://stackoverflow.com/questions/37976748/downloadmanager-fails-with-error-unknown-on-api-17)

## IllegalArgumentException

`崩溃在了mDownloadManager.enqueue(request)`

```java
public long enqueue(Request request) {
    ContentValues values = request.toContentValues(mPackageName);
    Uri downloadUri = mResolver.insert(Downloads.Impl.CONTENT_URI, values);
    long id = Long.parseLong(downloadUri.getLastPathSegment());
    return id;
}
```

```java
public final @Nullable Uri insert(@NonNull Uri url, @Nullable ContentValues values) {
    Preconditions.checkNotNull(url, "url");
    IContentProvider provider = acquireProvider(url);
    if (provider == null) {
        // 看这里 嘿嘿嘿
        throw new IllegalArgumentException("Unknown URL " + url);
    }
    try {
        long startTime = SystemClock.uptimeMillis();
        Uri createdRow = provider.insert(mPackageName, url, values);
        long durationMillis = SystemClock.uptimeMillis() - startTime;
        maybeLogUpdateToEventLog(durationMillis, url, "insert", null /* where */);
        return createdRow;
    } catch (RemoteException e) {
        // Arbitrary and not worth documenting, as Activity
        // Manager will kill this process shortly anyway.
        return null;
    } finally {
        releaseProvider(provider);
    }
}
```

原因是系统的DownloadManager Service被关闭了, 可以有两种解决方法

1. 告知用户去系统里找到相应的开关 打开下载服务
2. catch 住自己去手写下载

## SecurityException

原因是Context.getExternalFilesDir得到的地址 和Environment.getExternalStorageDirectory() 不一致

```java
private void checkFileUriDestination(ContentValues values) {
    String fileUri = values.getAsString(Downloads.Impl.COLUMN_FILE_NAME_HINT);
    if (fileUri == null) {
        throw new IllegalArgumentException(
                "DESTINATION_FILE_URI must include a file URI under COLUMN_FILE_NAME_HINT");
    }
    Uri uri = Uri.parse(fileUri);
    String scheme = uri.getScheme();
    if (scheme == null || !scheme.equals("file")) {
        throw new IllegalArgumentException("Not a file URI: " + uri);
    }
    final String path = uri.getPath();
    if (path == null) {
        throw new IllegalArgumentException("Invalid file URI: " + uri);
    }
    try {
        final String canonicalPath = new File(path).getCanonicalPath();
        final String externalPath = Environment.getExternalStorageDirectory().getAbsolutePath();
        if (!canonicalPath.startsWith(externalPath)) {
            // 看这里,嘿嘿嘿
            throw new SecurityException("Destination must be on external storage: " + uri);
        }
    } catch (IOException e) {
        throw new SecurityException("Problem resolving path: " + uri);
    }
}
```

解决方案：手动拼1个存储地址

```java
DownloadManager.Request request = new DownloadManager.Request(Uri.parse(你的APK下载地址));
request.setDestinationUri(你的app 本地存储URI));
try {
    long mDownloadId = instance.mSystemDownloadManager.enqueue(request);
} catch (SecurityException e) {
    File f = Environment.getExternalStorageDirectory();
    f = new File(f, "Android");
    f = new File(f, "data");
    f = new File(f, mContext.getPackageName());
    f = new File(f, "files");
    f = new File(f, Environment.DIRECTORY_DOWNLOADS);
    if (!f.exists()) {
        f.mkdirs();
    }
    request.setDestinationUri(f));
    instance.mDownloadId = instance.mSystemDownloadManager.enqueue(request);
} catch (IllegalArgumentException e) {
 // 让用户打开下载服务；或者手动写下载
}
```
        
# 参考&扩展

- [Android 快速实现文件下载](https://juejin.im/entry/57715565d342d30057dcea62)
- [Android 7.0 DownloadManager与FileProvider的坑](https://www.jianshu.com/p/c58d17073e65)
- [Android DownloadManager ERROR_UNKNOWN 在API 17 巨坑完美解决](http://quanke.name/posts/42104/)
- [android 源生DownloadManager 的两个Crash 坑](https://corydon.cc/2017/03/17/downloadbug/)