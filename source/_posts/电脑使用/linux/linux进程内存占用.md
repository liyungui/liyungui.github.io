---
title: Linux进程内存占用
date: 2019-03-26 10:43:53
categories:
  - 电脑使用
tags:
  - Linux
---

Linux进程占用的内存有 `VSS/RSS/PSS/USS` 四种形式

这四种形式首字母分别是Virtual/Resident/Proportional(比例的)/Unique

Virtual Set Size

 

VSS是单个进程**全部可访问**的地址空间，其大小可能包括还尚未在内存中驻留的部分。对于确定单个进程实际内存使用大小，VSS用处不大。

RSS是单个进程**实际占用**的内存大小，RSS不太准确的地方在于它包括该进程所使用共享库全部内存大小。对于一个共享库，可能被多个进程使用，实际该共享库只会被装入内存一次。

进而引出了PSS，PSS相对于RSS计算共享库内存大小是按比例的。N个进程共享，该库对PSS大小的贡献只有1/N。

USS是单个进程私有的内存大小，即该进程**独占**的内存部分。USS揭示了运行一个特定进程在的真实内存增量大小。如果进程终止，USS就是实际被返还给系统的内存大小。

综上所属，VSS>=RSS>=PSS>=USS