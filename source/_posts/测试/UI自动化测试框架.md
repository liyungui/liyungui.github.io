---
title: UI自动化测试框架
date: 2020-04-10 10:25:42
categories: 测试
tags: 测试
---

# 自动化测试

自动化测试听起来很神秘，学起来很简单，用起来很麻烦

# 框架选型

**手机原生APP**：跨平台用的最多的Appium，纯安卓的可以用Robotium。

**WEB**：selenium，Katalon(支持POM、录制)

**游戏**：网易Airtest，可以让你像测原生APP一样测试游戏。腾讯也有一款相同的产品：GAutomator。Airtest现在的优势还是Poco框架控件定位(Poco性能和兼容性强，而且Poco能获取属性值，测试更加灵活；而Airtest框架找图太不专业，换个分辨率就不行了)
