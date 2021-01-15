	将Eclipse代码导入到AndroidStudio的两种方式 http://www.open-open.com/lib/view/open1419597450031.html
	
## 兼容模式，保持目录结构 -- eclipse生成Gradle工程 ##

保持了Eclipse时代的代码目录结构，当你使用AndroidStudio时，你或者其他人也可以方便的使用Eclipse，互不干扰。

1. `File | Export | Android | Generate Gradle build files`

	出现警告界面，推荐AndroidStudio直接导入ADT的工程（一堆直接导入好处）

2. 选中项目工程（包括库工程）

3. 修改project的 build.gradle Gradle plugin 版本

		buildscript {
		    ...
		    dependencies {
		        classpath 'com.android.tools.build:gradle:2.0.0'
		    }
		}

4. 修改project的/gradle/wrapper/gradle-wrapper.properties gradle版本

		

5. 修改module的build.gradle 编译sdk版本

		android {
		    compileSdkVersion 23
		    buildToolsVersion "23.0.3"

6.android studio 导入，选择刚才生成的gradle工程即可

## 使用新目录结构 ##

android studio 直接导入 eclipse工程（带有lib工程的是选择主工程），目录结构发生变化。

推荐使用该方法

## 带你看懂import-summary.txt ##

导入成功后弹出来的import-summary.txt写了些很重要的东西

**Manifest Merging**

	Your project uses libraries that provide manifests, and your Eclipse
	project did not explicitly turn on manifest merging. In Android Gradle
	projects, manifests are always merged (meaning that contents from your
	libraries' manifests will be merged into the app manifest. If you had
	manually copied contents from library manifests into your app manifest
	you may need to remove these for the app to build correctly.

这段是说android studio 会自动合并Library的清单文件到主工程manifest（而eclipse不会）所以不用手工拷贝到主工程的清单文件中了，以前拷贝过的，要移除才能正确build。

**Ignored Files:**
--------------
The following files were *not* copied into the new Gradle project; you
should evaluate whether these are still needed in your project and if
so manually move them:

* KuaiWiFi_New.jks
* proguard\
* proguard\dump.txt
* proguard\mapping.txt
* proguard\seeds.txt

		确实不需要的：混淆文件、ant的ant.properties与build.xml、maven的pom.xml。
		需要再次声明的： LICENSE.txt。不声明属于盗版侵权啊~~
		自定义文件夹和文件：cert。 这个文件夹是自己创建的，不属于Android规定的目录，所以AndroidStudio没给拷贝。
**重要：这里列出了被忽略的文件，如果有需要的，手动拷贝到gradle工程中**

**Replaced Jars with Dependencies:**
--------------------------------
The importer recognized the following .jar files as third party
libraries and replaced them with Gradle dependencies instead.
You can disable the jar replacement in the import wizard and try again:

android-support-v4.jar => com.android.support:support-v4:20.0.0

jar包转成在线依赖。

		libs目录发现没有v4包，需要查看：
		setting | project structure | Modules | Dependecies 点加号，选择 Library dependency 看到jar转成在线依赖了。

**Moved Files:**
------------
Android Gradle projects use a different directory structure than ADT
Eclipse projects. Here's how the projects were restructured:

* AndroidManifest.xml => app\src\main\AndroidManifest.xml
* assets\ => app\src\main\assets\
* res\ => app\src\main\res\
* src\ => app\src\main\java\

**Next Steps:略过**
-----------
**Bugs:略过**
-----

