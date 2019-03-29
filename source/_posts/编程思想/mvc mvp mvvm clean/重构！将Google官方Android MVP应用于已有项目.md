---
title: 重构将Google官方Android MVP应用于已有项目
date: 2019-01-14 09:05:53
categories:
  - 编程思想
tags:
  - 编程思想
---

[重构！将Google官方Android MVP应用于已有项目](http://www.jianshu.com/p/bb5df9b7e357)

采用MVP架构进行重构，代码量上相对于原项目时有所增加的

# Google示例项目 #

[Android Architecture Blueprints [beta]](https://github.com/googlesamples/android-architecture)

# 重构 #

## 建立两个Base接口，BaseView和BasePresenter ##

	public interface BasePresenter {
	}

	public interface BaseView<T> {
	    void setPresenter(T presenter);//将Presenter实例传入view，调用时机为Presenter实现类的构造方法中
	}

## 创建契约类,统一管理View和Presenter的所有接口 ##

	public interface MainActivityContract {
	
	    interface View extends BaseView<Presenter> {
	
	        void showError();
	
	        void showLoading();
	
	        void stopLoading();
	
	        void showResults(ArrayList<String> list);
	
	        void showNetworkError();
	
	    }
	
	    interface Presenter extends BasePresenter {
	
	        void loadPosts(String url, boolean clearing);
	
	        void refresh(String url);
	
	        void loadMore(String url);
	
	    }
	
	}

## 创建Presenter实现类 ##

	public class MainActivityPresenter implements MainActivityContract.Presenter, NewsListener {
	
	    private MainActivityContract.View view;//持有View接口
	    private NewsModel model;//持有Model实现类
	
	    private ArrayList<String> list = new ArrayList<String>();
	
	    public MainActivityPresenter(MainActivityContract.View view) {
	        this.view = view;
	        this.view.setPresenter(this);//View设置Present
	        model = new NewsModel();
	    }
	
	    @Override
	    public void loadPosts(String url, boolean clearing) {
	        view.showLoading();
	        if (clearing) {
	            list.clear();
	        }
	        model.load(url, this);
	    }
	
	    @Override
	    public void refresh(String url) {
	        list.clear();
	        loadPosts(url, true);
	    }
	
	    @Override
	    public void loadMore(String url) {
	        model.load(url, this);
	    }
	
	    @Override
	    public void start() {
	
	    }
	
	    @Override
	    public void onSuccess(String result) {
	        list.add(result);
	        view.showResults(list);
	        view.stopLoading();
	
	    }
	
	    @Override
	    public void onError(String error) {
	        view.stopLoading();
	        view.showError();
	    }
	
	}

## 创建View实现类。 作为View和Presenter的桥梁，创建View和Presenter实现类的实例 ##

	public class MainActivity extends AppCompatActivity implements MainActivityContract.View {
	
	    private SwipeRefreshLayout refresh;
	    private TextView tvRefresh;
	    private TextView tvLoadMore;
	    private TextView tvContent;
	
	    private MainActivityContract.Presenter presenter;
	
	    private String cnnews = "cnnews";
	    private String usanews = "usanews";
	
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_main);
	
	        new MainActivityPresenter(this);//创建Presenter实例
	
	        refresh = (SwipeRefreshLayout) findViewById(R.id.refresh);
	        tvRefresh = (TextView) findViewById(R.id.tvRefresh);
	        tvLoadMore = (TextView) findViewById(R.id.tvLoadMore);
	        tvContent = (TextView) findViewById(R.id.tvContent);
	        refresh.setOnRefreshListener(new SwipeRefreshLayout.OnRefreshListener() {
	            @Override
	            public void onRefresh() {
	                refresh.setRefreshing(false);
	            }
	        });
	        tvRefresh.setOnClickListener(new View.OnClickListener() {
	            @Override
	            public void onClick(View v) {
	                presenter.refresh(cnnews);
	            }
	        });
	        tvLoadMore.setOnClickListener(new View.OnClickListener() {
	            @Override
	            public void onClick(View v) {
	                presenter.loadMore(usanews);
	            }
	        });
	
	        presenter.loadPosts(cnnews, false);
	    }
	
	    @Override
	    public void showError() {
	        tvContent.setText("出现错误");
	    }
	
	    @Override
	    public void showLoading() {
	        refresh.setRefreshing(true);
	    }
	
	    @Override
	    public void stopLoading() {
	        refresh.setRefreshing(false);
	    }
	
	    @Override
	    public void showResults(ArrayList<String> list) {
	        String content = "";
	        for (String string : list) {
	            if (!TextUtils.isEmpty(content)) {
	                content += "\n";
	            }
	            content += string;
	            tvContent.setText(content + "\n");
	        }
	    }
	
	    @Override
	    public void showNetworkError() {
	        tvContent.setText("网络错误");
	    }
	
	    @Override
	    public void setPresenter(MainActivityContract.Presenter presenter) {
	        if (null != presenter) {
	            this.presenter = presenter;
	        }
	    }
	}

## Model实现类 ##

Gson解析接口返回

	public class News {
	    private String content;
	
	    public String getContent() {
	        return content;
	    }
	
	    public void setContent(String content) {
	        this.content = content;
	    }
	}

网络请求异步，返回接口需要接口回调

	public interface NewsListener {
	
	    void onSuccess(String result);
	
	    void onError(String error);
	
	}

Retrofit网络请求

	public class NewsModel {
	
	    public void load(String url, final NewsListener listener) {
	        NewsAPI.get(url, new Callback<News>() {
	            @Override
	            public void onResponse(Call<News> call, Response<News> response) {
	                if (response.code() == 200) {
	                    listener.onSuccess(response.body().getContent());
	                }
	            }
	
	            @Override
	            public void onFailure(Call<News> call, Throwable t) {
	                listener.onError(call.request().url() + " faild");
	                t.printStackTrace();
	            }
	        });
	
	    }
	}

## mvp是如何互相持有的 ##

View与Presenter

	View中
		new MainActivityPresenter(this);//创建Presenter实例

		implements MainActivityContract.View
		@Override
		public void setPresenter(MainActivityContract.Presenter presenter) {
		    if (null != presenter) {
		        this.presenter = presenter;//持有了Presenter
		    }
		}

	Presenter中
		public MainActivityPresenter(MainActivityContract.View view) {
		    this.view = view;//持有了View
		    this.view.setPresenter(this);//View设置Present
		    model = new NewsModel();
		}

Presenter与Model

	Model中
		public void load(String url, final NewsListener listener) 

	Presenter中
		public class MainActivityPresenter implements MainActivityContract.Presenter, NewsListener 
	









