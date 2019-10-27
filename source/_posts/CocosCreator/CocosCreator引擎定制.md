---
title: CocosCreator引擎定制
date: 2019-10-17 14:30:53
tags: 
	- CocosCreator
categories:
	- 游戏
---

# Cocos Creator 引擎结构

引擎部分包括三个部分，全部都在 github 上开源

- **JavaScript**。 纯 JavaScript 层逻辑（如 UI 系统，动画系统）
- **Cocos2d-x-lite**。 原生平台相关的引擎功能
- **adapter**。 JavaScript 层适配以实现跨平台，包括：适配不同平台的BOM 和 DOM 等运行环境；引擎层面的适配
	- jsb-adapter。 适配原生平台
		- builtin。 适配原生平台的 runtime。包括：BOM 和 DOM 运行环境；相关的 jsb 接口，如 openGL, audioEngine 等
		- engine。 适配引擎层面的一些 api
	- weapp-adapter。 适配微信小游戏
	- qqplay-adapter。 适配 qq 玩一玩

## JSB 绑定

如果您需要修改 Cocos2d-x-lite 引擎提供的 JavaScript 接口，应该完成 JSB 绑定

# 参考&扩展

- [引擎定制工作流程](https://docs.cocos.com/creator/manual/zh/advanced-topics/engine-customization.html)