---
title: 果肉采集SDK设计文档
date: 2020-04-02 14:52:14
categories:
  - 直播
tags:
  - 直播
---

{% asset_img 类图.png %}

{% asset_img 时序图.png %}

{% asset_img 采集端通信时序图.png %}

# 二维码

二维码包含采集设备信息

`{"id":"123456789","name":"设备自定义名字","ip":"192.168.1.2","rtspPort"}`

# Socket连接

Socket连接成功，采集端返回采集设备信息

`{"id":"123456789","name":"设备自定义名字","ip":"192.168.1.2"}`

# 指令

基于自建Socket传输

## 开始采集 startCapture

```
{"opt":"startCapture","config":{"video":true,"audio":true,"camera":"front"}}
#config 可省略，有默认配置
#是否采集视频 video；
#是否采集音频 audio；
#摄像头 camera：前置摄像头 front；后置摄像头 back；

{"code":0,"msg":"ok"}
```

## 结束采集 stopCapture

```
{"opt":"stopCapture"}

{"code":0,"msg":"ok"}
```

## 心跳

暂定10s一次

```
{"opt":"ping"}

{"code":0,"msg":"ok"}
```

## 采集设置 setCaptureConfig

```
{"opt":"setCaptureConfig","config":{"video":true,"audio":true,"camera":"front"}}
#是否采集视频 video；
#是否采集音频 audio；
#摄像头 camera：前置摄像头 front；后置摄像头 back；

{"code":0,"msg":"ok"}
```

## 获取采集设置 getCaptureConfig

```
{"opt":"getCaptureConfig"}

{"code":0,"msg":"ok","data":{"video":true,"audio":true,"camera":"front"}}
#是否采集视频 video；
#是否采集音频 audio；
#摄像头 camera：前置摄像头 front；后置摄像头 back；
```


