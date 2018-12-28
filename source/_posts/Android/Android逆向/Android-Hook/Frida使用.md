---
title: Frida使用
date: 2018-12-11 18:16:53
tags:
	- Hook
---

# 安装


## 安装 frida tools

`pip install frida-tools`

## 安装 Android frida-server

[下载frida-server](https://github.com/frida/frida/releases)。 根据手机CPU下载不同文件`frida-server-12.2.26-android-arm.xz`

安装运行
	
	$ adb root # might be required
	$ adb push frida-server /data/local/tmp/ 
	$ adb shell "chmod 755 /data/local/tmp/frida-server"
	$ adb shell "/data/local/tmp/frida-server &"
	
快速冒烟测试(A quick smoke-test)

终端执行 `frida-ps -U` 能够看到手机上的进程列表

### 运行错误

#### 地址被占用

`Unable to start server: Error binding to address: Address already in use`

之前运行过frida-server。

杀死进程即可

	adb shell
	ps |grep frida
		root      4341  4292  41036  36132 ffffffff b5b29960 S /data/local/tmp/frida-server
		root      4354  4341  5748   1448  ffffffff b6d2f960 S /data/local/tmp/re.frida.server/frida-helper-32
	kill 4341

#### 运行后手机重启

bug。重新运行


# 工具

frida-discover 发现APP内部方法



