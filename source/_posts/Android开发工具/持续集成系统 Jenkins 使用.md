[Android Jenkins+Git+Gradle持续集成](http://www.jianshu.com/p/38b2e17ced73)

使用持续集成（CI）系统jenkins，自动检测并拉取Git上的最新代码，自动打包成不同的渠道apk，自动上传到内测分发平台蒲公英上和自建的FTP服务器上。接下来，测试人员只要打开一个（或多个）固定的网址，扫描一下二维码，就能下载最新的版本了…

# 基本使用 #

## 安装Jenkins ##

1. [下载](https://jenkins.io) 
2. 安装
3. 默认访问 [http://localhost:8080/](http://localhost:8080/) , 进入jenkins 主页面

## 安装Jenkins相关插件 ##

进入 主页面>`系统管理`>`管理插件`>`可选插件` 安装插件

1. git插件(GIT plugin)
2. ssh插件(SSH Credentials Plugin)
3. Gradle插件(Gradle plugin) - android专用

注：

1. 需要翻墙
2. Windows中要装好JDK、Git、Gradle的环境

## 配置Jenkins ##

1. **Global Tool Configuration**

	主页面>`系统管理`>`Global Tool Configuration`

	分别配置 JDK，Git，Gradle 的路径。
2. 全局属性 **ANDROID_HOME**

	主页面>`系统管理`>->`系统设置`->`全局属性` 版块勾选上`Environment variables`选项，增加 ANDROID_HOME

	打包是有可能会出现ANDROID_HOME not found的情况

## 新建并配置Job ##

1. 主页面，`新建` -> `构建一个自由风格的软件项目` 
2. `源码管理`，配置git仓库
3. `构建` -> `增加构建步骤` -> 选择 `Invoke Gradle script`

	`Gradle Version`z 选我们刚配置的gradle

	`Task` 填 `clean assembleRelease --stacktrace --debug` clean工程，然后打包所有渠道的Release版本

## 立即构建 ##

点击左侧菜单栏的立即构建，开始构建项目

`Build History` 出现构建任务列表，点击进入可以查看构建详情页

`Console Output` 查看构建输出的日志

返回项目地址 点击 `工作空间`，在app的build目录下面查看apk生成情况。
	
# 遇到的问题 #

1. 构建一个项目耗时很久，经常不成功

	国内被墙，gradle在线依赖很难下载成功。gradle这个问题在日常AS开发中一直存在，只能重复尝试。
	
# 存档
已有插件支持。一般存档apk包和mapping混淆规则

	*/build/outputs/apk/*course*-release-*.apk,*/build/outputs/mapping/release/mapping.txt
	
# 上传fir

已有插件支持。注意fir.im token 和 exinclude 排除掉unaligned包

	*/build/outputs/apk/*course*-release-unaligned.apk,