---
title: Android端架构_单Activity模式
date: 2018-05-07 16:53:01
tags: 架构
---

# 架构存在的必要 #

本架构带来的好处是：

- **单Activity模式，脱离系统限制**：
	- Android界面之间的切换要依赖系统的Activity
		- 切换过程和动画不可控制
		- 一个界面的生命周期也无法掌握（做一个缓存都很困难）
		- 界面之间的逻辑交互和信息传递麻烦且不清晰。
- **分层分责，更符合OOP原则**：
	- **可读性**：划分层次，各司其职，清晰明了。
	- **复用性**：基础设施可以快速复用。
	- **扩展性**：隔离了业务逻辑和基础设施，能够轻松扩展，拥抱变化
		- 纵向分层（Controller&Manager&Service以及Observer&CommandReceiver）
		- 横向分责（MVC&MVP以及状态机）
		- 不会有牵一发而动全身的尴尬
		- 纵向分层，下层对上层屏蔽具体实现逻辑，上层不用关心下层具体实现逻辑。

# 架构特性 #

高内聚，低耦合

- **单Activity的View栈**： 
	- 框架采用单Activity模式，通过一个Activity的生命周期来维护人机交互。
	- 通过维护一个View栈来实现界面的切换。 
	- 自由度高，自己控制切换形式和生命周期
- **MVC||MVP**： 
	- 实现数据与展现及业务逻辑分离
- **状态机**： 
	- 当前状态只关心与当前状态有关的消息，然后做出适合当前状态操作。 
	- 场景的分离，状态机让每个特定的场景的业务逻辑内聚，只关心自己的业务
- **纵向分层：Controller&Manager&Service**： 
	- 纵向分层，屏蔽底部实现 
		- Service提供基础的服务，比如存储服务，网络服务等。 
		- Manager通过service的服务，完成一个业务模块的具体事务。 
		- Controller帮助manager与其他（view） 
	- 业务逻辑的纵向分层，每一层只完成该层的任务，逻辑清晰，层次分明，复用性高
- **Observer&CommandReceiver**： 
	- 观察模式和命令模式，自上而下的命令，自下而上的汇报。 
	- 多用于界面展现纵向分层，使每一个控件只专注于展现和完成自己的交互
- **工厂模式**： 
	- 利用工厂来统一维护生命周期，按需加载控件。 
	- 统一管理，可新建一个工厂生产另外一套风格的控件

# 鸟瞰 #

## 核心类图 ##

{% asset_img framework.png %}

核心类BaseController，以它为中心所控制的各种Manager（UiManager、StateManager、UserManager、PersonManager），Manager也许会靠一些Service（NetService、StorageService、StatisticsService）支撑它。

## 点击一次按键后发生了什么？ ##

{% asset_img sequence.png %}

控件只能向上汇报自己被点击的Message，具体如何操作只能由能够做决定的层来处理这条Message(一般在当前State)，当前State明白意图后告诉Controller去执行具体的逻辑。Controller命令Manager去做具体模块的事务。Manager需要指挥多个Service来完成一次事务的处理，指挥NetService拉去网络数据，拉去成功后然后指挥StorageService将其保存到储存中。完成这些操作后，Controller接到Manager的完成通知会发出一个message，当前state收到消息会去告诉Controller更新相关界面。

# 最佳实践 #

## 快速上手 ##

### 从Activity开始:  ###

- 1）继承BaseActivity。 
- 2）**Controller**：实现BaseActivity的createController()方法，提供一个继承BaseController的Controller。 
- 3）**UiManager**：实现BaseController的createUiManager()方法，提供一个继承BaseUiManager的UiManager。 
- 4）**Factory**：在UiManager实现自己的ViewFactory、DialogFactory、PopupWindowFactory、

### State一个状态，Screen一张屏幕: ###

- State 
	- 继承一个状态，通过StateManager将状态加入栈中
	- forwardEnter() 进入状态时的回调（可在此时将Screen加到View树中）
	- pop() 将状态从栈中移除时回调（可在此时将Screen从View树中移除）
	- exit() 进入别的状态，来开始此状态时回调（可在此时停止一些有关于此屏幕的异步操作）
	- backEnter() 从别的状态中回到当前状态时回调（可在此时刷新数据显示）

			public abstract class State implements IUserEventProcessor {
					...
			 
				public boolean handleMessage(ICommandReceiver commandReceiver, StateManager stateManager,int messageId, IContainer params, IContainer result) {
					return false;
				}
					public abstract void pop(ICommandReceiver commandReceiver,State nextState, IContainer params,IContainer result);
				 
					public abstract void exit(ICommandReceiver commandReceiver, State nextState, IContainer params,IContainer result);
				 
					public abstract void forwardEnter(ICommandReceiver commandReceiver, State lastState,IContainer params, IContainer result);
				 
					public abstract void backEnter(ICommandReceiver commandReceiver, State lastState,IContainer params, IContainer result);
					...
			}
			
- Screen 
	- 继承Screen，实现各部分控件，在ViewFactory创建后，UiManager将其push到FrameView中，
	- MainActionBar 顶部栏
	- BottomBar 底部工具栏
	- ViewGroup 内容		

			public abstract class Screen extends FrameLayout implements MainActionBarListener,BottomBarListener,IObserver,ICommandReceiver {
				protected abstract MainActionBar createMainActionBar();
			 
				protected abstract BottomBar createBottomBar();
			 
				protected abstract ViewGroup createContent();
			}
	
### Observer接受汇报，CommandReceiver接受命令: ###

- Observer 
	- 向上汇报，例如按钮-我被点击了。
	- 消费者模式，一直上报到能够处理这条消息的层为止。
 
			public interface IObserver {
					boolean handleMessage(int messageId, IContainer params,IContainer result);
			}
			
- CommandReceiver 
	- 向下命令，例如将此数据显示。
	- 消费者模式，一直向下到能够执行此命令的层为止。
	
			public interface ICommandReceiver {
				boolean receiveCommand(int commandId, IContainer params, IContainer result);
			}
			
### Manager业务相关，Service基础操作 ###

- 多个Service可为同一个Manager服务。

- Service例如 NetService（网络请求），StorageService（本地储存），StatisticsService（统计）

- Manager例如UserManager（登录、注册、找回密码管理）、DetectManager（扫描答题卡管理）、PersonManager（一些登录后用户的个人数据管理）

# 最后 #

让搭建的基础设施变成可积累的资产，让逻辑一目了然，让定位问题变成简单。

框架对于不可预期的需求总是不完美的，但追求好的架构可以使代码具有高可维护性、高可读性、高扩展性，使我们更加轻松面对需求的变化和演进。

更多细节，请查阅代码	