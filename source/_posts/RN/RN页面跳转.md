---
title: RN页面跳转
date: 2018-07-27 10:48:26
tags:
	- RN
---
# [React Navigation](https://reactnavigation.org/docs/en/getting-started.html) #

## 安装 ##

	yarn add react-navigation

## createStackNavigator() ##

返回React component(包含路由配置)。可以直接将它输出为App.js的root component.

### 直接输出为App.js的root component ###
App.js
	
	import { createStackNavigator } from 'react-navigation';

	class HomeScreen extends React.Component {
	  render() {
	    return (
	      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
	        <Text>Home Screen</Text>
	      </View>
	    );
	  }
	}

	export default createStackNavigator({
	  Home: {
	    screen: HomeScreen
	  },
	});

### App.js渲染我们创建的component(包含路由配置) ###

	const RootStack = createStackNavigator({
	  Home: {
	    screen: HomeScreen
	  },
	});
	
	export default class App extends React.Component {
	  render() {
	    return <RootStack />;
	  }
	}

### 路由简写 ###

	const RootStack = createStackNavigator({
	  Home: {
	    screen: HomeScreen
	  },
	});

	const RootStack = createStackNavigator({
	  Home: HomeScreen
	});

### 添加第二个路由 ###

**有两个或以上的路由时，需 `initialRouteName` 指定初始路由(第一个页面)**

	class DetailsScreen extends React.Component {
	  render() {
	    return (
	      <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
	        <Text>Details Screen</Text>
	      </View>
	    );
	  }
	}
	
	const RootStack = createStackNavigator(
	  {
	    Home: HomeScreen,
	    Details: DetailsScreen,
	  },
	  {
	    initialRouteName: 'Home',
	  }
	);

## 跳转 ##

- this.props.navigation.**navigate**('RouteName')
	- 进入指定页面。
	- 不会重复创建和push
		- 若已在该页面，无操作
- this.props.navigation.**push**('RouteName')
	- 进入指定页面。
	- 会重复创建和push
		- 每次调用都会在最顶层加入该页面
- this.props.navigation.**goBack**()
	- 返回上一页面
- this.props.navigation.**popToTop**()
	- 回到第一个页面

**如果当前可返回，标题栏会自动展示返回箭头**

### 传参 ###

#### 使用API ####

	this.props.navigation.navigate('RouteName', {})
	this.props.navigation.push('RouteName', {})
	
	this.props.navigation.getParam(paramName, defaultValue).
	this.props.navigation.state.params 较少用。因为如果没有传参，该值为null。

#### 使用社群包 ####

[react-navigation-props-mapper](https://github.com/vonovak/react-navigation-props-mapper) 
