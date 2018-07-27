---
title: RN页面跳转
date: 2018-07-27 10:48:26
tags:
	- RN
---
# React Navigation #

## 安装 ##

	yarn add react-navigation

## 创建一个有两个页面（Main和Profile）的应用 ##

	import {
	  StackNavigator,
	} from 'react-navigation';
	
	const App = StackNavigator({
	  Main: {screen: MainScreen},
	  Profile: {screen: ProfileScreen},
	});

## 跳转 ##

	class MainScreen extends React.Component {
	  static navigationOptions = {
	    title: 'Welcome',
	  };
	  render() {
	    const { navigate } = this.props.navigation;
	    return (
	      <Button
	        title="Go to Jane's profile"
	        onPress={() =>
	          navigate('Profile', { name: 'Jane' });
	        }
	      />
	    );
	  }
	}