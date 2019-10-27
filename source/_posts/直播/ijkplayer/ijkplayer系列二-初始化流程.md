---
title: ijkplayer系列二-初始化流程
date: 2019-08-05 16:22:14
categories:
  - 直播
tags:
  - 直播
---

# 使用

实例：用ijkplayer播放CCTV1

```groovy
# required, enough for most devices.
compile 'tv.danmaku.ijk.media:ijkplayer-java:0.8.8'
compile 'tv.danmaku.ijk.media:ijkplayer-armv7a:0.8.8'

# Other ABIs: optional
compile 'tv.danmaku.ijk.media:ijkplayer-armv5:0.8.8'
compile 'tv.danmaku.ijk.media:ijkplayer-arm64:0.8.8'
compile 'tv.danmaku.ijk.media:ijkplayer-x86:0.8.8'
compile 'tv.danmaku.ijk.media:ijkplayer-x86_64:0.8.8'

# ExoPlayer as IMediaPlayer: optional, experimental
compile 'tv.danmaku.ijk.media:ijkplayer-exo:0.8.8'
```

导入官方demo目录下的这些文件：

{% asset_img 使用.png %}

开始播放

```java
// init player
videoView.setVideoURI(Uri.parse("http://106.36.45.36/live.aishang.ctlcdn.com/00000110240001_1/encoder/1/playlist.m3u8"));

videoView.setOnPreparedListener(new IMediaPlayer.OnPreparedListener() {
    @Override
    public void onPrepared(IMediaPlayer mp) {
        videoView.start();
    }
});
```
 
# IjkMediaPlayer和Native交互

**播放控制**相关的 `start、pause、stop` 等，调用 对应的 native 方法

**底层状态信息的上报(比如底层的播放状态回调)**相关的 `postEventFromNative` 等，这些方法由底层主动调用(有`@CalledByNative` 注解)

{% asset_img IjkMediaPlayer和Native交互.png %}

# 事件处理

在播放过程中，某些行为的完成或者变化，如prepare完成，开始渲染等，需要以事件形式通知到外部，以便上层作出具体的业务处理。

播放器底层上报事件时，实际上就是将待发送的消息放入消息队列，另外有一个线程会不断从队列中取出消息，上报给外部

# 初始化IjkVideoView

{% asset_img 初始化序列图.png %}

{% asset_img ijkplayer音视频播放.jpg %}

## setVideoURI & openVideo

```java
public class IjkVideoView extends FrameLayout implements MediaController.MediaPlayerControl {
    private void setVideoURI(Uri uri, Map<String, String> headers) {
        mUri = uri;
        mHeaders = headers;
        mSeekWhenPrepared = 0;
        openVideo();
        requestLayout();
        invalidate();
    }
}
```
```java
private void openVideo() {
    if (mUri == null || mSurfaceHolder == null) {
        // not ready for playback just yet, will try again later
        return;
    }
    // we shouldn't clear the target state, because somebody might have
    // called start() previously
    release(false);

    AudioManager am = (AudioManager) mAppContext.getSystemService(Context.AUDIO_SERVICE);
    am.requestAudioFocus(null, AudioManager.STREAM_MUSIC, AudioManager.AUDIOFOCUS_GAIN);

    try {
        mMediaPlayer = createPlayer(mSettings.getPlayer());
        mMediaPlayer.setOnPreparedListener(mPreparedListener);
        //这里省略一大波setListener......
        mCurrentBufferPercentage = 0;
        
        String scheme = mUri.getScheme();
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M &&
                mSettings.getUsingMediaDataSource() &&
                (TextUtils.isEmpty(scheme) || scheme.equalsIgnoreCase("file"))) {
            IMediaDataSource dataSource = new FileMediaDataSource(new File(mUri.toString()));
            mMediaPlayer.setDataSource(dataSource);
        }  else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.ICE_CREAM_SANDWICH) {
            mMediaPlayer.setDataSource(mAppContext, mUri, mHeaders);
        } else {
            mMediaPlayer.setDataSource(mUri.toString());
        }
        
        bindSurfaceHolder(mMediaPlayer, mSurfaceHolder);
        mMediaPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
        mMediaPlayer.setScreenOnWhilePlaying(true);
        mPrepareStartTime = System.currentTimeMillis();
        mMediaPlayer.prepareAsync();
        if (mHudViewHolder != null)
            mHudViewHolder.setMediaPlayer(mMediaPlayer);

        // REMOVED: mPendingSubtitleTracks

        // we don't set the target state here either, but preserve the
        // target state that was there before.
        mCurrentState = STATE_PREPARING;
        attachMediaController();
    } catch (IOException ex) {
        Log.w(TAG, "Unable to open content: " + mUri, ex);
        mCurrentState = STATE_ERROR;
        mTargetState = STATE_ERROR;
        mErrorListener.onError(mMediaPlayer, MediaPlayer.MEDIA_ERROR_UNKNOWN, 0);
    } catch (IllegalArgumentException ex) {
        Log.w(TAG, "Unable to open content: " + mUri, ex);
        mCurrentState = STATE_ERROR;
        mTargetState = STATE_ERROR;
        mErrorListener.onError(mMediaPlayer, MediaPlayer.MEDIA_ERROR_UNKNOWN, 0);
    } finally {
        // REMOVED: mPendingSubtitleTracks.clear();
    }
}
```
在这里， 做了下面几件事：

- 获得AudioManager
- 通过setting获取player的类型
- 初始化IMediaPlayer (createPlayer()函数)
- 然后调用setDataSource(String)
- 屏幕常亮等
- 设置MediaController
- mMediaPlayer.prepareAsync()   

### createPlayer

```java
public IMediaPlayer createPlayer(int playerType) {
    IMediaPlayer mediaPlayer = null;

    switch (playerType) {
        case Settings.PV_PLAYER__IjkExoMediaPlayer: {
            IjkExoMediaPlayer IjkExoMediaPlayer = new IjkExoMediaPlayer(mAppContext);
            mediaPlayer = IjkExoMediaPlayer;
        }
        break;
        case Settings.PV_PLAYER__AndroidMediaPlayer: {
            AndroidMediaPlayer androidMediaPlayer = new AndroidMediaPlayer();
            mediaPlayer = androidMediaPlayer;
        }
        break;
        case Settings.PV_PLAYER__IjkMediaPlayer:
        default: {
            IjkMediaPlayer ijkMediaPlayer = null;
            if (mUri != null) {
                ijkMediaPlayer = new IjkMediaPlayer();
                //各种设置；ijkMediaPlayer.setOption()
                mediaPlayer = ijkMediaPlayer;
        }
        break;
    }

    if (mSettings.getEnableDetachedSurfaceTextureView()) {
        mediaPlayer = new TextureMediaPlayer(mediaPlayer);
    }

    return mediaPlayer;
}
```

#### IjkMediaPlayer.setOption 配置

初始化后 IjkMediaPlayer 后，可以对其进行一系列配置，例如:

```java
// 设置硬解码
mIjkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "mediacodec", 1);

// 设置 opensles 方式输出音频
mIjkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "opensles", 1);
```
setOption() 会调用到底层 ff_ffplay.c 的 ffp_set_option() 方法

##### 软硬解码选择

跟踪 `pipeline/ffpipeline_android.c` 的 `ffpipeline_create_from_android` 方法

发现是 用函数指针记录 类 IjkMediaPlayer.setOption() 设置的属性

### IjkMediaPlayer.setDataSource & _setDataSource

```java
public void setDataSource(String path, Map<String, String> headers)
        throws IOException, IllegalArgumentException, SecurityException, IllegalStateException
{
    if (headers != null && !headers.isEmpty()) {
        StringBuilder sb = new StringBuilder();
        for(Map.Entry<String, String> entry: headers.entrySet()) {
            sb.append(entry.getKey());
            sb.append(":");
            String value = entry.getValue();
            if (!TextUtils.isEmpty(value))
                sb.append(entry.getValue());
            sb.append("\r\n");
            setOption(OPT_CATEGORY_FORMAT, "headers", sb.toString());
            setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT, "protocol_whitelist", "async,cache,crypto,file,http,https,ijkhttphook,ijkinject,ijklivehook,ijklongurl,ijksegment,ijktcphook,pipe,rtp,tcp,tls,udp,ijkurlhook,data");
        }
    }
    setDataSource(path);
}
```
```java
private native void _setDataSource(String path, String[] keys, String[] values)
            throws IOException, IllegalArgumentException, SecurityException, IllegalStateException;
```
`ijkplayer_jni.c`

```c
static void
IjkMediaPlayer_setDataSourceAndHeaders(
    JNIEnv *env, jobject thiz, jstring path,
    jobjectArray keys, jobjectArray values)
{
    MPTRACE("%s\n", __func__);
    int retval = 0;
    const char *c_path = NULL;
    IjkMediaPlayer *mp = jni_get_media_player(env, thiz);
    JNI_CHECK_GOTO(path, env, "java/lang/IllegalArgumentException", "mpjni: setDataSource: null path", LABEL_RETURN);
    JNI_CHECK_GOTO(mp, env, "java/lang/IllegalStateException", "mpjni: setDataSource: null mp", LABEL_RETURN);

    c_path = (*env)->GetStringUTFChars(env, path, NULL );
    JNI_CHECK_GOTO(c_path, env, "java/lang/OutOfMemoryError", "mpjni: setDataSource: path.string oom", LABEL_RETURN);

    ALOGV("setDataSource: path %s", c_path);
    retval = ijkmp_set_data_source(mp, c_path);
    (*env)->ReleaseStringUTFChars(env, path, c_path);

    IJK_CHECK_MPRET_GOTO(retval, env, LABEL_RETURN);

LABEL_RETURN:
    ijkmp_dec_ref_p(&mp);
}
```

### IjkMediaPlayer.prepareAsync & _prepareAsync

最终调用到 `ijkmp_prepare_async_l`  

```java
@Override
public void prepareAsync() throws IllegalStateException {
    _prepareAsync();
}

public native void _prepareAsync() throws IllegalStateException;
```
`ijkplayer_jni.c`

```c
static void
IjkMediaPlayer_prepareAsync(JNIEnv *env, jobject thiz)
{
    MPTRACE("%s\n", __func__);
    int retval = 0;
    IjkMediaPlayer *mp = jni_get_media_player(env, thiz);
    JNI_CHECK_GOTO(mp, env, "java/lang/IllegalStateException", "mpjni: prepareAsync: null mp", LABEL_RETURN);

    retval = ijkmp_prepare_async(mp);
    IJK_CHECK_MPRET_GOTO(retval, env, LABEL_RETURN);

LABEL_RETURN:
    ijkmp_dec_ref_p(&mp);
}
```
`ijkplayer.c`

```c
int ijkmp_prepare_async(IjkMediaPlayer *mp)
{
    assert(mp);
    MPTRACE("ijkmp_prepare_async()\n");
    pthread_mutex_lock(&mp->mutex);
    int retval = ijkmp_prepare_async_l(mp);
    pthread_mutex_unlock(&mp->mutex);
    MPTRACE("ijkmp_prepare_async()=%d\n", retval);
    return retval;
}

static int ijkmp_prepare_async_l(IjkMediaPlayer *mp)
{
    assert(mp);

	//状态判断，符合直接返回
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_IDLE);
    // MPST_RET_IF_EQ(mp->mp_state, MP_STATE_INITIALIZED);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_ASYNC_PREPARING);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_PREPARED);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_STARTED);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_PAUSED);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_COMPLETED);
    // MPST_RET_IF_EQ(mp->mp_state, MP_STATE_STOPPED);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_ERROR);
    MPST_RET_IF_EQ(mp->mp_state, MP_STATE_END);

    assert(mp->data_source);

    ijkmp_change_state_l(mp, MP_STATE_ASYNC_PREPARING);

    msg_queue_start(&mp->ffplayer->msg_queue);

    // released in msg_loop
    ijkmp_inc_ref(mp);
    mp->msg_thread = SDL_CreateThreadEx(&mp->_msg_thread, ijkmp_msg_loop, mp, "ff_msg_loop");
    // msg_thread is detached inside msg_loop
    // TODO: 9 release weak_thiz if pthread_create() failed;

    int retval = ffp_prepare_async_l(mp->ffplayer, mp->data_source);
    if (retval < 0) {
        ijkmp_change_state_l(mp, MP_STATE_ERROR);
        return retval;
    }

    return 0;
}
```

主要做了一下几件事：

- `ijkmp_change_state_l()`
	- 向`msg_queue`发送一个`FFP_MSG_PLAYBACK_STATE_CHANGED`消息
- `msg_queue_start()`
	- 向`msg_queue`发送一个`FFP_MSG_FLUSH`消息
- 创建消息循环线程，线程入口为`ijkmp_msg_loop`
	- 处理`msg_queue`发送的消息
- `ffp_prepare_async_l()`
	- 打开读取线程和视频解码播放进程 

#### `ijkmp_change_state_l`

```c
void ijkmp_change_state_l(IjkMediaPlayer *mp, int new_state)
{
    mp->mp_state = new_state;
    ffp_notify_msg1(mp->ffplayer, FFP_MSG_PLAYBACK_STATE_CHANGED);
}
```

#### `msg_queue_start`

`ff_ffmsg_queue.h`

```c
inline static void msg_queue_start(MessageQueue *q)
{
    SDL_LockMutex(q->mutex);
    q->abort_request = 0;

    AVMessage msg;
    msg_init_msg(&msg);
    msg.what = FFP_MSG_FLUSH;
    msg_queue_put_private(q, &msg);
    SDL_UnlockMutex(q->mutex);
}
```

#### 创建消息循环线程

#### `ffp_prepare_async_l`

`ijkmedia/ijkplayer/ff_ffplay.c`

```c
int ffp_prepare_async_l(FFPlayer *ffp, const char *file_name)
{
    //...
    //log信息，打印FFmpeg相关信息
    av_log(NULL, AV_LOG_INFO, "===== versions =====\n");
    ffp_show_version_str(ffp, "ijkplayer",      ijk_version_info());
    ffp_show_version_str(ffp, "FFmpeg",         av_version_info());
    ffp_show_version_int(ffp, "libavutil",      avutil_version());
    ffp_show_version_int(ffp, "libavcodec",     avcodec_version());
    ffp_show_version_int(ffp, "libavformat",    avformat_version());
    ffp_show_version_int(ffp, "libswscale",     swscale_version());
    ffp_show_version_int(ffp, "libswresample",  swresample_version());
    av_log(NULL, AV_LOG_INFO, "===== options =====\n");
    ffp_show_dict(ffp, "player-opts", ffp->player_opts);
    ffp_show_dict(ffp, "format-opts", ffp->format_opts);
    ffp_show_dict(ffp, "codec-opts ", ffp->codec_opts);
    ffp_show_dict(ffp, "sws-opts   ", ffp->sws_dict);
    ffp_show_dict(ffp, "swr-opts   ", ffp->swr_opts);
    av_log(NULL, AV_LOG_INFO, "===================\n");
    
    VideoState *is = stream_open(ffp, file_name, NULL);
    if (!is) {
        av_log(NULL, AV_LOG_WARNING, "ffp_prepare_async_l: stream_open failed OOM");
        return EIJK_OUT_OF_MEMORY;
    }

    ffp->is = is;
    ffp->input_filename = av_strdup(file_name);
    return 0;
}
```

做了以下几件事：

- logcat打印FFmpeg相关信息
- `stream_open()` 

##### `stream_open`

```c
static VideoState *stream_open(FFPlayer *ffp, const char *filename, AVInputFormat *iformat)
{
    /* start video display */
    //初始化队列 frame_queue_init()
    //第一个参数是解码出来的队列,第二个参数是未解码的队列
    //有三个队列：音频，视频，字幕
    if (frame_queue_init(&is->pictq, &is->videoq, ffp->pictq_size, 1) < 0)
        goto fail;
    if (frame_queue_init(&is->subpq, &is->subtitleq, SUBPICTURE_QUEUE_SIZE, 0) < 0)
        goto fail;
    if (frame_queue_init(&is->sampq, &is->audioq, SAMPLE_QUEUE_SIZE, 1) < 0)
        goto fail;

    if (packet_queue_init(&is->videoq) < 0 ||
        packet_queue_init(&is->audioq) < 0 ||
        packet_queue_init(&is->subtitleq) < 0)
        goto fail;

    //创建video_refresh_thread视频显示进程(视频渲染，音视频同步）
    is->video_refresh_tid = SDL_CreateThreadEx(&is->_video_refresh_tid, video_refresh_thread, ffp, "ff_vout");
    //创建read_thread数据读取线程
    is->read_tid = SDL_CreateThreadEx(&is->_read_tid, read_thread, ffp, "ff_read");
}
```

{% asset_img stream_open方法.png %}

主要做了三件事：

- `frame_queue_init()`开始视频展示
- 创建`video_refresh_thread`视频显示进程
- 创建`read_thread`数据读取线程

在`read_thread`里面向`msg_queue`发送了一个消息`ffp_notify_msg1(ffp, FFP_MSG_PREPARED)`;，消息循环线程收到这个消息后，会调用java层的handler发送`MEDIA_PREPARED`消息，然后在handler的handleMessage函数里面会处理这个消息：

```java
case MEDIA_PREPARED:
    player.notifyOnPrepared();
    return;
```

最终调用到我们设置的 `IMediaPlayer.OnPreparedListener`

```java
videoView.setOnPreparedListener(new IMediaPlayer.OnPreparedListener() {
    @Override
    public void onPrepared(IMediaPlayer mp) {
        videoView.start();
    }
});
```

# 初始化IjkMediaPlayer
   
## 构造函数 & initPlayer

构造函数在上面的 `IjkVideoView.createPlayer(int playerType)` 中被调用

这里只讲一下IjkMediaPlayer，其实我们除了使用IjkMediaPlayer，还可以使用IjkExoMediaPlayer或者AndroidMediaPlayer。只需要修改一下createPlayer(int playerType)的参数就行了。

```java
public final class IjkMediaPlayer extends AbstractMediaPlayer {
	public IjkMediaPlayer(IjkLibLoader libLoader) {
        initPlayer(libLoader);
    }
}
```
```java   
private void initPlayer(IjkLibLoader libLoader) {
    loadLibrariesOnce(libLoader);
    initNativeOnce();

    Looper looper;
    if ((looper = Looper.myLooper()) != null) {
        mEventHandler = new EventHandler(this, looper);
    } else if ((looper = Looper.getMainLooper()) != null) {
        mEventHandler = new EventHandler(this, looper);
    } else {
        mEventHandler = null;
    }

    /*
     * Native setup requires a weak reference to our object. It's easier to
     * create it here than in C++.
     */
    native_setup(new WeakReference<IjkMediaPlayer>(this));
}
```

`initPlayer` 方法，共做了四件事：

- loadLibrariesOnce() 加载 so 库
- initNativeOnce() 静态初始化底层，其实什么都没做
- 创建 EventHandler，用来处理底层状态信息的上报
- `native_setup()` 初始化底层创建播放器

### loadLibrariesOnce 加载 so 库

#### 加载 so 库

```java
libLoader.loadLibrary("ijkffmpeg");
libLoader.loadLibrary("ijksdl");
libLoader.loadLibrary("ijkplayer");
```

#### JNI_OnLoad

加载so,虚拟机先自动执行JNI_OnLoad；

卸载so,虚拟机先自动执行JNI_UnLoad；

`ijkplayer_jni.c`

```c
JNIEXPORT jint JNI_OnLoad(JavaVM *vm, void *reserved)
{
    JNIEnv* env = NULL;

    g_jvm = vm;
    if ((*vm)->GetEnv(vm, (void**) &env, JNI_VERSION_1_4) != JNI_OK) {
        return -1;
    }
    assert(env != NULL);

    pthread_mutex_init(&g_clazz.mutex, NULL );

    // FindClass returns LocalReference
    IJK_FIND_JAVA_CLASS(env, g_clazz.clazz, JNI_CLASS_IJKPLAYER);
    (*env)->RegisterNatives(env, g_clazz.clazz, g_methods, NELEM(g_methods) );

    ijkmp_global_init();
    ijkmp_global_set_inject_callback(inject_callback);

    FFmpegApi_global_init(env);

    return JNI_VERSION_1_4;
}
```

主要做了以下几件事：

- RegisterNatives()注册native方法`_start`(系列播放器控制API)
- `ijkmp_global_init` 初始化ffmpeg
- `FFmpegApi_global_init` 注册native方法`av_base64_encode`

##### RegisterNatives()注册native方法

```c
static JNINativeMethod g_methods[] = {
    {
        "_setDataSource",
        "(Ljava/lang/String;[Ljava/lang/String;[Ljava/lang/String;)V",
        (void *) IjkMediaPlayer_setDataSourceAndHeaders
    },
    { "_setDataSourceFd",       "(I)V",     (void *) IjkMediaPlayer_setDataSourceFd },
    { "_setDataSource",         "(Ltv/danmaku/ijk/media/player/misc/IMediaDataSource;)V", (void *)IjkMediaPlayer_setDataSourceCallback },
    { "_setAndroidIOCallback",  "(Ltv/danmaku/ijk/media/player/misc/IAndroidIO;)V", (void *)IjkMediaPlayer_setAndroidIOCallback },

    { "_setVideoSurface",       "(Landroid/view/Surface;)V", (void *) IjkMediaPlayer_setVideoSurface },
    { "_prepareAsync",          "()V",      (void *) IjkMediaPlayer_prepareAsync },
    { "_start",                 "()V",      (void *) IjkMediaPlayer_start },
    { "_stop",                  "()V",      (void *) IjkMediaPlayer_stop },
    { "seekTo",                 "(J)V",     (void *) IjkMediaPlayer_seekTo },
    { "_pause",                 "()V",      (void *) IjkMediaPlayer_pause },
    { "isPlaying",              "()Z",      (void *) IjkMediaPlayer_isPlaying },
    { "getCurrentPosition",     "()J",      (void *) IjkMediaPlayer_getCurrentPosition },
    { "getDuration",            "()J",      (void *) IjkMediaPlayer_getDuration },
    { "_release",               "()V",      (void *) IjkMediaPlayer_release },
    { "_reset",                 "()V",      (void *) IjkMediaPlayer_reset },
    { "setVolume",              "(FF)V",    (void *) IjkMediaPlayer_setVolume },
    { "getAudioSessionId",      "()I",      (void *) IjkMediaPlayer_getAudioSessionId },
    { "native_init",            "()V",      (void *) IjkMediaPlayer_native_init },
    { "native_setup",           "(Ljava/lang/Object;)V", (void *) IjkMediaPlayer_native_setup },
    { "native_finalize",        "()V",      (void *) IjkMediaPlayer_native_finalize },

    { "_setOption",             "(ILjava/lang/String;Ljava/lang/String;)V", (void *) IjkMediaPlayer_setOption },
    { "_setOption",             "(ILjava/lang/String;J)V",                  (void *) IjkMediaPlayer_setOptionLong },

    { "_getColorFormatName",    "(I)Ljava/lang/String;",    (void *) IjkMediaPlayer_getColorFormatName },
    { "_getVideoCodecInfo",     "()Ljava/lang/String;",     (void *) IjkMediaPlayer_getVideoCodecInfo },
    { "_getAudioCodecInfo",     "()Ljava/lang/String;",     (void *) IjkMediaPlayer_getAudioCodecInfo },
    { "_getMediaMeta",          "()Landroid/os/Bundle;",    (void *) IjkMediaPlayer_getMediaMeta },
    { "_setLoopCount",          "(I)V",                     (void *) IjkMediaPlayer_setLoopCount },
    { "_getLoopCount",          "()I",                      (void *) IjkMediaPlayer_getLoopCount },
    { "_getPropertyFloat",      "(IF)F",                    (void *) ijkMediaPlayer_getPropertyFloat },
    { "_setPropertyFloat",      "(IF)V",                    (void *) ijkMediaPlayer_setPropertyFloat },
    { "_getPropertyLong",       "(IJ)J",                    (void *) ijkMediaPlayer_getPropertyLong },
    { "_setPropertyLong",       "(IJ)V",                    (void *) ijkMediaPlayer_setPropertyLong },
    { "_setStreamSelected",     "(IZ)V",                    (void *) ijkMediaPlayer_setStreamSelected },

    { "native_profileBegin",    "(Ljava/lang/String;)V",    (void *) IjkMediaPlayer_native_profileBegin },
    { "native_profileEnd",      "()V",                      (void *) IjkMediaPlayer_native_profileEnd },

    { "native_setLogLevel",     "(I)V",                     (void *) IjkMediaPlayer_native_setLogLevel },
    { "_setFrameAtTime",        "(Ljava/lang/String;JJII)V", (void *) IjkMediaPlayer_setFrameAtTime },
};
```

##### `ijkmp_global_init`初始化ffmpeg

ffmpeg的初始化工作, ijkplayer是基于ffmpeg。最终调用了 `ffp_global_init()`

`ijkplayer.c`

```c
void ijkmp_global_init()
{
    ffp_global_init();
}
```

`ff_ffplay.c`

```c
void ffp_global_init()
{
    if (g_ffmpeg_global_inited)
        return;

    ALOGD("ijkmediaplayer version : %s", ijkmp_version());
    /* register all codecs, demux and protocols */
    avcodec_register_all();
#if CONFIG_AVDEVICE
    avdevice_register_all();
#endif
#if CONFIG_AVFILTER
    avfilter_register_all();
#endif
    av_register_all();

    ijkav_register_all();

    avformat_network_init();

    av_lockmgr_register(lockmgr);
    av_log_set_callback(ffp_log_callback_brief);

    av_init_packet(&flush_pkt);
    flush_pkt.data = (uint8_t *)&flush_pkt;

    g_ffmpeg_global_inited = true;
}
```

##### `FFmpegApi_global_init`

动态注册 `av_base64_encode` 函数

`/Users/liyungui/StudioProjects/ijkplayer/android/ijkplayer/ijkplayer-armv7a/src/main/jni/ijkmedia/ijkplayer/android/ffmpeg_api_jni.c`

```c
int FFmpegApi_global_init(JNIEnv *env)
{
    int ret = 0;

    IJK_FIND_JAVA_CLASS(env, g_clazz.clazz, JNI_CLASS_FFMPEG_API);
    (*env)->RegisterNatives(env, g_clazz.clazz, g_methods, NELEM(g_methods));

    return ret;
}
```

```c
static JNINativeMethod g_methods[] = {
    {"av_base64_encode", "([B)Ljava/lang/String;", (void *) FFmpegApi_av_base64_encode},
};
```

### initNativeOnce 静态初始化底层

最终调用了 `native_init` native方法，其实什么都没做

`ijkplayer_jni.c`

```c
static void
IjkMediaPlayer_native_init(JNIEnv *env)
{
    MPTRACE("%s\n", __func__);
}
```

### 创建 EventHandler，用来处理底层状态信息的上报

初始化一个handler，在c层通过调用java的方法来post message，处理底层状态信息的上报。

### native_setup 初始化底层创建播放器

最终调用了 `ijkmp_android_create`创建播放器
  
```java
private native void native_setup(Object IjkMediaPlayer_this);
``` 

`ijkplayer_jni.c`

```c
static void
IjkMediaPlayer_native_setup(JNIEnv *env, jobject thiz, jobject weak_this)
{
    MPTRACE("%s\n", __func__);
    IjkMediaPlayer *mp = ijkmp_android_create(message_loop);
    JNI_CHECK_GOTO(mp, env, "java/lang/OutOfMemoryError", "mpjni: native_setup: ijkmp_create() failed", LABEL_RETURN);

    jni_set_media_player(env, thiz, mp);
    ijkmp_set_weak_thiz(mp, (*env)->NewGlobalRef(env, weak_this));
    ijkmp_set_inject_opaque(mp, ijkmp_get_weak_thiz(mp));
    ijkmp_set_ijkio_inject_opaque(mp, ijkmp_get_weak_thiz(mp));
    ijkmp_android_set_mediacodec_select_callback(mp, mediacodec_select_callback, ijkmp_get_weak_thiz(mp));

LABEL_RETURN:
    ijkmp_dec_ref_p(&mp);
}
```

`ijkplayer_android.c`

```c
IjkMediaPlayer *ijkmp_android_create(int(*msg_loop)(void*))
{
	// 创建底层播放器对象，设置消息处理函数
    IjkMediaPlayer *mp = ijkmp_create(msg_loop);
    if (!mp)
        goto fail;

	// 创建图像渲染对象
    mp->ffplayer->vout = SDL_VoutAndroid_CreateForAndroidSurface();
    if (!mp->ffplayer->vout)
        goto fail;

	// 初始化视频解码器（软/硬）、音频输出设备（opensles/audioTrack）
    mp->ffplayer->pipeline = ffpipeline_create_from_android(mp->ffplayer);
    if (!mp->ffplayer->pipeline)
        goto fail;

    ffpipeline_set_vout(mp->ffplayer->pipeline, mp->ffplayer->vout);

    return mp;

fail:
    ijkmp_dec_ref_p(&mp);
    return NULL;
}
```
`ijkplayer.c`

```c
IjkMediaPlayer *ijkmp_create(int (*msg_loop)(void*))
{
    IjkMediaPlayer *mp = (IjkMediaPlayer *) mallocz(sizeof(IjkMediaPlayer));
    if (!mp)
        goto fail;

    mp->ffplayer = ffp_create();
    if (!mp->ffplayer)
        goto fail;

    mp->msg_loop = msg_loop;

    ijkmp_inc_ref(mp);
    pthread_mutex_init(&mp->mutex, NULL);

    return mp;

    fail:
    ijkmp_destroy_p(&mp);
    return NULL;
}
```

主要做了以下几件事：

- `ijkmp_android_create` 创建播放器
	- `ijkmp_create`创建IJKMediaPlayer
		- 创建 IjkMediaPlayer 结构体 
		- 设置IJKMediaPlayer结构体
			- 设置 mp->ffplayer
				-  ffplayer，通过 `ffp_create()`创建
			- 设置 mp->msg_loop	
	- 设置 mp->ffplayer->vout。
		- 输出设备vout，通过 `SDL_VoutAndroid_CreateForAndroidSurface()`创建
	- 设置 mp->ffplayer->pipeline
- jni_set_media_player

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
