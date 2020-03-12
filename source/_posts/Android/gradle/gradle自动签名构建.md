---
title: gradle自动签名构建
date: 2020-02-03 14:13:53
categories:
  - Android
tags:
	- Android
---

	gradle自动签名构建 http://www.tuicool.com/articles/MjqYbiu
	Android Studio用release模式进行调试  http://www.cnblogs.com/tianzhijiexian/p/4442804.html
module的buil.gradle android标签下

	signingConfigs {
        myConfig {
            storeFile file("xuehu.jks") // 放在module根目录（和buil.gradle同级），所以直接写了相对路径
            storePassword "xuehu2016"
            keyAlias "xuehu"
            keyPassword "xuehu2016"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.myConfig//不要忘了要在release的时候加入我么的签名配置信息
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }

如果调试时也希望使用签名

	buildTypes {
        debug {
            signingConfig signingConfigs.myConfig
        }
        release {
            signingConfig signingConfigs.myConfig//不要忘了要在release的时候加入我么的签名配置信息
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }

[Android studio的gradle配置 ](http://blog.chinaunix.net/uid-20771867-id-5106723.html)

1. 自动按照版本号和版本名称及日期重命名apk。
2. 自动按照日期升级versionCode。
3. 自动将apk文件复制出来。

# 将apk名 替换为 xuehu-渠道名_v版本名.apk。 #

- android标签下
- 甚至可以在buildTypes --> release { 标签下，仅release时才重命名apk

代码如下

	android.applicationVariants.all { variant ->
        variant.outputs.each { output ->
            def file = output.outputFile
            output.outputFile = new File(file.parent, file.name.replace(file.name, "xuehu-"+variant.productFlavors[0].name+"_v${variant.versionName}.apk"))
        }
    }

# 将打包后的文件复制到build目录下 #

- 不用深入到apk目录
- 同时还看不到unaligned的apk了
- android标签下
- 
代码如下

	task copyTask(type: Copy) {
	    from 'build/outputs/apk/'
	    into 'build/'
	    exclude '*-unaligned.apk'
	}
	
	task bd(dependsOn: ['assembleDebug', 'assembleRelease', 'copyTask']){
	    copyTask.mustRunAfter assembleRelease
	}

`gradle bd` 即可编译并复制到build目录下
