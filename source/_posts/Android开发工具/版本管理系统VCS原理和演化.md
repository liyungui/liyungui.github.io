	小李的版本管理系统 http://mp.weixin.qq.com/s?__biz=MzAxOTc0NzExNg==&mid=2665513204&idx=1&sn=c4c493d771a167a84ace01c3e016417e#rd

前言：这篇文章应读者要求所写，主要聊聊 `版本管理系统（Version Control System,简称 VCS）`， 这篇文章不能让你学会一门技术， 但是希望能帮你 `理解版本管理的原理`。

## “人肉” 版本管理 ##

另存为一个新文件

于是小李的电脑上就出现了这样的情况：

	Person.java
	Person_2015_10_12_还有希望.java
	Person_2015_10_15_这个算法也不错.java
	Person_2015_10_18_老师喜欢这个方案.java


## 锁定文件：避免互相覆盖 ##
后来老师给小李介绍了一个大一点的项目， 一个人搞不定了。小李叫来好基友小梁， 两个人意气风发，坚决要把这个项目如期拿下。 

小李把小梁的代码复制到自己电脑以后， 发现出了大问题：自己对Common目录下的public.js做了大改， 代码改动了好几百行，可是这些改动竟然被小梁的public.js覆盖掉了,   这一周的改动都丢失了 ！

最后还得寻求解决办法,  有室友推荐了个软件BeyondCompare ， 可以清晰的比较两个人的代码目录和文件，改动一目了然。

小李和小梁试用了一下，BeyondCompare 很好很强大， 只是改动多了，手工工作量还是挺大的。

干脆一不做，二不休， 开发一个版本控制系统（Version Control System）得了， 彻底解决文件被覆盖的问题。

这个VCS有这样的功能：

	(1) 支持把代码放到一个服务器上， 这样就是本地电脑出了问题也不怕
	
	(2) 任何人如果想对一个文件进行修改， 需要先对该文件做一个操作： checkout,   这会把文件锁住，其他人无法修改
	
	(3) 修改完以后， 需要做一个checkin 操作， 修改会被发到服务器端保存， 形成新的版本， 并且释放文件锁
	
	(4) 可以支持回退的功能，也就是说，可以回退到之前的版本去。 

码农翻身注： 微软的Visual SourceSafe就是这种风格的：文件被一个人独占式的锁住进行修改，如下图，标记为红色的文件就是被特定用户锁住了。

这个VCS包括服务器端，主要用来存放代码，进行版本管理。
还有一个客户端，主要用来和服务器端打交道，checkout/check in 代码。 

## 允许冲突：退一步海阔天空 ##
有了这个VCS , 小李和小梁如虎添翼， 再也不怕合作期间文件互相覆盖的问题了。 

老师又给小李和小梁介绍了三个师弟，进来帮助加快进度。

小师弟们对VCS不太熟， 经常性的把自己根本不用修改的文件也都checkout 出来，  并且迟迟不checkin , 搞的其想修改代码的人根本没法修改。 

怎么办呢？ 小李去找小梁商量： “要不咱把锁文件的功能去掉？ “

小梁说： “可是两个人，甚至多个人改了同一个文件怎么办？怎么提交？　以谁的为准？”

举个例子，小李修改了Person.java , 并且成功的提交到了服务器的VCS中。 与此同时，小梁也修改了Person.java , 提交的时候，系统就会提示：
“对不起， 小李已经修改了， 请下载最新版本。”

这时候小梁有两个选择：

	(1) 把自己的修改先择出来， 放到其他文件中暂存， 然后把服务器端的最新版本（包含小李的修改）下载到本机， 然后在把自己的修改加上去，最后提交到服务器。 
	
	(2) 把VCS 客户端 扩展一下，自动的去取服务器端的最新版本，然后自己本地的Person.java做一个 Merge  。 

这时候又会出现两种情况：

	A  小梁和小李的修改位于不同的地方， 没有冲突，这时候就可以自动的Merge了，Merge后向服务器端提交即可
	
	B  小梁和小李对同一行进行的修改，出现了冲突， 这时候只好人工来确定到底用谁的代码了， 人工Merge后再想服务器端提交。

鉴于同时改动一个地方的可能性虽然是有的，但是不常见，所以小李和小梁决定：

放弃文件锁， 提供一个Merge的功能就可以了。

(码农翻身注：开源的版本管理系统CVS, SVN都是采用的这种方式)

## 分支：多版本并行 ##

电子商城项目在师弟的帮助下，花了10个月才推向市场， 没想到大受欢迎， 高兴之余，也带来了新问题：

	(1) 已经上市的老版本有不少Bug需要修改
	
	(2) 用户提了一大批新功能，有些新功能还需要修改老代码， 有的不需要。 

很明显，这就不能在一个代码库中进行修改了， 如果这么做， 那修正了老版本的Bug以后就没法发布了，因为也包含新功能的代码，可能还没测试完成。
小李决定， 再次扩展现有的VCS， 支持分支的功能！

以刚刚发布的产品为基准， 创建一个新的分支V2.0  , 原来的分支叫V1.0

由两拨人分别在两个分支上做开发， 这样两者互不冲突， V1.0的Bug 修改以后就可以发布， 不用考虑V2.0

到了某一个时间点，例如V2.0开发完成，即将进入测试的时候， 需要把V1.0分支的代码修改Merge到V2.0中来， 为什么要这么做呢？

如果不Merge 过来， 那V2.0岂不还是有老版本遗留的Bug ？ 

当然Merge的时候有很大的可能会出现“冲突”，需要自动或者人工小心的处理掉。

如果在V2.0开发过程中，又有了新的需求， 还可以创建新的分支， 只要选择好基于哪个出发点来创建就行了。

## 分布式管理：给程序员放权 ##

随着电子商务越来越火，越来越多的人也想用小李和小梁的这套软件搭建独立的一个电子商城系统。

小李决定把源代码开放出去，让网络上的程序员都参与进来开发， 让电子商城系统发展壮大！

互联网的力量远远超出小李的想象， 参与到这个电子商城系统开发的竟然高达几百人。人多了，原来的版本管理系统有点力不从心了， 出现了各种新情况。

首先有些喜欢“小步提交”人感到特别不爽， 因为版本管理系统的服务器是集中式的， 不太稳定，时不时停机， 导致他们无法提交代码。

其次出现了“多人一起竞争”的情况， 多个人都对同一个文件进行了修改，为了获得最新版本，非常麻烦，有时候以为自己拿到了最新版本，可是提交的时候发现还是被别人捷足先登，先提交了，只好再取一次最新版本来合并。 

还有些人，喜欢两个人之间先交流一下代码， 然后再提交到服务器上， 由于现在没有合适的技术，只好通过Email把文件发来发去的方式来做。

但这些都不是最重要的，最重要的是有些程序员的代码没有经过好好测试就提交进入了主要的代码库， 惹了不少乱子。

如果在代码提交之前有人做一下代码审查就好了， 这样能够保证代码质量。 

之前的代码仓库是集中共享的， 这样是无法解决现在遇到的问题的：

小李突发奇想： 要不给每个人设置一个本地代码仓库？

工作之前先把服务器端的代码全部取到本地， 喜欢小步提交的人在本机想怎么折腾就怎么折腾， 没有网络也能玩起来， 只有在必要的时候再提交到集中式的服务器中去。

这么做依然解决不了提交代码时进行评审的需求。 

如果心胸再开阔一点，干脆让每个程序员的代码仓库都独立得了， 搞成这样：

点击看大图

工作流程也得改一改（仔细看，很重要）：

(1) 官方先设置一个代码仓库

(2) 每个程序员都可以克隆官方的代码仓库， 做出修改。

(3) 修改完以后，不直接推送到官方代码仓库， 相反，推送到自己的代码仓库去

(4) 通知项目维护者，请求他去拉取自己的修改

(5) 维护者在自己的私有代码仓库，获得贡献者的修改， 然后决定是否接受这个修改

(6) 维护者将最新的改动推送到官方仓库

码农翻身注：这个工作流程参考了Git网站的文档： https://git-scm.com/book/en/v2

这样一来大家都轻松了， 每个人都有自己的一亩三分地， 想怎么折腾就怎么折腾， 两个程序员之间也可以通过开放的代码仓库交换代码了。

项目维护者终于对代码提交有了“审批”的功能， 只把那些好的代码纳入到官方的仓库中。

小李为新的版本控制系统起了个牛气哄哄的名字，叫做 Hit ，他内心隐隐约约的觉得Hit才是版本管理系统的未来， 于是决定不再管那个什么电子商城的鸟系统， 全力的投入到Hit的开发中来。

码农翻身注：分布式版本管理系统除了Git之外，还有Mercury， IBM的RTC等。
## 程序员也爱社交 ##
等到Hit系统发布以后，小李惊奇发现，整个开源世界似乎发生了巨变。

之前小李想参与一个开源项目，或者说拿到committer(提交者)权限是非常非常难的，你得有很多的积累才行。

有一次小李发现了Struts的一个安全隐患,并且做了漂亮的修改， 但是苦于自己没有提交权限， 无法提交到Struts的代码仓库中， 通过Email 把Bug fix 发给了Struts的维护者，几乎是石沉大海。

现在好了，Hit是分布式的， 可以创建一个完全属于自己的Struts代码仓库了， 想怎么改就怎么改， 完全没有限制。

如果觉得代码不错， 就向Struts的官方维护者发一个请求， 让他们去合并就可以了。 

Hit受到了开源世界的极大好评。

小李决定趁热打铁，进一步降低使用Hit的门槛， 把Hit用一个Web系统包装起来， 不但能完成上述基本功能， 还要做一点社交化的创新。

以后每个人都有自己的专属页面， 上面能展示自己的参与的开源项目，关注的项目，最近一段时间的活动（代码提交等等）

还要像微博那样让大家互相关注，那些推出了好项目，提交了好代码的大V就能变成程序员中的明星， 就像下面这位：

Linux 创始人 Linus Torvalds

小李决定把这个Web版本的源码管理系统叫做HitHub 。

程序员们在HitHub上玩的不亦乐乎，关注他人， 参加开源项目，合作，分享。慢慢的开源世界的主要项目都搬家到HitHub上来了。

连一些著名企业在招聘的时候，都要问应聘者的HitHub账号，看看他在上面的活动情况。

HitHub火了。 
