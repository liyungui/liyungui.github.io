---
title: ProtoBuf使用
date: 2021-01-19 16:46:53
categories:
  - Java
tags: 
	- Java
---

# 概念

Google推出，高性能序列化框架，比JSON更快更小

# 常用类型

|proto类型	|java类型|
|---|---|
|double|	double|
|float	|float|
|int32	|int|
|int64	|long|
|bool	|boolean|
|string	|String|
|enum|	enum|

proto文件编译成Java文件时，proto类型会转换为对应的Java类型

# 修饰符

- optional：可选字段，不填会有默认值
- require：必填字段
- repeated：列表字段，等价于集合

# proto2和proto3

proto3 语法只保留 `repeated` 修饰符

proto3 增加了 `map<int32, bool>` 数据类型

# proto文件

```
syntax = "proto2"; // 声明语法版本：proto2
  
package test; // 相当于声明命名空间，防止多个文件中相同的message命名冲突
  
option java_package = "com.demo.bean"; // 编译之后的包名
option java_outer_classname = "PersonProto"; // 编译之后的类名
  
// 定义一个消息(一个类可以有多个消息)  
message PersonInfo {
    required int32 id = 1; //定义字段和该字段的编号
    optional string name = 2;
    repeated string remark = 3;
}

```

默认使用proto2语法编译

# 编译proto文件

执行命令之后，就可以看到生成的java文件放到定义的指定目录下

# 解析和序列化

```
byte[] toByteArray() ： 序列化message，返回一个byte数组。
static Person parseFrom(byte[] data) ： 将给定的byte数组解析成一个message。
void writeTo(OutputStream output) ： 序列化message，并将其写入一个输出流。
static Person parseFrom(InputStream input) ： 读取一个输入流并从其解析处一个message。
```

也额外提供了工具类将ProtoBuf转为json

# 实例

```
syntax = "proto3"; // 定义proto版本，如果没有指定proto版本，则采用proto2进行编译，proto2和proto3语法上有些差异
  
package test; // 相当于定于命名空间，防止不同的消息类型存在命名冲突
  
option java_package = "org.example.proto"; // 输出的包的名称
option java_outer_classname = "HeroProto"; // 编译之后输出的文件名称，即直接使用的类名称，如果没有定义，则采用文件名称的驼峰命名作为生成的类名称
  
message GaiLun {
    string hero_name = 1; // 名称
    int32 level = 2; // 等级
    repeated string skill = 3; // 技能列表
    string goods = 4; // 装备
    Group group = 5; // 分组
}
  
message LiBai {
   string hero_name = 1; // 名称
   int32 level = 2; // 等级
   repeated string skill = 3; // 技能列表
   string goods = 4; // 装备
   string friend = 5; // 队友
   Group group = 6; // 分组
}
  
// 枚举
enum Group {
    blue_group = 0;
    red_group = 1;
}
```

编译proto文件为java文件

复制java文件到项目的指定目录下

使用Proto对象

```
//建造者模式，支持链式调用
HeroProto.GaiLun.Builder gailunBuilder = HeroProto.GaiLun.newBuilder();
gailunBuilder.setHeroName("盖伦");
gailunBuilder.addAllSkill(Arrays.asList("Q", "W", "E", "R"));
gailunBuilder.setLevel(18);
gailunBuilder.setGoods("无尽之刃");
gailunBuilder.setGroup(HeroProto.Group.blue_group);

HeroProto.GaiLun gaiLun = gailunBuilder.build();

```

# 参考&链接

- [初识ProtoBuf](https://juejin.cn/post/6916146501945131022)
- [Java中简单使用Protobuf](https://juejin.cn/post/6918013164504219655)
- [Protobuf -java基础教程（译文）](https://juejin.cn/post/6844903767666589703)