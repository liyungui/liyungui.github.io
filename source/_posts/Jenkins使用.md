---
title: Jenkins使用
date: 2018-05-14 14:43:56
tags: Jenkins
---

# Jenkins #

- 持续集成
- 多服务器支持。Jenkins支持管理多台服务器
- 工作目录是工程根目录。http://ci.shensz.local/job/course_android_release/ws/ 对应的是 /data/ci/.jenkins/jobs/course_android_release/workspace/


# 多个job之间的串并联 #

为什么不能把产品的持续集成步骤统统建立在一个job上呢？

- 首先，Jenkins限制，一个job的一次构建的所有任务只能运行在一个节点上。那如果产品的编译/部署/测试需要在不同平台下（如编译必须在Linux下，而执行用例需要在Windows下）就必须建立不同的job
- 再次，如果只有一个job必然构建时间会变长，也就是意味着产品的质量反馈变慢（必须等到所有的任务才做完才能得到反馈）
- 还有，分开建job也是为了相互之间的“弱耦合”，之后相应job的配置改动能尽量小的影响到其他job
- 最后，这样可以使产品的持续集成流程更加清晰，及时发现产品相应的短板

## Jenkins实现 ##

### Build Triggers ###

B中 Build Triggers -- Build after other Projects are buit 

	Project to watch:依赖的项目名称，例如 A项目 
	Trigger only if build is stable：只有在A项目构建文档后进行构建，过滤条件

这样我们执行A项目构建，紧接着B项目也会构建。

### Post-build Actions ###

A中配置 Post-build Actions，projects to build 选 B

执行A构建，B也会在A构建完成后，进行构建。

## Jenkins插件 ##


# 360加固 #

官网上加固助手只提供了PC和Mac版本，Linux版本的，请邮件联系客服，回复很快。

- 在Jenkins中打开项目设置
- 在构建操作中点击新增构建步骤，选择Execute shell
- 在Command中输入以下内容：

		# Java环境变量，请替换为本机实际路径
		JAVA_HOME="/opt/jdk/bin"
		
		# 加固保环境变量，请替换为本机实际路径。需要执行权限，否则报错
		JIAGU_HOME="/home/dafan/mount1/360jiagu/jiagu/jiagu"
		
		# 登录360所需要的账户名和密码，请替换为自己的账号密码
		USER="360账号"
		PSWD="360密码"
		
		# 签名相关信息，请替换为实际签名的信息
		release_keyAlias="签名别名"
		release_keyPassword="文件密码"
		release_storeFile="签名文件路径"
		release_storePassword="签名密码"
		
		# 登录360
		$JAVA_HOME/java -jar $JIAGU_HOME/jiagu.jar -login $USER   $PSWD
		
		# 配置增强服务，升级通知 崩溃日志 支持x86 消息推送 可多选：-update -x86 -carshlog -msg，如下配置：
		$JAVA_HOME/java -jar $JIAGU_HOME/jiagu.jar -config -x86 -crashlog
		
		# 配置签名信息，用于加完完成后的自动重签名
		$JAVA_HOME/java -jar $JIAGU_HOME/jiagu.jar -importsign $release_storeFile   $release_storePassword $release_keyAlias $release_keyPassword
		
		# 加固，支持通配符，apk路径根据实际修改，如果通配符匹配到两个以上的input文件，就会卡在prepare to upload 一直没有进度。
		$JAVA_HOME/java -jar $JIAGU_HOME/jiagu.jar -jiagu ${PWD}/app/build/outputs/apk/*_release.apk ${PWD}/app/build/outputs/apk/ -autosign

# Jenkins插件 #

## [Copy Artifact Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Copy+Artifact+Plugin)  ##

把某个job的构建物(通常是WAR，JAR，TAR，apk等)拷贝到当前job的工作区

 多job串并联构建原则：一定要保证上游job的构建物是被存档的

## [Join Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Join+Plugin) ##

触发job的插件

亮点在于它触发job的条件是等待所有当前job的下游的job都完成才会发生。当然，只有在当前job有两个及以上的下游job时才有意义。      

## [Parameterized Trigger Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Parameterized+Trigger+Plugin) ##

各个job连接的时候可以传递一些job相关的信息

- 当前job的参数
- 自定义的参数
- SCM相关信息
- 运行的Node信息

比如 传递SVN Revision或是GIT Revision，保持各个构建的版本一致性

## [Build Pipeline Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Build+Pipeline+Plugin) ##

一个用于生成特定视图的插件，可以把job之间的关联关系可视化，使产品的流程也随之可视化。

## [Multijob Plugin](https://wiki.jenkins-ci.org/display/JENKINS/Multijob+Plugin) ##

Parameterized Trigger + Build Pipeline

但它是形成一个新的job，而不是一个视图。

并且它不要求job之间本身就存在依赖关系。

这样一来，建立job的时候可以保持相对的独立性，而通过这个插件来组装成产品所需要的持续集成环境。