---
title: ijkplayer系列三-数据读取线程
date: 2019-08-06 15:22:14
categories:
  - 直播
tags:
  - 直播
---

ijkplayer播放器的初始化流程(上一篇)，在IjkMediaPlayer.prepareAsync 中调用 `ff_ffplayer.c` `stream_open()` 创建了几个线程：

- 视频显示线程
- 数据读取线程 `read_thread`
- 消息循环处理线程

{% asset_img 线程.jpg %}

# 数据读取线程

{% asset_img 数据读取流程图.png %}

	1. 调用avformat_alloc_context
		1. 创建AVFormatContext对象，主要为函数指针赋值，确定默认打开文件的函数，以及关闭文件的函数
	2. 调用avformat_open_input
		1. 调用init_input：打开文件，探测视频格式
		2. 调用avio_skip：跳过初始化的字节
		3. 调用ff_id3v2_read_dict：判断是否有id3v2格式的字段
		4. 调用s->iformat->read_header：从buffer里面读取视频头，确定解码器
		5. 调用ff_id3v2_parse_chapters：解析id3v2中的章节、描述等信息
	3. 调用avformat_find_stream_info：解析视频中的各个流的信息，如video、audio流
	4. 调用avformat_seek_file：判断是否有seek操作，需要seek文件
	5. 调用avformat_match_stream_specifier：分离audio，video流信息，判断当前流的类型
	6. 调用av_find_best_stream：根据当前ffplayer找到video，audio，subtitle的流（一般的视频各个流都只有一个）
	7. 调用stream_component_open：打开audio，video的流信息，根据流信息找到decoder，然后开启各自的线程进行解码
	8. 调用ffp_notify_msg1发送FFP_MSG_PREPARED消息
	9. 进入无限循环，从解析流的线程中获取Packet，同步到video_refresh_thread线程中，进行时钟同步，开始播放
		1. 判断是否有seek操作is->seek_req，若有则调用avformat_seek_file
		2. 判断是否当前video、audio、subtitle的PacketQueue已满，如果已经满了，则直接进入下一次循环
		3. 判断当前视频是否暂停或者播放完成，判断是否为循环播放，以及循环播放次数，重新seek到start_time的位置，若未设置，默认为0
		4. 调用av_read_frame读取packet帧
		5. 将对应的packet放到对应的video、audio、subtitle的PacketQueue中
		6. 判断ffp->packet_buffering，如果是的话，则调用ffp_check_buffering检查Buffer

```c
static int read_thread(void *arg)
{

	//...
	// Utils.c。探测数据源的格式。
	//内部实现是调用id3v2_parse()读取网络数据包头信息
	//ff_id3v2_parse_apic()/id3v2.c
	//更改ic的AVFormatContext型的参数
   err = avformat_open_input(&ic, is->filename, is->iformat, &ffp->format_opts);
  	//...
  	//解析流并找到相应解码器
  	//注册解码器是在初始化时，JNI_Load() -->ijkmp_global_init() --> avcodec_register_all();
  	err = avformat_find_stream_info(ic, opts);
	//...
   /* open the streams */
   //音视频读取和解码
    if (st_index[AVMEDIA_TYPE_AUDIO] >= 0) {
        stream_component_open(ffp, st_index[AVMEDIA_TYPE_AUDIO]);
    }

    ret = -1;
    if (st_index[AVMEDIA_TYPE_VIDEO] >= 0) {
        ret = stream_component_open(ffp, st_index[AVMEDIA_TYPE_VIDEO]);
    }
	//...
	//循环读取数据，然后把数据放入相应的audio队列或者video队列中
	for (;;) {
		//省略...判断是否队列已满，停止读取数据
		//判断是否需要响应用户操作拖动进度条
	   if (is->seek_req) {
          avformat_seek_file();
      } 
	   ret = av_read_frame(ic, pkt);
	   packet_queue_put(&is->audioq, pkt); 
	   //如果是视频的话 
	   //packet_queue_put(&is->videoq, pkt);  
   }
}
```

# 音视频读取和解码


```c
static int stream_component_open(FFPlayer *ffp, int stream_index)
{
  	//...
    codec = avcodec_find_decoder(avctx->codec_id);
    switch (avctx->codec_type) {
        case AVMEDIA_TYPE_AUDIO   : is->last_audio_stream    = stream_index; forced_codec_name = ffp->audio_codec_name; break;
        // FFP_MERGE: case AVMEDIA_TYPE_SUBTITLE:
        case AVMEDIA_TYPE_VIDEO   : is->last_video_stream    = stream_index; forced_codec_name = ffp->video_codec_name; break;
        default: break;
    }
	//...
    switch (avctx->codec_type) {
    case AVMEDIA_TYPE_AUDIO:
        /* prepare audio output */
        //audio_open调用aout->open_audio(aout, pause_on);
        //最终会调用aout_open_audio_n()
        //最后创建音频播放线程 SDL_CreateThreadEx(&opaque->_audio_tid, aout_thread);
        //aout_thread线程从解码好的音频帧队列sampq中，循环取数据推入AudioTrack中播放。
        if ((ret = audio_open(ffp, channel_layout, nb_channels, sample_rate, &is->audio_tgt)) < 0)
            goto fail;
      	//...
        decoder_init(&is->auddec, avctx, &is->audioq, is->continue_read_thread);
      	//...
     	//decoder_start();创建音频解码线程 SDL_CreateThreadEx(&is->_audio_tid, audio_thread, ffp, "ff_audio_dec");
     	//audio_thread 线程从audioq队列中获取音频包，解码并加入sampq音频帧列表中 
        if ((ret = decoder_start(&is->auddec, audio_thread, ffp, "ff_audio_dec")) < 0)
            goto fail;
        SDL_AoutPauseAudio(ffp->aout, 0);
        break;
    case AVMEDIA_TYPE_VIDEO:
   		//...
        decoder_init(&is->viddec, avctx, &is->videoq, is->continue_read_thread);
        ffp->node_vdec = ffpipeline_open_video_decoder(ffp->pipeline, ffp);
   		//...
   		//decoder_start();创建视频解码线程 SDL_CreateThreadEx(&is->_video_tid, video_thread, ffp, "ff_video_dec");
   		//video_thread 线程从videoq队列中获取视频包，解码并放入pictq列表中
        if ((ret = decoder_start(&is->viddec, video_thread, ffp, "ff_video_dec")) < 0)
            goto fail;
       	//...
        break;
    }
fail:
    av_dict_free(&opts);

    return ret;
}
```

# 总结

- 读取数据的时候，当queue满了的时候，会delay。然而并不会断开连接。
- 在读取的时候，有很多操作，这些操作都是受java层界面的影响，比如pause和resume操作，seek操作等。如果界面按了暂停什么的，都会反馈到这里，然后这里无限for循环的时候会相应作出各种操作。
- `read_thread` 线程里面会创建两个解码线程，一个音频播放线程。

# 参考&扩展

- [github](https://github.com/bilibili/ijkplayer)
- [ijkplayer 源码分析（上）](https://www.jianshu.com/p/5345ab4cf979) 王英豪，基于k0.8.8版本
- [ijkplayer框架深入剖析](https://cloud.tencent.com/developer/article/1032547) 金山云团队，基于k0.7.6版本
- [ijkplayer视频播放器源码分析(android)](https://www.jianshu.com/p/7d9b86919682) 尸情化异，基于k0.5.1版本，系列专栏5篇：使用，初始化，数据读取，音频解码播放，视频解码播放
- [ijkplayer read_thread命令简单解析](https://blog.csdn.net/Guofengpu/article/details/85060662)
