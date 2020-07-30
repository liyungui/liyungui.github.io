	http://segmentfault.com/q/1010000003486813

已知的有：

- mock-server
- Api Faker
- apimocker

## Mock Server- Moco 使用指南 ##

	http://www.coderli.com/mock-server-moco-guide/
	https://github.com/dreamhead/moco
	https://github.com/dreamhead/moco/blob/master/moco-doc/apis.md 配置文件

1. 下载、配置、启动服务jar

	`java -jar D:\moco-runner-0.10.2-standalone.jar http -p 12306 -c D:\foo.json`
	
	foo.json配置如下。没有request字段，匹配优先级最低，只有在匹配不到的情况下，才匹配该返回
	
		[
		  {
		    "response" :
		      {
		        "text" : "Hello, Moco"
		      }
		  }
		]
	
2. 浏览器访问 http://localhost:12306/ 返回 Hello, Moco。cmd窗口能看到请求响应日志

3. 配置文件

	Moco支持动态加载配置文件，所以修改/添加配置文件都是不需要重启服务的。这点非常方便
	
	 Moco支持在全局的配置文件中引入其他配置文件，这样就可以分服务定义配置文件，便于管理。
		
		例如你有两个项目Boy和Girl需要使用同一个Mock Server，那么可以分别定义boy.json和girl.json配置文件，然后在全局文件中引入即可： 
			全局配置如下：
				[ { "context": "/boy", "include": "boy.json" }, { "context": "/girl", "include": "girl.json" } ]
			在boy.json和girl.json中分别定义:
				//boy
				[ { "request" : { "uri" : "/hello" }, "response" : { "text" : "I am a boy." } } ]
				//girl
				[ { "request" : { "uri" : "/hello" }, "response" : { "text" : "I am a girl." } } ]
			注意，此时需要通过参数-g加载全局配置文件（否则配置文件解析会报错）。即：
			java -jar D:\moco-runner-0.10.2-standalone.jar start -p 12306 -g foo.json

			启动成功后，我们分别通过http://localhost:12306/girl/hello 和 http://localhost:12306/boy/hello 访问服务，便可得到对应的reponse结果。

			其实全局文件的引入方式还有直接include等，不过个人觉得context这种方式应该比较常用，管理起来也比较方便。

	get请求--默认，可省略method字段

		{
		    "request": {
		        "method": "get",
		        "uri": "/getBoy",
		        "queries": {
		            "name": "onecoder"
		        }
		    },
		    "response": {
		        "text": "Hey."
		    }
		}
		上述配置匹配的url即为：http://localhost:12306/getBoy?name=onecoder，返回值即为: Hey.

	对于rest风格的url，Moco支持正则匹配。

		{ "request": { "uri": { "match": "/searchboy/\\w+" } }, "response": { "text": "Find a boy." } }
		此时，访问http://localhost:12306/boy/searchboy/*** 结尾加任何参数均可匹配到。

	post请求
	
		{
		    "request": {
		        "method": "post",
		        "forms": {
		            "name": "onecoder"
		        }
		    },
		    "response": {
		        "text": "Hi."
		    }
		}

	对于Header、Cookies等请求信息的配置也是支持的

	template功能--动态返回参数值

		{
		    "request": {
		        "uri": "/template"
		    },
		    "response": {
		        "text": {
		            "template": "${req.queries['name']}"
		        }
		    }
		}
		url：http://localhost:12306/template?name=onecoder 访问，则会返回onecoder。

	json参数--formal， escape the quote in text

		{
		  "request": 
		    {
		      "uri": "/json",
		      "text": 
		        {
		          "json": "{\"foo\":\"bar\"}"
		        }
		    },
		  "response": 
		    {
		      "text": "foo"
		    }
		}

	json参数--If the response is JSON, we don't need to write JSON text with escape character in code.	

		{
		    "request": {
		        "uri": "/json",
		        "json": {
		            "foo": "bar"
		        }
		    },
		    "response": {
		        "text": "foo"
		    }
		}

	json参数--文件

		{
		  "request": 
		    {
		      "uri": "/json",
		      "file": 
		        {
		          "json": "your_file.json"
		        }
		    },
		  "response": 
		    {
		      "text": "foo"
		    }
		}

### 最佳实践 ###

每个接口都定义成独立json文件，通过context和include加载到全局配置文件中。

	[
		{ "context": "/api/appoint/order/detail", "include": "json/order_detail.json" }, json文件夹和jar包同目录
		{ "context": "/api/appoint/order/set_service_complete", "include": "json/blank.json" }
	]

### 问题 ###

如果发现 Invalid UTF-8 start byte 0xb2 错误，只需将json文件以 UTF-8 无BOM编码保存即可解决。

如果发现返回错误码400，就是请求方法不对造成的，默认都是响应get请求，在request中指定"method" : "post"即可解决。

	[
	    {
		 "request" :
	    {
	      "method" : "post"
	    
	    },
	        "response": {
	            "json": {
	                "id": 1392912176805,
	                "state": {
	                    "code": 2000,
	                    "msg": "操作成功"
	                },
	              
	                "data": {
	    }
	            }
	        }
	    }
	]

默认返回编码是gbk，如果app是utf-8就会乱码。
	
	String ret = new String(data,"gbk");
