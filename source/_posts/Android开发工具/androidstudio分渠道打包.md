	使用Gradle构建Android应用的渠道包（清楚讲解） http://www.tuicool.com/articles/RJNnE3m
	Android studio 多渠道打包(超简洁版) http://www.cnblogs.com/0616--ataozhijia/p/4203997.html

友盟、酷传等第三方都有自动化工具来做

本文在gradle利用manifestPlaceholders这个属性来替换渠道值，实现分渠道打包

一般渠道的统计是用友盟之类的

## 在AndroidManifest.xml里配置PlaceHolder ##
渠道信息一般在 AndroidManifest.xml 中 application 下：
 
	<meta-data android:name="UMENG_CHANNEL" android:value="wandoujia" />
 
修改成以下的样子：

	<meta-data android:name="UMENG_CHANNEL" android:value="${UMENG_CHANNEL_VALUE}" />
	其中${UMENG_CHANNEL_VALUE}中的值就是你在gradle中自定义配置的值。

## 配置module的 build.gradle##

build.gradle文件android 标签下就利用productFlavors这样写：

	productFlavors {
		wandoujia {
			manifestPlaceholders = [UMENG_CHANNEL_VALUE: "wandoujia"]
		}
		baidu {
			manifestPlaceholders = [UMENG_CHANNEL_VALUE: "baidu"]
		}
		c360 {
			manifestPlaceholders = [UMENG_CHANNEL_VALUE: "c360"]
		}
		uc {
			manifestPlaceholders = [UMENG_CHANNEL_VALUE: "uc"]
		}
	}
	其中[UMENG_CHANNEL_VALUE: "wandoujia"]就是对应${UMENG_CHANNEL_VALUE}的值。会自动逐个替换manifest的值

build.gradle文件更简洁的写法

	productFlavors {
		wandoujia {}
		baidu {}
		c360 {}
		uc {}
		productFlavors.all { 
			flavor ->flavor.manifestPlaceholders = [UMENG_CHANNEL_VALUE: name]
		}
	}
	其中name相对应各个productFlavors的选项值，自动逐个替换manifest的值，这样就达到自动替换渠道值的目的了。

可以在defaultConfig标签下加上默认渠道

	android {
		...
		defaultConfig {
		   	...
		    manifestPlaceholders = [ UMENG_CHANNEL_VALUE:"default_channel" ]
		}	
	}

生成apk时，选择相应的Flavors来生成指定渠道的包就可以了，而且生成的apk会自动帮你加上相应渠道的后缀，非常方便和直观。大家可以自己反编译验证。

## 一次性生成所有渠道包 ##

android studio底栏中有个命令行工具 `Terminal` ,打开后就CMD可以自动切换到当前项目的目录下。

`gradlew assembleRelease` 有的项目下会有graldew.bat这个文件，可以使用该命令。gradlew这个命令的gralde的版本无法控制，有时候会莫名其妙的下载老版本的gradle。不建议使用。

`gradle assembleRelease` 所有生成的apk在项目的 `build\outputs\apk` 下

	手动调用gradle,
		需要在系统变量添加GRADLE_HOME变量，指向gradle根目录（bin上一级）
		PATH里添加gradle的bin目录。

## 生成单个渠道包 ##

打开Android Studio的Gradle tasks面板(右边侧边栏)，会发现模块多了很多任务,双击该任务生成对应的apk

`gradle assembleWandoujiaRelease` 命令方式生成