---
title: hexo个性化NexT主题
date: 2018-12-20 08:57:53
categories:
  - 电脑使用
tags:
  - hexo
  - NexT
---

[NexT](https://github.com/iissnan/hexo-theme-next) ，简洁且功能不少，也是在 Github 上 被Star最多。本文是v5.1.4

/themes/目录下

	git clone https://github.com/iissnan/hexo-theme-next.git

把 hexo-theme-next 改名为 next，站点配置文件中修改成如下

	## Themes: https://hexo.io/themes/
	theme: next

# 常用设置 #

主题风格

	scheme: Pisces

# 炫酷效果 #

## 1. 在右上角或者左上角实现fork me on github ##

点击[这里](https://github.com/blog/273-github-ribbons)挑选自己喜欢的样式，并复制粘贴代码到 `themes/next/layout/_layout.swig` 文件中 放在 `<div class="headband"></div>` 的下一行

	<a href="https://github.com/liyungui"><img style="position: absolute; top: 0; right: 0; border: 0;" src="https://s3.amazonaws.com/github/ribbons/forkme_right_darkblue_121621.png" alt="Fork me on GitHub"></a>


## 2. 添加RSS ##

安装 Hexo 插件

	npm install --save hexo-generator-feed

站点配置启用插件

	# Extensions
	## Plugins: http://hexo.io/plugins/
	plugins: hexo-generate-feed

next主题配置 

	# Set rss to false to disable feed link.
	# Leave rss as empty to use site's feed link.
	# Set rss to specific value if you have burned your feed already.
	rss: /atom.xml

重新生成，会在 `./public` 文件夹中看到 `atom.xml` 文件

	hexo g

## 3. 设置动态背景(背景动画) ##

主题配置。最好只开启一种背景动画

	canvas_nest: false
	
	three_waves: false
	
	canvas_lines: true
	
	canvas_sphere: false

如需更改颜色和数量，修改文件。[参考文档](https://github.com/hustcc/canvas-nest.js/blob/master/README-zh.md)

	themes/next/source/lib/canvas-nest/canvas-nest.min.js

## 4. 实现点击出现桃心效果 ##

将[js代码](http://7u2ss1.com1.z0.glb.clouddn.com/love.js)保存到 `/themes/next/source/js/src/love.js`

在 `\themes\next\layout\_layout.swig` 末尾添加

	<!-- 页面点击小红心 -->
	<script type="text/javascript" src="/js/src/love.js"></script>

## 5. 修改文章内链接文本样式 ##

修改文件 themes\next\source\css\_common\components\post\post.styl ，在末尾添加如下css样式

	// 文章内链接文本样式
	.post-body p a{
	  color: #0593d3;
	  border-bottom: none;
	  border-bottom: 1px solid #0593d3;
	  &:hover {
	    color: #fc6423;
	    border-bottom: none;
	    border-bottom: 1px solid #fc6423;
	  }
	}

选择 .post-body 是为了不影响标题，选择 p 是为了不影响首页“阅读全文”的显示样式

## 6. 修改文章底部的那个带#号的标签 ##

修改模板 `/themes/next/layout/_macro/post.swig`，搜索 `rel="tag">#`，将 `#` 换成 `<i class="fa fa-tag"></i>`

## 7. 在每篇文章末尾统一添加“本文结束”标记 ##

在路径 `\themes\next\layout\_macro` 中新建 `passage-end-tag.swig` 文件,并添加以下内容：

	<div>
	    {% if not is_index %}
	        <div style="text-align:center;color: #ccc;font-size:14px;">-------------本文结束<i class="fa fa-paw"></i>感谢您的阅读-------------</div>
	    {% endif %}
	</div>

打开\themes\next\layout\_macro\post.swig文件，在post body 之后(`{### END POST BODY ###}`)：

	<div>
	  {% if not is_index %}
	    {% include 'passage-end-tag.swig' %}
	  {% endif %}
	</div>

主题配置文件末尾添加：

	# 文章末尾添加“本文结束”标记
	passage_end_tag:
  	enabled: true

## 8. 修改作者头像并旋转 ##

打开\themes\next\source\css\_common\components\sidebar\sidebar-author.styl，在里面添加如下代码：

	.site-author-image {
	  display: block;
	  margin: 0 auto;
	  padding: $site-author-image-padding;
	  max-width: $site-author-image-width;
	  height: $site-author-image-height;
	  border: $site-author-image-border-width solid $site-author-image-border-color;
	
	  /* 头像圆形 */
	  border-radius: 80px;
	  -webkit-border-radius: 80px;
	  -moz-border-radius: 80px;
	  box-shadow: inset 0 -1px 0 #333sf;
	
	  /* 设置循环动画 [animation: (play)动画名称 (2s)动画播放时长单位秒或微秒 (ase-out)动画播放的速度曲线为以低速结束 
	    (1s)等待1秒然后开始动画 (1)动画播放次数(infinite为循环播放) ]*/
	 
	
	  /* 鼠标经过头像旋转360度 */
	  -webkit-transition: -webkit-transform 1.0s ease-out;
	  -moz-transition: -moz-transform 1.0s ease-out;
	  transition: transform 1.0s ease-out;
	}
	
	img:hover {
	  /* 鼠标经过停止头像旋转 
	  -webkit-animation-play-state:paused;
	  animation-play-state:paused;*/
	
	  /* 鼠标经过头像旋转360度 */
	  -webkit-transform: rotateZ(360deg);
	  -moz-transform: rotateZ(360deg);
	  transform: rotateZ(360deg);
	}
	
	/* Z 轴旋转动画 */
	@-webkit-keyframes play {
	  0% {
	    -webkit-transform: rotateZ(0deg);
	  }
	  100% {
	    -webkit-transform: rotateZ(-360deg);
	  }
	}
	@-moz-keyframes play {
	  0% {
	    -moz-transform: rotateZ(0deg);
	  }
	  100% {
	    -moz-transform: rotateZ(-360deg);
	  }
	}
	@keyframes play {
	  0% {
	    transform: rotateZ(0deg);
	  }
	  100% {
	    transform: rotateZ(-360deg);
	  }
	}

## 9. 博文压缩 ##

安装插件

	$ npm install gulp -g
	$ npm install gulp-minify-css gulp-uglify gulp-htmlmin gulp-htmlclean gulp --save

站点根目录据新建 `gulpfile.js`

	var gulp = require('gulp');
	var minifycss = require('gulp-minify-css');
	var uglify = require('gulp-uglify');
	var htmlmin = require('gulp-htmlmin');
	var htmlclean = require('gulp-htmlclean');
	// 压缩 public 目录 css
	gulp.task('minify-css', function() {
	    return gulp.src('./public/**/*.css')
	        .pipe(minifycss())
	        .pipe(gulp.dest('./public'));
	});
	// 压缩 public 目录 html
	gulp.task('minify-html', function() {
	  return gulp.src('./public/**/*.html')
	    .pipe(htmlclean())
	    .pipe(htmlmin({
	         removeComments: true,
	         minifyJS: true,
	         minifyCSS: true,
	         minifyURLs: true,
	    }))
	    .pipe(gulp.dest('./public'))
	});
	// 压缩 public/js 目录 js
	gulp.task('minify-js', function() {
	    return gulp.src('./public/**/*.js')
	        .pipe(uglify())
	        .pipe(gulp.dest('./public'));
	});
	// 执行 gulp 命令时执行的任务
	gulp.task('default', [
	    'minify-html','minify-css','minify-js'
	]);

执行` hexo g && gulp`生成博文 就会根据 gulpfile.js 中的配置，对 public 目录中的静态资源文件进行压缩。

## 10. 修改``代码块自定义样式 ##

打开 `\themes\next\source\css\_custom\custom.styl`,向里面加入：(颜色可以自己定义)

	// Custom styles.
	code {
	    color: #ff7600;
	    background: #fbf7f8;
	    margin: 2px;
	}
	// 大代码块的自定义样式
	.highlight, pre {
	    margin: 5px 0;
	    padding: 5px;
	    border-radius: 3px;
	}
	.highlight, code, pre {
	    border: 1px solid #d6d6d6;
	}

更多个性化配置参考

[NexT主题配置优化-出土指南](https://www.titanjun.top/2018/04/03/NexT%E4%B8%BB%E9%A2%98%E9%85%8D%E7%BD%AE%E4%BC%98%E5%8C%96-%E5%87%BA%E5%9C%9F%E6%8C%87%E5%8D%97/) 这个博客配置我挺喜欢的

[hexo的next主题个性化配置教程](https://segmentfault.com/a/1190000009544924#articleHeader9)

[打造个性超赞博客Hexo+NexT+GithubPages的超深度优化](https://reuixiy.github.io/technology/computer/computer-aided-art/2017/06/09/hexo-next-optimization.html)







