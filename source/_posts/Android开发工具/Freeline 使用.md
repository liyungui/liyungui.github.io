[Freeline](https://github.com/alibaba/freeline)

Freeline只更改了debug包，不会影响release包的处理

# Features #

以下列表为 Freeline 支持的热更新情况：

|| Java | drawable, layout, etc. | res/values | native so|
|:-----:|:----:|:----:|:----:|:----:| 
| add | √ | √ |√ | √ |
| change | √ | √ |√ | √ |
| remove | √ | √ |x| - |

# Limitations #


- 第一次增量资源编译的时候可能会有点慢
- **不支持删除带 id 的资源**，否则可能导致 aapt 编译出错
- **暂不支持抽象类的增量编译**
- 不支持开启 Jack 编译
- 不支持 Kotlin/Groovy/Scala

# 使用 #

配置 project-level 的 build.gradle，加入 freeline-gradle 的依赖：

	buildscript {
	    repositories {
	        jcenter()
	    }
	    dependencies {
	        classpath 'com.antfortune.freeline:gradle:0.8.7'
	    }
	}

主 module 的 build.gradle，应用 freeline 插件的依赖：

	apply plugin: 'com.antfortune.freeline'
	
	android {
	    ...
	}

最后，在命令行执行以下命令来下载 freeline 的 python 和二进制依赖。

	Windows[CMD]: gradlew initFreeline -Pmirror
	Linux/Mac: ./gradlew initFreeline -Pmirror

	-Pmirror，从国内镜像地址来下载。

安装 Android Studio freeline 插件

# 遇到的错误 #

1. `ImportError: No module named 'build_commands'`

	freeline目前只支持 python 2.7+，python3.5会报错

2. `apktime file not found`

		Execution failed for task ':xuehu365:mergeXuehuDebugAssets'.
		> C:\AndroidStudioProjects\xuehu\xuehu365\build\intermediates\assets\debug\apktime file not found.
		Missing the `productFlavor` configuration?
		You can try to add `productFlavor` to freeline DSL, for example:
		
		  freeline {
		      hack true
		      productFlavor 'your-flavor'
		  }
		
		Then re-run `python freeline.py` again.

	在主module build.gradle中 加入（修复提示已经说得很清楚）

		freeline {
		      hack true
		      productFlavor 'your-flavor'
		  }

# 注意点

- debug 模式下不要开启混淆
- 如果有多个 productFlavor 的话，需要配置指定 flavor
- 增加编译出错，可以强制进行全量编译 `python freeline.py -f`