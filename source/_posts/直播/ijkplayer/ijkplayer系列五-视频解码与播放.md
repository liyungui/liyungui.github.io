---
title: ijkplayer系列五-视频解码与播放
date: 2019-08-08 10:22:14
categories:
  - 直播
tags:
  - 直播
---

# 解码线程

从数据读取线程分析那篇文章我们可以看到，ijkplayer的视频解码线程的入口函数是`video_thread()/ff_ffplayer.c`

## `video_thread`

```c
static int video_thread(void *arg)
{
    FFPlayer *ffp = (FFPlayer *)arg;
    int       ret = 0;

    if (ffp->node_vdec) {
        ret = ffpipenode_run_sync(ffp->node_vdec);
    }
    return ret;
}
```

`ffpipenode_run_sync()/ff_ffpipenode.c`

```c
int ffpipenode_run_sync(IJKFF_Pipenode *node)
{
    return node->func_run_sync(node);
}
```

最终调用的实际是 `ffp->node_vdec->func_run_sync(node);`

又是直接运行的ffplayer结构体里面的函数，肯定和音频播放一样，在之前初始化的时候给这个函数指针赋值过，那么我们回过头看看到底在哪里为它赋值的:

我们还是看到之前初始化的`ijkmp_android_create()`调用`ffpipeline_create_from_android()`，然后里面有一句:

`pipeline->func_open_video_decoder = func_open_video_decoder;`

然后我们再返回看到在`stream_component_open()/ff_ffplayer.c`里面有一句:

```c
decoder_init(&is->viddec, avctx, &is->videoq, is->continue_read_thread);
ffp->node_vdec = ffpipeline_open_video_decoder(ffp->pipeline, ffp);
```

点进去`ffpipeline_open_video_decoder(ffp->pipeline, ffp);`：

```c
IJKFF_Pipenode* ffpipeline_open_video_decoder(IJKFF_Pipeline *pipeline, FFPlayer *ffp)
{
    return pipeline->func_open_video_decoder(pipeline, ffp);
}
```

结合上面的分析，在`stream_component_open()/ff_ffplayer.c`里面其实运行了`func_open_video_decoder()/ffpipeline_android.c`，然后把返回值赋值给`ffp->node_vdec`;继续跟着流程到`func_open_video_decoder()`。由于这里跳转比较麻烦，我就直接上：

```c
func_open_video_decoder()
{
        |(调用)
    //(这里其实有个判断，是用硬解码还是软解，我们只分析硬解码)
    node = ffpipenode_create_video_decoder_from_android_mediacodec(ffp, pipeline, opaque->weak_vout);
    return node;
        |(执行)
    //alloc一个IJKFF_Pipenode 
    IJKFF_Pipenode *node =  ffpipenode_alloc(sizeof(IJKFF_Pipenode_Opaque));
    node->func_destroy  = func_destroy;
    node->func_run_sync = func_run_sync;
    node->func_flush    = func_flush;
    reutnr node;
}    
```

最终 `ffp->node_vdec =node`

现在终于找到赋值的地方了，前面调用的`ffp->node_vdec->func_run_sync(node);`现在看来就是调用的`func_run_sync()`函数

### `func_run_sync`

```c
static int func_run_sync(IJKFF_Pipenode *node)
{
    IJKFF_Pipenode_Opaque *opaque   = node->opaque;
    FFPlayer              *ffp      = opaque->ffp;
    VideoState            *is       = ffp->is;
    Decoder               *d        = &is->viddec;
    PacketQueue           *q        = d->queue;

	//...
    opaque->enqueue_thread = SDL_CreateThreadEx(&opaque->_enqueue_thread, enqueue_thread_func, node, "amediacodec_input_thread");
	//...
    while (!q->abort_request) {
      	//...
        ret = drain_output_buffer(env, node, timeUs, &dequeue_count, frame, &got_frame);
  		//...
		ret = ffp_queue_picture(ffp, frame, pts, duration, av_frame_get_pkt_pos(frame), is->viddec.pkt_serial);
     //...
    }
	fail:
	//...
}
```

#### 线程`enqueue_thread_func`

在视频解码流程里面又创建了一个线程:

`opaque->enqueue_thread = SDL_CreateThreadEx(&opaque->_enqueue_thread, enqueue_thread_func, node, "amediacodec_input_thread");
`

```c
从命名来看，是一个input_thread，我们先来看看这个线程:


static int enqueue_thread_func(void *arg)
{
    IJKFF_Pipenode        *node     = arg;
    IJKFF_Pipenode_Opaque *opaque   = node->opaque;
    FFPlayer              *ffp      = opaque->ffp;
    VideoState            *is       = ffp->is;
    Decoder               *d        = &is->viddec;
    PacketQueue           *q        = d->queue;
//...
    while (!q->abort_request) {
        ret = feed_input_buffer(env, node, AMC_INPUT_TIMEOUT_US, &dequeue_count);
        if (ret != 0) {
            goto fail;
        }
    }
//...
}
```

点进去`feed_input_buffer()/ffpipenode_android_mediacodec_vdec.c`:

```c
staticint feed_input_buffer(JNIEnv *env, IJKFF_Pipenode *node, int64_t timeUs, int*enqueue_count)
{
    if(ffp_packet_queue_get_or_buffering(ffp, d->queue, &pkt,&d->pkt_serial, &d->finished) < 0) { //取得数据包
        //...
        input_buffer_ptr= SDL_AMediaCodec_getInputBuffer(opaque->acodec, input_buffer_index,&input_buffer_size); //得到硬解码应该输入的buffer的地址
        //...
        memcpy(input_buffer_ptr,d->pkt_temp.data, copy_size);
        //...
        amc_ret= SDL_AMediaCodec_queueInputBuffer(opaque->acodec, input_buffer_index, 0,copy_size, time_stamp, 0); 
//送到AMediaCodec解码器
        //...
    }
}
```

OK，这一步原来就是用硬解码器解码。这个`input_thread`也就只是把每一帧数据送到解码器去解码而已。

#### `drain_output_buffer_l`

从硬解码器中获得解码后的数据

```c
static int drain_output_buffer_l(JNIEnv *env, IJKFF_Pipenode *node, int64_t timeUs,int *dequeue_count)
{
	//...
	//从硬解码器中获得解码后的数据
	output_buffer_index= SDL_AMediaCodec_dequeueOutputBuffer(opaque->acodec, &bufferInfo,timeUs); 
	//...
}
```

#### `ffp_queue_picture`

把数据插入到显示队列 `ijkplayer->ffplayer->is->pictq` 中

# 显示线程

显示线程从 `is->pictq` 读取数据，然后直接推送给硬件设备，完成渲染。

前面关于启动流程的分析我们知道，IjkMediaPlayer.prepareAsync `stream_open`中创建了视频显示进程

`is->video_refresh_tid = SDL_CreateThreadEx(&is->_video_refresh_tid, video_refresh_thread, ffp, "ff_vout");`

## `video_refresh_thread()/ff_ffplayer.c`

```c
video_refresh_thread(void *arg)
              |(调用)
video_refresh(ffp, &remaining_time);
              |(调用)
 video_display2(ffp);
              |(调用)
video_image_display2(ffp);
```

### `video_image_display2`

```c
static void video_image_display2(FFPlayer *ffp)
{
    VideoState *is = ffp->is;
    Frame *vp;
	
	//从队列中取出数据
	//然后调用SDL_VoutDisplayYUVOverlay()完成渲染。
    vp = frame_queue_peek(&is->pictq);
    if (vp->bmp) {
        SDL_VoutDisplayYUVOverlay(ffp->vout, vp->bmp);
        ffp->stat.vfps = SDL_SpeedSamplerAdd(&ffp->vfps_sampler, FFP_SHOW_VFPS_FFPLAY, "vfps[ffplay]");
        if (!ffp->first_video_frame_rendered) {
            ffp->first_video_frame_rendered = 1;
            ffp_notify_msg1(ffp, FFP_MSG_VIDEO_RENDERING_START);
        }
    }
}
```

#### `SDL_VoutDisplayYUVOverlay`

```c
int SDL_VoutDisplayYUVOverlay(SDL_Vout *vout, SDL_VoutOverlay *overlay)
{
    if (vout && overlay && vout->display_overlay)
        return vout->display_overlay(vout, overlay);

    return -1;
}
```

在初始化的时候，在 `ijkmp_android_create()`里面调用的`SDL_VoutAndroid_CreateForAndroidSurface();` 赋值的：

`vout->display_overlay = func_display_overlay;`

所以其实调用了 `func_display_overlay()` 完成渲染。从pictq列表中获取视频frame数据，然后再写入nativewindows的视频缓冲中进行渲染。

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
