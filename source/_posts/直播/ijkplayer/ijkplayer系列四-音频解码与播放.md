---
title: ijkplayer系列四-音频解码与播放
date: 2019-08-07 10:22:14
categories:
  - 直播
tags:
  - 直播
---

{% asset_img 播放器基本框图.png %}

播放器必然是通过**多线程**同时进行解封装、解码、视频渲染等工作的

# 解码线程

从数据读取线程分析那篇文章我们可以看到，ijkplayer的音频解码线程的入口函数是`audio_thread()/ff_ffplayer.c`

```c
static int audio_thread(void *arg)
{
	//...
    do {
        ffp_audio_statistic_l(ffp);
        //解码帧存放到frame中
        //里面是调用传进去的codec的codec->decode()方法解码
        if ((got_frame = decoder_decode_frame(ffp, &is->auddec, frame, NULL)) < 0)
            goto the_end;
            //...
            while ((ret = av_buffersink_get_frame_flags(is->out_audio_filter, frame, 0)) >= 0) {
				//...
				//能否把解码的frame写入音频解码帧列表is->sampq中(播放线程从这里面读取数据播放)
				//里面会判断sampq队列是否满了
				如果没位置放我们的frame的话，会调用pthread_cond_wait()方法阻塞队列
				//如果有位置放frame的话，就会返回frame应该放置的位置的地址的指针
                if (!(af = frame_queue_peek_writable(&is->sampq)))
                    goto the_end;

        		//...
        		//把frame放入到sampq相应位置
        		av_frame_move_ref(af->frame, frame);
        		//唤醒线程(音频播放线程因为sampq队列为空而阻塞，这里可以唤醒它)
        		rame_queue_push(&is->sampq);
				//...
        }
    } while (ret >= 0 || ret == AVERROR(EAGAIN) || ret == AVERROR_EOF);
 the_end:
	//...
    av_frame_free(&frame);
    return ret;
}
```

# 播放流程

在初始化的时候，有个方法没有跟进去分析，那就是在 `native_setup`--> `ijkmp_android_create()/ijkplayer_android.c` --> `ffpipeline_create_from_android()/ijkplayer_android.c`：

该方法里面一句

	pipeline->func_open_audio_output  = func_open_audio_output;
	
`func_open_audio_output()/ffpipeline_android.c:`

```c
static SDL_Aout *func_open_audio_output(IJKFF_Pipeline *pipeline, FFPlayer *ffp)
{
    SDL_Aout *aout = NULL;
    if (ffp->opensles) {
        aout = SDL_AoutAndroid_CreateForOpenSLES();
    } else {
        aout = SDL_AoutAndroid_CreateForAudioTrack();
    }
    if (aout)
        SDL_AoutSetStereoVolume(aout, pipeline->opaque->left_volume, pipeline->opaque->right_volume);
    return aout;
}
```

从上面可以看出，音频播放也分为:`opensles,audiotrack`,然后我们就来看看`audiotrack`吧：

```c
SDL_Aout *SDL_AoutAndroid_CreateForAudioTrack()
{
    SDL_Aout *aout = SDL_Aout_CreateInternal(sizeof(SDL_Aout_Opaque));
    if (!aout)
        return NULL;

    SDL_Aout_Opaque *opaque = aout->opaque;
    opaque->wakeup_cond  = SDL_CreateCond();
    opaque->wakeup_mutex = SDL_CreateMutex();
    opaque->speed        = 1.0f;

    aout->opaque_class = &g_audiotrack_class;
    aout->free_l       = aout_free_l;
    aout->open_audio   = aout_open_audio;
    aout->pause_audio  = aout_pause_audio;
    aout->flush_audio  = aout_flush_audio;
    aout->set_volume   = aout_set_volume;
    aout->close_audio  = aout_close_audio;
    aout->func_get_audio_session_id = aout_get_audio_session_id;
    aout->func_set_playback_rate    = func_set_playback_rate;

    return aout;
}
```

在上一篇数据读取线程我们分析到了在`stream_component_open()`里面会调用`aout->open_audio(aout, pause_on);`

再看现在初始化:

	aout->open_audio   = aout_open_audio;	
所以 `stream_component_open()`里面相当于直接调用了`aout_open_audio()/ijksdl_aout_android_audiotrack.c`

`aout_open_audio()` --> `aout_open_audio_n()` --> 创建音频播放线程

	SDL_CreateThreadEx(&opaque->_audio_tid, aout_thread, aout, "ff_aout_android");
		
## aout_thread

在这个函数内部会调用 `aout_thread_n()/ijksdl_aout_android_audiotrack.c`

```c
static int aout_thread_n(JNIEnv *env, SDL_Aout *aout)
{
  SDL_Aout_Opaque *opaque = aout->opaque;
    SDL_Android_AudioTrack *atrack = opaque->atrack;
    SDL_AudioCallback audio_cblk = opaque->spec.callback;
    void *userdata = opaque->spec.userdata;
    uint8_t *buffer = opaque->buffer;
  	//...
    if (!opaque->abort_request && !opaque->pause_on)
        //...

    while (!opaque->abort_request) {
        //...省略了一堆设置播放器相关的配置(播放速度，音量）
        //...SDL_Android_AudioTrack_set_xxx()
        audio_cblk(userdata, buffer, copy_size);
        if (opaque->need_flush) {
            SDL_Android_AudioTrack_flush(env, atrack);
            opaque->need_flush = false;
        }

        if (opaque->need_flush) {
            opaque->need_flush = 0;
            SDL_Android_AudioTrack_flush(env, atrack);
        } else {
            int written = SDL_Android_AudioTrack_write(env, atrack, buffer, copy_size);
            if (written != copy_size) {
                ALOGW("AudioTrack: not all data copied %d/%d", (int)written, (int)copy_size);
            }
        }

        // TODO: 1 if callback return -1 or 0
    }
```

### `audio_cblk()`

`audio_cblk()` 实际上就是调用的 `opaque->spec.callback`(上面初始化赋值的)

上一篇 `stream_component_open()` 里面调用的 `audio_open()`，有这么一句代码:

`wanted_spec.callback = sdl_audio_callback;`

其实就是调用到sdl_audio_callback()这个函数来了。

### `sdl_audio_callback`

```c
static void sdl_audio_callback(void *opaque, Uint8 *stream, int len)
{
	//...
    while (len > 0) {
        if (is->audio_buf_index >= is->audio_buf_size) {
        	//解码音频帧
           audio_size = audio_decode_frame(is);
           if (audio_size < 0) {
                /* 发生错误，就输出silence */
           //...
           } else {
               if (is->show_mode != SHOW_MODE_VIDEO)
                   update_sample_display(is, (int16_t *)is->audio_buf, audio_size);
               is->audio_buf_size = audio_size;
           }
           is->audio_buf_index = 0;
        }
        len1 = is->audio_buf_size - is->audio_buf_index;
        if (len1 > len)
            len1 = len;
        if (!is->muted && is->audio_buf && is->audio_volume == SDL_MIX_MAXVOLUME)
        	//拷贝解码的音频帧
            memcpy(stream, (uint8_t *)is->audio_buf + is->audio_buf_index, len1);
        else {
           //...
        }
        len -= len1;
        stream += len1;
        is->audio_buf_index += len1;
    }
    is->audio_write_buf_size = is->audio_buf_size - is->audio_buf_index;
    /* Let's assume the audio driver that is used by SDL has two periods. */
  //...
}
```

#### `audio_decode_frame`

解码音频帧

```c
/**
 * Decode one audio frame and return its uncompressed size.
 *
 * The processed audio frame is decoded, converted if required, and
 * stored in is->audio_buf, with size in bytes given by the return
 * value.
 */
static int audio_decode_frame(FFPlayer *ffp)｛
    af = frame_queue_peek_readable(&is->sampq)
    is->audio_buf = af->frame->data[0];
｝
```

判断解码后的is->sampq是否为空，如果为空，就阻塞(上面解码的时候，每向is->sampq放入一frame，就唤醒线程)；否则把队列的第一个frame赋值给ffp->is->audio_buf

#### 拷贝解码的音频帧

`memcpy(stream, (uint8_t *)is->audio_buf + is->audio_buf_index, len1);`

copy到stream中，stream从命名来看是一个流，流的另外一头在哪里呢？

再返回到 `aout_thread_n()` 中：

`SDL_Android_AudioTrack_write(env, atrack, buffer, copy_size);`

buffer就是刚刚的stream,该函数继续调用:

```c
 (*env)->SetByteArrayRegion(env, atrack->byte_buffer, 0, (int)size_in_byte, (jbyte*) data);
J4AC_AudioTrack__write(env, atrack->thiz, atrack->byte_buffer, 0, (int)size_in_byte);
```

把data拷贝到数组中，进行转换。为了下一笔把这个数组，也就是音频帧传递给java

```c
jint J4AC_android_media_AudioTrack__write(JNIEnv *env, jobject thiz, jbyteArray audioData, jint offsetInBytes, jint sizeInBytes)
{
    return (*env)->CallIntMethod(env, thiz, class_J4AC_android_media_AudioTrack.method_write, audioData, offsetInBytes, sizeInBytes);
}
```

调用了java层的 `AudioTrack.java`中的 `write()` 函数

这里又用到了bilibili另外一个开源项目:[jni4android](https://link.jianshu.com/?t=https://github.com/Bilibili/jni4android)。这个项目可以直接在c里面生成一个java的装饰类。这里用到的java就是`AudioTrack.java`，生成的文件就是`AudioTrack.h`和`AudioTrack.c`

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
