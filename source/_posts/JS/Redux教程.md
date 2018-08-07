
---
title: Redux教程
date: 2018-08-01 15:41:20
tags:
	- JS
	- Redux
---

# 基础使用 #

## 动机 ##

### 让 state的变化变得可预测 ###

随着 JavaScript 单页应用开发日趋复杂，JavaScript 需要管理比任何时候都要多的 state(状态)

通过限制更新发生的时间和方式(三大原则)，让 state的变化变得可预测。

### 易于测试 ###

- 不需要模拟任何东西，因为它们都是纯函数。
- 只需**dispatch(action)，断言state变化**，写测试就是这么简单

## 核心概念 ##

Redux核心概念没有任何魔法。两个普通JavaScript对象，一个普通JavaScript函数用来串联两个对象

90% 的代码都是纯 JavaScript，没用 Redux、Redux API 和其它魔法。Redux 里有一些工具来简化这种模式，但是主要的想法是如何根据这些 action 对象来更新 state

### state ###

**普通JavaScript对象，描述状态**

实例：todo 应用的 state

	{
	  todos: [{
		id: 1
	    text: 'Eat food',
	    completed: true
	  }, {
		id: 2
	    text: 'Exercise',
	    completed: false
	  }],
	  visibilityFilter: 'SHOW_COMPLETED'
	}
		visibilityFilter取值：SHOW_ALL,SHOW_ACTIVE
		
### action ###

**普通JavaScript对象，描述已发生事件**

- 必须使用一个字符串类型的 `type` 字段来表示将要执行的动作
	- 实际开发中，type 会被定义成**字符串常量**
- 大型应用建议使用单独的模块或文件来存放 action
- **尽量减少在 action 中传递的数据**

实例

	{ type: 'ADD_TODO', text: 'Go to swimming pool' }
	{ type: 'TOGGLE_TODO', id: 1 }
	{ type: 'SET_VISIBILITY_FILTER', filter: 'SHOW_ALL' }

实例

	const ADD_TODO = 'ADD_TODO'

	import { ADD_TODO, REMOVE_TODO } from '../actionTypes'
	{ type: ADD_TODO, text: 'Build my first Redux app' }

#### action 创建函数 ####

生成 action 的方法

	let nextTodoId = 0
	export const addTodo = text => ({
	  type: 'ADD_TODO',
	  id: nextTodoId++,
	  text
	})

### reducers ###

**普通JavaScript函数，描述action如何改变state**

**接收 state 和 action，并返回新的 state**

**是纯函数**。保持 reducer 纯净非常重要，只单纯执行计算

- **相同的输入必须产生相同的输出**
	- 只要传入参数相同，每次返回计算得到的 state 就一定相同
- **不修改传入参数**
- 不执行有副作用的操作
	- 如 API 请求和路由跳转；
		- 这些应该在 dispatch action 前发生
- **不调用非纯函数**
	- 如 Date.now() 或 Math.random()。不能保证每次输出一致

**Redux 首次执行时，state 为 undefined，此时我们可借机设置并返回应用的初始 state**

#### 根reducer ####

- 调用你的一系列 reducer
- 每个 reducer 处理 根据 key 筛选出 state 中的那部分数据
- 将所有 reducer 的结果合并成一个大的对象 返回

实际开发中，一般编写很多小reducer函数来分别管理 state 的一部分，再开发一个 根reducer 调用这些 reducer，实现管理整个应用的 state

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
		    case 'ADD_TODO':
		      return [
		        ...state,
		        {
		          id: action.id,
		          text: action.text,
		          completed: false
		        }
		      ]
		    case 'TOGGLE_TODO':
		      return state.map(todo =>
		        (todo.id === action.id)
		          ? {...todo, completed: !todo.completed}
		          : todo
		      )
		    default:
		      return state
		  }
	}

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

#### combineReducers(reducers) ####

**生成一个根reducer函数**

完全等价上面的todoApp()。

	import { combineReducers } from 'redux'
	const todoApp = combineReducers({
	  visibilityFilter,
	  todos
	})
		使用了简写，因为键值对同名，省略key

##### 最简洁写法 #####

**不推荐**。会造成 reducer 爆炸，而且不合符开闭原则。

**推荐每个reducer一个单独文件**

- 将所有顶级的 reducer 放到一个独立的文件中
- 通过 export 暴露出每个 reducer 函数
- 使用 import * as reducers 得到一个以它们名字作为 key 的 object，可以直接传给combineReducers()

实例：

	import { combineReducers } from 'redux'
	import * as reducers from './reducers'
	
	const todoApp = combineReducers(reducers)

### store ###

**Redux对象，联系Action和Reducer**

- **单一store**
- **单一 state tree**

#### store职责 ####

- **管理 state**；
	- 获取 state，getState()
	- 更新 state，dispatch(action)
- **管理 state监听器** 状态有更新，回调监听器
	- 注册监听器，subscribe(listener)
	- 注销监听器，通过 subscribe(listener) 返回的函数来注销

#### 创建 store ####

**createStore(reducer, [preloadedState], enhancer)**

- reducer
	- function，使用 combineReducers() 将多个 reducer 合并成为一个。
- preloadedState
	- 可选。 设置 state 初始状态
- enhancer 
	- 可选。 function，是一个组合 store creator 的高阶函数，返回一个新的强化过的 store creator

实例：监听器管理

	// subscribe() 返回一个函数用来注销监听器
	const unsubscribe = store.subscribe(() =>
	  console.log(store.getState())
	)
	
	// 停止监听 state 更新
	unsubscribe();

### 严格的单向数据流 ###

**意味着数据都遵循相同的生命周期**

#### 调用 store.dispatch(action) ####

#### Redux store 调用传入的根 reducer 函数 ####

createStore(reducer)时传入的，是根 reducer

#### Redux store 保存了根 reducer 返回的完整 state 树 ####

现在，可以应用新的 state 来更新 UI

如果你使用了 React Redux 这类的绑定库，这时就应该调用 component.setState(newState) 来更新 UI

所有注册的监听器都将被调用

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

## 搭配 React ##

Redux 和 React 之间没有关系。

Redux 支持 React、Angular、Ember、jQuery 甚至纯 JavaScript。

尽管如此，Redux 还是和 React 和 Deku 这类库搭配起来用最好

- 这类库允许你以 state 函数的形式来描述界面
- Redux 通过 action 的形式来发起 state 变化。

### 安装 React Redux ###

Redux 默认并不包含 React 绑定库，需要单独安装

	npm install --save react-redux

### 容器组件和展示组件 ###

**将组件分为两类，更易于复用和维护**

- Container和Presentational Components
- Fat和Skinny
- Smart和Dumb
- Stateful和Pure

甚至直接称为：

- Screens和Components

||展示组件|	容器组件|
|-|-|-|
|作用|	描述如何展现（骨架、样式）|	描述如何运行（数据来源获取、状态更新）|
|状态|一般没有。有UI状态而不是数据|有。往往充当数据源，给其他组件提供数据和行为|
|直接使用Redux|	否|	是|
|数据来源|	props|	监听 Redux state
|数据修改|	从 props 调用回调函数|	向 Redux 派发 actions|
|创建方式|	手动，一般常用函数式无状态组件实现|	通常用 React Redux的connect() 生成|
|示例|Page，Sidebar，Story，List|UserPage，FollowersSidebar，StoryContainer，FollowedUserList|

**展示组件只定义外观并不关心数据来源和如何改变。传入什么就渲染什么**

**大部分的组件都应该是展示型的，但需要少数的几个容器组件把它们和 Redux store 连接起来**

**有时偶尔混用 容器和展示。** 比如 含有“Add”按钮的输入框

### 传入 Store ###

**容器组件需要使用store来获取state**。有两种方法

- 把store以 props 的形式传入到所有容器组件中。
	- 太麻烦
	- 必须要用 store 把展示组件包裹一层
- **使用 React Redux 组件 `<Provider>`** 
	- 不必显示地传递store，只需要在渲染根组件时使用即可
	- 让Provider内所有容器组件都可以访问 store

实例：index.js

	let store = createStore(todoApp)
	
	render(
	  <Provider store={store}>
	    <App />
	  </Provider>,
	  document.getElementById('root')
	)

		API：render(element,container)。实例是获取首页id为root的div

### React Redux的connect() ###

**容器组件 通常用 React Redux的connect() 生成**

- 这个方法做了性能优化来避免很多不必要的重复渲染。
	- 不必为了性能而手动实现 React 性能优化建议 中的 shouldComponentUpdate()。

- 实现原理：使用 store.subscribe() 从 Redux state 树中读取部分数据，并通过 props 把这些数据提供给要渲染的组件

### 实现容器组件 ###

容器组件管理数据(state)，涉及到**读取和修改**

- 读取数据后，需要把state映射到展示组件的props中
	- 定义 `mapStateToProps()` 指定映射规则
- 修改数据是通过dispatch(action)实现，需要把action映射为期望注入展示组件的props中的回调方法
	- 定义 `mapDispatchToProps()`

#### 实例：FilterLink ####

- **FilterLink** 得到当前过滤器并渲染 Link
	- **Link** 带有 callback 回调功能的链接
		- onClick() 当点击链接时会触发

代码

	import { connect } from 'react-redux'
	import { setVisibilityFilter } from '../actions'
	import Link from '../components/Link'
	
	const mapStateToProps = (state, ownProps) => ({
	  active: ownProps.filter === state.visibilityFilter
	})
	
	const mapDispatchToProps = (dispatch, ownProps) => ({
	  onClick: () => dispatch(setVisibilityFilter(ownProps.filter))
	})//点击发送SET_VISIBILITY_FILTER的action
	
	export default connect(
	  mapStateToProps,
	  mapDispatchToProps
	)(Link)

#### 实例：VisibleTodoList ####

- **VisibleTodoList** 根据当前显示的状态来对 todo 列表进行过滤，并渲染 TodoList
	- **TodoList** 用于显示 todos 列表。
		- todos: Array 以 { text, completed } 形式显示的 todo 项数组。
		- onTodoClick(index: number) 当 todo 项被点击时调用的回调函数。
	- **Todo** 一个 todo 项。
		- text: string 显示的文本内容。
		- completed: boolean todo 项是否显示删除线。
		- onClick() 当 todo 项被点击时调用的回调函数。

代码

	import { connect } from 'react-redux'
	import { toggleTodo } from '../actions'
	import TodoList from '../components/TodoList'
	import { VisibilityFilters } from '../actions'
	
	const getVisibleTodos = (todos, filter) => {
	  switch (filter) {
	    case VisibilityFilters.SHOW_ALL:
	      return todos
	    case VisibilityFilters.SHOW_COMPLETED:
	      return todos.filter(t => t.completed)
	    case VisibilityFilters.SHOW_ACTIVE:
	      return todos.filter(t => !t.completed)
	    default:
	      throw new Error('Unknown filter: ' + filter)
	  }
	}
	
	const mapStateToProps = state => ({
	  todos: getVisibleTodos(state.todos, state.visibilityFilter)
	})
	
	const mapDispatchToProps = dispatch => ({
	  toggleTodo: id => dispatch(toggleTodo(id))
	})//点击发送TOGGLE_TODO的action
	
	export default connect(
	  mapStateToProps,
	  mapDispatchToProps
	)(TodoList)

#### reselect计算衍生数据 ####
如果你担心 mapStateToProps 创建新对象太过频繁，可以学习如何使用 reselect 来 计算衍生数据

## 实例 ##

### Todos ###

	git clone https://github.com/reactjs/redux.git
	
	cd redux/examples/todos
	npm install
	npm start
	
	open http://localhost:3000/