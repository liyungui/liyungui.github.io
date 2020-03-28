---
title: Android热修复技术选型
date: 2019-08-12 17:18:53
categories:
  - Android
tags:
  - Android
---

# 背景

目前Android业内，热修复技术百花齐放，各大厂都推出了自己的热修复方案，使用的技术方案也各有所异，当然各个方案也都存在各自的局限性。在面对众多的方案，希望通过梳理这些热修复方案的对比及实现原理，掌握热修复技术的本质，同时也对项目接入做好准备。

推荐 阿里《深入探索Android热修复技术原理》一书

# 什么是热修复技术？

简单来说，就是通过下发补丁包，让已安装的客户端动态更新，让用户可以不用重新安装APP，就能够修复软件缺陷的一种技术。

## 修复什么

- 代码修复
- 资源修复
- SO库修复

# 怎么选择热修复技术方案？

## 国内主流的技术方案

||Sophix 阿里|Tinker 腾讯微信|nuwa 大众|AndFix 阿里支付宝|Robust 美团|Amigo 饿了么|
|---|---|---|---|---|---|---|
|类替换|yes|yes|yes|no|no|yes|
|So替换|yes|yes|no|no|no|yes|
|资源替换|yes|yes|yes|no|no|yes|
|全平台支持|yes|yes|yes|no|yes|yes|
|即时生效| yes |no|no|yes|yes|no|
|性能损耗|较少|较小|较大|较小|较小|较小|
|接入复杂度|傻瓜式接入|复杂|较低|复杂|复杂|较低|
|开发透明|yes|yes|yes|no|no|yes|
|侵入式打包|无侵入|依赖侵入式|依赖侵入式|依赖侵入式|依赖侵入式|依赖侵入式|
|补丁包大小|小|较小|较大|一般|一般|较大|
|Rom体积|较小|Dalvik较大|较小|较小|较小|大|
|成功率|高|较高|较高|一般|最高|较高|
|热度|高|高|低|低|高|低|
|开源|no|yes|yes|yes|yes|yes|
|收费|收费（设有免费阈值）|收费（基础版免费，但有限制）|免费|免费|免费|免费|
|监控|提供分发控制及监控|提供分发控制及监控|no|no|no|no|

## Tinker

dex合成替换

### 优点
- 开源
- 补丁包小
- 功能全面

### 缺点
#### 接入复杂
目前最快捷的集成方式是 集成 bugly 升级sdk。

需要的工作

- 代理 Application
- 接入 tinker-support 插件
- 编写tinker gradle 脚本

#### 打包复杂
每次打包需要修改tinker gradle 脚本的配置

#### 补丁激活成功率低
测试下来发现激活成功率 大概 60%
#### 补丁合成dex性能消耗大

主流配置的机器，平均合成时间 1800秒

### 价格
基础版 免费：最大补丁大小:500k  日请求量 <1万

专业版 399 - 2899元/月

## Sophix

### 优点
- 补丁即时生效，不需要应用重启；
- 补丁包同样采用差量技术，生成的PATCH体积小；
- 对应用无侵入，几乎无性能损耗；
- 两行代码，傻瓜式接入。

### 价格

免费阈值：月活设备(MAU): 5万。

每个月，每台设备收费0.015元。

计费周期：系统每日生成账单，进行结算。当月收取过的，不再进行收费。即只计算日增量设备

## Robust
java hook 插桩

### 优点
- 无差别兼容Android2.3-8.0版本；
- 无需重启补丁实时生效，
- 补丁修补成功率高达99.9%(所有热修复方案中成功率最高的）

### 缺点
- 只支持方法级别的Bug修复，不支持资源及so
- bug修复通过java hook 代码实现
- 补丁的下发和合并等需要自己实现

## 总结

如果考虑付费，推荐选择阿里的Sophix，Sophix是综合优化的产物，功能完善、开发简单透明、提供分发及监控管理。

如果不考虑付费，只需支持方法级别的Bug修复，不支持资源及so，推荐使用Robust。补丁修补成功率高达99.9%(所有热修复方案中成功率最高的）

如果考虑需要同时支持资源及so，使用Tinker。不建议使用，因为实现原理是 dex合成后替换，dex合成成功率不高(60%)

如果公司综合实力强，可考虑自研，灵活性及可控制最强。

从Github上的热度及提交记录上看，nuwa、AndFix、Amigo等的提交都是2 years ago。

# 热修复技术方案原理

{% asset_img 热修复原理.png %}

# 代码热修复方案的两个方向

**native hook和类加载(插入dex/替换dex)**

类加载有两种实现，所以又称三大流派

美团 Robust 这种 java方法插桩hook的，只能实现代码修复，无法实现资源和so修复；所以不在常规讨论范围内。

# native hook方案

## 阿里手淘Dexposed和支付宝Andfix

- 基于Xposed框架改进，AOP实现对Java的hook
- 定位：紧急bug修复（不重启即时生效）
- 核心：在native层将虚拟机中的旧方法替换为新方法
	- 
- 优点：
	- 即时生效
	- 没有插桩或代码改写，对正常运行不引入任何性能开销
	- 对所改写方法的性能开销也极低（微秒级），基本可以忽略不计；
	- 能hook同进程的所有Java代码（包括Android SDK）
- 缺点：
	- Dexposed不支持ART（4.4以上不能用）
	- 不支持新增方法，新增类，新增field等
		- 类已经被加载，内存中方法描述符(结构体)已经固定
	- 最大挑战：稳定性与兼容性。
		- 实践发现**修复成功率非常低** ，时常出现崩溃，补丁无效的现象
	- native异常排查困难	 
	
```java
private static native void replaceMethod(Method dest, Method src);
```

replaceMethod在dalvik和art（art每个版本都不同）上的调用不同，native hook这种解决方案兼容性差的问题在这里则体现得特别明显。但是原理类似，这里我们以6.0为例art_method_replace_6_0：

```cpp
void replace_6_0(JNIEnv* env, jobject src, jobject dest) {
  //通过Method对象得到底层Java函数对应ArtMethod的真实地址
    art::mirror::ArtMethod* smeth = (art::mirror::ArtMethod*) env->FromReflectedMethod(src);
    art::mirror::ArtMethod* dmeth = (art::mirror::ArtMethod*) env->FromReflectedMethod(dest);

    dmeth->declaring_class_->class_loader_ =
            smeth->declaring_class_->class_loader_; //for plugin classloader
    dmeth->declaring_class_->clinit_thread_id_ =
            smeth->declaring_class_->clinit_thread_id_;
    dmeth->declaring_class_->status_ = smeth->declaring_class_->status_-1;

  // 把原方法的各种属性都改成补丁方法的
    smeth->declaring_class_ = dmeth->declaring_class_;
    smeth->dex_cache_resolved_types_ = dmeth->dex_cache_resolved_types_;
    smeth->access_flags_ = dmeth->access_flags_;
    smeth->dex_cache_resolved_methods_ = dmeth->dex_cache_resolved_methods_;
    smeth->dex_code_item_offset_ = dmeth->dex_code_item_offset_;
    smeth->method_index_ = dmeth->method_index_;
    smeth->dex_method_index_ = dmeth->dex_method_index_;

  // 实现的指针也替换为新的
    smeth->ptr_sized_fields_.entry_point_from_interpreter_ =
            dmeth->ptr_sized_fields_.entry_point_from_interpreter_;
    smeth->ptr_sized_fields_.entry_point_from_jni_ =
            dmeth->ptr_sized_fields_.entry_point_from_jni_;
    smeth->ptr_sized_fields_.entry_point_from_quick_compiled_code_ =
            dmeth->ptr_sized_fields_.entry_point_from_quick_compiled_code_;

    LOGD("replace_6_0: %d , %d",
            smeth->ptr_sized_fields_.entry_point_from_quick_compiled_code_,
            dmeth->ptr_sized_fields_.entry_point_from_quick_compiled_code_);
}

// 把方法都改成public
void setFieldFlag_6_0(JNIEnv* env, jobject field) {
    art::mirror::ArtField* artField =
            (art::mirror::ArtField*) env->FromReflectedField(field);
    artField->access_flags_ = artField->access_flags_ & (~0x0002) | 0x0001;
    LOGD("setFieldFlag_6_0: %d ", artField->access_flags_);
}
```

在dalvik上的实现略有不同，是通过jni bridge来指向补丁的方法。

## 兼容问题的根源

Native层对方法的替换，都是以Android官方源码的结构定义为标准，很多手机ROM厂商是会修改这些结构的

## 阿里百川hotfix

{% asset_img hotfix.png %}

# dex插入

## 腾讯QQ空间和大众Nuwa

- 基于multidex（安卓分包方）Hook ClassLoader.pathList.dexElements[]
	- 一个ClassLoader可以包含多个dex文件
	- 每个dex文件是一个Element
	- 多个dex文件排列成一个有序的数组dexElements
	- 按dex顺序查找类，找到则返回
- 核心：将修复类打包成dex，插入到dexElements最前面

{% asset_img dex插入.png %}


## `CLASS_ISPREVERIFIED`

为了提供性能，apk安装期间Dalvik会为已验证的类打上`CLASS_ISPREVERIFIED`

Vm的判定规则：“当一个类中引用了另外一个类，则一般要求两个类来自同一个Dex文件”。

`CLASS_ISPREVERIFIED` 是触发Vm判定规则的前提。

{% asset_img VM规则判断.png %}

增量方案为解决这个问题，需要进行“打桩”。

打桩的目的就是防止类被打上 `CLASS_ISPREVERIFIED` 标签。

打桩，就是在所有类中分别引用另外一个独立Dex文件(为了打桩特意封装的)中的类。通常做法是在每一个类中增加构造器并引用另外一个dex中的类。

在类加载的最后阶段，虚拟机会对未打上 `CLASS_ISPREVERIFIED` 标签的类 再次进行 **校验和优化** ，如果在同一时间点加载大量类，那么就会出现严重的性能问题，如启动时白屏。

## 优点

- 不需要考虑对dalvik虚拟机和art虚拟机做适配
- 代码是非侵入式的，对apk体积影响不大

## 缺点

- 需要下次启动才修复
- 最大挑战：**性能损耗大**
	- Dalvik平台为了避免类被加上 `CLASS_ISPREVERIFIED`，使用插桩，单独放一个帮助类在独立的dex中让其他类调用。可能导致严重的性能问题，如启动时白屏。
	- Art平台可能地址错乱

# dex替换

## 微信Tinker

- 基于Instant Run
	- 全量替换dex 
- 核心：合并补丁包生成全量新dex
- 优点：
	- 微信自研DexDiff/DexMerge算法，补丁包最小化
	- 避免dalvik 插桩带来的性能损耗和art地址错乱问题
- 缺点：
	- 需要下次启动生效
	- 性能痛点
		- Dex合并内存消耗在vm head上，容易OOM，最后导致合并失败 
		- 如果本身app占用内存已经比较高，容易导致app被系统杀掉
		- 补丁影响启动时间。大补丁合并很耗时
- 已知问题：
	- 不支持部分三星android-21机型，加载补丁时会主动抛出"TinkerRuntimeException:checkDexInstall failed"；
	- 对于资源替换，不支持修改remoteView。例如transition动画，notification icon以及桌面图标。

{% asset_img dex替换.png %}

# 两种方案总结

底层替换存在不同定制Rom的**兼容性**问题，同时**不能做新增field**的修复，但修复**立即生效**。

类加载方案在合成全量补丁的时候存在**性能问题**，修复需要**重启**应用(冷启动)，但是**兼容性较好**。

# Sophix 代码热修复-双剑合璧

Sophix对类文件修复 采用底层替换方案为主，类加载方案为次(兜底策略)的模式，将二者结合起来，并对二者另辟蹊径，加以突破。

## 基于底层替换方案的突破

底层替换方案通过在运行时利用hook操作native指针实现“热”的特性。但这里有一个关键点，底层替换所操作的指针，实际上是 `ArtMethod` 。

在类被加载，类中的每个方法都会有对应的ArtMethod，它记录了**方法包括所属类和内存地址信息**

Andfix正是通过篡改ArtMethod，将补丁方法ArtMethod的成员值逐一赋给旧方法，实现替换。

问题就出现在 **逐一替换** 上。因为Andfix的 `ArtMethod` 方法结构是根据Android开源代码写死的，面对国内厂商的定制，经常会导致两者ArtMethod方法结构不一致，这也是兼容问题产生的根本原因。

为了解决这个问题，Sophix采用了对旧ArtMethod进行 **完整替换**。

通过动态测量ArtMethod的size（通过c层的mempy(dest ,src ,size)方法），进行全量拷贝。这样做无论ArtMethod被修改成什么样，只需要统一执行拷贝，就可以完成替换，完全无视修改虚拟机导致的ArtMethod结构差异。

## 另辟蹊径的冷启动修复

底层替换虽能使修复即时生效，但由于类加载后，**方法结构已固定**，这就造成使用上会有诸多限制。

相反类加载方案的使用场景更为广泛。

Sophix使用类加载作为兜底方案。在热部署无法使用的情况下，自动降级为冷部署方案。

无论是冷部署还是热部署，都需要通过同一套补丁兼顾。

### Art虚拟机

在Art虚拟机下，默认支持多dex加载，虚拟机会优先加载命名为classes.dex的文件。

Sophix利用了这一点，将补丁文件命名为classes.dex，并对原有dex文件进行排序。这样一来，art虚拟机就会先加载补丁文件，后续加载的同类名的类会被忽略，最后将加载得到的dexFile把dexElements整体替换。

{% asset_img sophix-art.png %}

### Dalvik虚拟机

Dalvik默认只加载classes.dex，其他dex则被忽略。

Sophix就需要一个全量dex。

tinker采用自主研发的dexDiff技术，从方法和指令的维度进行dex**合成**，但Dex合成过程发生在虚拟机堆内存上，修复的成功率极大的受到性能问题的影响。

为了解决这个问题，Sophix换了一种思路，从类的维度，对照补丁包中出现的类，在原有包中做**删除**操作。为了避免删除整个类信息而导致dex结构发生偏移，所以只对旧包中类的入口进行删除，实际上类的信息还在dex包中。这样一来，冷启动后，原有的类就不会被加载，相比Tinker的合成方案，Sophix的思路更为**轻量化**。              
{% asset_img sophix-dalvik.png %}
        
# 总结

至此，Sophix对类文件修复的基本原理描述完毕。

可以说Sophix吸取了百家之长，对问题的解决之法堪称巧妙，展现出底层技术的重要性，若没有对虚拟机等底层技术的深耕探索，在系统框架的纷繁规则面前，也只能至于庭前止步。

# 参考&扩展

- [Android热修复技术，你会怎么选？](https://www.jianshu.com/p/6ae1e09ebbf5)
- [Android热修复技术原理详解](https://www.cnblogs.com/popfisher/p/8543973.html)
- [最全面的Android热修复技术——Tinker、nuwa、AndFix、Dexposed](https://www.cnblogs.com/aademeng/articles/6883861.html)
- [两种热修复方案及Sophix原理](https://www.jianshu.com/p/853dae4092d7)
- [Android热修复技术选型——三大流派解析](http://mp.weixin.qq.com/s/uY5N_PSny7_CHOgUA99UjA?spm=a2c4g.11186623.2.13.16023a3cQhCyHh)
- [为什么使用 Tinker？](http://www.tinkerpatch.com/Docs/intro)
- [Sophix产品优势](https://help.aliyun.com/document_detail/51416.html?spm=a2c4g.11186623.6.543.6ed62ef2MAnXZM)
- [Tinker 价格](http://www.tinkerpatch.com/Price)
- [Sophix 价格](https://help.aliyun.com/document_detail/57064.html?spm=a2c4g.11186623.3.2.7c44140cp41XQl)
