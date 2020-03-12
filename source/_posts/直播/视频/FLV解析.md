---
title: FLV解析
date: 2019-12-04 11:42:14
categories:
  - 直播
tags:
  - 直播
---

# FLV封装格式

一个文件头（File Header）+一个文件体（File Body）。结构如下图：

{% asset_img flv结构.png %}

# 文件头

```cpp
typedef unsigned char byte;
typedef struct {
    byte Signature[3]; //文件标识，3字节；固定内容"FLV"(0x46, 0x4c, 0x4c)
    byte Version; //版本，目前为0x1
    byte Flags; //前5位保留为0；第6位标识是否存在音频tag；第7位保留为0；第8位标识是否存在视频tag；
    uint DataOffset; //文件体偏移，4字节；即文件头大小，版本1总为9
} FLV_HEADER; //9字节
```

{% asset_img header实例.png %}

Flags 这里为5，即 00000101，表示音视频tag都有

# 文件体

一连串的 `back-pointer`(反向指针，即指向前面的指针)和 `tag` 构成

## `back-pointer`

固定4个字节，表示前一个tag的size。

## tag

分三种类型，video、audio、scripts。

tag由header和data两部分组成。

header结构相同，不同类型tag 的 data结构各不相同

### tag header

```cpp
typedef unsigned char byte;
typedef unsigned int uint;
typedef struct {
    byte TagType; //tag类型；8为Audio,9为Video,18为scripts
    byte DataSize[3]; //tag data长度，3字节；
    byte Timestamp[3]; //时间戳，3字节；相对毫秒值，第一个tag时间戳总是0
    byte TimestampExtended; //扩展时间戳，1字节，时间戳高8位，上面时间戳3位不够用的时候，将使用该字节；
    byte StreamId[3]; //StreamId，3字节，总是0；
} TAG_HEADER; //11字节
```

{% asset_img tag-header实例.png %}

图中红色部分是两个 `back-pointer`，都是4个字节。他们中间就是第一个TAG

蓝色是第一个tag的tag data长度，3个字节

第一个 `back-pointer` 是0x00000000，那是因为后面是第一个TAG。所以他为0。

第一个tag的tag data长度为0x000125=293。那么到第一个TAG结束，总共有293+24=137=0x13D。(header 9 + back-pointer 4 + tag-header 11 = 24)

第二个 `back-pointer` 是0x00000130=304，即第一个tag长度(293 + 11 = 304)

### 脚本 tag data

又被称为 `MetaData Tag`

存放一些关于FLV视频和音频的元信息，比如：duration、width、height等。通常该类型Tag会作为FLV文件的第一个tag，并且只有一个

脚本的数据类型 都是以数据类型+（数据长度）+数据的格式出现的，数据类型占1byte，数据长度看数据类型是否存在，后面才是数据。

一般来说，该Tag Data结构包含两个AMF包。

AMF（Action Message Format）是Adobe设计的一种通用数据封装格式，在Adobe的很多产品中应用，简单来说，AMF将不同类型的数据用统一的格式来描述。

第一个AMF包封装字符串类型数据，用来装入一个“onMetaData”标志，这个标志与Adobe的一些API调用有关。第1个字节表示AMF类型，一般为0x02，表示字符串；第2、3个字节用来标识字符长度，一般总是0x000A。后面字节为具体的字符串onMetaData。

第二个AMF包封装一个数组类型，这个数组中包含了音视频信息项的名称和值。第1个字节表示AMF包类型，一般总是0x08，表示数组。第2-5个字节表示数组元素个数，后面几位是各数组元素的封装，数组元素为(名称-值)组成的对

```
duration 时长
width 视频宽度
height 视频高度
videodatarate 视频码率
framerate 视频帧率
videocodecid 视频编码方式
audiosamplerate 音频采样率
audiosamplesize 音频采样精度
stereo 是否为立体声
audiocodecid 音频编码方式
filesize 文件大小
```

### 视频 tag data

{% asset_img 视频tag-data结构.png %}

一个字节包含了视频数据的参数信息，从第二个字节开始为视频流

帧类型，4bit

```
1 keyframe （for AVC，a seekable frame）
2 inter frame （for AVC，a nonseekable frame）
3 disposable inter frame （H.263 only）
4 generated keyframe （reserved for server use）
5 video info/command frame
```

视频编码类型，4bit

```
1 JPEG （currently unused）
2 Sorenson H.263
3 Screen video
4 On2 VP6
5 On2 VP6 with alpha channel
6 Screen video version 2
7 AVC //H.264
```

#### AVC视频tag

视频编码类型是AVC（H.264）的话，VideoTag data 最前面4个字节表示AVCPacketType 和CompositionTime。

```
byte AVCPacketType; //AVCPacketType，1字节
byte CompositionTime [3]; //CompositionTime，3字节
```

#### AVCPacketType

```
0 AVCDecoderConfigurationRecord(AVC sequence header)
1 AVC NALU
2 AVC end of sequence (lower level NALU sequence ender is not required or supported)
```

AVCDecoderConfigurationRecord.包含着是H.264解码相关比较重要的sps和pps信息，给AVC解码器送数据流之前一定要把sps和pps信息送出，否则的话解码器不能正常解码。而且在解码器stop之后再次start之前，如seek、快进快退状态切换等，都需要重新送一遍sps和pps的信息.AVCDecoderConfigurationRecord在FLV文件中一般情况也是出现1次，也就是第一个video tag.

#### CompositionTime

AVCPacketType ==1 该值才有意义；其他情况下该值为0

#### sps pps

`0x01+sps[1]+sps[2]+sps[3]+0xFF+0xE1+sps size(2字节)+sps+01+pps size(2字节)+pps`

#### 实例

{% asset_img 视频tag实例.png %}

```
---tag header---
TagType =0x09=9。这是一个video tag。
DataSize =0x000030=48。长度为48。
Timestamp =0x000000。
TimestampExtended =0x00。
StreamId =0x000000

---tag data---
视频参数（帧类型，编码类型）= 0x17;1 = 关键帧，7 = AVC //H.264
AVCPacketType = 0x00
CompositionTime = 0x000000
sps[1]=0x64
sps[2]=00
sps[3]=0D
sps size=0x001B=27
跳过sps(27个字节)后，是0x01
pps size=0x0005
跳过5个字节，就到了`back-pointer`=0x3B，即59(tag-header 11 + tag data 48)。
```

### 音频 tag data

{% asset_img 音频tag-data结构.png %}

一个字节包含了音频数据的参数信息，从第二个字节开始为音频流

音频编码类型，4bit

```
0 Linear PCM，platform endian
1 ADPCM
2 MP3
3 Linear PCM，little endian
4 Nellymoser 16-kHz mono
5 Nellymoser 8-kHz mono
6 Nellymoser
7 G.711 A-law logarithmic PCM
8 G.711 mu-law logarithmic PCM
9 reserved
10 AAC
14 MP3 8-Khz
15 Device-specific sound
```

音频采样率，2bit

```
0 5.5kHz
1 11KHz
2 22 kHz
3 44 kHz //FLV并不支持48KHz的采样率；对于AAC总是3
```

音频采样精度，1bit

```
0 8bits
1 16bits //压缩过的音频都是16bit
```

音频类型，1bit

```
0 sndMono
1 sndStereo //对于AAC总是1
```

# FLV解析流程

{% asset_img FLV解析.jpg %}

# 参考&扩展

- [FLV解析](https://www.jianshu.com/p/4c86b55833ca) 文件结构 + 解析代码
- [视频flv格式是什么文件 怎么打开播放](http://www.365jz.com/article/24612)  周杰伦《东风破》MV文件16进制分析
