	http://liukun.engineer/2016/04/10/Android-Studio-advanced-configuration/

1. 显示行号

	Editor | General | Appearance | Show line numbers

2. 驼峰选择。Ctrl + Left / Right 键改变字符选择区域的时候 Android Studio 默认不支持‘驼峰’单词的选择

	Editor | General | Smart Keys | Use “CamelHumps” words
	如果你仍然希望当鼠标在单词上双击之后选中整个单词，需要作如下设置：
		选择 Editor | General
		取消选中 ‘Honor Camel Humps words settings when selecting on double click’

3. 命名前缀

	Editor | Code Style | Java | Code Generation 给普通 Field 添加一个’m’前缀，给 Static filed 添加一个’s’前缀
	
4. 快速导包。默认 Alt + Enter 和 Control + Alt + O 进行逐个导包和清除无用导包

	Editor | General | Auto Import 
		
		勾选 Optimize imports on the fly  会自动清除无用导包
		勾选 Add unambiguous imports on the fly  自动导入没有二义性的包

5. 工程模板。创建 Module 时并没有将 Android 开发中常用的文件目录全部生成，比如默认只生成了一个 drawable 文件夹

	配置方法1。复杂

		进入 Android Studio 安装目录
		依次进入 plugins | android | lib | templates | gradle-projects | NewAndroidModule | root | res
		在res文件夹下创建 drawable-hdpi 等文件夹(可选：从对应的 mipmap文件夹中拷贝 iclauncher.png到创建的 drawable文件夹中)
		回到 NewAndroidModule 目录，用编辑器打 recipe.xml.ftl文件
		加入以下配置

	配置方法2。简单

		进入 Android Studio 安装目录
		依次进入 plugins | android | lib | templates | gradle-projects | NewAndroidModule
		用编辑器打开 recipe.xml.ftl文件，并加入以下配置
			<mkdir at ....

6. 活动模板(Live Templates)。输入 sout 后按 enter 键， Android Studio 会自动帮我们写入 System.out.println();

		Editor | Code Style | Live Templates
		点击最右侧的加号并选择 Template Group
		在弹出的对话框中输入一个活动模板分组的名称，如 custom
		在左侧选中上一步中创建的 custom 分组，点击右边的加号
		选择 Live Template ，在 Abbreviation 中对输入 psh
		在 Description 中输入这个活动模板的描述
		在 Template text 中输下代码
		点击下方的 Define 按钮，选中 java 表示这个模板用于java代码
		点击右侧的 Edit variables
		选择 Expression 下拉框中的 className 并勾选 Skip if…（AS会自动将我们在代码模板中用’$’符包裹的 className自动替换为当前类不含包名的类名）
		点击 Apply 和 Ok 让设置生效

7. eclipse风格快捷键

	Keymap 选择 Eclipse

8. JDK Required tools.jar‘ seems to be not in Android Studio classpath. Please ensure JAVA_HOME points to JDK rather than JRE.

		设置JAVA_HOME变量的路径，后面一直要加”\“才正确，才能正常指引进入里面的得到的文件
		原来”G:\Program Files\Java\jdk1.8.0_31“
		改成”G:\Program Files\Java\jdk1.8.0_31\“

9. 每次启动弹出 Fetching Android SDK component information对话框

		这个获取的过程可能需要很长的时间，也不一定能够成功的获取。
		安装目录/bin/idea.properties文件
			disable.android.first.run=true

10. 自动提示代码

	Editor | General | Code Completion

		Case sensitive completion 选择None

11. Logcat配色

	Editor | Color & Fonts | Android Logcat

		Foreground，取消勾选 Use inherited attributes
		Assert:	#AA66CC
		Debug:	#33B5E5
		Error:	#FF4444
		Info:	#99CC00
		Verbose:	#FFFFFF
		Warning:	#FFBB33

12. 关联源码

AS 默认使用 compileSdkVersion 制定的版本

C:\Users\用户.AndroidStudio2.1\config\options\jdk.table.xml 文件

发现24的确没有指定源码

直接把23版本的源码地址复制到24，搞定