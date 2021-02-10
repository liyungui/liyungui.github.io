---
title: ijkplayer使用的坑
date: 2019-08-05 15:22:14
categories:
  - 直播
tags:
  - 直播
---

# 常用配置

```
1: 设置是否开启变调
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"soundtouch",isModifyTone?0:1);
2:设置是否开启环路过滤: 0开启，画面质量高，解码开销大，48关闭，画面质量差点，解码开销小
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_CODEC,"skip_loop_filter",isSkipLoopFilter?0:48L);
3:设置播放前的最大探测时间
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT,"analyzemaxduration",100L);
4:设置播放前的探测时间 1,达到首屏秒开效果
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT,"analyzeduration",1);
5:播放前的探测Size，默认是1M, 改小一点会出画面更快
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT,"probesize",1024*10);
6:每处理一个packet之后刷新io上下文
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT,"flush_packets",1L);
7: 是否开启预缓冲，一般直播项目会开启，达到秒开的效果，不过带来了播放丢帧卡顿的体验
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"packet-buffering",isBufferCache?1:0);
8:播放重连次数
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"reconnect",5);
9:最大缓冲大小,单位kb
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"max-buffer-size",maxCacheSize);
10:跳帧处理,放CPU处理较慢时，进行跳帧处理，保证播放流程，画面和声音同步
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"framedrop",5);
11:最大fps
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER,"max-fps",30);
12:设置硬解码方式
jkPlayer支持硬解码和软解码。 软解码时不会旋转视频角度这时需要你通过onInfo的what == IMediaPlayer.MEDIA_INFO_VIDEO_ROTATION_CHANGED去获取角度，自己旋转画面。或者开启硬解硬解码，不过硬解码容易造成黑屏无声（硬件兼容问题），下面是设置硬解码相关的代码

mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "mediacodec", 1);

mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "mediacodec-auto-rotate", 1);

mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "mediacodec-handle-resolution-change", 1);
13.SeekTo设置优化
某些视频在SeekTo的时候，会跳回到拖动前的位置，这是因为视频的关键帧的问题，通俗一点就是FFMPEG不兼容，视频压缩过于厉害，seek只支持关键帧，出现这个情况就是原始的视频文件中i 帧比较少

mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_PLAYER, "enable-accurate-seek", 1);
14. 解决m3u8文件拖动问题 比如:一个3个多少小时的音频文件，开始播放几秒中，然后拖动到2小时左右的时间，要loading 10分钟
mediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT, "fflags", "fastseek");//设置seekTo能够快速seek到指定位置并播放
```

# 不支持https

官方依赖默认不支持

自己编译so文件，或者网上找支持的

# rtmp延迟高

```
播放前的最大探测时间 调低
播放前的探测Size 调低
每处理一个packet之后刷新io上下文
预缓冲 关闭
跳帧处理 开启

mediaPlayer.setOption(1, "analyzemaxduration", 100L);  
mediaPlayer.setOption(1, "probesize", 10240L);  
mediaPlayer.setOption(1, "flush_packets", 1L);  
mediaPlayer.setOption(4, "packet-buffering", 0L);  
mediaPlayer.setOption(4, "framedrop", 1L);  
```

# m3u8

## 表现

高码率m3u8卡顿，音画不同步，只有画面没有声音

## 原因

这个问题一般是首屏加速优化，探测Size(主因)和探测时间(可能影响) 设置过低 导致的

## 解决方案

```
//预加载100k，画面加载更快
ijkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT, "probesize", 102400);
//设置播放前的探测时间。这个可以不配置
ijkMediaPlayer.setOption(IjkMediaPlayer.OPT_CATEGORY_FORMAT, "analyzeduration", 1000L);
```    

## 警告日志

`W/IJKMEDIA: Stream #1: not enough frames to estimate rate; consider increasing probesize`

## 源码分析

`libavformat/utils.c` 的 `avformat_find_stream_info` 函数

遍历两次流，设置每个流需要的编解码器和计算帧率的参数，初始化每个流的解析器paser

然后死循环 读数据进来并解码分析数据流

```
/* We did not get all the codec info, but we read too much data. */
if (read_size >= probesize) {
    ret = count;
    av_log(ic, AV_LOG_DEBUG,
           "Probe buffer size limit of %"PRId64" bytes reached\n", probesize);
    for (i = 0; i < ic->nb_streams; i++)
        if (!ic->streams[i]->r_frame_rate.num &&
            ic->streams[i]->info->duration_count <= 1 &&
            ic->streams[i]->codecpar->codec_type == AVMEDIA_TYPE_VIDEO &&
            strcmp(ic->iformat->name, "image2"))
            av_log(ic, AV_LOG_WARNING,
                   "Stream #%d: not enough frames to estimate rate; "
                   "consider increasing probesize\n", i);
    break;
}
```

# 暂停状态下从后台返回前台黑屏

使用TextureRenderView渲染视图，在退到后台前调用getBitmap方法获取当前画面，使用当前画面遮盖播放器；

# 播放完成后，再次播放只有声音，画面不动

原因是重置了播放器，没有重置surface；
    
# 参考&扩展

- [IjkMediaPlayer 播放无声音Bug](https://blog.csdn.net/qq_34420120/article/details/91415061)
- [ffmpeg学习七：`avformat_find_stream_info`函数源码分析](https://blog.csdn.net/u011913612/article/details/53642355) 无声音bug 源码分析