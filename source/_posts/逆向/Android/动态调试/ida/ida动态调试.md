---
title: ida动态调试
date: 2019-12-06 13:51:53
categories:
  - 逆向
tags:
	- 逆向
---

# ida动态调试

支持动态调试 dex，so，二进制文件

# dex动态调试
	
网上的教程都是ida6.6调试dex，
但是自己在红米真机一直不能操作成功 
	Permission denied 然后 the file cannot be loaded by the debugger plugin
然后Google中看到一篇老外的英文文章，ida调试Android二进制文件
最后在 Android软件安全与逆向分析8.5也看到一样的内容
以为总算看到了正确方法，而网上的教程都是错误的。
后来在模拟器环境调试才发现网上 ida6.6调试dex 是正确的

打开classes.dex

Debugger->Debugger Options
	勾选在进程入口挂起，suspend on process entry point
	点击Set specific options 填入APP包名和入口activity
		对应manifest的package name 和 activity的完整路径
		<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.simpleencryption">
		<activity android:label="@string/app_name" android:name=".MainActivity">
		
Debugger->Process Options
	端口这里改为8700。
	这里默认端口是23946，我在这里困扰了很久，就是因为这个端口没有改为8700所致
	apk调试端口。ddms里面可以看到（后面为调试端口）
	
下断点，f9运行，ida弹框running（无法取消），
	只有触发断点才能自动取消running提示框，然后操作ida

debugger--debugger window--locals 
	该窗口可以看到本地变量，但是值都表示为bad type（hex 格式显示也是这样）	
	
# so动态调试

ida动态调试安卓动态链接库so（远程附加调试）

必须先运行一遍功能代码，从而加载so库

step 1:move android_server to your target and execute

step 2: port forwarding

step 3:apk必须先运行一遍功能代码，从而加载so库

step 4: IDA Pro Configuration
	debugger--attach -- remore armlinux/anroid debugger
	选择进程，进入调试界面
	
	这时候发现不是在我们要调试的so库（libdebugjniso.so）领空（本例在libc.so）
	用一个ida打开要调试so库，function Window找到要下断方法偏移地址（本例0xc38）
	回到调试ida，ctr+s 打开段选择对话框，找到调试so库基址（两个同名的，取第一个），48a64000
	基址+偏移，快捷键g跳转到该地址（48a64c38），右键-code，下断。
	
	操作apk（设置标题功能），断下
		apk附加调试后，操作一直假死，没有操作成功
		
		
问题：附加不上端口
	ida报错：
		irs_recv: 等待的操作过时。
	cmd日志：
		[1] Accepting connection from 127.0.0.1...
		[1] Could not establish the connection
		[1] Closing connection from 127.0.0.1...
		
		
# 二进制文件动态调试

ida动态调试安卓二进制文件（原生应用，远程运行调试）

http://finn.svbtle.com/remotely-debugging-android-binaries-in-ida-pro
Android软件安全与逆向分析8.5
	
必须使用ida6.1版本32位版
	6.6版本debugger菜单下没有 run -- remore armlinux/anroid debugger
	后来在模拟器环境调试才发现是有的，一直觉得没有。是因为加载了dex后的确没有（所有版本都这样）
网上的教程都是ida6.6调试dex，最后在 Android软件安全与逆向分析8.5总算看到了正确方法。
后来在模拟器环境调试才发现网上 ida6.6调试dex 是正确的

64位版本远程附加调试报错是 Incompatible debugging server: address size is 4 bytes, expexted 4
然后提示the file cannot be loaded by the debugger plugin
自然想到32位，切换一看，成功

老外网站提到的另一种无法加载文件错误
无法the file cannot be loaded by the debugger plugin 修复
http://finn.svbtle.com/error-the-file-cant-be-loaded-by-the-debugger-plugin

	step 1:move android_server to your target and execute
		Push the android_server
			adb push "C:\Program Files (x86)\IDA 6.6\dbgsrv\android_server" /data/local/tmp
			IDA 6.6\dbgsrv\android_server
			有人说ida6.4版本后已经移除（反正我6.6还有），同目录下有Android,linux,mac,arm等远程服务
		Connect to your device and navigate to /data/local/tmp
			adb shell
			su
			cd /data/local/tmp
			ll 列出目录下所有文件信息（包含隐藏文件，文件权限，比ls详细）
		Set permissions
			chmod 755 /data/local/tmp/android_server
		Execute android_server
			./android_server	
			Listening on port #23946...执行后反馈显示。保留该cmd窗口，观察后续连接反馈
			
	step 2: port forwarding
		adb forward tcp:23946 tcp:23946 在计算机上另开一个cmd
			We can confirm this has worked by running:
			netstat -a -n | findstr 23946
			TCP    127.0.0.1:23946        0.0.0.0:0              LISTENING
	
	step 3: move binaries to your target and executable
		adb push "C:\debugnativeapp" /data/local/tmp/debugnativeapp
		chmod 755 /data/local/tmp/debugnativeapp
		
	step 4: IDA Pro Configuration
		debugger--run -- remore armlinux/anroid debugger
		最关键的，自己在这里困扰很久。作者也说他在这里经历过所有错误
		主要核心看ida 最上面的note可知：all paths must be valid on the remote computer
			而国内千篇一律的教程是本地计算机路径
			ida6.6没有该菜单，相似的Debugger > Process Options
				默认填的就是我们选的dex路径（讲dex调试和二进制文件调试肯定不一样），大家也不改
				后来在模拟器环境调试才发现，是因为加载了dex后才没有（所有版本都这样）
		路径填 /data/local/tmp/debugnativeapp
		目录 /data/local/tmp
		hostName localhost 
		port 23946
			