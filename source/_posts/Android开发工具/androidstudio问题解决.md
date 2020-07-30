# 一直卡在building“project xxx”gradle project info #

原因是需要下载该项目需要的gradle版本。

	1. 本地没有gradle，
	2. 项目需要的gradle版本和本地版本不一致

解决方案
	
	1.修改项目gradle版本为本地版本。首选
		项目/gradle/wrapper/gradle-wrapper.properties 的distributionUrl属性
	2.手动下载项目gradle版本。对gradle版本有特定要求时使用
		放到 C:\Users\Administrator\.gradle\wrapper\dists目录
# failed to find Build Tools revision 23.0.2 #

Build Tools revision和本地不一致，修改module配置,改成本地版本

	module的build.gradle
		android {
		    compileSdkVersion 23
		    buildToolsVersion "23.0.3" 

# NDK not configured #

local.properties文件中添加你的ndk路径

	ndk.dir=C\:\\Android\\ndk-r13b-windows_64


#  查看源码只有 throw new RuntimeException("Stub!"); #

注意看android studio上面有句话 `Sources for ‘Android API 23 Platform’ not found`

说明没有关联到源码。

关联源码的两种方法：

- 点提示后面的Download和Refresh
- C\Users\用户名\.AndroidStudio2.0\config\options\jdk.table.xml 
	- 删除该文件重启as

# Unsupported major.minor version 52.0 #

升级到java8。

java 8 class file的版本是52，Java 7虚拟机只能支持到51。

有时候会出现Android Studio 2.2.3 run可以，gradle打包却不行的问题。

原因是2.2.3默认使用了自带的JDK环境，gradle打包却使用的是环境变量JAVA_HOME配置的java

# Error running app: This version of Android Studio is incompatible with the Gradle Plugin used. Try disable ... #

- 禁用Instant Run
- 更新android studio 和gradle插件
- 删除project下的build文件夹
- clean项目，重新编译跑程序