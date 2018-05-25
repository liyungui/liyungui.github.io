---
title: AndroidManifest合并原理
date: 2018-05-24 18:44:53
tags: Android
---

[ss](http://mouxuejie.com/blog/2016-02-05/androidmanifest-merge/)

[啊啊](https://developer.android.com/studio/build/manifest-merge?hl=zh-cn)

APK 只能包含一个 AndroidManifest.xml 文件，但 Android Studio 项目可以包含多个文件（通过主源集、构建变体和导入的库提供）。因此，在构建应用时，Gradle 构建会将所有清单文件合并到一个清单文件中。

清单合并工具通过遵循某些**合并冲突启发式算法**，和 **合并首选项**(通过特殊 XML 属性定义)，来合并各个文件中的所有 XML 元素 。

# 合并优先级 #

**从优先级最低的文件合并至优先级最高的文件**

{% asset_img manifest-merger_priority.png %}

## 库清单文件 ##

多个库，则其清单优先级与依赖顺序（库出现在 Gradle dependencies 块中的顺序，由高到低）匹配

## 构建变体 ##

变体有多个源集，则其清单优先级如下(由高到低)：

- 构建变体清单（如 src/demoDebug/）
- 构建类型清单（如 src/debug/）
- 产品定制清单（如 src/demo/）

如果使用的是定制维度，清单优先级将与每个维度在 flavorDimensions 属性中的列示顺序(由高到低)对应。

# 合并冲突启发式算法 #

## 默认合并规则 ##

{% asset_img merge.png %}

### 编码原则：不依赖于默认属性值 ###

高优先级清单实际上依赖于属性的默认值而不需要声明，则可能会导致意外结果。

例如，高优先级清单不声明android:launchMode 属性，则会使用 "standard" 的默认值；但如果低优先级清单声明此属性具有其他值，该值将应用于合并清单（替代默认值）。因此，您应该按期望明确定义每个属性。（每个属性的默认值都会记录在 [Manifest reference](https://developer.android.com/guide/topics/manifest/manifest-intro?hl=zh-cn) 中）。

## 合并工具为减少合并冲突的特殊规则 ##

- `<manifest>`元素的属性绝不合并—仅使用优先级最高的清单中的属性。
- `<uses-feature>`元素 `<uses-library> `元素`android:required`属性 使用 **OR** 合并，因此如果出现冲突，系统将应用 "true" 并始终包括某个清单所需的功能或库。
- `<uses-sdk>`元素始终使用较高优先级的清单中的值，但以下情况有些特殊：
	- minSdkVersion，低优先级清单的值 较高
		- 默认，使用 低优先级清单的值
		- 应用 overrideLibrary 合并规则，使用 较高优先级的清单中的值
	- targetSdkVersion，低优先级清单的值 较低
		- 合并工具将使用高优先级清单中的值
		- 但也会添加任何必要的系统权限，以确保所导入的库继续正常工作
			- 适用于 较高的 Android 版本需要更多权限限制的情况。 如需了解有关此行为的详细信息，请参阅有关隐式系统权限的部分。
- `<intent-filter>`元素。 每个元素都被视为唯一元素，直接添加至合并清单中的常用父元素。

# 合并规则标记 #

- 是什么：是一个 XML 属性
- 作用：标记如何解决合并冲突和属性的首选项
- 作用域：整个元素或元素的特定属性
- 合并工具会在高优先级清单文件中寻找这些标记
- 所有标记均属于 Android `tools` 命名空间，必须先在 `<manifest>`元素中声明此命名空间

## 元素/节点标记 ##

**tools:node="xx"**

- **merge** 
	- 元素的默认行为
	- 合并所有属性以及所有嵌套元素。 例如：`<activity>` 嵌套 `<intent-filter>`
- **merge-only-attributes**
	- 仅合并属性，不合并嵌套元素
- **remove**