---
title: 内存Code部分的占用
date: 2019-04-11 16:43:53
categories:
  - Android
tags:
  - 性能优化
---

加载 dex，so文件 占用的内存

**工具**：Linux /proc/<pid>/smaps 文件分析脚本

python代码 (本目录下 smap.py文件)：https://gist.github.com/LanderlYoung/aedd0e1fe09214545a7f20c40c01776c

# 参考&扩展

- [我这样减少了26.5M Java内存！](https://wetest.qq.com/lab/view/359.html?from=adsout_qqtips_past2_359) 腾讯WeTest上企鹅FM的内存优化