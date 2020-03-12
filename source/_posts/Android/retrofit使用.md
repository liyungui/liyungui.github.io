---
title: retrofit使用
date: 2018-12-20 15:47:53
categories:
  - Android
tags:
  - Android
---

# OkHttp

## 概念

**OkHttp** 是基于http协议封装的一套请求客户端，虽然它也可以开线程，但根本上它更偏向真正的请求，跟**HttpClient**, **HttpUrlConnection**的职责是一样的

Android 4.4后，HttpURLConnection底层实现已被OkHttp替换。可见OkHttp的性能已经被Google认同

volley, retrofit, android-async-http 帮你封装了具体的请求，线程切换以及数据转换


android-async-http内部实现是基于HttpClient, 6.0之后系统不再自带HttpClient，在最近的更新中将HttpClient的所有代码copy了一份进来，所以还能使用

Volley是官方出的，可以支持HttpUrlConnection, HttpClient, OkHttp，如果习惯使用Volley，直接写个OkHttp扩展就行了。

## 优势

- 支持HTTP2.0/SPDY
- socket自动选择最好路线，并支持自动重连
- 拥有自动维护的socket连接池，减少握手次数
- 拥有队列线程池，轻松写并发
- 拥有Interceptors轻松处理请求与响应（比如GZIP压缩,LOG打印请求日志等）
- 实现基于Headers的缓存策略

## OkHttp 发送HTTP请求的初步分析

Dispatcher类 中有两个集合分别为：runningAsyncCalls、readyAsyncCalls分别存放正在执行的请求，等待执行的请求

该类中有一个ThreadPoolExecutor线程池(核心线程0，最大线程Integer.MAX_VALUE，队列Integer.MAX_VALUE，保活60秒)执行器，利用该执行器来执行**异步请求**的execute方法。异步请求发送在非当前工作线程，即创建异步请求的线程，而是从线程池中获取一条线程执行网络请求。同步请求则直接是在当前工作线程中执行。

该类对**异步请求**的管理是通过maxRequests、maxRequestsPerHost进行控制的，前者控制线程池中同时运行的最大请求数，防止同时运行线程过多，造成OOM。后者限制了同一hostname下的请求数，防止一个应用占用的网络资源过多，优化用户体验。

## 设置最大并发数

```java
OkHttpClient().dispatcher(). maxRequests(8);
OkHttpClient().dispatcher().setMaxRequestsPerHost(8);
```

# 一、应用示例--get请求 #

下面以聚合数据平台的免费的一个笑话的接口为例 
	
	接口文档地址：https://www.juhe.cn/docs/api/id/95。 
	接口地址：http://japi.juhe.cn/joke/content/list.from。
	请求参数说明：
		sort	string	是	类型，desc:指定时间之前发布的，asc:指定时间之后发布的
	 	page	int	否	当前页数,默认1
	 	pagesize	int	否	每次返回条数,默认1,最大20
	 	time	string	是	时间戳（10位），如：1418816972
	 	key	string	是	您申请的key

**添加依赖**

	compile 'com.squareup.retrofit2:retrofit:2.0.2'
	compile 'com.squareup.retrofit2:converter-gson:2.0.0'  
	compile 'com.google.code.gson:gson:2.3'

**根据返回json数据建立自己的javabean**

JokeInfo

**定义服务接口 --retrofit把API请求转为接口**

	public interface JokeService {
	    @GET("/joke/content/list.from")
	    Call<JokeInfo> getJokeInfoList(@Query("sort") String sort, @Query("page") int page, @Query("pagesize") int pagesize, @Query("time") String time, @Query("key") String key);
	}

**封装retrofit的包装类（单例模式）**

	public class RetrofitWrapper {
	    private static RetrofitWrapper instance;
	    private Context mContext;
	    private Retrofit retrofit;
	
	    private RetrofitWrapper() {
	        retrofit = new Retrofit.Builder().baseUrl(Constant.BASE_URL).addConverterFactory(GsonConverterFactory.create()).build();
	    }
	
	    public static RetrofitWrapper getInstance() {
	        if (instance == null) {
	            synchronized (RetrofitWrapper.class) {
					if (instance == null) {
	                	instance = new RetrofitWrapper();
					}
	            }
	        }
	        return instance;
	    }
	
	    public <T> T create(Class<T> service) {
	        return retrofit.create(service);
	    }
	
	    public class Constant {
	        public static final String BASE_URL = "http://api2.juheapi.com";
	    }
	}

**调用接口（Activity中）**

	JokeService jokeService = RetrofitWrapper.getInstance().create(JokeService.class); //RetrofitWrapper.getInstance()就是获取一个retrofit对象
    Call<JokeInfo> call = jokeService.getJokeInfoList("desc", 1, 2, "1418816972", "eb46c85bea73462583e38b84c3a25c4b");
    call.enqueue(new Callback<JokeInfo>() {
        @Override
        public void onResponse(Call<JokeInfo> call, Response<JokeInfo> response) {
            JokeInfo ji = response.body();
            //这里显示了列表中的第一条的内容，所以get(0)
            Toast.makeText(MainActivity.this, ji.getResult().getData().get(0).getContent(), Toast.LENGTH_LONG).show();
        }

        @Override
        public void onFailure(Call<JokeInfo> call, Throwable t) {
            Toast.makeText(MainActivity.this, t.getMessage(), Toast.LENGTH_LONG).show();
        }
    });

# 超时时间

默认超时时间，10秒

```java
public class OkHttpClient implements Cloneable, Call.Factory, WebSocket.Factory {
	public static final class Builder {
		connectTimeout = 10_000;
      	readTimeout = 10_000;
      	writeTimeout = 10_000;
  }
}
```

自定义

```java
OkHttpClient.Builder httpClientBuilder = new OkHttpClient.Builder();
httpClientBuilder
		.connectTimeout(60, TimeUnit.SECONDS)
    	.readTimeout(60, TimeUnit.SECONDS)
    	.writeTimeout(60, TimeUnit.SECONDS);//设置超时时间
httpClientBuilder.hostnameVerifier(new HostnameVerifier() {
    @Override
    public boolean verify(String hostname, SSLSession session) {
        return true;
    }
});
SSLSocketFactory sslSocketFactory = createSSLSocketFactory();
if (sslSocketFactory != null) {
    httpClientBuilder.sslSocketFactory(sslSocketFactory);
}
```
  
# 二、概念描述 #

## 请求URL  ##

`@Url`

	@GET
    public Call<ResponseBody> profilePicture(@Url String url);

### How Urls Resolve Against Your Base Url ###

完整url（包括 scheme）--不管baseUrl，直接访问

	Retrofit retrofit = Retrofit.Builder()  
	    .baseUrl("https://your.api.url/");
	    .build();
	
	UserService service = retrofit.create(UserService.class);  
	service.profilePicture("https://s3.amazon.com/profile-picture/path");
	
	// request url results in:
	// https://s3.amazon.com/profile-picture/path

非完整url（不包括 scheme）--拼接到baseUrl后访问

	Retrofit retrofit = Retrofit.Builder()  
	    .baseUrl("https://your.api.url/");
	    .build();
	
	UserService service = retrofit.create(UserService.class);  
	service.profilePicture("profile-picture/path");
	
	// request url results in:
	// https://your.api.url/profile-picture/path
	
非完整url（不包括 scheme）且以 `/`开头 --拼接到baseUrl中的 `host` 后访问。  urls that start with a `leading slash` will be appended to only the `base url’s host` url

	Retrofit retrofit = Retrofit.Builder()  
	    .baseUrl("https://your.api.url/v2/"); //升级了接口，v2版本
	    .build();
	
	UserService service = retrofit.create(UserService.class);  
	service.profilePicture("/profile-picture/path");
	
	// request url results in:
	// https://your.api.url/profile-picture/path

## 请求路径 Path Parameters ##

`@Path` 

	@GET("group/{id}/users")
	Call<List<User>> groupList(@Path("id") int groupId);

	@GET("group/{id}/users")
	Call<List<User>> groupList(@Path("id") int groupId, @Query("sort") String sort); 

	@GET("group/{id}/users")
	Call<List<User>> groupList(@Path("id") int groupId, @QueryMap Map<String, String> options);

## 请求方法 ##

`GET, POST, PUT, DELETE, HEAD`

## 请求参数 Query Parameters ##

`@Query()` ，如果传入 `null` ，retrofit 会自动忽略改参数

	public interface FutureStudioClient {  
	    @GET("/tutorials")
	    Call<List<Tutorial>> getTutorials(
	        @Query("page") Integer page
	    );
	
	    @GET("/tutorials")
	    Call<List<Tutorial>> getTutorials(
	            @Query("page") Integer page,
	            @Query("order") String order,
	            @Query("author") String author,
	            @Query("published_at") Date date
	    );
	} 
	方法2，如果后面三个参数传null，效果和方法1一样

`@QueryMap`

	Call<List<News>> getNews(@QueryMap Map<String, String> options);

## 请求体 ##

- `@RequestBody`
- `@Body` **自定义请求体格式**

	- 使用创建Retrofit对象时定义的转换器。没有定义转换器只能用 `@RequestBody`
	- json格式请求体： {"passWord":"134","userName":"lili"}

- `@FormUrlEncoded 和 @Field/@FieldMap` **Url编码**

	- userName=lili&passWord=123

- `@Multipart 和 @Part` 分割线分割

示例：

	@POST("users/new")
	Call<User> createUser(@Body User user);
		Caused by: java.lang.IllegalArgumentException: Unable to create @Body converter for class com.xuehu365.xuehu.User (parameter #1)
		Caused by: java.lang.IllegalArgumentException: Could not locate RequestBody converter for class com.xuehu365.xuehu.User.
			Tried:
				* retrofit2.BuiltInConverters
				* retrofit2.GsonConverterFactory
		出现这个错误的原因是retrofit版本太低，2.0.0-beta版本不支持@body，升级最新版本即可解决

	@FormUrlEncoded
	@POST("user/edit")
	Call<User> updateUser(@Field("first_name") String first, @Field("last_name") String last);

	@Headers({"Content-type:application/json;charset=UTF-8"})
	@POST("auth/update_user_info")
   	Call<UserInfoResultBean> updateUserBirthday(@Body RequestBody body);   	
		HashMap<String, Long> map = new HashMap<>();
		map.put("birthday", date);
		String json = new Gson().toJson(map);
		RequestBody body = RequestBody.create(MediaType.parse("application/json;charset=UTF-8"), json);
		NetService.getInstance().getService().updateUserBirthday(body)
    
	Call<User> update(@FieldMap Map<String, String> fields);

	@Multipart
	@PUT("user/photo")
	Call<User> updateUser(@Part("photo") RequestBody photo, @Part("description") RequestBody description);


## 请求头操作 HEADER MANIPULATION ##

- 静态

		@Headers("Cache-Control: max-age=640000")
		@GET("widget/list")
		Call<List<Widget>> widgetList();

		@Headers({
		    "Accept: application/vnd.github.v3.full+json",
		    "User-Agent: Retrofit-Sample-App"
		})
		@GET("users/{username}")
		Call<User> getUser(@Path("username") String username);

- 动态

		@GET("user")
		Call<User> getUser(@Header("Authorization") String authorization)

- OkHttp interceptor

	Headers that need to be added to every request can be specified using an OkHttp interceptor.

## 返回体转换器 ##

	Gson: com.squareup.retrofit2:converter-gson  
	Jackson: com.squareup.retrofit2:converter-jackson  
	Moshi: com.squareup.retrofit2:converter-moshi  
	Protobuf: com.squareup.retrofit2:converter-protobuf  
	Wire: com.squareup.retrofit2:converter-wire  
	Simple XML: com.squareup.retrofit2:converter-simplexml  
	Scalars (primitives, boxed, and String): com.squareup.retrofit2:converter-scalars 
	
	自定义转换器，需要继承Converter.Factory，在build adapter时传入我们自定义转换器即可使用

## Interceptor ##

	httpClient.addInterceptor(new Interceptor()

### 开启OkHttp自带Interceptor 打印请求和响应log ###

Since logging isn’t integrated by default anymore in Retrofit 2, we need to add a logging interceptor for OkHttp. 

Luckily OkHttp already ships with this interceptor and you only need to activate it for your OkHttpClient.

The developers of OkHttp have released a separate logging interceptor project, which implements logging for OkHttp.

1.  You can add it to your project with a quick edit of your `build.gradle`:

		compile 'com.squareup.okhttp3:logging-interceptor:3.3.1'  

2. `your OkHttpClient class`:

		OkHttpClient.Builder httpClientBuilder = new OkHttpClient.Builder();
		
		// add your other interceptors …
	
	    // add logging as last interceptor
	    HttpLoggingInterceptor logging = new HttpLoggingInterceptor();
	    // set your desired log level
	    logging.setLevel(Level.BODY);
	    httpClientBuilder.addInterceptor(logging);  // <-- this is the important line!

3. `your retrofit use your custom OkHttpClient defined above`

		new Retrofit.Builder().client(BaseOkHttpClient.getInstance())...

### Log Levels ###

Logging too much information will blow up your Android monitor, that’s why OkHttp’s logging interceptor has four log levels: `NONE`, `BASIC`, `HEADERS`, `BODY`. 

### 遇到的问题：NoClassDefFoundError: Failed resolution of: Lokhttp3/internal/Platform; ###

	java.lang.NoClassDefFoundError: Failed resolution of: Lokhttp3/internal/Platform;
		at okhttp3.logging.HttpLoggingInterceptor$Logger$1.log(HttpLoggingInterceptor.java:112)
		at okhttp3.logging.HttpLoggingInterceptor.intercept(HttpLoggingInterceptor.java:160)
		at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:92)
		at okhttp3.internal.http.RealInterceptorChain.proceed(RealInterceptorChain.java:67)

- [版本一致](http://stackoverflow.com/questions/39545629/noclassdeffounderror-failed-resolution-of-lokhttp3-internal-platform)，**没有解决**

		compile 'com.squareup.okhttp3:logging-interceptor:3.4.1'
		compile 'com.squareup.okhttp3:okhttp:3.4.1'

		甚至让retrofit 移除okhttp 
		compile ('com.squareup.retrofit2:retrofit:2.1.0') {
	        // exclude Retrofit’s OkHttp peer-dependency module and define your own module import
	        exclude module: 'okhttp'
	    }

- [方法数超限，开启 multiDex](http://stackoverflow.com/questions/35578135/noclassdeffounderror-for-okhttpclient)，**搞定**

		defaultConfig {
		    ...
		    multiDexEnabled true
		}
		
		dependencies {
			compile 'com.android.support:multidex:1.0.0'
		}

- 总结

	retrofit2 升级到2.1.0，okhttp3 升级到3.4.1 开启multiDex

		compile 'com.squareup.retrofit2:retrofit:2.1.0'
	    compile 'com.squareup.retrofit2:converter-gson:2.1.0'
	    compile 'com.squareup.okhttp3:logging-interceptor:3.4.1'
	    compile 'com.squareup.okhttp3:okhttp:3.4.1'	
	
		compile 'com.android.support:multidex:1.0.0'

### 自定义Interceptor实现 添加get方法通用查询参数 + 优雅log ###
	
	http://blog.yzapp.cn/Retrofit1.html

	OkHttpClient.Builder httpClientBuilder = new OkHttpClient.Builder();
    httpClientBuilder.addInterceptor(new Interceptor() {
        @Override
        public Response intercept(Chain chain) throws IOException {
            Request originalRequest = chain.request();
            HttpUrl originalHttpUrl = originalRequest.url();

            HttpUrl url = originalHttpUrl.newBuilder()
                    .addQueryParameter("appId", "xuehu")
                    .addQueryParameter("clientType", "3")
                    .addQueryParameter("version", "v1.0")
                    .addQueryParameter("clientVersion", App.getAppVsersion())
                    .build();

            Request.Builder requestBuilder = originalRequest.newBuilder()
                    .url(url)
                    .method(originalRequest.method(), originalRequest.body());

            Request request = requestBuilder.build();
            Response response = chain.proceed(request);

            MediaType contentType = null;
            String bodyString = null;
            if (response.body() != null) {
                contentType = response.body().contentType();
                bodyString = response.body().string();
            }
            LogHelp.d("lyg", "request: " + request.method() + request.url());
            LogHelp.d("lyg", "response: " + response.code() + "\n" + bodyString);
            if (response.body() != null) {// 深坑！打印body后原ResponseBody会被清空，需要重新设置body
                ResponseBody body = ResponseBody.create(contentType, bodyString);
                return response.newBuilder().body(body).build();
            } else {
                return response;
            }
        }
    });

## 泛型封装的失败 ##

尝试封装一个通用的请求方法

	public class PostAPI<B, T> {
	    public void post(String url, B body, BaseCallBack<Response<T>> callBack) {
	        PostService service = BaseRetrofit.getInstance().create(PostService.class);
	        Call<Response<T>> call = service.post(url, body);
	        call.enqueue(callBack);
	    }
	}
	
	public interface PostService {
	    @POST
	    <B, T> Call<Response<T>> post(@Url String url, B b);
	}

报错

	java.lang.IllegalArgumentException: Method return type must not include a type variable or wildcard: retrofit2.Call<com.xuehu365.xuehu.model.response.Response<T>>
	
# 结合rxjava

不结合rxjava

```java
//定义接口
public interface BusinessService {
	@GET("nats/info")
	Call<NatsInfoBean> getNatsConfig(@Query("clazz_plan_id") String clazz_plan_id);
	//rxjava
	@GET("nats/info")
    Observable<NatsInfoBean> getNatsConfig(@Query("clazz_plan_id") String clazz_plan_id);
}

public class NetService {	
	public synchronized BusinessService getBusinessService() {
        if (mBusinessService == null) {
            mBusinessService = getRetrofit().create(BusinessService.class);
        }
        return mBusinessService;
    }
    private Retrofit getRetrofit() {
        if (mRetrofit == null) {
            mRetrofit = new Retrofit.Builder()
                    .client(getBaseOkHttpClientBuilder().build())
                    .addConverterFactory(GsonConverterFactory.create(CustomGson.getsInstance().getGson()))
                    .addCallAdapterFactory(RxJavaCallAdapterFactory.create())//rxjava才需要
                    .baseUrl(ConstDef.BASE_URL)
                    .build();
        }
        return mRetrofit;
    }
}

//使用接口
NetService.getInstance().getBusinessService()
	.enqueue(new Callback<NatsInfoBean>(){});
//使用接口,rxjava
NetService.getInstance().getBusinessService()
	.subscribe(new Subscriber<OrderStatusBean>(){})
```

**总结：**

- 定义接口返回值为 `Observable`。原来为 `Call`
- 创建 `Retrofit实例`时额外 `addCallAdapterFactory(RxJavaCallAdapterFactory.create())`
- 调用接口获取返回值改为 `观察者模式`。原来是 `Callback`

# 参考&扩展

[OkHttp, Retrofit, Volley应该选择哪一个？](http://www.jianshu.com/p/77d418e7b5d6) 

[Retrofit分析-漂亮的解耦套路](http://www.jianshu.com/p/45cb536be2f4) 

[Retrofit初探和简单使用](http://mp.weixin.qq.com/s?__biz=MjM5NDkxMTgyNw==&mid=2653057382&idx=2&sn=68c882cc9fc197f67ad7caba80630314#wechat_redirect) 

[github地址](https://github.com/square/retrofit) 

[文档地址](http://square.github.io/retrofit/) 

[用法详解系列](https://futurestud.io/blog/retrofit-2-upgrade-guide-from-1-9) 


