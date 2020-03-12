---
title: 无源码调试Android dex
date: 2019-12-06 13:41:53
categories:
  - 逆向
tags:
	- 逆向
---

标 题: 【原创】阿里聚安全技术分享之APK无源码调试
作 者: alimobsec
时 间: 2014-12-18,14:42:14
链 接: http://bbs.pediy.com/showthread.php?t=195660
这年头，apk全都是加密啊，加壳啊，反调试啊，小伙伴们表示已经不能愉快的玩耍了。静态分析越来越不靠谱了
我们的目标是——“debug apk step by step”。

那些不靠谱的工具
	IDA pro
	触发断点，在watch view和Locals窗口都能看到内存变量的值
	仔细观察下，就算你勾选了“Hex display”，你还是无法看到变量的值
	WTF！我特么忙活了半天居然还不如直接logcat来得痛快！
	
	apktool+eclipse
	debug窗口表示命中第30行的断点
	variables窗口没有任何本地变量的值，寄存器的值也没有
	单步步入、单步步过等调试按钮都是灰色的，快捷键F5678都没反应
	测试失败
	
	apktool+android studio
	可以看到现在程序停在哪一行，虽然不明显
	本地变量能看到，但是寄存器还是木有啊
	单步按钮还有单步快捷键都能用了，看起来好多了啊
	我还是想说，问题是寄存器的值还是没法直观的看到啊
	测试失败
	
apktool+idea 正菜来了
	下断点
	新建远程调试：依次点击run-> edit configuration->“＋”号->Remote，命名为mytest
	run->debug->mytest
	断下，按两次resume，apk才能跑起来
	测试成功
				
另外，阿呆曾经提到一篇文章用jdb远程调试android程序的文章，
链接为：http://resources.infosecinstitute.com/android-hacking-security-part-6-exploiting-debuggable-android-applications/

http://www.kanxue.com/bbs/showthread.php?p=1338639

----------

下载[最新版Apktool](http://ibotpeaches.github.io/Apktool/install/)，按照教程操作

	个人推荐下载bat。把apktool.jar和apktool.bat放到同一目录即可。
		一是不用每次都敲 java -jar apktool.jar apktool
		二是在编译回apk时，cmd会把 b 参数解析成文件名（一直报找不到文件错误）
	
apktool 加-d参数反编译成java文件，全部拷贝到一个空java工程src目录下
	其实是伪java。每一行都是a=0;然后smali作为行注释
	-d的作用就是编译成 debug模式（.java，不加的话是.smali）
	apktool d -d test.apk -o test

manifest 加入debuggable属性，重打包，安装
	android:debuggable="true"
	
使用-d选项重打包apk，签名(其他签名工具)，安装
	加-d才可以调试，否则断点无效
	apktool b -d test -o debug.apk
	
am命令启动apk，停留在等待调试器界面
	adb shell am start -D -W -n com.snda.wifilocating/com.lantern.launcher.ui.MainActivity
		出现ddms自动附加调试的话，尝试先让app进入等待调试模式，再开idea
		
eclipse调试按钮更多，远程调试，地址local，端口调试端口，附加上就可以断点调试了。
	一直没成功。
	附加不上，
	附加上是把原来的等待调试的杀死，启动了新进程
	附加上了，断不下来
	
有文章说在入口类入口方法第一行加 等待调试器代码（有api可调），可以远程附加调试
	onCreate第一行（.prologue后面）
	invoke-static {}, Landroid/os/Debug;->waitForDebugger()V
	的确会等待调试器附加，但是附加上去还是无法断点调试（断不下）
	
有文章甚至说反编译为jar包，加入一个空java工程中，就可以实现远程附加断点调试
	尝试失败

后来尝试用idea，成功！！

必须用另一个idea打开一个Android工程（上面我们是java工程），才能在tools--Android--Android device monitor 打开ddms，查看目标程序的调试端口（8700），同时防止adb掉线

新建远程调试：依次点击run-> edit configuration->“＋”号->Remote，host写localhost，端口写上面查到的

点击run->debug->unnamed，其中unnamed是第9步中新建的远程调试的名字
	如果adb掉线，会出现连接拒绝，重连adb即可解决。 Unable to open debugger port (localhost:8700): java.net.ConnectException "Connection refused: connect"

# [Smalidea+IntelliJ IDEA/Android Studio无源码调试](https://bbs.pediy.com/thread-220743.htm) #

[smalidea](https://github.com/JesusFreke/smali/wiki/smalidea)是一个IntelliJ IDEA/Android Studio smali语言插件，可实现动态调试smali代码。支持14.1或以上版本的IDEA

## 一、反编译apk为smali ##
- baksmail:
			
		java -jar baksmali-2.2.1.jar  d myapp.apk -o ~/projects/myapp/src
- apktool:

		java -jar apktool.jar d myapp.apk -o ~/projects/myapp/src

## 使apk可调试 ##

- 使用模拟器
- 重打包apk。修改Manifest application 属性 android:debuggable="true"
- 编译一个debug版 的rom
- 修改测试机的 /default.prop 文件的ro.debuggable=1。需root

## 开始调试 ##

------------

来自 看雪 古河 使用AndBug调试Android Java Bytecode
	http://bbs.pediy.com/showthread.php?t=141995
	
	附参考：看雪 anbn Android动态逆向分析工具（一）——Andbug之基本操作 系列。更加详细
		http://bbs.pediy.com/showthread.php?t=183412

AndBug的主页是：https://github.com/swdunlop/AndBug

必须Linux环境（我是Ubuntu 14）。Python开发，需要python-dev，bottle库（Python Web Framework）

github下载后解压，进入根目录，开启终端，make
	make 报错就是没有python-dev（Ubuntu自带Python，但没有python-dev）
		sudo apt-get install python-dev
		
在模拟器中启动apk，在命令行下输入 adb shell ps，找到相应的进程pid，在这个例子中pid是243
	apk 必须debuggable，否则附加调试会出现 Connection reset by peer 错误
	
	Ubuntu adb 问题。
		sudo add-apt-repository ppa:nilarimogard/webupd8
		sudo apt-get update
		sudo apt-get install android-tools-adb
		
	安卓设备连接 adb 问题
		lsusb 配合插拔usb设备，确定 USB设备。
		发现usb口是当前使用的端口：Bus 002 Devices 004：ID 230b:0100		
		ID 230b 就是idVendor ，0100就是 idProduct

		新建并编辑一个文件
		sudo vi /etc/udev/rules.d/70-android.rules
		在里面写入：
		SUBSYSTEM=="usb", ATTRS{idVendor}=="230b", ATTRS{idProduct}=="0100",MODE="0666"
			ID 230b 就是idVendor ，0100就是 idProduct
			其实还应该写一个OWNER项，用来指定是哪个用户有权限操作
			如果不写则是root（不是所有用户都可以访问）
			
		保存退出，再设置一下权限
		sudo chmod a+rx /etc/udev/rules.d/70-android.rules
		
		向adb_usb.ini文件写入厂商id（注意加 0x前缀）
		echo 0x230b > ~/.android/adb_usb.ini
			用户根目录下，ls -a 可以发现
			
		重启USB服务
		sudo service udev restart
		
进入AndBug根目录，输入PYTHONPATH=lib ./andbug shell -p 8723，命令attach上目标进程
	andbug是Python脚本，andbug shell 附加调试命令
	adb shell ps | grep "com.yuki" 可以找到对应名字的pid
	
	[Errno 104] Connection reset by peer 问题
	搜索了好久，包括原贴和官网上都没有解决。
	我尝试去attach其它进程，发现其它进程是可以成功的，
	继而我想到可能是debuggable的问题，逆向AndroidManifest添加 android:debuggable=true 成功。

classes 命令，查看apk调用了哪些类
	classes java.net 查看调用的包含java.net的类
	
methods 命令，查看apk调用了哪些类方法

break java.net.URL 断点类调用。
	也可断点方法调用 break 类名 方法名（类名和方法名间空格）
	Android4.4.2上实际操作发现断java.net.URL会在触摸屏幕触发断点
		 com.android.okhttp.Connection.connect 这个断点效果好
		 break com.android.okhttp.Connection connect

break-list命令查看断点设置情况
break-remove 536870916	删除已设置断点

操作apk，触发断点

navi命令，提示 server地址http://localhost:8080 查看线程状态
	!! command not supported: "navi."  问题
	这是需要 bottle库（Python Web Framework）
		apt-get install python-bottle
		
	Error: 500 Internal Server Error 问题
	访问http://localhost:8080 错误。
	解释说是地址，或资源问题。没有搞定（rooted红米note1 Android4.4.2）
	后来过了很长一段时间，用华为 g521-L076 测试成功（rooted，Android4.3）
	
	
resume 恢复运行

suspend 进程暂停命令

help 帮助命令

class-trace 类跟踪命令
取消跟踪也可以使用break-remove命令实现。

method-trace 方法跟踪命令

列举当前线程信息
命令：threads 会列出函数调用的情况，参数，以及堆栈情况。

示指定类中的静态变量的信息
命令：statics com.android.internal.view.menu.MenuBuilder

查看对象信息
通过class-trace命令可以跟踪到目标函数中对象的Id信息，

通过对象的Id使用inspect命令，可以查处该队形的详细信息。
由于在break命令设置断点后，触发断点时反馈的信息，没有包含Object Id的信息，导致inspect命令用起来不是很方便。

19、源码关联命令
命令：source 与源代码关联起来，可以是smali代码。
命令：dump 展示指定方法的代码。

20、Web输出命令
命令：navi
注：为了支持navi命令，需要安**ottle库。

退出命令
命令：exit	 


