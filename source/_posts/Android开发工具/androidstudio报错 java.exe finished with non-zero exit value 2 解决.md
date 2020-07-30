ZipException: duplicate entry: 

java.exe finished with non-zero exit value 2

## 1. 方法数超过65k（65536） ##
解决方案： 开启multidex支持

	defaultConfig {
		...
		multiDexEnabled true // Enabling multidex support.
	}

## 2. 依赖包冲突 ##

一般是v4包、三方依赖等

解决方案：保持lib module 和主 module 依赖版本一致