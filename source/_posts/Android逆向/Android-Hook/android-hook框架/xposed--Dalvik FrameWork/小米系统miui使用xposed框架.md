---
title: 小米系统miui使用xposed框架
date: 2018-05-18 16:44:42
tags: 
	- Hook

---

[解除系统对XPosed框架限制](http://www.miui.com/thread-2973594-1-1.html)	

从9月23日开始，XPosed框架被系统限制，许多XP模块童鞋捉急。

然而，高手在民间，不过几日，先是论坛许多miui优化包都放出XP框架可用，说明已破解，但从他们的包内确实找不出关键点。

又一日，网友『尛』便爆出解决方法，赶脚试试，果然奏效，在这里再次感谢『尛』。


发这帖是对 『尛』帖子的诠释，以下操作步骤仅为我的见解，不排除有比我更好的方法，希望能帮助到大家，祝基友国庆刷机愉快！

先说主要的：

1. 请到官方17日的包内提取两个文件：app_process 和 libandroid_runtime.so

		其位置分别在：system/Bin下 和 system/Lib/下（为什么要17日的包？因为17日的包好找，不是内测的基友也可以下载到哦）

2. 下载你想刷的官方的最新包。

3. 把提取的 app_process 和 libandroid_runtime.so 文件替换到新下载包的同目录下（就是提取时的目录），直接覆盖确认。

		替换文件在PC上操作，不要解压rom包。双击rom包，拖曳文件到相应位置直接覆盖替换，无需改权限什么的。
4. 刷机--成功！（注意：请使用论坛雯雯的rec2.8.5刷入，使用官方REC可能因签名问题失败)
		
		推荐使用第三方rec刷包(雯雯2.8.5，论坛置顶，这个REC刷官方rom和ota都能成功，真乃刷机神器！)。
楼主机型 ：2014011    HM1STD    红米1S3G移动版
其他机型自测，据我观察论坛大部分机型几乎都可使用。

**注意：请不要在手机系统上通过RE管理器直接替换文件，否则100%变砖！**

我note 4g联通增强版就是在万恶的百度贴吧看教程用RE替换，然后变砖的。增强版刷机后资料全丢

	http://en.miui.com/forum.php?mod=viewthread&tid=176904&highlight=Xposed Fix for Xposed restrictions on MIUI 7. KitKat Only (4.4.x)
英国miui论坛提供的一个xposed apk，兼容4.4.x。note 4g联通增强版测试成功

          
          