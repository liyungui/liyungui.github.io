---
title: Android视频录制app解决方案汇总
date: 2019-09-03 14:52:14
categories:
  - 直播
tags:
  - 直播
---

[Android视频录制app解决方案汇总](https://www.zybuluo.com/lichangadd/note/148109)

现在视频App很多：蝌蚪音客、美拍、小影、还有最近火起来的小咖秀。

这类App的技术难点基本都是在音视频处理这一块

iOS对多媒体处理的支持还算比较丰富，Android差很多。

这里总结蝌蚪音客在多媒体处理上遇到的问题，供大家参考下。

# 一、录制方视频(1：1)  #

现在市面上的视频应用的视频尺基本全部都是1：1的，这对于Android开发者来说就是一个比较棘手的问题，Android原生Recorder类并不支持视频比例的设置。

所以只能想其他办法，目前常用的办法大致可以分为2种：

## a. 摒弃原生接口，使用FFmpeg或OpenCV等方式进行录制  ##

- **缺点**

	对开发者技术要求较高，FFmpeg和OpenCV**移植麻烦**，**多机型兼容复杂** 并且要求开发者一定程度的**C语言功底**

- **最难解决的问题是性能问题**

	FFmeg和OpenCV都是开源方案，如果要真正达实用级别往往还**需要优化定制**，这对于熟练于做Android展现的开发者来说完全就是一个新的领域。蝌蚪音客就尝试过这种方案，结果视频的码率只能做到15fps左右，这明显是不够的。

## b. 使用原生API录制，遮罩1：1视觉效果  ##

- 在录制界面使用遮罩的方式给用户一种1：1的错觉。

- 在预览视频时，使用FFmpeg进行视频裁剪。

**如果团队没有驾驭FFmpeg的能力，个人建议使用这种方式。**

视频录制功能来说相对简单，而且裁剪命令优化后基本可以可以做到视频预览一遍也就基本裁剪完毕(**耗时>=视频时长**，真心伤)。

# 二、本地视频压缩 # 

**本地视频压缩除了FFmpeg之外目前还没有了解到有其他方案**

但是压缩命令的优化可是一门学问，使用 `x264` 还是 `mpeg4`，`码率`，`分辨率`，`帧频`，`文件大小` 等都会影响到 `压缩速度` 而且差别相当大。

在android平台运行效率实在蛋疼，测试压缩一个mp4，**耗时>=视频时长x6**。网络说在CentOS服务器上跑都是 耗时=视频时长

# 三、m3u8解决方案  #

绝对不建议创业公司**自己编写播放器，绝对无底洞**，还不如直接使用MP4文件格式。

m3u8国内比较出名的是 **vitamio**，还有一些韩国人的技术方案。但是vitamio的**开源版本感觉很久没有更新**，而且商业版本的授权动则几十万

**推荐使用百度媒体云的m3u8的解决方案**，代码家的AnimeTaste使用的就是这个，完全免费，项目质量还算稳定。但是**只能做成单例**，如果想集成到listview中，需要费点事。

# 四、视频滤镜、水印  #

- 水印 

	**FFmpeg** 在视频处理的过程中可以并行处理水印。

- 视频滤镜

	赶紧花钱招大牛吧。

	据说小影的开发Leader在视频处理领域里沉浸了20多年。

	目前这部分笔者还是在了解阶段，目前看到的方案有使用GPUImage进行处理的，但是无奈对图像处理的知识掌握的太少，迟迟没有动手。

# 五、[趣拍云](https://www.qupaicloud.com/) #

阿里百川和趣拍合作推出，包括 短视频sdk 和 直播sdk。收费不便宜