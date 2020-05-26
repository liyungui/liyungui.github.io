---
title: 网易UI自动化测试Airtest
date: 2020-04-10 10:25:42
categories: 测试
tags: 测试
---

# Airtest

## 框架概述

2018 GDC 开幕第一天，谷歌发布了一款由网易研发的游戏 UI 自动化测试框架：Airtest Project。
 
谷歌方面表示 Airtest 是安卓游戏开发最强大、最全面的自动测试方案之一

该工具已经应用于网易内部《梦幻西游》手游、《荒野行动》、《阴阳师》等数十个游戏项目中

## 框架结构

Airtest 主要包含了三部分：

- **Airtest**。底层自动化测试框架
	- 基于图像识别
- **Poco**。底层自动化测试框架
	- 基于UI控件搜索
- **Airtest IDE**。跨平台的 UI 自动化测试编辑器
- **AirLab**。真机自动化云测试平台，目前提供了TOP100手机兼容性测试、海外云真机兼容性测试等服务
- **私有化手机集群技术方案**。从硬件到软件，提供了企业内部私有化手机集群的解决方案

## 框架特性

- **基于Python**。可以引入Python库扩展脚本能力
	- 因此写出来的所有脚本都是Python代码
	- 建议在使用前，先学习Python的基础语法知识
	- 通过添加PYTHONPATH设置，可以使用本地的python运行脚本
- **灵活定位控件**。
	- 支持 图像识别 和 UI控件搜索 两种方式定位控件
- **IDE功能完善**，能**快速简单**编写脚本。	
	- 支持 自动化脚本录制、一键回放、报告查看，轻而易举实现自动化测试流程
- 可利用**手机集群**进行**大规模自动化**测试，为游戏与 APP 快速实现兼容性测试

# 快速上手

## 安装

## 连接设备

### 连接Android手机

1. 安卓手机 打开 USB调试
2. IDE -- 右侧 Device Screen -- 点击 refresh ADB
3. 看到设备后，点击对应设备的 Connect 按钮
4. 连接成功，右侧会显示手机屏幕的镜像

## 录制脚本

### 基于Airtest图像识别

1. `Airtest Assistant`窗口 点击 `start recording` 
2. 点击 `Device Screen` 手机镜像 相应位置按钮，自动生成代码
3. 点击 `Run script` 查看效果

```python
# -*- encoding=utf8 -*-
__author__ = "liyungui"

from airtest.core.api import *

auto_setup(__file__) # 自动配置运行环境

touch(Template(r"tpl1586491050046.png", record_pos=(-0.106, -0.708), resolution=(1080.0, 2280.0)))
```

自动录制生成的图标不够精确，还可以点击Airtest辅助窗上的touch按钮，然后在设备窗口上框选精确的图标，也可以自动生成一条touch语句

### 基于Poco控件搜索

#### SDK集成

`Android/iOS`原生应用，是即插即用的，无需接入SDK。

但由于游戏引擎使用OpenGL等图形接口直接渲染，而没有使用原生的UI系统，需要集成SDK与游戏的Runtime进行通信获取整个UI结构

如果使用的引擎或平台不在文档中，同样支持自行扩展SDK。

实际上在网易游戏内部，就是用这种方式支持了`Messiah/NeoX/梦幻`等多个自研引擎


#### 初始化poco

1. `Poco Assistant`窗口 下来选择 对应平台 `Android`
2. 会在手机上安装 `Yosemite` 和 `PocoService`
3. 提示是否要初始化poco，选择是，会自动导入并初始化poco

#### 录制脚本

1. `Poco Assistant`窗口 点击 `poco auto recording` 
2. 点击 `Device Screen` 手机镜像 相应位置按钮，自动生成代码
3. 点击 `Run script` 查看效果

```python
# -*- encoding=utf8 -*-
__author__ = "liyungui"

from airtest.core.api import *

auto_setup(__file__) # 自动配置运行环境

from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
poco("com.zy.course.dev:id/tv_user_name").click()
```

自动录制出的语句不一定能够适应所有场景，采用更合理的选择器编写代码，通常会增强整个自动化脚本的健壮性和可读性

## 执行脚本

运行脚本

## 查看测试报告

脚本运行完毕后，点击查看报告按钮（`快捷键Ctrl+L`），会使用默认浏览器打开结果报告页面。报告中将展示出每一个步骤的内容和实际执行过程的截图、运行结果，方便查看步骤是否执行成功。

这个报告非常直观，点赞！

# `.air`脚本

## 本质：含有`同名.py文件`的文件夹

实际上`.air脚本`文件是一个普通的`文件夹`，里面附带了一个同名的`.py`文件，AirtestIDE在执行脚本时，实际上执行的是里面的`.py`文件

# 图片类Template

`classTemplate(filename, threshold=None, target_pos=5, record_pos=None, resolution=(), rgb=False)`

- **filename**。图片名。IDE截图默认3参数之一
- **record_pos**。截图位置。IDE截图默认3参数之一
	- 优先在录制时的位置附近查找
	- 如果找不到符合条件的图片，再扩大寻找范围到整个画面。
	- 这样能够提升查找图片的速度和精确度
- **resolution**。截图屏幕分辨率。IDE截图默认3参数之一
	- 在不同分辨率设备上进行缩放
		- 默认使用Cocos引擎的缩放规则
			- [Cocos引擎的缩放规则](http://docs.cocos.com/creator/manual/zh/ui/multi-resolution.html)
			- [代码](https://github.com/AirtestProject/Airtest/blob/73618beb07acf5c6b9b9704575a6bd1561c7c2db/airtest/utils/resolution.py#L11)
	- 方便图片的跨分辨率匹配
- **threshold**。图像识别阈值
	- 取值范围为[0, 1]，默认值是0.7
	- 建议阈值设定在[0.6, 0.9]之间
		- 过低混入错误结果
		- 过高导致经常找不到
	- 与图像识别的成功率息息相关
	- 可信度大于阈值时才会返回识别结果
- **rgb**。是否灰度识别还是彩色识别
- **target_pos**。点击位置
	- 将图片划分为三横三列[1, 9]，默认值是5(图片正中间)

后面三个参数可以单独配置，也可以脚本全局配置

**血泪经验：只用来识别图标**。不同设备环境的字体效果实在太多惊喜！

## 图像识别阈值

官方强烈推荐使用“图片编辑器”修改阈值。

【注意】实际开发过程中，发现图像编辑器识别结果的区域和置信区间仅供参考，很多时候是不准的。定位问题以测试报告为准

1. 在脚本框中双击图片打开“图片编辑器”
2. 点击` Snapshot + Recognition` 按钮来实时验证识别结果。
3. 识别结果的可信度会直接呈现在下方状态栏上，可信度大于阈值时才会返回识别结果

## 图像匹配过程日志

我们可以通过日志分析图像匹配的完整过程

```
[05:10:15][INFO]<airtest.core.api> Try finding:
渲染后的图片 Template(/Users/liyungui/StudioProjects/course_auto_test/test_single.air/tpl1581872345150.png)
[05:10:15][DEBUG]<airtest.core.api> resize: (100, 47)->(100, 47), resolution: (2160.0, 1080.0)=>(2280, 1080)
[05:10:15][DEBUG]<airtest.core.api> try match with SURFMatching
[05:10:17][DEBUG]<airtest.aircv.keypoint_base> [SURF] threshold=0.7, result={'result': [281, 205], 'rectangle': [(226, 180), (226, 229), (336, 229), (336, 180)], 'confidence': 0.8972115218639374}
[05:10:17][DEBUG]<airtest.aircv.keypoint_base> find_best_result() run time is 2.02 s.
[05:10:17][DEBUG]<airtest.core.api> match result: {'result': [281, 205], 'rectangle': [(226, 180), (226, 229), (336, 229), (336, 180)], 'confidence': 0.8972115218639374}
```

**日志完整展示了图像匹配的6个过程**

- resize：缩放截图尺寸
	- `(100, 47)->(100, 47)`。
	- 示例中屏幕分辨率变化不大，所以是原尺寸，即1倍
- resolution：缩放屏幕尺寸
	- `(2160.0, 1080.0)=>(2280, 1080)`
	- 示例中屏幕分辨率变化不大
- try match with SURFMatching 使用SURF算法匹配图片
- [SURF] 找到一个匹配结果(阈值，点击区域，图片区域，置信区间)
	- threshold=0.7 阈值
	- result= 结果
		- {'result': [281, 205], 
		- 'rectangle': [(226, 180), (226, 229), (336, 229), (336, 180)], 
		- 'confidence': 0.8972115218639374}
- `find_best_result` 挑一个最匹配的结果
- match result 最终的匹配结果

# [如何生产兼容性强的脚本](https://airtest.doc.io.netease.com/tutorial/9_Improved_compatibility/)

## 如何选择Airtest/Poco

**结论：Poco优先，图像脚本辅助(比如游戏暂时没有集成SDK)。**

因为poco性能和兼容性更强，而且Poco能获取属性值，测试更加灵活

截图脚本在更换一台不同分辨率的手机/更换一个环境之后，就经常遇到执行失败

这个缺陷是由于图片类Template设计导致的

GitHub上开发成员对这个[issues](https://github.com/AirtestProject/Airtest/issues/4)也是建议换poco

# Airtest模拟输入

- touch 触摸。可设置 位置、次数、时长等参数
- swipe 滑动
- text  输入内容
- keyevent 按键(回车、删除)
- snapshot 截图
- wait 等待图片元素出现
- sleep 睡眠一段时间

# Airtest断言

- `assert_exists` 断言图片存在
- `assert_not_exists` 断言图片不存在
- `assert_equal` 断言值相等
- `assert_not_equal` 断言值不相等

只有Poco才能获取属性值

# Poco UI属性

UI对象常见的属性值

```
type :  android.widget.TextView 
name :  com.zy.course.dev:id/tv_title 
text :  关于我们 
enabled :  True 
visible :  True 
resourceId :  b'com.zy.course.dev:id/tv_title' 
zOrders :  {'global': 0, 'local': 2} 
package :  b'com.zy.course.dev' 
anchorPoint :  [0.5, 0.5] 
dismissable :  False 
checkable :  False 
scale :  [1, 1] 
boundsInParent :  [0.17777777777777778, 0.02850877192982456] 
focusable :  False 
touchable :  False 
longClickable :  False 
size :  [0.17777777777777778, 0.02850877192982456] 
pos :  [0.2388888888888889, 0.48333333333333334] 
focused :  False 
checked :  False 
editalbe :  False 
selected :  False 
scrollable :  False 
```

## name

- 有id：包名:id/id值
- 无id：同view的type

## touchable

是否可以触摸。可以用来判断view是否可点击

# Poco选择UI

## 基本选择器(Basic Selector)

通过**节点属性**来选择 **可见UI**

- poco实例后加一对括号
- 遍历，将满足条件的所有UI返回

### `__call__`

```python
class Poco(agent, **options):
	def __call__(name=None, **kw)
```

- 只能选择可见UI。即使设置visible=False也无法返回不可见UI
- 查找UI是懒执行(只有使用该UI时才查找)
- kw支持两种模式，任选其一(两种模式不能同时生效)
	- 属性名='期望值'。`text='关于我们'`
	- 属性名Matches='期望值正则表达式'。`textMatches='^关于.*$'`
- 返回值是 UI对象的代理 UIObjectProxy

### 实例

TextView 的 id不唯一

```python
poco(text='关于我们')
poco(textMatches='^关于.*$')
```

## 相对选择器(Relative Selector)

直接用节点属性没法选出你所想要的UI时，还可以通过UI之间的渲染**层级关系**进行选择

### 子类`child`

```python
class UIObjectProxy(poco, name=None, **attrs):
	def child(name=None, **attrs)
```

### 后代`offspring`

```python
class UIObjectProxy(poco, name=None, **attrs):
	def offspring(name=None, **attrs)
```

### 所有子类`children()`

### 实例

```python
poco('com.zy.course.dev:id/item_about').child('com.zy.course.dev:id/tv_title')
```

## 空间顺序选择器(Sequence Selector)

按照空间排布顺序来选择

- 从上到下，从左往右，索引从0开始
- 一旦选择，UI位置发生变化，索引值不变，消失(移除或者隐藏)的UI不能再访问

## 坐标系

- 从左往右。x轴，0到1
- 从上到下。y轴，0到1

### 实例

```python
poco('com.zy.course.dev:id/tv_title')[0]
```

# Poco等待

```python
class UIObjectProxy(poco, name=None, **attrs):
	def wait(timeout=3) 等待UI出现，单位秒。
		返回UI对象的代理 UIObjectProxy
	wait_for_appearance(timeout=120)等待UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
	wait_for_disappearance(timeout=120)等待UI消失，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
```

```python
class UIObjectProxy(poco, name=None, **attrs):
	wait_for_all(objects, timeout=120)等待所有UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		无返回值
	wait_for_any(objects, timeout=120)等待任一UI出现，单位秒；
		超时抛异常PocoTargetTimeout。
		返回第一个出现的UI对象的代理 UIObjectProxy
```

# Poco操作UI

```
exists 验证UI可见
focus 设置焦点的局部坐标(0到1)
click/long_click 默认点击UI正中，也可以指定局部坐标(0到1)
	click()
	click('center')
	click([0.5,0.5])
	focus([0.5,0.5]).click()
swipe 滑动
	swipe('up')
	swipe([0.2, -0.2])
	swipe([0.2, -0.2], duration=0.5)
drag_to 拖拽UI到UI
	drag_to(poco(text='岩石司康饼'))	
```

# Poco操作UI属性

- 直接访问属性名
- get方法。`get_text()`
- set方法。`set_text('hello')`

# Poco如何支持WebView检视

Poco对WebView的检视的支持程度，主要取决于WebView本身的兼容性情况，目前兼容性最好的WebView方案是Android系统自带内核 `Google-WebView`

Android设备设置可以设置浏览器使用系统内核自带的WebView

微信/QQ上的 `X5 WebView` 内核也支持使用系统内核。打开调试页面，将最下方的的 `强制使用系统内核` 打开，并且 `清除TBS内核` ，做完之后重启微信/QQ。 再进入这个页面，点击 `查看版本信息` 。如果版本信息为 `0(null)` 则设置成功。

# 命令行运行脚本--部署本地Python环境

使用AirtestIDE命令行来运行脚本，虽然很方便，但是不适合更复杂的操作（例如想同时用多个命令行运行多台手机、多个脚本等情况），以及对于一些Python开发者来说，可能需要在脚本中使用其他功能强大的Python第三方库。

因此我们更加推荐在本地python环境中安装airtest和pocoui，然后用命令行运行脚本。

## Python版本选择

支持Python(**2.7或<=3.6**)，我们更推荐使用 Python3 ，如果你愿意的话我们也同样建议使用 virtualenv 等虚拟环境新建一个干净的python环境

如果使用了python3.7，找图框架依赖的opencv模块需要 [安装 Visual C++ redistributable 2015](https://pypi.org/project/opencv-contrib-python/)

## Airtest和Poco安装

`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple airtest` python3 要用 pip3 来安装


`pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pocoui`

注意：`-i https://pypi.tuna.tsinghua.edu.cn/simple` 是清华镜像站，解决被墙问题，5分钟同步一次

## 赋予adb可执行权限

在Mac/Linux系统下，需要手动赋予adb可执行权限，否则可能在执行脚本时遇到 Permission denied 的报错:

```
# mac系统
> cd /usr/local/lib/python3.7/site-packages/airtest/core/android/static/adb/mac
# linux系统
> cd {your_python_path}/site-packages/airtest/core/android/static/adb/linux
> chmod +x adb
```

## Airtest脚手架

`airtest/cli/__main__.py`

支持 Airtest 所有命令，包括 `run，report，info`等

## 运行脚本

下面两个命令效果相同

```
>airtest run untitled.air --device Android:///手机设备号 --log log目录
>python -m airtest run untitled.air --device Android:///手机设备号 --log log目录
```

`airtest.cli.runner`负责运行脚本

```
--log参数 没有指定，将不保存log内容和截图
--log log, log内容放到当前命令行的执行目录/log
```

# 测试报告

`airtest.report.report.py`负责生成测试报告

## 使用命令行来生成报告

脚本运行过程，与报告生成过程是独立的两个步骤


```shell
airtest run untitled.air --log log
airtest report untitled.air --lang zh --export log_out --plugin poco.utils.airtest.report
```

```
--log_root LOG_ROOT   log & screen data root dir, 默认值是 测试用例脚本目录(untitled.air)/log
```

## 使用PYTHON代码生成报告

### 调用`simple_report`生成报告

```python
from airtest.report.report import simple_report

# 自动配置运行环境;
# logdir=True会在脚本目录下生成log文件夹(log.txt和步骤截屏)
auto_setup(__file__, logdir=True)  

try:
    main()
finally:
    # generate html report
    # 在脚本目录下生成log.html
    simple_report(__file__, logpath=True) 
```

缺陷：无法指定一系列参数(如增加poco语法支持插件)

### 调用airtest运行脚本和生成报告

```python
import os

os.system("airtest run multitest.air --device Android://127.0.0.1:5037/37KRX18A25012338 --log log")
os.system("airtest report multitest.air --lang zh --export log_out --plugin poco.utils.airtest.report")
```

# 参考&扩展

- [官网](http://airtest.netease.com/)
- [文档](https://airtest.doc.io.netease.com/)
- [源码](https://github.com/AirtestProject/Airtest)
- [Poco如何支持WebView检视](http://airtest.netease.com/docs/cn/6_poco_framework/poco_webview.html)
- [如何生成报告](https://airtest.doc.io.netease.com/IDEdocs/about_report/Report_guidelines/#_11)

