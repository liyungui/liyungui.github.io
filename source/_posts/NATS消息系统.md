---
title: NATS消息系统
date: 2018-07-12 16:08:02
tags:
	- IM
---

# 简单原理 #

NATS的服务端监听了一个端口，并将此端口暴露在公网。所有客户端通过长连接连上这个IP的端口，可以相互实时传输消息，发布和订阅消息。

# 物理架构 #

以下是发起连麦的一个例子，序号表示发生的顺序。

注：

- req表示请求(有响应回执)
- sub表示订阅主题
- pub表示发布广播。req和pub的时候可以带上消息、一般是一串JSON文本。
- $classid.mic.request这种字符串是一个主题(频道)。

{% asset_image NATS.png %}

## NATS集群起什么作用？ ##

1. 去单点，提高可用性，当单机挂掉的时候，备用机器补上；
2. 提高并发，单机并发只能到60000+，但多机器可以非常高；

## 为什么学生发起连麦是点对点req而不是发广播pub？ ##

假设网络畅通的前提下，两种做法对比：

1. 如果直接广播这个$classid.mic.request连麦请求，后台可能没有收到消息，或者后台收到之后处理消息发生异常，没有正确入队。造成**状态不一致**：其他学生会以为这个学生已经成功入队，事实上没有；
2. 如果是学生发起req请求，后台接收到消息之后，进行入队处理，成功会发送回执消息，并广播「成功入队」的消息给所有人，可以确保入队是已经执行成功的。这个状态有接收方(后台)的验证，是可信的；

## 设计原则 ##

- 传递信息量相同的情况下，消息越短越好。

	所有JSON都需要uglify，不能排版，不能有多余的空格。有n个学生，则消息量会被放大n倍，这些消息都要吞噬掉服务器的CPU、内存、带宽。如果可能，应该用二进制协议而非文本协议，性能更高，带宽要求更小。

- 不影响正常功能的情况下，消息覆盖人数越少越好。

	可用「奥卡姆剃刀」。那么提个问题，禁言消息怎么设计？

	- 是设计成每个人一个主题，老师点对点沟通？
	- 还是设计成大班中的每个人都接收到禁言消息？
	- 还是小班中每个人都接收到禁言消息？

- 协商定义好每个主题的触发条件、内容格式，形式(广播/点对点)。当新增角色模块，如管路员的时候，对照格式规范，对各自的逻辑进行编码即可。

# 性能测试 #

一般上课过程中，可能的publisher是老师、辅导老师、管理员。publisher不会很多，学生上线发的状态、心跳除外，因为订阅者也只有老师端和管理员。

所以大部分情况下，频繁发布消息的人只有老师。

	# -s  nats地址
	# -np publisher数量
	# -ns subcriber数量
	# -n  总的消息数量，会按publisher数量平均分
	# -ms 消息的长度
	# foo.shit 发布订阅的主题
	# 性能测试不要开启日志，日志的IO会严重影响性能，直接下降2个数量级。
	# 配置文件的max_connections也非常重要，会直接限制连接数
	nats-bench -s nats://mobile:$passwd@localhost:4222 -np 1 -ns 1000 -n 10000 -ms 128 foo.shit

注：

- 由于公网的网络有上限，实际吞吐量会比较小。
- 使用自带工具[nats-bench](https://nats.io/documentation/tutorials/nats-benchmarking/)测试。
- 20000+并发后，报错：「Can't connect: nats: no servers available for connection」，需要修改~/go/src/github.com/nats-io/go-nats/nats.go中的DefaultTimeout为30秒，参照本页性能优化小节。

{% asset_image 1.png %}

# 各端使用方法 #

## 前端 ##

前端使用的客户端是[websocket-nats](https://github.com/isobit/websocket-nats)，后端把原来的TCP协议通过[ws-tcp-relay](https://github.com/isobit/ws-tcp-relay)转成了websocket协议。

性能测试结果如下：

{% asset_image 2.png %}

## C++ ##

## Java ##

java客户端是[java-nats](https://github.com/nats-io/java-nats)

### Android ###

Gradle/Grails

	compile 'io.nats:jnats:1.0'

### 常见问题 ###

#### 重复收到消息 ####

原因是重复subscribe(String subject)

每次subscribe都会生成一个AsyncSubscriptionImpl并添加到队列中接受消息

所以要特别注意动态订阅的主题重复订阅问题

	SubscriptionImpl subscribe(String subject, String queue, MessageHandler cb,
                               BlockingQueue<Message> ch) {
        final SubscriptionImpl sub;
        try {
            if (cb != null) {
                sub = new AsyncSubscriptionImpl(this, subject, queue, cb);
                // If we have an async callback, start up a sub specific Runnable to deliver the messages
                logger.debug("Starting subscription for subject '{}'", subject);
                subexec.submit(new Runnable() {
                    public void run() {
                        try {
                            waitForMsgs((AsyncSubscriptionImpl) sub);
                        } catch (InterruptedException e) {
                            logger.debug("Interrupted in waitForMsgs");
                            Thread.currentThread().interrupt();
                        }
                    }
                });
            } 

            // Sets sid and adds to subs map
            addSubscription(sub);
			...
        } finally {
            mu.unlock();
        }
    }

#### 重复收到自己reply to request的消息 ####

如果所有subscribe使用了同一个MessageHandler，就会出现这种情况。因为我们request和publish的主题相同，我们发送reply的publish，自己也会收到，然后又reply自己...反复循环

	if ("help".equals(msg.getSubject())) {
        NATSManager.getInstance().getNATSService().reply(msg.getSubject(), msg.getReplyTo(), "I can help!".getBytes(), new NATSService.CallBack() {
            @Override
            public void onError(Exception e) {
                e.printStackTrace();
            }
        });
    }



# 异常处理 #

## slow consumer ##
 

# 安装/搭建/启动 #

这节和以后的内容，仅后端同学关注即可。

## 安装Go语言环境与nast服务端 ##

Go 语言虽然是静态编译型语言，但是它却拥有脚本化的语法，支持多种编程范式(函数式和面向对象)。

去[Go官网](https://golang.org/)下载Linux的安装包，按照[安装文档](https://golang.org/doc/install)安装，注意GOROOT和PATH环境变量的配置。

安装并验证hello程序之后，安装nast服务端：

	# 执行命令后，我的go workspace是默认的$HOME/go，所以会安装在go workspace目录内
	go get github.com/nats-io/gnatsd
	# 在PATH环境变量中加入$HOME/go/bin并source，执行以下命令，验证安装成功
	gnatsd version
	  
	# 安装nats-top，跟top类似的监控工具
	go get github.com/nats-io/nats-top
	# 测试是否安装成功
	nats-top
	  
	# 安装go client，用来测试
	go get github.com/nats-io/go-nats
 

## 配置文件 ##

为了便于多人维护和守护执行，建议用配置文件配置而非用启动参数，故障时便于他人重启。

	# nast.conf
	  
	# 监听端口
	port: 4222
	net: "0.0.0.0"
	 
	# 监控服务
	http_port: 8222
	 
	# 对客户端鉴权，timeout为验证限时
	authorization {
	  user:     mobile
	  password: samplepassword
	  timeout:  3
	}
	 
	# 日志, trace为打印所有的原始消息
	debug: false
	trace: true
	logtime: true
	log_file: "/home/zhonggy/nats/logs/gnatsd.log"
	 
	 
	# PID文件
	pid_file: "/home/zhonggy/nats/gnatsd.pid"
	 
	# 最大连接数，很重要，否则很容易不够用
	max_connections: 1000000
	 
	# 控制命令最大长度
	max_control_line: 512
	 
	# 消息最大长度
	max_payload: 65536
	 
	# socket往客户端写的时间，超过deadline时间会标记为slow consumer
	# 会丢弃消息并断开slow consumer，以避免高负载导致整个系统异常
	# 客户端会收到异常，慢消息异常应该由客户端去处理而非服务器来hold
	# 参考: https://nats.io/documentation/server/gnatsd-slow-consumers/
	write_deadline: "3s"

建立start启动脚本：

	#!/bin/sh
	 
	gnatsd -c ./nats.conf &

## 性能优化 ##

### 内核参数调整 ###

所有的高并发性能优化，必然牵扯到打开文件数内核参数，如MySQL，Nginx的优化必然先优化系统内核参数。

每个socket连接都会占用一个文件描述符fd。可通过以下命令查看数量。如果不做配置，则不可能达到高并发。

	ls /proc/$pid/fd/

修改内核参数：

	# vi /etc/sysctl.conf
	# 修改内核可打开的文件上线
	fs.file-max = 6815744
	# 执行sysctl -p生效
	# sysctl -a | grep file-max检查是否设置成功
	  
	# vi /etc/security/limits.conf
	# 修改每用户可打开文件数
	* soft nofile 1024000
	* hard nofile 1024000
	# 重新ssh登陆后ulimit -n检查是否设置成功
 

## 日志 ##
## 用户权限 ##
## 集群 ##

# demo #

	public static void main(String[] args) {
        try {
            private String url = "nats://android:cKCOzJv2ywY20H8a@192.168.30.53:4222";
            final Connection nc = Nats.connect(url);
            // Simple Async Subscriber
            nc.subscribe("foo", new MessageHandler() {
                @Override
                public void onMessage(Message msg) {
                    System.out.printf("Received a message: %s\n", new String(msg.getData()));
                }
            });
            // Simple Publisher
            nc.publish("foo", "Hello World".getBytes());
	
            // Replies
            nc.subscribe("help", new MessageHandler() {
                @Override
                public void onMessage(Message msg) {
                    try {
                        System.out.printf("Received a message: %s\n", new String(msg.getData()));
                        nc.subscribe(msg.getReplyTo(), new MessageHandler() {
                            @Override
                            public void onMessage(Message msg) {
                                System.out.printf("Received a message: %s\n", new String(msg.getData()));
                            }
                        });
                        nc.publish(msg.getReplyTo(), "I can help!".getBytes());
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            });
            // Requests
            Message msg = nc.request("help", "help me".getBytes(), 10000);
	
			//nc.close();
	
	
            nc.subscribe("1.vote.ask", new MessageHandler() {
                @Override
                public void onMessage(Message msg) {
                    System.out.printf("Received a message: %s\n", new String(msg.getData()));
                }
            });
            nc.publish("1.vote.ask", "{\"code\":0,\"msg\":\"\",\"data\":{\"online_num\":{\"chatroom_id\":\"liveroom_262\",\"total_online_num\":1,\"detail_online_num\":[{\"team_id\":352,\"online_num\":1}]},\"vote\":null,\"connect\":null,\"timestamp\":1531884212049}}".getBytes());
	
            nc.subscribe("1.vote.data", new MessageHandler() {
                @Override
                public void onMessage(Message msg) {
                    System.out.printf("Received a message: %s\n", new String(msg.getData()));
                }
            });
            nc.publish("backend.vote.answer", "{\"data\":{\"display\":false,\"custom\":{\"class_id\":1,\"team_id\":1,\"vote_id\":1,\"answer\":\"B\"}}}".getBytes());
            nc.publish("backend.vote.answer", "{\"data\":{\"display\":false,\"custom\":{\"class_id\":1,\"team_id\":2,\"vote_id\":1,\"answer\":\"B\"}}}".getBytes());
            nc.publish("backend.vote.answer", "{\"data\":{\"display\":false,\"custom\":{\"class_id\":1,\"team_id\":3,\"vote_id\":1,\"answer\":\"B\"}}}".getBytes());
	
        } catch (Exception e) {
            e.printStackTrace();
        }
    }