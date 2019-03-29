---
title: MVP模型
date: 2019-01-14 09:08:56
categories:
  - 编程思想
tags:
  - 编程思想
---

[mvp in android](http://blog.csdn.net/lmj623565791/article/details/46596109)     

**MVC**
	
	Model：业务逻辑(biz)和实体模型(bean)
	View：对应于布局文件(xml)
	Controllor：对应于Activity

View对应于布局文件，其实能做的事情特别少，关于该布局文件中的数据绑定的操作，事件处理的代码都在Activity中，造成了**Activity既像View又像Controller**（当然了Data-Binder的出现，可能会让View更像View吧）。这可能也就是为何，在该文中有一句这样的话：

	Most of the modern Android applications just use View-Model architecture，everything is connected with Activity.

而当将架构改为**MVP**以后，Presenter的出现，将Actvity视为View层，Presenter负责完成View层与Model层的交互。现在是这样的：

	Model 依然是业务逻辑和实体模型
	View 对应于Activity，负责View的绘制以及与用户交互
	Presenter 负责完成View于Model间的交互

**减少了Activity的职责**，简化了Activity中的代码，将复杂的逻辑代码提取到了Presenter中进行处理。与之对应的好处就是，耦合度更低，更方便的进行测试。

这个开发架构，在慢慢演变，出现了一种思路，就是将Model继续分解，出来一个管理**Model**的**DataManager**,对Model进行统一管理。

有了这个DaraManager之后，Presenter不直接对应Model,而是对应调用DataManager的接口，DataManager内部实现各个 Model 的实现细节。

## （一）Model ##

实体类User、业务类UserBiz(接口类IUserBiz)

	public class User {
	    private String username;
	    private String password;
	    ...getter setter method...
	}

	public interface IUserBiz {
	    public void login(String username, String password, OnLoginListener loginListener);
	}

	public class UserBiz implements IUserBiz {
	    @Override
	    public void login(final String username, final String password, final OnLoginListener loginListener) {
	        //模拟子线程耗时操作
	        new Thread() {
	            @Override
	            public void run() {
	                try {
	                    Thread.sleep(2000);
	                } catch (InterruptedException e) {
	                    e.printStackTrace();
	                }
	                //模拟登录成功
	                if ("zhy".equals(username) && "123".equals(password)) {
	                    User user = new User();
	                    user.setUsername(username);
	                    user.setPassword(password);
	                    loginListener.loginSuccess(user);
	                } else {
	                    loginListener.loginFailed();
	                }
	            }
	        }.start();
	    }
	}

	public interface OnLoginListener {
	    void loginSuccess(User user);
	    void loginFailed();
	}

## (二) View ##

Presenter与View交互是通过接口。所以我们这里需要定义一个接口ILoginView

本例中有两个方法：login和clear

### View交互接口考虑： ###

1. 该操作需要什么？（getUserName, getPassword）
2. 该操作过程中，对应的友好的交互？(showLoading, hideLoading)
3. 该操作的结果，对应的反馈？(toMainActivity,showFailedError)

### 完整接口IUserLoginView ###
	public interface IUserLoginView {
	    String getUserName();
	    String getPassword();
	
	    void clearUserName();
	    void clearPassword();
	
	    void showLoading();
	    void hideLoading();
	
	    void toMainActivity(User user);
	    void showFailedError();
	}

### View交互接口的实现类--Activity ###

控件肯定需要的（findViewById、setOnClickListener），然后需要和Presenter交互，肯定就需要Presenter啦

	public class UserLoginActivity extends ActionBarActivity implements IUserLoginView {
	    private EditText mEtUsername, mEtPassword;//控件
	    private Button mBtnLogin, mBtnClear;
	    private ProgressBar mPbLoading;
	
	    private UserLoginPresenter mUserLoginPresenter = new UserLoginPresenter(this);//Presenter
	
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_user_login);
	
	        initViews();
	    }
	
	    private void initViews() {
	       	...findViewById....
	        mBtnLogin.setOnClickListener(new View.OnClickListener() {
	            @Override
	            public void onClick(View v) {
	                mUserLoginPresenter.login();
	            }
	        });
	        mBtnClear.setOnClickListener(new View.OnClickListener() {
	            @Override
	            public void onClick(View v) {
	                mUserLoginPresenter.clear();
	            }
	        });
	    }
	
	    @Override
	    public String getUserName() {
	        return mEtUsername.getText().toString();
	    }
	
	    @Override
	    public String getPassword() {
	        return mEtPassword.getText().toString();
	    }
	
	    @Override
	    public void clearUserName() {
	        mEtUsername.setText("");
	    }
	
	    @Override
	    public void clearPassword() {
	        mEtPassword.setText("");
	    }
	
	    @Override
	    public void showLoading() {
	        mPbLoading.setVisibility(View.VISIBLE);
	    }
	
	    @Override
	    public void hideLoading() {
	        mPbLoading.setVisibility(View.GONE);
	    }
	
	    @Override
	    public void toMainActivity(User user) {
	        Toast.makeText(this, user.getUsername() +
	                " login success , to MainActivity", Toast.LENGTH_SHORT).show();
	    }
	
	    @Override
	    public void showFailedError() {
	        Toast.makeText(this,
	                "login failed", Toast.LENGTH_SHORT).show();
	    }
	}

## （三）Presenter ##
Presenter是用作Model和View之间交互的桥梁。presenter完成二者的交互，那么肯定需要二者的实现类。大致就是从View中获取需要的参数，交给Model去执行业务方法，执行的过程中需要的反馈，以及结果，再让View进行做对应的显示。

本例中有两个方法：login和clear

	public class UserLoginPresenter {
	    private IUserBiz userBiz;
	    private IUserLoginView userLoginView;
	    private Handler mHandler = new Handler();
	
	    public UserLoginPresenter(IUserLoginView userLoginView) {
	        this.userLoginView = userLoginView;
	        this.userBiz = new UserBiz();
	    }
	
	    public void login() {
	        userLoginView.showLoading();
	        userBiz.login(userLoginView.getUserName(), userLoginView.getPassword(), new OnLoginListener() {
	            @Override
	            public void loginSuccess(final User user) {
	                //需要在UI线程执行
	                mHandler.post(new Runnable() {
	                    @Override
	                    public void run() {
	                        userLoginView.toMainActivity(user);
	                        userLoginView.hideLoading();
	                    }
	                });
	
	            }
	            @Override
	            public void loginFailed() {
	                //需要在UI线程执行
	                mHandler.post(new Runnable() {
	                    @Override
	                    public void run() {
	                        userLoginView.showFailedError();
	                        userLoginView.hideLoading();
	                    }
	                });
	
	            }
	        });
	    }
	
	    public void clear() {
	        userLoginView.clearUserName();
	        userLoginView.clearPassword();
	    }
	}

## 总结 ##

mvc模式中，Activity既负责View的初始化、数据绑定等操作(v)，还负责业务逻辑控制(c)，Activity代码臃肿

mvp模式，Activity单纯的负责View的初始化、数据绑定等操作(v)，present通过接口和view交互（Activity实现接口，present包含接口--Activity）

## mvp接口迷局 ##

MVP的问题在于，使用接口去连接view层和presenter层，这就导致一个逻辑复杂的页面，接口会有很多，十几二十个都不足为奇。维护接口的成本就会非常的大。

这个问题的解决方案就是你得根据自己的业务逻辑去斟酌着写接口。你可以定义一些基类接口，把一些公共的逻辑，比如网络请求成功失败，toast等等放在里面，之后你再定义新的接口的时候可以继承自那些基类，这样会好不少。

## mvp开源库 ##

[A Model-View-Presenter library for modern Android apps](https://github.com/sockeqwe/mosby)

