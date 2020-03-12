---
title: APP弱网络测试工具
date: 2019-08-29 15:40:53
categories:
  - Android
tags:
  - Android
---

弱网络专项测试的方案主要有


# PC上使用抓包工具设置延时模拟弱网

- 在PC上的Fiddler在设置延时
- 将Android设备的网络代理到PC上

# 专有服务器上构建弱网络Wi-Fi

- 在专有服务器上构建弱网络Wi-Fi
- 移动设备连接该Wi-Fi进行弱网络测试

相关的技术方案有Facebook的ATC和腾讯的Wetest-WiFi;

# 缺陷

- 需要额外的PC或者服务器，弱网环境构建成本高；
- 需要安装、部署额外的工具，并且弱网络环境需要在PC上或者Web上进行配置，使用成本高；
- 弱网络环境功能并不完善，比如Fiddler不支持丢包、抖动等弱网环境；

# QNET

- 无需ROOT手机，只需安装一个独立app
- 弱网模拟功能强大。2G，3G，4G，丢包，抖动
- 支持 TCP/UDP网络协议抓包，导出为Pcap文件

## 已知问题

引起APP频繁刷新，某些生命周期相关的方法会频繁回调，可能引起ANR


# 参考&扩展

- [QNET，一款给力的APP弱网络测试工具](https://www.520mwx.com/view/53152)


