---
title: 得到Android彻底组件化方案
date: 2018-06-19 11:37:17
tags:
	- 架构
---

# 一、模块化：组件化与插件化 #

## 模块化、插件化和组件化的关系 ##

项目发展到一定程度，就必须进行模块化的拆分。

模块化是一种指导理念，其核心思想就是分而治之、降低耦合。

而在 Android 工程实践，目前有两种途径(两大流派)，一个是组件化，一个是插件化。

## 插件化和组件化的区别 ##

组件化和插件化的区别，有一个很形象的图：

{% asset_img 1.png %}

上图看上去比较清晰，其实容易导致一些误解，下面五个小问题，图中可能说的不太清楚：

- 整体的各组件缺一不可吗？
	- 不是的。
	- 组件化的第一个目标就是**降低 整体与组件 的依赖关系**，缺少任何组件都能正常运行
- 组件**独立运行**支持吗？
	- 可以。
	- 组件化的第二个目标就是**组件可以独立运行**，补足一些基本功能之后都是可以独立运行的
- 组件化和插件化可以都用右图来表示吗？
	- 可以。
	- 每个组件都可以看成一个单独的整体
- 右图中的小机器人可以**动态的添加和修改**吗？
	- 如果组件化和插件化都用右图来表示，答案就不一样了
	- 组件化，**编译期**可以
	- 插件化，编译期和**运行时**可以
- 组件化和插件化的最大区别（应该也是唯一区别）
	- 组件化在运行时不具备动态添加和修改组件的功能，但是插件化是可以的

## 如何取舍插件化和组件化 ##

理想的代码组织形式是插件化的方式，届时就具备了完备的运行时动态化

奈何目前还没有一个完美兼容的插件化方案(RePlugin关注中)

在插件化和组件化取舍的一个重要原则是：**产品对动态性的要求**比较高，考虑插件化。一般来说，电商类或广告类产品对动态性要求比较强烈，而类似“得到 APP”这类的知识服务产品，每个功能的推出都是经过精细打磨的，对这种即时的动态性要求不高，所以不需要采用插件化。

产品对动态性的要求比较高，选择**插件化**之前也需要从两个方面权衡一下。

- **兼容性**。一是插件化不可避免的去 hook 一些系统的 api，也就不可避免地有兼容性的问题，因此每个插件化方案需要有专门的团队去负责维护；
- **开发节奏**。二是从一个业务逻辑复杂的项目中去拆分插件化需要的时间可能是非常巨大的，需要考虑对开发节奏的影响。

因此，对大多数产品来说，组件化都是一个不错甚至最佳的选择，它没有兼容性，可以更方便地拆分，并且几乎没有技术障碍，可以更顺利地去执行。特别是对急需拆分的产品来说，组件化是一个可退可守的方案，可以更快地执行下去，并且将来要是迁移到插件化，组件化拆分也是必经的一步。

# 二、为何组件化 #

现状：

- 业务复杂，代码交织在一起，可谓牵一发而动全身
- 花费在熟悉代码的时间甚至大于新需求的开发时间
- 大量代码堆积在一起，编译非常耗时。“得到 APP”Android端几十万行代码，编译一次大约10分钟
- 每个改动都需要测试人员进行大范围的回归
- 各项目组重复造轮子

目标：**优化代码结构，提升编码效率，降低编译耗时，减轻测试回归压力，组件复用**

# 三、何为彻底组件化 #

彻底组件化，主要是为了更好地强调两点：**独立运行，动态集成**。只有做到了代码隔离，才可以称之为“彻底”的

**组件可以独立运行，可以动态加载或卸载组件(组件之间针对接口编程，间接引用)**

# 四、如何彻底组件化 #

要实现彻底组件化，需要考虑的问题主要包括下面四个：

- 组件独立运行。每个组件都是一个完整的整体，如何让其单独运行和调试呢？

- 代码解耦与代码隔离。如何将一个庞大的工程拆分成有机的整体？如何从根本上避免组件之间的直接引用呢？也就是如何从根本上杜绝耦合的产生呢？

- 数据传递和UI跳转。因为每个组件都会给其他组件提供服务，那么主项目（Host）与组件、组件与组件之间如何传递数据？UI 跳转可以认为是一种特殊的数据传递，在实现思路上有啥不同？

- 组件的生命周期。我们的目标是可以做到对组件可以按需、动态的使用，因此就会涉及到组件加载、卸载和降维的生命周期。

{% asset_img architecture.png %}

对三种 module 进行区分：

- 依赖库 library，被其他组件直接引用。比如网络库 module 可以认为是一个 library。

- 组件 Component，是一个完整的功能模块。比如读书或者分享 module 就是一个 Component。我们讲的组件化也主要是针对这种类型

- 主项目 Host，负责拼装组件以形成一个完整app 的 module。一般我们称之为主项目、主 module 或者 Host

## 组件独立运行 ##

设置一个变量 isRunAlone，标记当前是否需要独立运行，根据 isRunAlone 的取值，使用不同的 gradle 插件和 AndroidManifest 文件，甚至可以添加 Application 等 Java 文件，以便可以做一下初始化的操作。

为了避免不同组件之间资源名重复，在每个组件的 build.gradle 中增加 resourcePrefix "xxx_"，从而固定每个组件的资源前缀

下面是读书组件的 build.gradle 的示例：

	if(isRunAlone.toBoolean()){    
		apply plugin: 'com.android.application'
	}else{  
		apply plugin: 'com.android.library'
	}
	.....
	resourcePrefix "readerbook_"
	sourceSets {
	  main {
	      if (isRunAlone.toBoolean()) {
	          manifest.srcFile 'src/main/runalone/AndroidManifest.xml'
	          java.srcDirs = ['src/main/java','src/main/runalone/java']
	          res.srcDirs = ['src/main/res','src/main/runalone/res']
	      } else {
	          manifest.srcFile 'src/main/AndroidManifest.xml'
	      }
	  }
	}

## 代码解耦与代码隔离 ##

Android 的 multiple module 功能，很容易把代码进行初步的拆分

组件针对接口编程

- 坚决**避免组件之间直接引用**（compile) 。
	- 直接引用难免会导致使用其他组件的具体实现类，这样针对接口编程的要求就成了一句空话。
	- 更严重的是，一旦对组件进行动态地加载或卸载，就会导致严重地崩溃。
- **代码编写期间组件之间完全不可见**。
	- 杜绝了直接使用具体的实现类的情况，
- **自动打包依赖的组件**

通过 **自定义gradle插件 + 配置文件**，从根本上杜绝耦合的产生。每个组件都 apply 这个插件

配置文件，每个组件声明自己所需要的其他组件，配置分为 debug 和 release 两种，可以在日常开发和正式打包之间更灵活的切换。

自定义gradle插件，分析运行的 task 命令，如果是打包命令(例如 assembleRelease)自动根据配置文件引入依赖组件，不是(例如 sync/build)则不引入

自定义gradle插件，自动的识别和修改组件的属性，识别出当前调试的组件，然后把这个组件修改为 application 项目，而其他组件则默默的修改成 library 项目。因此不论是要单独编译一个组件还是要把这个组件集成到其他组件中调试，都是不需要做任何的手动修改，使用起来相当的方便。

	// 根据配置添加各种组件依赖，并且自动化生成组件加载代码
	if (project.android instanceof AppExtension) {
	       AssembleTask assembleTask = getTaskInfo(project.gradle.startParameter.taskNames)
	       if (assembleTask.isAssemble
	               && (assembleTask.modules.contains("all") || assembleTask.modules.contains(module))) {
	         // 添加组件依赖
	          project.dependencies.add("compile","xxx:reader-release@aar")
	         // 字节码插入的部分也在这里实现
	       }
	}
	
	private AssembleTask getTaskInfo(List<String> taskNames) {
	   AssembleTask assembleTask = new AssembleTask();
	   for (String task : taskNames) {
	       if (task.toUpperCase().contains("ASSEMBLE")) {
	           assembleTask.isAssemble = true;
	           String[] strs = task.split(":")
	           assembleTask.modules.add(strs.length > 1 ? strs[strs.length - 2] : "all");
	       }
	   }
	   return assembleTask
	}

## 数据传递和UI跳转 ##

### 数据传递 ###

向 Router 请求 组件功能 的具体实现，与 Binder 的 C/S 架构很相像。

一个很容易犯的小错误就是通过持久化的方式来传递数据，例如 file、sharedpreference 等方式，这个是需要避免的。

#### 组件声明自己提供的服务 ####

组件声明自己提供的服务(抽象类或者接口)

简单起见，专门建立了一个 componentservice 的依赖库，里面定义了每个组件向外提供的 service 和一些公共 model。将所有组件的 service 整合在一起，是为了在拆分初期操作更为简单，后面需要改为自动化的方式来生成。这个依赖库需要严格遵循开闭原则，以避免出现版本兼容等问题。

#### 组件注册服务的具体实现 ####

主项目加载组件时，组件注册服务的具体实现到 Router中。

### UI跳转 ###

UI 的跳转也是组件提供的一种特殊的服务，可以归属到上面的数据传递中去。不过一般 UI 的跳转我们会单独处理，一般通过短链的方式来跳转到具体的 Activity。每个组件可以注册自己所能处理的短链的 schme 和 host，并定义传输数据的格式。然后注册到统一的 UIRouter 中，UIRouter 通过 schme 和 host 的匹配关系负责分发路由。

UI 跳转部分的具体实现是通过在每个 Activity 上添加注解，然后通过 apt 形成具体的逻辑代码。这个也是目前 Android 中 UI 路由的主流实现方式。

声明注册服务以及UI跳转已经有成熟的注解框架，后期考虑替换

## 组件的生命周期 ##

要动态的管理组件，给每个组件添加几个生命周期状态：加载、卸载和降维。

为此我们给每个组件增加一个 ApplicationLike 类，里面定义了 onCreate 和 onStop 两个生命周期函数。

- 加载：onCreate()。主项目调用 onCreate() 就称之为组件的加载。组件把自己的服务实现注册到 Router 里面去。

- 卸载：onStop()。组件将自己的服务实现从 Router 中取消注册。不过这种使用场景可能比较少，一般适用于一些只用一次的组件。

- 降维：降维使用的场景更为少见，比如一个组件出现了问题，我们想把这个组件从本地实现改为一个 wap 页。降维一般需要后台配置才生效，可以在 onCreate 对线上配置进行检查，如果需要降维，则把所有的 UI 跳转到配置的 wap 页上面去。

主项目负责加载组件，由于主项目和组件之间是隔离的，那么主项目如何调用组件 ApplicationLike 的生命周期方法呢，目前我们采用的是基于编译期字节码插入的方式，扫描所有的 ApplicationLike 类（其有一个共同的父类），然后通过 javassisit 在主项目的 onCreate 中插入调用 ApplicationLike.onCreate 的代码。

# 五、组件化的拆分步骤 #

组件化的拆分是个庞大的工程，可以分成三步：

- 从产品需求到开发阶段再到运营阶段都有清晰边界的功能开始拆分。比如读书模块、直播模块等，这些开始分批先拆分出去

- 在拆分中，造成组件依赖主项目的依赖模块继续拆出去。比如账户体系等

- 最终主项目就是一个 Host，包含很小的功能模块（比如启动图）以及组件之间的拼接逻辑

# 六、组件化过程中要注意的问题 #

一是技术细节上的不断完善，二是团队的共识建设问题

方案中数据传输和 UI 跳转是分开的两个功能，这是在实际拆分中才做出的选择，因为数据传输更为频繁，且交互形式更多样，使用一个标准化的路由协议难以满足，因此把数据传输改成了接口 + 实现的形式，针对接口编程就可以更加灵活地处理这些情况。

# 七、组件化后的具体成果 #

- **代码结构非常清晰**，分层结构以及之间的交互很明了，团队中的任何一个人都可以很轻松的绘制出代码结构图，这个在之前是没法做到的
- 每次开发需求的时候，面对的代码越来越少，不用背负那么重的代码包袱，可以说达到了“**代码越写越少**”的理想情况。
- 每个组件的**编译耗时大大降低**。从 10 分钟降到了几十秒，工作效率有了很大地提升
- **减轻测试回归压力**。可以分组件测试
- **组件可以复用**。新产品可以使用已有的组件，提升整个公司效率

# 八、总结 #

方案在设计之初参考了目前已有的组件化和插件化方案，站在巨人的肩膀上又加了一点自己的想法，主要是组件化生命周期以及完全的代码隔离方面。特别是代码隔离，不仅要有规范上的约束(针对接口编程)，更要有机制保证开发者不犯错(自定义gradle插件)，我觉得只有做到这一点才能认为是一个彻底的组件化方案