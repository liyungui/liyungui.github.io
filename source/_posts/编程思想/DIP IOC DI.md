---
title: DIP IOC DI
date: 2019-08-07 10:58:53
categories:
  - 编程思想
tags:
  - 编程思想
---
	
# DIP 依赖倒置原则
	
Dependence Inversion Principle

实际开发，经常出现高层模块(复杂业务模块；调用者)依赖底层模块(基本原子操作；被调用者)，高层模块往往复杂而多变，改动带来新风险。

这类问题的解决方案就是 **依赖倒置原则**

- 高层模块不应该直接依赖底层模块,两者都应该依赖抽象.
- 抽象不应依赖细节.
- 细节应该依赖抽象.

**本质** 就是在高层模块(调用者)定义一个 **中间件(抽象层)**，底层模块(被调用者) 实现中间件(实现了依赖倒置)；也就是我们常说的 **面向抽象(接口)编程** 

# IOC和DI 控制反转和依赖注入

Inversion of Control

Dependency Injection

示例：用户注册模块

```java
public interface UserDao{
    void insert(User user);
}

public class UserDaoImpl implements UserDao{
    @override
    public void insert(User user){
        //存储的具体实现
    }
}

public interface UserService{
    void storeUser(User user);
}

public class UserServiceImpl implments UserService{
    private UserDao userDao;
    
    public UserService(){
        userDao=new UserDaoImpl();
    }
    
    @override
    public void storeUser(User user){
        //用户信息校验通过
        userDao.insert(user);
    }
}
```

上面的代码已经尽可能的遵循DIP原则

在UserServiceImpl中,通过new来创建UserDao对象(即 UserDao对象的控制权实际在UserServiceImpl中，两者耦合)

解决方案：增加一个中间件(容器)，负责创建和存储所有注册对象(控制权转移，解耦)，运行时按需从容器中取对象

**控制反转是DIP原则的升级**,旨在解决对象依赖问题

控制反转是一种思维方式的变化,**依赖注入**则是该思想的**具体实践**.

# 总结

控制反转和依赖倒置皆提现了**常规线性思维的转变**

倒置"一词其实反映的是逆常规思维(从抽象到具体)。常规思维是线性的,人认识事物的本质是从具体到抽象。即:将类与类直接打交道改编为抽象与抽象打交道,也就是所谓的面向抽象(抽象类或接口)编程.

**控制反转是DIP原则的升级**,旨在解决对象依赖这问题

控制反转是一种思维方式的变化,**依赖注入**则是该思想的**具体实践**.

实现控制反转通常有**两种方式**:依赖查找和依赖注入.

- **依赖查找**:容器提供回调接口和上下文给组件,需要组件自己实现查找合适的对象的过程,此类以**EJB**为代表.
- **依赖注入**:组件不做任何定位查询,只需向容器提供普通的java方法,然后容器根据这些方法自行决定依赖关系.此类以**Spring**为代表.
	- 自动注入,更为自动和简单
	- 基本能够实现对原有代码的无侵入

# 参考&扩展

- [白话设计——浅谈DIP和IOC](https://www.jianshu.com/p/c899300f98fa)