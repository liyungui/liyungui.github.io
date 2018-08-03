
---
title: Redux教程
date: 2018-08-01 15:41:20
tags:
	- JS
	- Redux
---

# 介绍 #

## 动机 ##

随着 JavaScript 单页应用开发日趋复杂，JavaScript 需要管理比任何时候都要多的 state(状态)

通过限制更新发生的时间和方式，**Redux 试图让 state 的变化变得可预测**。这些限制条件反映在 Redux 的三大原则中

## 核心概念 ##

Redux核心概念没有任何魔法。两个普通JavaScript对象，一个普通JavaScript函数用来串联两个对象

90% 的代码都是纯 JavaScript，没用 Redux、Redux API 和其它魔法。Redux 里有一些工具来简化这种模式，但是主要的想法是如何根据这些 action 对象来更新 state

### state ###

**普通JavaScript对象，描述状态**

实例：todo 应用的 state

	{
	  todos: [{
	    text: 'Eat food',
	    completed: true
	  }, {
	    text: 'Exercise',
	    completed: false
	  }],
	  visibilityFilter: 'SHOW_COMPLETED'
	}


### action ###

**普通JavaScript对象，描述已发生事件**

- 必须使用一个字符串类型的 `type` 字段来表示将要执行的动作
	- 实际开发中，type 会被定义成**字符串常量**
- 大型应用建议使用单独的模块或文件来存放 action
- **尽量减少在 action 中传递的数据**

实例

	{ type: 'ADD_TODO', text: 'Go to swimming pool' }
	{ type: 'TOGGLE_TODO', index: 1 }
	{ type: 'SET_VISIBILITY_FILTER', filter: 'SHOW_ALL' }

实例

	const ADD_TODO = 'ADD_TODO'

	import { ADD_TODO, REMOVE_TODO } from '../actionTypes'
	{ type: ADD_TODO, text: 'Build my first Redux app' }

#### action 创建函数 ####

生成 action 的方法

	function addTodo(text) {
	  return {
	    type: ADD_TODO,
	    text
	  }
	}

### reducers ###

**普通JavaScript函数，描述action如何改变state**

**接收 state 和 action，并返回新的 state**

**永远保持 reducer 纯净非常重要**。即：**只单纯执行计算。只要传入参数相同，返回计算得到的 state 就一定相同。没有特殊情况、没有副作用，没有 API 请求、没有变量修改。**

- 不修改传入参数；
- 不执行有副作用的操作
	- 如 API 请求和路由跳转；
- 不调用非纯函数
	- 如 Date.now() 或 Math.random()。

**Redux 首次执行时，state 为 undefined，此时我们可借机设置并返回应用的初始 state**

实际开发中，一般编写很多小reducer函数来分别管理 state 的一部分：

	function visibilityFilter(state = 'SHOW_ALL', action) {
	  switch (action.type) {
	    case 'SET_VISIBILITY_FILTER':
	      return action.filter
	    default:
	      return state
	  }
	}

	function todos(state = [], action) {
  		switch (action.type) {
		...
	}

再开发一个 reducer 调用这两个 reducer，进而来管理整个应用的 state：

	const initialState = {
	  visibilityFilter: VisibilityFilters.SHOW_ALL,
	  todos: []
	};

	function todoApp(state = initialState, action) {
	  return {
	    todos: todos(state.todos, action),
	    visibilityFilter: visibilityFilter(state.visibilityFilter, action)
	  };
	}

## 三大原则 ##

### 单一数据源 ###

**单一的 state tree: 整个应用的 state 被储存在一棵 object tree 中，并且这个 object tree 只存在于唯一一个 store 中。**

	store.getState()

### State 是只读的 ###

**唯一改变 state 的方法就是触发 action**

	store.dispatch({
	  type: 'SET_VISIBILITY_FILTER',
	  filter: 'SHOW_COMPLETED'
	})

- 确保了视图和网络请求都不能直接修改 state
	- 视图和网络请求只能表达想要修改的意图
- 所有的修改都被集中化处理，且严格按照一个接一个的顺序执行
- **action是store数据的唯一来源**

### 使用纯函数来执行修改 ###

**编写 reducers 描述 action 如何改变 state tree **

	function visibilityFilter(state = 'SHOW_ALL', action) {
	  switch (action.type) {
	    case 'SET_VISIBILITY_FILTER':
	      return action.filter
	    default:
	      return state
	  }
	}

	function todos(state = [], action) {
  		switch (action.type) {
		...
	}

	import { combineReducers, createStore } from 'redux'
	let reducer = combineReducers({ visibilityFilter, todos })
	let store = createStore(reducer)