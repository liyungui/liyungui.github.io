---
title: 修改第三方aar重打包
date: 2019-11-27 20:15:53
categories:
  - 逆向
tags:
	- 逆向
---

# 解压aar

`unzip myLib.aar -d tempFolder`

# 解压`classes.jar`

解压aar中的`classes.jar`。 

`unzip classes.jar -d tempFolderClasses`

# 逆向源码

这里推荐使用 `jd-gui`，支持直接逆向aar

# 修改源码

- 新建项目
- 引用原aar
- 拷贝目标类源码（包名一致）
- 修改报错
	- `jd-gui`发编译的特点：可读性高；原义性低。
	- 混淆容易造成类名重复
- 修改源码（实现自己的逻辑）
- 编译生成class文件
	- 会报错（重复类；合并失败）
	- class文件路径 `/build/intermediates/javac`

`jd-gui`逆向示例：

```java
import com.tencent.liteav.basic.c.a;
import com.tencent.liteav.basic.structs.a;

protected a mNotifyListener;
protected a mRestartListener;
```

同名类a，编译期报错。

修改方式：删掉一个导包，完整包名的方式来使用类

# 替换class文件

替换tempFolderClasses文件夹下旧的.class文件

# 打包`classes.jar`

打包源码为jar

`jar cvf classes.jar -C tempFolderClasses/ .`（注意斜杠后面加`空格与.`）

# 打包aar

打包所有文件(res文件、classes.jar、AndroidManifest.xml等)为aar

`jar cvf newAAR.aar -C tempFolder/ .`