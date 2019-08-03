---
title: web渲染
date: 2019-07-30 15:28:14
categories:
  - web
tags:
  - web
---

# 基础术语

## Rendering

- **SSR 服务端渲染**: Server-Side Rendering - 服务端渲染HTML.
- **CSR 客户端渲染**: Client-Side Rendering - 客服端浏览器使用DOM渲染.
**Rehydration 同构**: 服务端和客户端使用同一份DOM渲染
**Prerendering 预渲染**: 编译时启动一个客户端渲染出初始化的静态HTML

## Performance

- **TTFB**: Time to First Byte - seen as the time between clicking a link and the first bit of content coming in.
- **FP**: First Paint - the first time any pixel gets becomes visible to the user.
- **FCP**: First Contentful Paint - the time when requested content (article body, etc) becomes visible.
- **TTI**: Time To Interactive - the time at which a page becomes interactive (events wired up, etc).
 
## SPA 和 MPA

**SPA 单页面应用** Single-page Application 

{% asset_img spa.png %}

**MPA 多页面应用多页面应用** Multi-page Application 

{% asset_img mpa.png %}

### 对比

| |单页面应用|多页面应用|
|---|---|---|
|组成|一个外壳页面和多个页面片段组成|多个完整页面构成|
|资源共用(css,js)|共用，只需在外壳部分加载|不共用，每个页面都需要加载|
|刷新方式|页面局部刷新或更改|整页刷新|
|url 模式|a.com/#/pageone  a.com/#/pagetwo|a.com/pageone.html  a.com/pagetwo.html|
|用户体验|用户体验良好。首屏时间慢，页面切换快|用户体验比较差。首屏时间快，页面切换慢|
|转场动画|容易实现|无法实现|
|数据传递|容易|依赖 url传参、或者cookie 、localStorage等|
|搜索引擎优化(SEO)|SEO差。需要单独方案、实现较为困难、可利用服务器端渲染(SSR)优化|SEO效果好。实现方法简易|
|使用范围|高要求的体验度、追求界面流畅的应用|适用于追求高度支持搜索引擎的应用 |
|开发成本|较高，常需借助专业的框架|较低 ，但页面重复代码多|
|维护成本|相对容易|相对复杂|

# 历史

后端渲染 -- 前端渲染 -- 后端渲染

看一门技术的发展主要应该看背后的人是谁，应用场景是哪些，最后才是技术细节。

1. 后端发现页面中的 JS 很麻烦（虽然简单，但是坑多），于是让公司招聘专门写 JS 的人，也就是前端

2. 前端名义上是程序员，实际上就是在写样式（CSS）和做特效(JS)，所以所有程序员中前端工资最低，职位也最低。所以前后端的鄙视链就出现了。
3. nodejs 和前端 mvc 的兴起让前端变得复杂起来，前端发现翻身的机会，于是全力支持这两种技术，造成本不该做成 SPA 的网站也成了 spa。慢慢地前后端分离运动从大公司开始兴起，目的就是前端脱离后端的指指点点，独立发展。（表面上是为了「代码分离」，实际上是为了「人员分离」，也就是「前后端分家」，前端不再附属于后端团队）
4. spa 之后发现 **seo** 问题很大，而且**首屏渲染速度**很慢，但是自己选的路再难走也要走下去，于是用 nodejs 在服务端渲染这一条路被看成是一条出路
5. 其实这是第二个翻身的机会，如果 nodejs 服务器渲染成为主流，其实就相当于前端把后端的大部分工作给抢了，工资压过普通后端指日可待
6. 然而结果是 nodejs 服务端渲染始终是小众，因为后端也没那么脆弱，java php rails 十多年沉淀的技术岂是你说推翻就推翻的，已经运行多年的项目又岂是容你随便用 nodejs 重写的，另一方面 golang 等技术的兴起也给 nodejs 不少压力。最终只有少部分前端特别强势的团队成功用上了 Node.js 做渲染（比如阿里的一些团队），大部分公司依然是用 PHP 渲染 HTML。
7. 于是 nodejs 退一步说好好好我不抢你们的工作，我只做中间层（大部分工作就是渲染页面和调用后台接口），绝不越雷池。后端说算你识相。现在 nodejs 主要搞什么微服务，也是为了抢后端还没注意的市场。

## 前端的矛盾

前后端代码可以分离，但是人员绝对不应该分离。前后端撕逼的事情在大公司天天都在发生，全都是因为前后是两个团队，利益不同。实际上前端推 nodejs 渲染就是在试图重新让前后端合成一体。

但是前端不能明说这件事，因为如果要把前后端部门合并，拆掉的肯定是前端部门。

合，则相当于自断前程。
不合，则永远没法解决seo和首屏加载慢的问题。
所以前端真的挺矛盾的。

## JS的矛盾

凡是浏览器上的框架（Vue React）都说自己能适应「复杂」场景，凡是 Node.js 上的框架（express fastify koa）都说自己是「轻量级」框架。

为啥？因为浏览器是 JS 的主战场，而且无敌手。而服务器上，JS 的经验积累还是太少了，搞企业级服务，Node.js 是敌不过 Java、PHP 的，没办法，发展得太晚了。所以目前只能搞「轻量级」咯。`egg.js` 号称是企业级 Node.js 框架，用过的人来评我就不评了。

## 大前端

有些大佬提出「大前端」的概念，意思是前端也要会后端，但是我们心还是前端的。

这不就是把以前的『前后端一个人做』换了个说法嘛。以前是后端一个人做，现在前端一个做。

反正你现在让后端去学前端，后端肯定是不愿意躺这浑水的。只能前端自己想办法咯。

想来想去就只有 Node.js 中间层做 HTML 渲染了。

由于阿里 nodejs 用得还算多，却招不到人，所以从功利的角度出发，也许你学 nodejs 比学 java 更容易进阿里，毕竟阿里的 java 大神多如云，nodejs 大神却不多。

## 开历史倒车？

其实并**不是**。以前是 Back-end（或者说 Full-stack）工程师负责 SSR，但是现在是 Front-end 工程师负责 SSR 了啊。在目前这个知识爆炸的年代，前后端的职能目前已经被分割得很开，大家都不愿意去淌对方那摊混水，而 Rendering 这事从语义上出发就属于 Front-end 的范畴，让 Back-end 去做这事，其实很多人是不愿意的。

回到问题本身，SSR 的「又流行」其实是 Front-end 社区**工具栈不断进化**的体现，也是历史的必然啊。几年前，SPA/CSR 概念的大热，让很多 Front-end 把他们当做万金油了。其实大家都知道 CSR 有着 SEO 和 页面渲染速度的问题，但苦于社区中没有解决这个问题的工具栈，所以大家都对这个问题**视而不见**了。

而随着 Front-end 社区造轮子大潮的兴起，出现了一个很关键的历史转折点 —— Node.js 的出现。Node.js 赋予了 Front-end 在服务端执行 Js 的能力，有了这个环境和土壤，Front-end 工程师们终于可以考虑如何用 Js 来实现 SSR 了，于是 React 和 Vue 等主流框架后面开始支持 SSR 也就成了必然。

所以之前并不是不流行，而是因为前后端职能的分离，Back-end 不愿意做这事了，Front-end 没有条件去做。现在有条件了，自然又开始流行了。

# 利弊

{% asset_img vs.png %}

# 同构

为了解决客户端渲染首屏慢与 SEO 问题，同构开始出现。

同构：前后端共用 JS，首次渲染时使用 Node.js 来直出 HTML。一般来说同构渲染是介于前后端中的共有部分。

简单说下在使用 Vue SSR（nuxt）的一些坑：

服务端必须是 node.js 或者专门跑个 node.js 来支持；

document 对象找不到，由于前端使用的 window，在 node 环境不存在；

数据预获取时，组件尚未实例化（无法使用 this ），于是在 created 生命钩子调用 method 里的方法行不通，数据请求及格式化等操作都应该放置在专门的数据预取存储容器（data store）或"状态容器（state container）"中处理；

string-based 模板性能肯定要比 virtual-dom-based 模板的性能好。string-base 模板只要填数据即可，virtual-dom-based 模板需要经历 Vue 模板语法 ---> Vnode ---> 拼接字符串 html 的过程。 有关性能的消耗对比，可以参考这篇文章[实测Vue SSR的渲染性能：避开20倍耗时](https://mp.weixin.qq.com/s?__biz=MzUxMzcxMzE5Ng==&mid=2247485601&amp;idx=1&amp;sn=97a45254a771d13789faed81316b465a&source=41#wechat_redirect)；

缓存方面，只能做到页面级的缓存。如果用户特定（user-specific），即对于不同用户需要渲染不同内容，缓存是不可用的。

是否有其他解决客户端渲染不足之处的方法？

答案肯定是有的：

处理 SEO 问题时，使用 prerender... 、升级搜索引擎，以及其他。

白屏可以加 loading、Skeleton Screen 效果、以及其他。

# 参考&扩展

- [Google开发者：SSR、CSR、预渲染、伪同构等渲染架构](https://developers.google.com/web/updates/2019/02/rendering-on-the-web)
- [知乎问答：为什么现在又流行服务器端渲染html？](https://blog.csdn.net/B9Q8e64lO6mm/article/details/79418969)
- [服务端渲染 vs 客户端渲染](https://juejin.im/entry/5a111eb7f265da431c6fe51c)
- [前端：你要懂的单页面应用和多页面应用](https://juejin.im/post/5a0ea4ec6fb9a0450407725c)



