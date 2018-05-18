---
title: APK签名
date: 2018-05-17 11:27:25
tags: Android
---

# 查看签名 #

使用第三方sdk时经常要求绑定签名

## 使用自带开发工具keytool ##

### CERT.RSA ###

解压软件解压apk，META-INF目录下的CERT.RSA文件(目录下还有 CERT.SF 和 MANIFEST.MF)

如果没有，说明该APK没有签名

	keytool -printcert -file D:\Desktop\CERT.RSA

输出如下：

	所有者: CN=zhu ting, OU=shensz.cn, O=shensz.cn, L=GuangZhou, ST=GuangDong, C=86
	发布者: CN=zhu ting, OU=shensz.cn, O=shensz.cn, L=GuangZhou, ST=GuangDong, C=86
	序列号: 47f26b4c
	有效期为 Mon Feb 29 14:13:57 CST 2016 至 Fri Feb 22 14:13:57 CST 2041
	证书指纹:
	         MD5:  98:95:04:E5:36:1B:26:90:B1:3D:C6:13:16:65:DF:D0
	         SHA1: 79:33:F3:FC:F5:8D:76:66:4E:FB:52:5B:7E:A1:68:A4:06:3F:A3:28
	         SHA256: 2E:8B:4A:C4:DB:74:E5:44:E4:92:D9:3A:B6:6C:8D:87:93:E6:23:98:BF:AA:A5:EE:A5:3D:B5:87:A0:53:96:2C
	签名算法名称: SHA256withRSA
	主体公共密钥算法: 2048 位 RSA 密钥
	版本: 3
	
	扩展:
	
	#1: ObjectId: 2.5.29.14 Criticality=false
	SubjectKeyIdentifier [
	KeyIdentifier [
	0000: A2 43 E0 12 F7 12 18 C5   3B 83 7B 73 DB 40 C4 A8  .C......;..s.@..
	0010: 8A E6 DD D6                                        ....
	]
	]

### keystore ###

	keytool -list -v -keystore e:\debug.keystore -storepass xxx(密匙)



