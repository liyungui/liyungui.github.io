---
title: RTSP协议
date: 2019-06-04 12:51:53
categories:
  - 网络
tags:
  - 网络
---

# 网络模型

{% asset_img 架构.png %}

RTSP (Real-time Streaming Protocol) 实时流协议。提供流的远程控制服务(play, seek, pause, stop等)

SDP (Session Description Protocol) 会话描述协议。RTSP客户端和服务端通过SDP传递信息。常用于 通知协议(SAP)、会话初始协议(SIP)、实时流协议(RTSP)

RTP (Real-time Transport Protocol) 实时传输协议。提供端到端的实时传输服务，但并不保证服务质量，服务质量由RTCP来提供。

RTCP (Real-time Transport Control Protocol) 实时传输控制协议

RSVP (Resource Reservation Protocol) 资源预留协议。在路由器上预留一定的带宽，能在一定程度上为流媒体的传输提供服务质量。

## RTP和RTCP属于应用层？

不少人也把RTP归为应用层协议，因为从应用开发的角度来说，RTP的实现还是要靠开发者自己。

## UDP实现流媒体

UDP是无序且可以丢包的

要在UDP上实现流式传输，就需要**降低延迟和恢复数据包时序**。

在发送端，为降低延迟，往往对传输数据进行预处理(降低质量和高效压缩)。

在接收端，为了恢复数据包时序，采用了接收缓冲；为了播放媒体流畅，则采用了播放缓冲。

# RTSP消息格式

RTSP的消息有两大类，一是请求消息(request)，一是回应消息(response)，两种消息的格式不同。

## 请求消息

```
方法 URI RTSP版本 CR LF
消息头 CR LF CR LF
消息体 CR LF
```

## 回应消息

```
RTSP版本 状态码 解释 CR LF
消息头 CR LF CR LF
消息体 CR LF
```

## 字段解释

```
方法 包括：OPTIONS、SETUP、PLAY、TEARDOWN DESCRIBE
URI 是接收方（服务端）的地址，例如：rtsp://192.168.22.136:5000/v0
RTSP版本 一般都是 RTSP/1.0
CR LF 表示回车换行，需要接收端有相应的解析

状态码 是一个数值，200表示成功
解释 是与状态码对应的文本解释

消息头 需要有两个CR LF

消息体 非必须
```

## 实例

```
DESCRIBE rtsp://192.168.1.211 RTSP/1.0
CSeq: 1
Accept: application/sdp
User-Agent: magnus-fc
```

```
RTSP/1.0 200 OK
CSeq: 1
Server: GrandStream Rtsp Server V100R001
Content-Type: application/sdp
Content-length: 256
Content-Base: rtsp://192.168.1.211/0

v=0
o=StreamingServer 3331435948 1116907222000 IN IP4 192.168.1.211
s=h264.mp4
c=IN IP4 0.0.0.0
t=0 0
a=control:*
m=video 0 RTP/AVP 96
a=control:trackID=0
a=rtpmap:96 H264/90000
m=audio 0 RTP/AVP 97
a=control:trackID=1
a=rtpmap:97 G726-16/8000
```

# 一次基本交互

{% asset_img 常用方法.png %}

{% asset_img 一次基本交互.png %}

# 常用命令及其消息实例

## OPTIONS

OPTIONS请求是客户端向服务器询问可用的方法，请求和回复实例如下：

```
C->S:  OPTIONS rtsp://example.com/media.mp4 RTSP/1.0
       CSeq: 1
       Require: implicit-play
       Proxy-Require: gzipped-messages
 
S->C:  RTSP/1.0 200 OK
       CSeq: 1
       Public: DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE
```

## DESCRIBE

客户端向服务器请求媒体资源描述，服务器端通过SDP协议回应客户端的请求。

资源描述中会列出所请求媒体的媒体流及其相关信息，典型情况下，音频和视频分别作为一个媒体流传输。实例如下：

```
C->S: DESCRIBE rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 2
 
S->C: RTSP/1.0 200 OK
      CSeq: 2
      Content-Base: rtsp://example.com/media.mp4
      Content-Type: application/sdp
      Content-Length: 460
 
      m=video 0 RTP/AVP 96
      a=control:streamid=0
      a=range:npt=0-7.741000
      a=length:npt=7.741000
      a=rtpmap:96 MP4V-ES/5544
      a=mimetype:string;"video/MP4V-ES"
      a=AvgBitRate:integer;304018
      a=StreamName:string;"hinted video track"
      m=audio 0 RTP/AVP 97
      a=control:streamid=1
      a=range:npt=0-7.712000
      a=length:npt=7.712000
      a=rtpmap:97 mpeg4-generic/32000/2
      a=mimetype:string;"audio/mpeg4-generic"
      a=AvgBitRate:integer;65790
      a=StreamName:string;"hinted audio track"
```

## SETUP

SETUP请求确定了具体的媒体流如何传输，该请求必须在PLAY请求之前发送。

SETUP请求包含媒体流的URL和客户端用于接收RTP数据(audio or video)的端口以及接收RTCP数据(meta information)的端口。

服务器端的回复通常包含客户端请求参数的确认，并会补充缺失的部分，比如服务器选择的发送端口。

```
C->S: SETUP rtsp://example.com/media.mp4/streamid=0 RTSP/1.0
      CSeq: 3
      Transport: RTP/AVP;unicast;client_port=8000-8001
 
S->C: RTSP/1.0 200 OK
      CSeq: 3
      Transport: RTP/AVP;unicast;client_port=8000-8001;server_port=9000-9001;ssrc=1234ABCD
      Session: 12345678
```

## PLAY

客户端通过PLAY请求来播放一个或全部媒体流，PLAY请求可以发送一次或多次，发送一次时，URL为包含所有媒体流的地址，发送多次时，每一次请求携带的URL只包含一个相应的媒体流。

PLAY请求中可指定播放的range，若未指定，则从媒体流的开始播放到结束，如果媒体流在播放过程中被暂停，则可在暂停处重新启动流的播放。

```
C->S: PLAY rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 4
      Range: npt=5-20
      Session: 12345678
 
S->C: RTSP/1.0 200 OK
      CSeq: 4
      Session: 12345678
      RTP-Info: url=rtsp://example.com/media.mp4/streamid=0;seq=9810092;rtptime=3450012
```

## PAUSE

PAUSE请求会暂停一个或所有媒体流，后续可通过PLAY请求恢复播放。

PAUSE请求中携带所请求媒体流的URL，若参数range存在，则指明在何处暂停，若该参数不存在，则暂停立即生效，且暂停时长不确定。

```
C->S: PAUSE rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 5
      Session: 12345678
 
S->C: RTSP/1.0 200 OK
      CSeq: 5
      Session: 12345678
```

## TEARDOWN

结束会话请求，该请求会停止所有媒体流，并释放服务器上的相关会话数据。

```
C->S: TEARDOWN rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 8
      Session: 12345678
 
S->C: RTSP/1.0 200 OK
      CSeq: 8
```

## GET_PARAMETER

检索指定URI数据中的参数值。

不携带消息体的GET_PARAMETER可用来测试服务器端或客户端是否可通(类似ping的功能)。

```
S->C: GET_PARAMETER rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 9
      Content-Type: text/parameters
      Session: 12345678
      Content-Length: 15
 
      packets_received
      jitter
 
C->S: RTSP/1.0 200 OK
      CSeq: 9
      Content-Length: 46
      Content-Type: text/parameters
 
      packets_received: 10
      jitter: 0.3838
```

## SET_PARAMETER

用于设置指定媒体流的参数。

```
C->S: SET_PARAMETER rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 10
      Content-length: 20
      Content-type: text/parameters
 
      barparam: barstuff
 
S->C: RTSP/1.0 451 Invalid Parameter
      CSeq: 10
      Content-length: 10
      Content-type: text/parameters
 
      barparam
```

## REDIRECT

重定向请求，用于服务器通知客户端新的服务地址，客户端需要向这个新地址重新发起请求。

重定向请求中可能包含Range参数，指明重定向生效的时间。

客户端若需向新服务地址发起请求，必须先teardown当前会话，再向指定的新主机setup一个新的会话。

```
S->C: REDIRECT rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 11
      Location: rtsp://bigserver.com:8001
      Range: clock=19960213T143205
```

## ANNOUNCE

ANNOUNCE请求有两个用途：

- (1)C->S：客户端向服务器端发布URL指定的媒体信息描述；
- (2) S->C：实时全量更新对话描述。若媒体表示中新增了一个媒体流，则整个媒体表示的description都要被重新发送，而不是只发送新增部分。

```
C->S: ANNOUNCE rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 7
      Date: 23 Jan 1997 15:35:06 GMT
      Session: 12345678
      Content-Type: application/sdp
      Content-Length: 332
 
      v=0
      o=mhandley 2890844526 2890845468 IN IP4 126.16.64.4
      s=SDP Seminar
      i=A Seminar on the session description protocol
      u=http://www.cs.ucl.ac.uk/staff/M.Handley/sdp.03.ps
      e=mjh@isi.edu (Mark Handley)
      c=IN IP4 224.2.17.12/127
      t=2873397496 2873404696
      a=recvonly
      m=audio 3456 RTP/AVP 0
      m=video 2232 RTP/AVP 31
 
S->C: RTSP/1.0 200 OK
      CSeq: 7
```

## RECORD

请求录制指定范围的媒体数据，请求中可指定录制的起止时间戳；若未指定时间范围，则使用presentation description中的开始和结束时间，这种情况下，如果会话已开始，则立即启动录制操作。

```
C->S: RECORD rtsp://example.com/media.mp4 RTSP/1.0
      CSeq: 6
      Session: 12345678
 
S->C: RTSP/1.0 200 OK
      CSeq: 6
      Session: 12345678
```

# PC拉流海康摄像头实例

Wireshark抓取PC播放海康摄像头视频流：

```
OPTIONS rtsp://10.3.8.202:554 RTSP/1.0
CSeq: 2
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
 
RTSP/1.0 200 OK
CSeq: 2
Public: OPTIONS, DESCRIBE, PLAY, PAUSE, SETUP, TEARDOWN, SET_PARAMETER, GET_PARAMETER
Date:  Mon, Jan 29 2018 16:56:47 GMT
 
DESCRIBE rtsp://10.3.8.202:554 RTSP/1.0
CSeq: 3
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Accept: application/sdp
 
RTSP/1.0 401 Unauthorized
CSeq: 3
WWW-Authenticate: Digest realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", stale="FALSE"
Date:  Mon, Jan 29 2018 16:56:47 GMT
 
DESCRIBE rtsp://10.3.8.202:554 RTSP/1.0
CSeq: 4
Authorization: Digest username="admin", realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", uri="rtsp://10.3.8.202:554", response="3fc4b15d7a923fc36f32897e3cee69aa"
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Accept: application/sdp
 
RTSP/1.0 200 OK
CSeq: 4
Content-Type: application/sdp
Content-Base: rtsp://10.3.8.202:554/
Content-Length: 551
 
v=0
o=- 1517245007527432 1517245007527432 IN IP4 10.3.8.202
s=Media Presentation
e=NONE
b=AS:5050
t=0 0
a=control:rtsp://10.3.8.202:554/
m=video 0 RTP/AVP 96
c=IN IP4 0.0.0.0
b=AS:5000
a=recvonly
a=x-dimensions:2048,1536
a=control:rtsp://10.3.8.202:554/trackID=1
a=rtpmap:96 H264/90000
a=fmtp:96 profile-level-id=420029; packetization-mode=1; sprop-parameter-sets=Z00AMp2oCAAwabgICAoAAAMAAgAAAwBlCA==,aO48gA==
a=Media_header:MEDIAINFO=494D4B48010200000400000100000000000000000000000000000000000000000000000000000000;
a=appversion:1.0
 
SETUP rtsp://10.3.8.202:554/trackID=1 RTSP/1.0
CSeq: 5
Authorization: Digest username="admin", realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", uri="rtsp://10.3.8.202:554/", response="ddfbf3e268ae954979407369a104a620"
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Transport: RTP/AVP;unicast;client_port=57844-57845
 
RTSP/1.0 200 OK
CSeq: 5
Session:       1273222592;timeout=60
Transport: RTP/AVP;unicast;client_port=57844-57845;server_port=8218-8219;ssrc=5181c73a;mode="play"
Date:  Mon, Jan 29 2018 16:56:47 GMT
 
PLAY rtsp://10.3.8.202:554/ RTSP/1.0
CSeq: 6
Authorization: Digest username="admin", realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", uri="rtsp://10.3.8.202:554/", response="b5abf0b230de4b49d6c6d42569f88e91"
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Session: 1273222592
Range: npt=0.000-
 
RTSP/1.0 200 OK
CSeq: 6
Session:       1273222592
RTP-Info: url=rtsp://10.3.8.202:554/trackID=1;seq=65373;rtptime=3566398668
Date:  Mon, Jan 29 2018 16:56:47 GMT
 
GET_PARAMETER rtsp://10.3.8.202:554/ RTSP/1.0
CSeq: 7
Authorization: Digest username="admin", realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", uri="rtsp://10.3.8.202:554/", response="bb2309dcd083b25991c13e165673687b"
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Session: 1273222592
 
RTSP/1.0 200 OK
CSeq: 7
Date:  Mon, Jan 29 2018 16:56:47 GMT
 
TEARDOWN rtsp://10.3.8.202:554/ RTSP/1.0
CSeq: 8
Authorization: Digest username="admin", realm="IP Camera(10789)", nonce="6b9a455aec675b8db81a9ceb802e4eb8", uri="rtsp://10.3.8.202:554/", response="e08a15c27d3daac14fd4b4bcab424a5e"
User-Agent: LibVLC/2.2.8 (LIVE555 Streaming Media v2016.02.22)
Session: 1273222592
 
RTSP/1.0 200 OK
CSeq: 8
Session:       1273222592
Date:  Mon, Jan 29 2018 16:57:03 GMT
```

# 参考&扩展

- [RTP协议分析](https://blog.csdn.net/u011006622/article/details/80675054)流媒体架构
- [RTSP协议学习](https://blog.csdn.net/lory17/article/details/60144734) 协议，常用方法，完整抓包，源码实现
- [网络流媒体协议之——RTSP协议](https://www.cnblogs.com/linhaostudy/p/11140823.html) 更多方法的抓包(REDIRECT、RECORD等)
- [RTSP、HTTP、HTTPS、SDP四种协议详解](https://blog.csdn.net/feixiaku/article/details/39231629)