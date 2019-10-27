---
title: ijkplayer系列六-音视频同步
date: 2019-08-08 14:22:14
categories:
  - 直播
tags:
  - 直播
---

# 音视频同步

对于播放器来说，音视频同步是一个关键点，同时也是一个难点，同步效果的好坏，直接决定着播放器的质量。

通常音视频同步的解决方案就是选择一个**参考时钟**，播放时读取音视频帧上的时间戳，同时参考当前时钟的时间来安排播放。如下图所示：

{% asset_img 音视频同步示意图.png %}

如果音视频帧的播放时间大于当前参考时钟上的时间，则不急于播放该帧，直到参考时钟达到该帧的时间戳；如果音视频帧的时间戳小于当前参考时钟上的时间，则需要“尽快”播放该帧或丢弃，以便播放进度追上参考时钟。

## 参考时钟的选择

有多种方式：

- 选取视频时间戳作为参考时钟源
- 选取音频时间戳作为参考时钟源
- 选取外部时间作为参考时钟源

考虑人对视频、和音频的敏感度，在存在音频的情况下，**优先选择音频**作为主时钟源。

ijkplayer在**默认**情况下是使用**音频**作为参考时钟源

## 保存播放音频帧时间

每播放一帧音频都将这一帧的播放时间保存在 `Video_State` 这个结构体的 `audio_clock` 中

```c
static int audio_decode_frame(FFPlayer *ffp) {
    ...
    if (!(af = frame_queue_peek_readable(&is->sampq)))
            return -1;
    
    ...
    /* update the audio clock with the pts */
    if (!isnan(af->pts))
        is->audio_clock = af->pts + (double) af->frame->nb_samples / af->frame->sample_rate;
    else
        is->audio_clock = NAN;
}
```

## 处理保存的音频帧时间

```c
static void sdl_audio_callback(void *opaque, Uint8 *stream, int len) {
    
    audio_size = audio_decode_frame(ffp);
    
    if (!isnan(is->audio_clock)) {
        set_clock_at(&is->audclk, 
                     is->audio_clock - (double)(is->audio_write_buf_size) / is->audio_tgt.bytes_per_sec - SDL_AoutGetLatencySeconds(ffp->aout), 
                     is->audio_clock_serial, 
                     ffp->audio_callback_time / 1000000.0);
        sync_clock_to_slave(&is->extclk, &is->audclk);
    }
}
```

`set_clock_at` 的第二个参数就是处理后的当前音频帧播放的秒数

## 视频渲染同步

```c
static int video_refresh_thread(void *arg)
{
    FFPlayer *ffp = arg;
    VideoState *is = ffp->is;
    double remaining_time = 0.0;
    while (!is->abort_request) {
        if (remaining_time > 0.0) {
            av_usleep((int)(int64_t)(remaining_time * 1000000.0));
        }
        //REFRESH_RATE = 0.01
        remaining_time = REFRESH_RATE;
        if (is->show_mode != SHOW_MODE_NONE 
            && (!is->paused || is->force_refresh))
            video_refresh(ffp, &remaining_time);
    }
    return 0;
}
```

`remaining_time` 是视频渲染线程需要同步时间(也就是sleep时间)，单位是us。通过 `video_refresh()` 计算出来。

### 计算同步时间

```c
static void video_refresh(FFPlayer *opaque, double *remaining_time){
    FFPlayer *ffp = opaque;
    VideoState *is = ffp->is;
    double time;

    Frame *sp, *sp2;

    if (!is->paused 
        && get_master_sync_type(is) == AV_SYNC_EXTERNAL_CLOCK 
        && is->realtime) {
        check_external_clock_speed(is);
    }

    if (!ffp->display_disable 
        && is->show_mode != SHOW_MODE_VIDEO 
        && is->audio_st) {
        time = av_gettime_relative() / 1000000.0;
        if (is->force_refresh 
            || is->last_vis_time + ffp->rdftspeed < time) {
            video_display2(ffp);
            is->last_vis_time = time;
        }
        *remaining_time = FFMIN(*remaining_time, is->last_vis_time + ffp->rdftspeed - time);
    }
    if (is->video_st) {
retry:
        if (frame_queue_nb_remaining(&is->pictq) == 0) {
            // nothing to do, no picture to display in the queue
        } else {
            double last_duration, duration, delay;
            Frame *vp, *lastvp;

            /* dequeue the picture */
            lastvp = frame_queue_peek_last(&is->pictq);
            vp = frame_queue_peek(&is->pictq);

            // 跳帧处理。
            if (vp->serial != is->videoq.serial) {
                frame_queue_next(&is->pictq);
                goto retry;
            }

            if (lastvp->serial != vp->serial) {
                is->frame_timer = av_gettime_relative() / 1000000.0;
            }

            if (is->paused)
                goto display;

            /* compute nominal last_duration */
            // 计算此帧的播放时长
            last_duration = vp_duration(is, lastvp, vp);
            // 计算当前需要delay的时间。
            delay = compute_target_delay(ffp, last_duration, is);
            
            time= av_gettime_relative()/1000000.0;
            av_gettime_relative(), is->frame_timer, delay);
            if (isnan(is->frame_timer) || time < is->frame_timer) {
                is->frame_timer = time;
            }
            
            if (time < is->frame_timer + delay) {
                // 计算出真正需要 sleep 的时间，然后跳到display 渲染此帧
                *remaining_time = FFMIN(is->frame_timer + delay - time, *remaining_time);
                goto display;
            }
            is->frame_timer += delay;
            if (delay > 0 && time - is->frame_timer > AV_SYNC_THRESHOLD_MAX) {
                is->frame_timer = time;
            }
            SDL_LockMutex(is->pictq.mutex);
            if (!isnan(vp->pts)) {
                // 修改 Clock ，下次同步计算处理
                update_video_pts(is, vp->pts, vp->pos, vp->serial);
            }
            SDL_UnlockMutex(is->pictq.mutex);

            if (frame_queue_nb_remaining(&is->pictq) > 1) {
                Frame *nextvp = frame_queue_peek_next(&is->pictq);
                duration = vp_duration(is, vp, nextvp);
                if(!is->step && (ffp->framedrop > 0 || (ffp->framedrop && get_master_sync_type(is) != AV_SYNC_VIDEO_MASTER)) && time > is->frame_timer + duration) {
                    frame_queue_next(&is->pictq);
                    goto retry;
                }
            }
            
            // 字幕处理    
            ...
            
            frame_queue_next(&is->pictq);
            is->force_refresh = 1;

            SDL_LockMutex(ffp->is->play_mutex);
            if (is->step) {
                is->step = 0;
                if (!is->paused)
                    stream_update_pause_l(ffp);
            }
            SDL_UnlockMutex(ffp->is->play_mutex);
        }
display:
        /* display picture */
        if (!ffp->display_disable 
            && is->force_refresh 
            && is->show_mode == SHOW_MODE_VIDEO 
            && is->pictq.rindex_shown) {
            // 渲染视频
            video_display2(ffp);
        }
    }
    
    ...
}
```

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
- [ijkplayer 音视频同步流程分析](https://www.jianshu.com/p/96217ec4356e)
