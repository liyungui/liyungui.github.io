---
title: git使用
date: 2019-03-07 15:10:53
categories:
  - 电脑使用
tags:
  - 开发工具
---

[git-flow 的工作流程](https://www.git-tower.com/learn/git/ebook/cn/command-line/advanced-topics/git-flow)

# git认证 #

Git客户端可以通过 `http` 方式和 `ssh`方式连接git服务器上的仓库

http 方式 http://192.168.1.120/mywork.git

ssh 方式 git@192.168.1.120:mywork.git （git为当前机器系统登录用户）

## [SSH Key](http://blog.sina.com.cn/s/blog_6e572cd60101qls0.html) ##

1. 存储在 ~/.ssh 文件夹，一般是 `id_rsa` `id_rsa.pub`

		$ cd ~/.ssh

2. 生成新 SSH

		$ ssh-keygen -t rsa -C "david.l@xuehu365.com"
		Generating public/private rsa key pair.
		Enter file in which to save the key (/c/Users/Administrator/.ssh/id_rsa):
		Enter passphrase (empty for no passphrase):
		Enter same passphrase again:
		Your identification has been saved in /c/Users/Administrator/.ssh/id_rsa.
		Your public key has been saved in /c/Users/Administrator/.ssh/id_rsa.pub.
		The key fingerprint is:
		SHA256:BWinjIvY2cjlR/fsWN/zuJyLpnstOuvI1khAd/yDLcs david.l@xuehu365.com
		The key's randomart image is:
		+---[RSA 2048]----+
		|       ...       |
		|      + o.o      |
		|     = + ..+     |
		|    o = ..o +    |
		| + B o oS+ o .   |
		|. * + . . E      |
		|     . . * . o   |
		|       .+.+ =o+o |
		|       .o.*O..*=.|
		+----[SHA256]-----+

	会要求输入文件名，密码，确认密码，可以直接三次回车，使用默认文件名，空密码

3. 复制id_rsa.pub的内容到github
4. 测试

		$ssh -T david@github.com

# 创建本地仓库repository，提交文件 #

**1. `git init`初始化git项目**

 	在D:/testgit目录下执行以上命令
	成功反馈 Initialized empty Git repository in D:/testgit/.git/，发现testgit目录下多个.git文件夹
	pwd显示当前 目录 
	cd ./AndroidStudioProjects/MyApplication 进入项目目录

**2. 在testgit目录下创建 readme.txt ，写入1111111**
**
3. `git add readme.txt` 添加到暂存区**，无任何返回说明add成功

**4. `git commit -m "第一次提交"` 提交到仓库**。第一次提交是提交注释

	[master (root-commit) 9b057ed] 第一次提交
	 1 file changed, 1 insertion(+)
	 create mode 100644 readme.txt

**5. `git status`查看是否还有文件未提交**

	On branch master
	nothing to commit, working directory clean //没有修改未提交

**6. readme.txt增加一行内容 222222**

**7. `git status`**

	On branch master
	Changes not staged for commit: //stage暂存
	  (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory) //discard丢弃

        modified:   readme.txt

	no changes added to commit (use "git add" and/or "git commit -a")

**8. `git diff readme.txt` 对比差异**

	diff --git a/readme.txt b/readme.txt
	index 35241c7..8b0f06c 100644
	--- a/readme.txt
	+++ b/readme.txt
	@@ -1 +1,2 @@
	-111111111111111111
	\ No newline at end of file
	+111111111111111111
	+22222222222222222
	\ No newline at end of file

`git add readme.txt` 因为上面说还没暂存以提交（要先暂存）

`git status`
	On branch master
	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)
	
	        modified:   readme.txt

`git commit  -m "增加了一行内容 2222222"`

	[master b5fd23c] 增加了一行内容 2222222
	 1 file changed, 2 insertions(+), 1 deletion(-)


# 版本回退 #

可以回退到某一历史版本(撤销提交)

- git reset 
	- 回到某次提交，类似于穿越时空。中间的提交记录会丢失。**版本历史干净**
	- reset有三个参数soft,mixed,hard分别对应head的指针移动，index（暂存区）、以及工作目录的修改，当缺省时，默认为mixed参数
- git revert
	- 生成一个新的提交来撤销某次提交，此次提交之前的commit都会被保留，对于项目的版本历史来说是往前走的。**保留完整历史**

**1. `git log` 查看历史记录**，由近到远显示。`git log –pretty=oneline`是一行展示一条记录，方便查看（只展示注释）
	
	commit b5fd23c15ef2cdec3d70bbcb607f174e0e702055
	Author: David <david.l@xuehu365.com>
	Date:   Tue Apr 19 16:24:37 2016 +0800
	
	    增加了一行内容 2222222
	
	commit 9b057ed353d5de1b5bb88f082b6345ec6080c5f5
	Author: David <david.l@xuehu365.com>
	Date:   Tue Apr 19 15:53:07 2016 +0800
	
	    第一次提交
	
**2. `git reset  --hard HEAD^` 回退一个版本**。如果要回退到上上个版本只需把HEAD^ 改成 `HEAD^^` 以此类推

	HEAD is now at 9b057ed 第一次提交
	
打开readme.txt发现文件内容的确变成了 111111. 或者cat readme.txt命令查看

git log 发现， 只有第一次提交的历史记录了（没有回退这次记录，也没有第二次增加内容提交的记录）

**3. `git reflog` 查看所有历史记录（带版本号，精确的），已经reset掉的也会展示**

	9b057ed HEAD@{0}: reset: moving to HEAD^
	b5fd23c HEAD@{1}: commit: 增加了一行内容 2222222
	9b057ed HEAD@{2}: commit (initial): 第一次提交

**4. `git reset --hard b5fd23c`**

	HEAD is now at b5fd23c 增加了一行内容 2222222

`cat readme.txt`

	111111111111111111
	22222222222222222

**5. git revert**

git revert与reset的区别是git revert会生成一个新的提交来撤销某次提交，此次提交之前的commit都会被保留，也就是说对于项目的版本历史来说是往前走的。而git reset 则是回到某次提交，类似于穿越时空。

# 工作区、暂存区、仓库 #

`git add` 是把工作区的内容添加到了暂存区(index)

`git commit` 是把暂存区的内容提交到了仓库

`git checkout -- <file>...`是丢弃工作区的修改，返回到暂存区的状态。一定不要忘了 -- ，否则就成了创建分支

**所以提交流程是，先add 再commit**

# 远程仓库 #

注册github账号，本地Git仓库和github仓库之间的传输是通过SSH加密的
	
1. 创建SSH Key

	用户目录/.ssh目录下（我的C:\Users\Administrator\ .ssh）是否有id_rsa和id_rsa.pub这两个文件。没有则在git bash中创建
		
2. 把公钥放到服务器

	登录github,打开” settings”中的SSH Keys页面，然后点击“Add SSH Key”,填上任意title，在Key文本框里黏贴id_rsa.pub文件的内容

3. 到服务器创建仓库
4. 添加远程仓库到本地

	`git remote add <主机名> <网址>` 添加远程主机

	`git remote rm <主机名>` 删除远程主机

	`git remote rename <原主机名> <新主机名>`	修改远程主机名

5. `git push`推送本地仓库到远程仓库


6. `git clone`从远程仓库克隆到本地仓库（会在本地仓库根目录下生成新文件夹）（克隆是默认主机名为origin，可用 -o指定主机名;默认克隆master分支，可用 -b 指定分支名）

	git clone -o jQuery https://github.com/jquery/jquery.git

7. `git fetch <远程主机名> <分支名>` 取回远程主机特定分支的更新（**并不和本地代码合并，通常用来查看他人进度**）（省略分知名就是取回所有分支更新）

8. `git pull <远程主机名> <远程分支名>:<本地分支名>` 取回远程主机某个分支的更新，再**与本地的指定分支合并。实质上等同于先做git fetch，再做git merge。**

		git pull origin next:master //取回origin主机的next分支，与本地的master分支合并

	与当前分支合并，则冒号后面的部分可以省略

		git pull origin next //取回origin/next分支，再与当前分支合并。等同于下面两条命令
		git fetch origin next
		git merge origin/next

	如果当前分支与远程分支存在追踪关系，可以省略远程分支名

		git pull origin

	如果远程主机删除了某个分支，默认情况下，git pull 不会在拉取远程分支的时候，删除对应的本地分支。这是为了防止，由于其他人操作了远程主机，导致git pull不知不觉删除了本地分支。但是，你可以改变这个行为，加上参数 -p 就会在本地删除远程已经删除的分支。

	error: Your local changes to the following files would be overwritten by merge:Please, commit your changes or stash them before you can merge.错误解决

		http://blog.chinaunix.net/uid-10415985-id-4142896.html
		git stash
		git pull
		git stash pop
		然后可以使用git diff -w +文件名 来确认代码自动合并的情况.

9. `git push <远程主机名> <本地分支名>:<远程分支名>` 分支推送顺序的写法是<来源地>:<目的地>，所以git pull是<远程分支>:<本地分支>，而git push是<本地分支>:<远程分支>。

	如果当前分支与多个主机存在追踪关系，则可以使用-u选项指定一个默认主机，这样后面就可以不加任何参数使用git push。

		git push --all origin 不管是否存在对应的远程分支，将本地的所有分支都推送到远程主机
		git push origin --tags 不会推送标签（tag），除非使用--tags选项
		git push --force origin 远程主机版本比本地新，推送会报错，要求先在本地做git pull合并差异，然后再推送到远程主机。--force选项，覆盖远程主机上更新的版本

# 分支 #

1. `git branch dev` 创建分支
2. `git checkout dev` 切换分支
3. `git checkout –b dev` 创建并切换到分支。相当于上面两条命令 `-d`删除分支
4. `git checkout -b dev origin/dev` 作用是checkout远程的dev分支，在本地起名为dev分支，并切换到本地的dev分支
4. `git branch` 查看分支 `-r查看远程分支，-a查看所有分支（本地和远程）`当前分支前面会添加一个星号
5. `git branch --set-upstream master origin/master` 本地master分支追踪远程origin/master分支
6. `git branch -m devel develop` 重命名本地分支devel为develop

		git checkout -b dev
			Switched to a new branch 'dev'
		编辑readme.txt，增加一行333333
		git add readme.txt
		git commit -m "dev分支增加内容33333" //提交修改
			[dev 88ac64e] dev分支增加内容33333
		 	1 file changed, 2 insertions(+), 1 deletion(-)
		git checkout master //切换到master分支
			Switched to branch 'master'
		cat readme.txt
			111111111111111111
			22222222222222222
		git merge dev
			Updating b5fd23c..88ac64e //88ac64e就是最新的提交3333那次版本
			Fast-forward
			 readme.txt | 3 ++-
			 1 file changed, 2 insertions(+), 1 deletion(-)
		查看发现master分支readme.txt也有3333了
		git branch -d dev
			Deleted branch dev (was 88ac64e).

6. 解决冲突

	新建分支dev，增加内容4444，提交，切换到master，增加内容5555，合并dev，发现冲突，查看文件内容并修改，重新提交（master就变成了修改后的版本）
		
		git merge dev
			Auto-merging readme.txt
			CONFLICT (content): Merge conflict in readme.txt
			Automatic merge failed; fix conflicts and then commit the result.
		cat readme.txt
			111111111111111111
			22222222222222222
			33333333333333333
			<<<<<<< HEAD
			55555555555555555
			=======
			44444444444444444
			>>>>>>> dev
		git status
			On branch master
			You have unmerged paths.
			  (fix conflicts and run "git commit")
			Unmerged paths:
			  (use "git add <file>..." to mark resolution)			
			        both modified:   readme.txt			
			no changes added to commit (use "git add" and/or "git commit -a")
	
		修改readme.txt内容（我这里就不改了）
		git add readme.txt
		git commit -m "master解决冲突"
			[master af8ac43] master解决冲突
		git status
			On branch master
			nothing to commit, working directory clean

7. 分支管理策略。

	通常合并分支时，git一般使用”Fast forward”模式，在这种模式下，删除分支后，会丢掉分支信息，现在我们来使用带参数 –no-ff来禁用”Fast forward”模式。`git merge –no-ff  -m “注释” dev`

![](http://jbcdn2.b0.upaiyun.com/2012/07/Git-branch-management-strategy5.png)
![](http://jbcdn2.b0.upaiyun.com/2012/07/Git-branch-management-strategy6.png)
			
	图片来自 http://blog.jobbole.com/23398/ 图片解释了–no-ff合并和普通合并，分支模型的区别

8. bug分支

	比如我在开发中接到一个404 bug时候，我们可以创建一个404分支来修复它，但是，当前的dev分支上的工作还没有提交。Git提供了一个stash功能，可以把当前工作现场 ”隐藏起来”，等以后恢复现场后继续工作。确定在哪个分支上修复bug，比如我现在是在主分支master上来修复的，现在我要在master分支上创建一个临时分支issue-404。修复完成后，切换到master分支上，并完成合并，最后删除issue-404分支。

	回到dev分支上干活，git status发现工作区是干净的，那么我们工作现场去哪里呢？我们可以使用命令 `git stash list`查看，发现工作现场还在，Git把stash内容存在某个地方了，但是需要恢复一下，可以使用如下2个方法：

		1. git stash apply恢复，恢复后，stash内容并不删除，你需要使用命令git stash drop来删除最上面一条记录。
		2. git stash pop,恢复的同时把stash内容也删除了。

## 分支合并

	git merge dev
	
## 合并commit

分支提交记录(向右增长)

	[master] dd2e86 - 946992 -9143a9 - a6fd86 - 5a6057
	[feature] 76cada - 62ecb3 - b886a0

合并单个commit

	git checkout master
	git cherry-pick 62ecb3  合并 62ecb3 到master
	
合并连续的commit

	合并 76cada ~62ecb3 到 master
	git checkout -b newNameBranch 62ecb3
	git rebase --onto master 76cada^ 指明从哪个commit开始    


# gitignore #

	http://www.bubuko.com/infodetail-946833.html

有时添加.gitignore文件后并没有忽略我们想要忽略的文件，解决方法就是**清除缓存**，原因gitignore对已经追踪(track)的文件无效，清除缓存后文件将以未追踪的形式出现.然后再**重新添加提交**一下,.gitignore文件里的规则就可以起作用了

	git rm -r --cached .
	git add .
	git commit -m "update .gitignore"


## git配置 ##

### 文件名区分大小写 ###

工程/.git/config文件

	[core]
	repositoryformatversion = 0
	filemode = false
	bare = false
	logallrefupdates = true
	symlinks = false
	ignorecase = false #默认为true
	hideDotFiles = dotGitOnly

或者直接命令行 

	Add ignorecase = false to [core] in .git/config;

# git blame && git show 查看某一行代码的修改历史 #

	git blame file_name
	可以使用 -L指定开始和结束行:
		实例：git blame ./ScreenLivePlayback.java  -L 1101,+9

其显示格式为： 
commit ID | 代码提交作者 | 提交时间 | 代码位于文件中的行数 | 实际代码 

类似于下面这样

	f604879e (yingyinl              2014-09-23 23:39:55 -0700   35) typedef enum
	9be6b4bd (yingyinl              2014-01-01 21:22:50 -0800   36) {
	597886b5 (Shengjie Yu           2015-09-29 12:00:24 +0800   37)     Index_R_Hue = 0,    //Index_Range0_Hue
	9be6b4bd (yingyinl              2014-01-01 21:22:50 -0800   38)     Index_R_Sat,
	9be6b4bd (yingyinl              2014-01-01 21:22:50 -0800   39)     Index_R_brt,
	9be6b4bd (yingyinl              2014-01-01 21:22:50 -0800   40)     Index_R_Offset,
	9be6b4bd (yingyinl              2014-01-01 21:22:50 -0800   41)     Index_R_Gain,
	f604879e (yingyinl              2014-09-23 23:39:55 -0700   42) 

这样，我们就可以知道commit ID了，然后使用命令：git show commitID来看

对应 AS git 插件中的 `git -- annotate`

# git-flow 工作流程 #

在团队开发中使用版本控制系统时，商定一个统一的工作流程是至关重要的

git-flow是非常流行的工作流程

git-flow 并不是要替代 Git，它仅仅是把标准的 Git 命令用脚本组合了起来。所以并不需要安装什么特别的东西就可以使用 git-flow 工作流程

## 在项目中设置 git-flow ##

项目根目录 执行 `git flow init`，一个交互式安装助手将引导您完成初始化操作。强烈建议使用默认的命名机制，并且一步一步地确定下去

git-flow 它不会以任何一种戏剧性的方式来改变你的仓库，你还是可以使用普通的 Git 命令

### 分支的模式 ###

预设两个主分支在仓库中：

- **master** 只能用来包括产品代码。不能直接工作在这个 master 分支上。不直接提交改动到 master 分支上也是很多工作流程的一个共同的规则。
- **develop** 是你进行任何新的开发的基础分支。

## 功能开发 ##

### 开始新功能 ###

	$ git flow feature start rss-feed
	Switched to a new branch 'feature/rss-feed'
	
	Summary of actions:
	- A new branch 'feature/rss-feed' was created, based on 'develop'
	- You are now on branch 'feature/rss-feed'

git-flow 会直接签出这个新的分支，这样你就可以直接进行工作了。

### 完成新功能 ###

经过一段时间艰苦地工作和一系列的聪明提交，我们的新功能终于完成了：

	$ git flow feature finish rss-feed
	Switched to branch 'develop'
	Updating 6bcf266..41748ad
	Fast-forward
	    feed.xml | 0
	    1 file changed, 0 insertions(+), 0 deletions(-)
	    create mode 100644 feed.xml
	Deleted branch feature/rss-feed (was 41748ad).

 “feature finish” 命令会把我们的工作整合到主 “develop” 分支中去。也会删除这个当下已经完成的功能分支，并且换到 “develop” 分支。

## 管理 releases ##

### 创建 release ###

	$ git flow release start 1.1.5
	Switched to a new branch 'release/1.1.5'

“develop” 分支的代码已经是一个成熟的 release 版本时，可以开始生成一个新的 release 了

release 分支是使用版本号命名的

release 分支都是基于 “develop” 分支的

开始完成针对 release 版本号的最后准备工作，并且进行最后的编辑。

### 完成 release ###

	git flow release finish 1.1.5

这个命令会完成如下一系列的操作：

- 首先，git-flow 会拉取远程仓库，以确保目前是最新的版本。
- 然后，release 的内容会被合并到 “master” 和 “develop” 两个分支中去，这样不仅产品代码为最新的版本，而且新的功能分支也将基于最新代码。
- 为便于识别和做历史参考，release 提交会被标记上这个 release 的名字（在我们的例子里是 “1.1.5”）。
- 清理操作，版本分支会被删除，并且回到 “develop”。

## hotfix ##

release 版本发现一些小错误。需要 hotfix

### 创建 Hotfixes ###

	$ git flow hotfix start missing-link

因为这是对产品代码进行修复，所以这个 hotfix 分支是基于 “master” 分支。这也是和 release 分支最明显的区别，release 分支都是基于 “develop” 分支的。你不应该在一个还不完全稳定的开发分支上对产品代码进行地修复。

### 完成 Hotfixes ###

	$ git flow hotfix finish missing-link

类似 release，修复这个错误当然也会直接影响到项目的版本号！

- 完成的改动会被合并到 “master” 中，同样也会合并到 “develop” 分支中，这样就可以确保这个错误不会再次出现在下一个 release 中。
- 这个 hotfix 程序将被标记起来以便于参考。
- 这个 hotfix 分支将被删除，然后切换到 “develop” 分支上去。

**注意：git flow 操作都是本地仓库进行的(仅仅commit)，需要手动 push**

# rebase保持分支整洁

## 背景

一个feature分支一般都有多次commit。最后提交到主干分支(master或develop)后，会看到乱七八糟的所有增量修改历史。其实对别人来说，我们的改动应该就是增加或者删除，给别人看开发过程的增量反而太乱。于是我们可以将feature分支的提交合并后然后再merge到主干这样看起来就清爽多了。

## rebase

可以对某一段线性提交(commit)历史进行编辑、删除、复制、粘贴；因此，合理使用rebase命令可以使我们的提交历史干净、简洁！

**特别注意：**

不要通过rebase对任何公共仓库中的公共分支(push)进行修改；即**只能rebase修改自己个人分支**

## merge Vs rebase

### merge

	git checkout feature
	git merge master

{% asset_img merge.jpg %}

为了保持时间顺序，生成一个新的commit记录，插到 feature 最后面

如果主干分支变动频繁，每次变动都需merge，严重污染feature分支，难以理解历史变更记录

### rebase

	git checkout feature
	git rebase master

{% asset_img rebase.jpg %}

直接将feature提交记录，插到主干分支最后面（本来feature有部分提交是在主干分支前面的，为了保持feature提交连续性，就直接整理插到主干分支最后面）
	
产生完美线性的项目历史记录，更加清晰，易于理解

可以从feature分支顶端一直跟随到项目的开始而没有任何的分叉

## Interactive Rebase

比自动rebase更强大，将提交移动到新分支时更改提交记录。

通常用于在合并feature分支到主干分支之前清理杂乱的历史记录（比如合并成一条提交记录）

要开始基于交互式会话rebase，需要 -i 选项：

	git checkout feature
	git rebase -i master

合并提交记录的命名

	pick：保留该commit（缩写:p）
	
	reword：保留该commit，但我需要修改该commit的注释（缩写:r）
	
	edit：保留该commit, 但我要停下来修改该提交(不仅仅修改注释)（缩写:e）
	
	squash：将该commit和前一个commit合并（缩写:s）
	
	fixup：将该commit和前一个commit合并，但我不要保留该提交的注释信息（缩写:f）
	
	exec：执行shell命令（缩写:x）
	
	drop：我要丢弃该commit（缩写:d）
	
一般都是第一个提交记录reword，其余的squash

# 参考&扩展

- [Merge vs Rebase](https://juejin.im/post/5c7690ab518825404713e709)
- [使用git rebase合并多次commit](https://github.com/zuopf769/how_to_use_git/blob/master/%E4%BD%BF%E7%94%A8git%20rebase%E5%90%88%E5%B9%B6%E5%A4%9A%E6%AC%A1commit.md)
