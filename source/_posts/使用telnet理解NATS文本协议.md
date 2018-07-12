---
title: 使用telnet理解NATS文本协议
date: 2018-07-12 17:13:24
tags:
	- IM
---

# 连接 #

	# 连接消息系统所在的host:port
	telnet localhost 4222

	Trying 127.0.0.1...
	Connected to localhost.
	Escape character is '^]'.
	INFO {"server_id":"r9W3SWa4LURYr3Ngwh0cyj","version":"1.1.1","git_commit":"","go":"go1.10.1","host":"0.0.0.0","port":4222,"auth_required":false,"tls_required":false,"tls_verify":false,"max_payload":65536}

可以看到服务端反馈了了一个INFO类型的信息，给出了server端的信息。

# 订阅 #

	# 在另一个终端窗口连接消息系统
	telnet localhost 4222
	# 订阅一个消息，主题为foo，定义subject ID为1，sid要求是数字的唯一ID
	# 语法：SUB <subject> [queue group] <sid>\r\n
	SUB foo 1

# 发布 #

	# 回来第一个窗口
	# 发布一个消息，主题为foo，长度为11，内容为：Hello NATS!\
	# 语法：PUB <subject> [reply-to] <#bytes>\r\n[payload]\r\n
	PUB foo 11
	Hello NATS!

可以看到订阅端收到了消息

	MSG foo 1 11
	
	HELLO NATS!

# 取消订阅 #

	# 语法：UNSUB <sid>
	UNSUB 1

# PING和PONG #

server如果观察到死掉的client，会自动关闭，降低负载。为了确保client是在线状态，每隔一段时间会有一个PING信息，client需要应答PONG，如果应答不及时，连接会被close掉。

	# server发送PING
	PING
	# client应答PONG
	PONG

# OK和ERROR #

如果是发送成功，服务器端返回

	+OK

否则：返回ERROR，语法：-ERR <error message>

	-ERR 'Authorization Timeout'

 

可以看到文本协议都非常简单，更多协议直接在[NATS protocol](https://nats.io/documentation/internals/nats-protocol/)查阅。