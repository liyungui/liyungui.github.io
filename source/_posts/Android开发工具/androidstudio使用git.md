	http://jingyan.baidu.com/article/6766299761b1be54d51b84a0.html

1. 在studio中设置git插件

	`File->Setting->Version Control->Git`,添加您刚刚安装的git地址目录,例如: C:\Program Files\Git\bin\git.exe , 
	然后可以点击Test测试一下，如下图：那么你就设置成功了。

2. 初始化git项目(git init)

	`VCS->Enable Control Integration->Select "Git"`

3. 为git添加remote(git remote)

	`git remote add origin "https://github.com/xxx/xxx.git"` 使用Git Bash，将目录切换到项目的目录，然后输入git添加remote的命令

		pwd显示当前 目录 
		cd ./AndroidStudioProjects/MyApplication 进入项目目录

4. 将代码添加到VCS(git add)

	`选中要提交的文件->VCS->Git->Add`

5. 提交变化(git commit)

	`VCS->Commit Changes`在提交的时候可以选择Commit and Push,就可以直接push到服务器

6. Git Push

	`VCS->Git->Push`

7. clone project到studio

	`VCS-> checkout from version control->Git`
	
# 设置代理

建议给项目单独设置代理

项目根目录 `gradle.properties`

```
# https走http协议端口
systemProp.http.proxyHost=127.0.0.1
systemProp.http.proxyPort=1088
systemProp.https.proxyHost=127.0.0.1
systemProp.https.proxyPort=1088
```	