adb pull push文件出现Permission denied,明明已经root

其实很简单

首先adb root

如果提示 adbd cannot run as root in production builds 
安装一个叫超级adbd的apk

地址http://www.anzhi.com/soft_616421.html#

在手机上赋予root权限，再开启用超级adbd,就行了


此时再push pull就无压力了