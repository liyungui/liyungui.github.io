---
title: TCP三次握手四次挥手
date: 2019-04-11 17:51:53
categories:
  - 网络
tags:
  - 网络
---

# 三次握手，四次挥手

{% asset_img 三次握手.png %}
{% asset_img 四次挥手.png %}

# TCP标志位

SYN，ACK，FIN 存放在TCP的标志位(一共6个)

**SYN**：**同步**序列编号(Synchronize Sequence Numbers)

- 请求创建连接
- 同步的是初始序列编号(ISN,Initialize Sequence Numbers)
	- 初始序列号是**随机**生成的
- SYN=1

**FIN**：**结束**连接(Finish)

- 请求关闭连接
- FIN=1
- 在四次分手时，我们发现FIN发了两遍。这是因为TCP的连接是双向的，一次FIN只能关闭一个方向。

**ACK**：**确认**字符(Acknowledgement）

- **确认接受**
- ACK为1表示确认号有效，为0表示报文中不包含确认信息，忽略确认号字段

三次握手和四次分手，在回应的时候都会加上ACK=1，表示消息接收到了，并且在建立连接以后的发送数据时，都需加上ACK=1,来表示数据接收成功。

# TCP包编号

**seq**: **序列号**(Sequence)

- 数据包序列编号。

	发送一个数据会被拆成多个数据包来发送，序列号就是对每个数据包进行编号，这样接受方才能对数据包进行再次拼接。

- 初始序列号是**随机**生成的

**ack**: **确认**字符(Acknowledgement）

- ack=seq+1

	也是下一个数据包的序列编号seq

# TCP状态

- **LISTEN** - 某个Socket处于**监听**，侦听来自远方TCP端口的连接请求;
- **SYN-SENT** - 已发送SYN报文
- **SYN-RECEIVED** - 已接受SYN报文
- **ESTABLISHED**- 已建立连接
- **FIN-WAIT-1** - 已发送FIN报文，等待对方FIN报文
- **FIN-WAIT-2** - 已发送FIN报文，已收到对方ACK报文，等待对方FIN报文；此时已是**半连接**（告诉对方，我暂时还有点数据需要传送给你，稍后再关闭连接）；`FIN_WAIT_1`状态下，收到了对方同时带FIN标志和ACK标志的报文时，可以直接进入`TIME_WAIT`状态，而无须经过`FIN_WAIT_2`状态。
- **LAST-ACK** - 等待对方最后的ACK
- **TIME-WAIT** -已收到对方FIN报文，已发送ACK报文，等待足够的时间（至少一个报文的来回时间）以确保对方成功接受ACK报文；如果超时没有再次收到 FIN 报文，则代表对方成功接受 ACK 报文，可以进入 CLOSED 状态。这个状态需要**特别注意**
- **CLOSED** - 连接已关闭；也是初始状态
- **CLOSING** - **比较特殊少见**，双方几乎同时close某Socket；发送FIN报文，马上收到对方FIN(正常应收到ACK)
- **CLOSE_WAIT** - 等待关闭；已收到FIN报文，已发送ACK报文，此时等待己方去关闭连接（如果己方没有数据要发送，发送FIN报文，收到ACK即可关闭连接）

# 为什么需要三次握手

**为了避免资源浪费**

更细的话，这个问题从两个方面来回答

- 三次握手才能确认两端的收发能力；没有确认收发能力发送数据浪费资源
- 避免建立不必要连接。
	- 两次握手就建立连接话（客户端发送连接请求，服务端接收到并发送确认），如果一个连接请求在网络中跑的慢，超时了，客户端重发请求，跑的慢的请求最后到了服务器，服务端就会创建两个连接，浪费资源；
	- 加第三次握手（客户端确认），客户端在接受到一个服务器的ACK后，后面的ACK就可以抛弃。

# 为什么需要四次分手

由于TCP连接是全双工(双向)的，因此每个方向都必须单独进行关闭。每个方向的关闭又需要请求和确认，所以一共就4次

原则是当一方完成它的数据发送任务后就能发送一个FIN来终止这个方向的连接。收到一个 FIN只意味着这一方向上没有数据流动，一个TCP连接在收到一个FIN后仍能发送数据。首先进行关闭的一方将执行主动关闭，而另一方执行被动关闭。

# 初始序列号(ISN)为什么要随机生成

如果ISN是固定的，攻击者很容易猜出后续的确认号

# 半连接队列

服务器第一次收到客户端的 SYN 之后，就会处于 SYN_RCVD 状态，此时双方还没有完全建立其连接，服务器会把此种状态下请求连接放在一个队列里，我们把这种队列称之为**半连接队列**。

## SYN-ACK 重传

服务器发送完SYN-ACK包，如果未收到客户确认包，服务器进行首次重传，等待一段时间仍未收到客户确认包，进行第二次重传，如果重传次数超 过系统规定的**最大重传次数**，系统将该连接信息从半连接队列中删除。

注意，每次重传等待的**超时时间**不一定相同，一般会是指数增长，例如间隔时间为 1s, 2s, 4s, 8s, ….

## SYN攻击

DDoS攻击的一种

最常见又最容易被利用的一种攻击手法

利用TCP协议缺陷，短时间内不断向服务器发送大量的半连接请求（伪造不存在的IP），服务器回复确认包，并等待客户的确认，由于源地址是不存在的，服务器需要不断的重发直至超时，这些伪造的SYN包将长时间占用未连接队列，正常的SYN请求被丢弃，目标系统运行缓慢，严重者引起网络堵塞甚至系统瘫痪。

### 防范

#### 注册表设置 

启用 SynAttackProtect ，指定 SYN_RCVD 状态中的 TCP 连接阈值，超过 SynAttackProtect 时，触发 SYN flood 保护

#### 丰富带宽资源

#### 防火墙

最有效的方法

当然前提是攻击在防护带宽范围之内，也就是为什么第二条推荐带宽资源，这是保证在防火墙前面不会造成堵塞

# 全连接队列

已经完成三次握手，建立起连接的就会放在全连接队列中。

如果队列满了就有可能会出现丢包现象。

# 三次握手过程中可以携带数据吗

**第三次握手可以携带数据**

此时客户端已经处于 established 状态，也就是说，对于客户端来说，他已经建立起连接了，并且也已经知道服务器的接收、发送能力是正常的了，所以能携带数据页没啥毛病。

假如第一次握手可以携带数据的话，恶意攻击者根本就不理服务器的接收、发送能力是否正常，疯狂着重复发 SYN 报文。这会让服务器花费很多时间、内存空间来接收这些报文。让服务器更加容易受到攻击了。

# 参考&扩展

- [关于三次握手与四次挥手面试官想考我们什么？](https://juejin.im/post/5caed6925188251ac6386c7b)
- [对TCP三次握手四次分手还不清楚，超简单解析](https://baijiahao.baidu.com/s?id=1593714120815701015&wfr=spider&for=pc)
- [四次挥手](https://baike.baidu.com/item/%E5%9B%9B%E6%AC%A1%E6%8C%A5%E6%89%8B/7794287?fr=aladdin#2)
- [漫画：一招学会TCP的三次握手和四次挥手](https://juejin.im/post/5cb93204f265da039955d770)


