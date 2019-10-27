---
title: 微信语音编码-silk
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

# [Android微信语音聊天记录及文本聊天记录 数据库破解 silk 整理](http://blog.csdn.net/voler_HJL/article/details/53788126) #

**微信语音文件存储位置**

	根目录 -》tencent -》MicroMsg -》名字很长又很乱的那个文件夹 -》voice2 

**播放**

.amr后缀，但它并不是真正的.amr文件，amr播放器是播放不了的 

其实是silk v3格式，QQ的语音文件也是这种格式 

# [微信语音文件的格式转换](http://www.jianshu.com/p/71137d5acf78) #

起初，iOS 只是去掉了文件头的 amr，添上就能还原为 amr 了；Android 则是原生的 amr。

微信6.0 之后开始采用 silk 编码来传输语音，必须用 slik v3 解码器

这方面许多人做过工作，罗列一下：

## 个人 ##

**kn007**: 

[解码转换QQ微信的SILK v3编码音频为MP3或其他格式](https://kn007.net/topics/decoding-qq-wechat-silk-v3-encoded-audio-to-mp3-or-other-formats/)

[Windows下批量转换Silk v3音频文件为MP3格式](https://kn007.net/topics/batch-convert-silk-v3-audio-files-to-mp3-in-windows/)

[更新了Silk2MP3](https://kn007.net/topics/update-silk2mp3-to-official-version/)

**snakeninny**：

[从微信中提取语音文件，并转换成文字的全自动化解决方案](http://bbs.iosre.com/t/topic/3199)

**hangcom**：《iOS应用逆向工程》的作者，之前还开发了朋友圈导出。

[微信语音文件的解析](https://zhuanlan.zhihu.com/p/21783890)

**杨树下的狐狸**：Android 方案

[微信的语音聊天记录可以从手机提取出来保存到PC上么？ - 知乎](https://www.zhihu.com/question/19909162/answer/80640430)

**cxun**：整体解决方案

（暂时失效）[微信聊天记录查看器（程序+源码）](http://www.cnblogs.com/cxun/p/4338643.html)

## 商用 ##

iTools：可以转换 aud 到 wav

楼月微信聊天记录导出恢复助手：同上

其他还有：Silk 手机音频播放器、Silk 转换工具、WeBack 等等。

# [Skype Silk 与Opus的关系](http://tiger-beach.blogspot.com/2014/04/skype-silk-opus.html) #

Skype自2009年1月以来一直采用自己的SILK音频编码解码器，但是从2012年起过渡到新的Opus标准。

Opus标准已经获互联网工程任务组（IETF）批准，标准格式为RFC 6716。

Opus支持6kbps到510kbps的可变比特率。

它是一个有损声音编码的格式，适用于网络上的实时声音传输。

由于是一个开放格式，Opus在使用上没有任何专利限制。

Opus合并了Xiph.org的CELT低延时音频编解码器和Skype的SILK语音编解码器，专为互联网音频设计，可用于替代现有的私有音频编解码器

由 Xiph.Org、Mozilla、微软、Broadcom、Octasic和Google联合开发。
