---
title: mifare classic 卡密码攻击
date: 2017-07-22 14:39:23
tags:
	- RFID
---

# M1卡结构 #

Mifare Classic 提供 1 Kb - 4Kb 的容量

现在国内采用的多数是 Mifare Classic 1k(S50)[简称 M1 卡]

- **M1卡有 16 个扇区，每个扇区 4 个段，每段 16 字节** (16 * 4 * 16byte = 1024, 1kb)
- **每个扇区的3段 保存 KeyA(6字节)，控制位(4字节)，KeyB(6字节)。M1卡允许每个扇区有一对独立密码**
- **0扇区0段称为厂商段 保存卡的UID(4字节)，卡UID校验位(1字节)，厂商数据(11字节)。规范要求出厂前设置写保护，只能读取不能修改。也有不按规范生产的可修改的UID卡**
![](1.jpg)
![](m1cpu.png)
# 密码破解的几种方法 #

mifare classic 1k 加密算法的漏洞只是使得猜解密码的时间变短，使得猜解密码成为可能

## 一、使用默认密码字典暴破 ##

很多应用IC卡都没有更改默认密码

## 二、nested authentication 攻击（大家常说的验证漏洞攻击） ##

**必须已经知道某一个扇区的密码**

- 对等加密算法
	- 读卡器跟tag中都保存着同样的密码，用同样的算法加密
- rfid的验证过程
	- tag 发送uid给 reader
	- 第一次验证(0扇区密码验证)
		1. tag 发送一个随机数nt（明文）给reader
		2. reader 发送 nt和一个随机数nr(密文)，给tag
		3. tag 解密
			- nt是自己之前发送的nt，则认为正确。
				- 失败就停止，不会发送任何数据了
			- 发送 nr(密文) 给reader 
		4. reader 解密
			- nr是自己之前发送的nr，则认为正确。
		5. **之后所有的数据都通加密传输**
	- 其他扇区密码验证
		- tag发送一个随机数nt（密文）给reader
			- **这个数据中就包含了这个扇区的密码信息**

## 三、darkside攻击 ##

研究人员大量测试之后，发现算法还存在这样一个漏洞

当读卡器发送的加密数据中的某8bit全部正确的时候tag会给读卡器发送一个加密的4bit的数据回复NACK，其他任何情况下tag都会直接停止交互

这个4bit的加密的NACK就相当于把tag中的key带出来了，然后再结合算法漏洞破解出key，如果一个扇区的key破解出来，就可以再使用nested authentication 攻击破解其他扇区密码

## 四、监控正常验证过程获得key ##

nested authentication攻击 和 darkside攻击

- 都是通过一般的读卡器，把tag中的密码破解出来，破解的原理中，都是要让tag中发送出来一段密文。

使用PM3等监控加密数据交换，然后通过“XOR效验与算Key”程序算出密码来

这种情况下一般都是内部人员做案，或者把读卡器中的SAM偷出来，SAM实际上就是保存读卡器中密码的一个模块，然后通过另外的读卡器插入SAM，用正常的授权的卡刷卡，然后监控交换数据，从而算出密码。

## 五、USB监控导入密码到读卡器过程获得key ##

电脑控制程序导入密码（假设是二进制等不能直接观看的密码文件）到读卡器的时候，我们通过监控USB口（串口）数据通信，能明文看到密码

# 常用工具 #

- **mfoc**(Mifare Classic Offline Cracker) 以及目前网络上淘宝上充斥的各类破解工具
	- 基于**nested authentication**攻击原理和**默认密码**
		- 首先使用默认密码对每个扇区进行测试
		- 如果某个扇区存在默认密码，然后就是用nested authentication攻击获得其他扇区的密码。
- **Mfcuk**（MiFare Classic Universal Kit ） 以及PM3的darkside攻击 
	- **darkside攻击**
		- 破解算法的原理本身就不是100%成功的
		- 如果长时间破解不出来，就停了重新换个nt，重新选个时间破解，跟运气也有些关系。

- radiowar的**nfcgui**
	- 就是给**nfc-list  nfc-mfsetuid  nfc-mfclassic**  这三个工具写了个gui界面

以上三个都是基于Libnfc库开发

# 参考&扩展

- [RFID破解三两事](http://www.freebuf.com/articles/wireless/8792.html) 详解了密码攻击原理

- [谈谈 Mifare Classic 破解](https://bobylive.com/static/1491) 详解了M1卡结构
