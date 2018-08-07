---
title: RN布局
date: 2018-07-26 16:21:21
tags:
	- RN
---

# 属性 `props` #

组件 `Image` 的属性 `source` 和 `style`

	render() {
	    let pic = {
	      uri: 'https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg'
	    };
	    return (
	      <Image source={pic} style={{width: 193, height: 110}} />
	    );
	}

自定义组件使用属性

	render() {
	    return (
	      <Text>Hello {this.props.name}!</Text>
	    );
	}

	render() {
	    return (
	      <View style={{alignItems: 'center'}}>
	        <Greeting name='Rexxar' />
	        <Greeting name='Jaina' />
	        <Greeting name='Valeera' />
	      </View>
	    );
	}

## 样式属性 `style` ##

### 属性值 ###

#### 普通的JavaScript对象 ####

最简单，最常用

#### 数组 ####

数组中居后的样式对象优先级更高，这样可以间接实现样式的继承

借鉴CSS中的“**层叠**”做法：即后声明的属性会**覆盖**先声明的同名属性

#### 推荐：使用StyleSheet.create集中定义组件的样式 ####

	const styles = StyleSheet.create({
	  bigblue: {
	    color: 'blue',
	    fontWeight: 'bold',
	    fontSize: 30,
	  },
	  red: {
	    color: 'red',
	  },
	});

	render() {
	    return (
	      <View>
	        <Text style={styles.red}>just red</Text>
	        <Text style={styles.bigblue}>just bigblue</Text>
	        <Text style={[styles.bigblue, styles.red]}>bigblue, then red</Text>
	        <Text style={[styles.red, styles.bigblue]}>red, then bigblue</Text>
	      </View>
	    );
	}

	展示结果:
		红色
		大字蓝色
		大字红色
		大字蓝色

### 宽高 ###

#### 固定宽高 ####

	<View style={{width: 50, height: 50, backgroundColor: 'powderblue'}} />

#### 弹性（Flex）宽高 ####

`flex` 指定宽高占总宽高的比例，相当于 weight

# 状态 `state` #

## `props` 和  `state` 的区别 ##
`props` 一经指定，在被指定的组件的**生命周期中不再改变**。 

对于需要**改变**的数据，我们需要使用 `state`

调用 `setState()` 修改状态

实例：不停闪烁的文字。

文字内容本身在组件创建时就已经指定好了，所以文字内容应该是一个prop。

而文字的显示或隐藏的状态（快速的显隐切换就产生了闪烁的效果）则是随着时间变化的，因此这一状态应该写到state中。

	class Blink extends Component {
	  constructor(props) {
	    super(props);
	    this.state = { showText: true };//初始化状态
	
	    // 每1000毫秒对showText状态做一次取反操作
	    setInterval(() => {
	      this.setState(previousState => {//会传入当前状态
	        return { showText: !previousState.showText };
	      });
	    }, 1000);
	  }
	
	  render() {
	    // 根据当前showText的值决定是否显示text内容。不展示时显示空字符串
	    let display = this.state.showText ? this.props.text : ' ';
	    return (
	      <Text>{display}</Text>
	    );
	  }
	}
	
	render() {
	    return (
	      <View>
	        <Blink text='I love to blink' />
	        <Blink text='Yes blinking is so great' />
	        <Blink text='Why did they ever take this out of HTML' />
	        <Blink text='Look at me look at me look at me' />
	      </View>
	    );
	}

**也可以使用一些“状态容器”比如Redux来统一管理数据流**

# Flexbox布局 #

React Native中的Flexbox的工作原理和web上的CSS基本一致，当然也存在少许差异。

- flexDirection的默认值是column而不是row，
- flex只能指定一个数字值。

## flexDirection ##

**方向**

- row。左右
- row-reverse。右左
- column。上下**默认值**
- colum-reverse。下上右左

## justifyContent 和 alignItems ##

**子元素沿着主轴的排列方式**

**子元素沿着次轴的排列方式**

- flex-start 起始对齐
- center 居中
- flex-end 末尾对齐

以下只适用于主轴排列方式

- space-around 剩余空间均匀的分布在children**周围**(两边)。
- space-between 剩余空间均匀的分布在children**之间**

以下只适用于次轴排列方式

- stretch 撑满次轴。**子元素在次轴方向上不能有固定的尺寸**。

# ListView #

展示长列表数据的组件

## FlatList ##

特点：

- 垂直的滚动列表，元素之间结构近似而仅数据不同
- 元素个数可以增删
- 优先渲染屏幕上可见的元素

使用：

FlatList组件必须的两个属性

- data 列表的数据源
- renderItem 逐个解析数据源，返回一个组件

实例

	const styles = StyleSheet.create({
	  container: {
	   flex: 1,
	   paddingTop: 22
	  },
	  item: {
	    padding: 10,
	    fontSize: 18,
	    height: 44,
	  },
	})
	
	render() {
	    return (
	      <View style={styles.container}>
	        <FlatList
	          data={[
	            {key: 'Devin'},
	            {key: 'Jackson'},
	            {key: 'James'},
	            {key: 'Joel'},
	            {key: 'John'},
	            {key: 'Jillian'},
	            {key: 'Jimmy'},
	            {key: 'Julie'},
	          ]}
	          renderItem={({item}) => <Text style={styles.item}>{item.key}</Text>}
	        />
	      </View>
	    );
	}

## SectionList ##

特点：

适用于需要分组的数据，也许还带有分组标签的

使用：

- sections 列表的数据源，每个对象包含title和data
- renderItem 逐个解析数据源，每个data子元素返回一个组件
- renderSectionHeader 逐个解析数据源，返回一个组件
- keyExtractor

实例

	const styles = StyleSheet.create({
	  container: {
	   flex: 1,
	   paddingTop: 22
	  },
	  sectionHeader: {
	    paddingTop: 2,
	    paddingLeft: 10,
	    paddingRight: 10,
	    paddingBottom: 2,
	    fontSize: 14,
	    fontWeight: 'bold',
	    backgroundColor: 'rgba(247,247,247,1.0)',
	  },
	  item: {
	    padding: 10,
	    fontSize: 18,
	    height: 44,
	  },
	})
	
	render() {
	    return (
	      <View style={styles.container}>
	        <SectionList
	          sections={[
	            {title: 'D', data: ['Devin']},
	            {title: 'J', data: ['Jackson', 'James', 'Jillian', 'Jimmy', 'Joel', 'John', 'Julie']},
	          ]}
	          renderItem={({item}) => <Text style={styles.item}>{item}</Text>}
	          renderSectionHeader={({section}) => <Text style={styles.sectionHeader}>{section.title}</Text>}
	          keyExtractor={(item, index) => index}
	        />
	      </View>
	    );
	}




