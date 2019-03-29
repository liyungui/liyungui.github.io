---
title: MVVM和MVPVM
date: 2019-01-14 09:10:56
categories:
  - 编程思想
tags:
  - 编程思想
---

	MVVM	http://mp.weixin.qq.com/s?__biz=MzA4MjU5NTY0NA==&mid=401410759&idx=1&sn=89f0e3ddf9f21f6a5d4de4388ef2c32f#rd
	教你认清MVC，MVP和MVVM http://android.jobbole.com/82942/
	MVPVM in Action http://blog.zhaiyifan.cn/2016/03/16/android-new-project-from-0-p3/
	官方文档 http://developer.android.com/intl/zh-cn/tools/data-binding/guide.html

mvvm解决的问题就是我们开发中 findViewById 手工设置view数据。关键技术是 **数据绑定框**架（Data Binding Library）。其他的跟mvc模型一样，存在Activity兼具V和C，导致代码过重。

Google的数据绑定框架（Data Binding Library）其语法和使用方式和 JSP 中的 EL 表达式非常类似,而且提供丰富的扩展功能

## Data Binding Library ##

**配置环境**

	Gradle 1.3.0-betal 1 以上
	Android Studio 1.3 以上
	更新 Android Support repository
	更新 Android Support library

Android Studio 2.0 已经内置了该框架的支持，app目录（module目录）下的build.gradle文件，添加下面的内容

	android {
	    ....
	    dataBinding {
	        enabled = true
	    }
	}

**布局layou文件，< layout>< data>< variable>，绑定数据和事件**

	<layout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:tools="http://schemas.android.com/tools">
	
	    <data>
	        <variable
	            name="user"
	            type="com.example.testbind.User"/>
			<variable
	            name="handlers"
	            type="com.example.testbind.Handlers"/>
	    </data>

	    <RelativeLayout
	        android:layout_width="match_parent"
	        android:layout_height="match_parent"
	        android:paddingBottom="@dimen/activity_vertical_margin"
	        android:paddingLeft="@dimen/activity_horizontal_margin"
	        android:paddingRight="@dimen/activity_horizontal_margin"
	        android:paddingTop="@dimen/activity_vertical_margin"
	        tools:context="com.example.testbind.MainActivity">
	        <TextView
	            android:layout_width="wrap_content"
	            android:layout_height="wrap_content"
	            android:text="@{user.name}" //private name 也可以这样写，只有User类符合javaBean规范
				android:onClick="@{handlers.onClick}" />  //函数也是不用()的
	    </RelativeLayout>
	</layout>

**自定义Class（VM）**

	public class User extends BaseObservable {
	    private String name;
	    @Bindable   
	    public String getName() {//get方法有@Bindable，编译阶段会生成BR.[property name]。另外xml< variable>定义的变量也会生成BR.[property name]。
	        return name;
	    }
	    public void setName(String name) {
	        this.name = name;
	        notifyPropertyChanged(BR.name);
	    }
	}
	public interface Handlers {
	    public void onClick(View view); //必须和onClick方法签名一致
	}

	

**Activity文件中，DataBindingUtil绑定V和VM**
	
	protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
		ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
        final User user = new User();
        user.setName("lili");
        binding.setUser(user);
        binding.setHandlers(new Handlers() {
            @Override
            public void onClick(View view) {
                Toast.makeText(MainActivity.this,"hh",Toast.LENGTH_SHORT).show();
                user.setName("haha");
            }
        });
	}

**通过id找view**

databinding会自动为定义了id的view生成binding成员变量，使用非常方便。

	<EditText
        android:id="@+id/etPhone" ...
	<EditText
	        android:id="@+id/et_phone" ...
	都会生成在binding类中生成etPhone变量（驼峰命名，xml即使有snake命名也会替换成驼峰命名）
		private LoginActivityBinding binding;
		binding.etPhone.getText().toString();

		
## 更新界面 ##

**方案一、数据类继承BaseObservable，调用notifyPropertyChanged**

**数据类继承BaseObservable**，然后通过**调用notifyPropertyChanged**方法来通知界面属性改变

在需要通知的属性的get方法上加上@Bindable，这样编译阶段会生成BR.[property name]，然后使用这个调用**notifyPropertyChanged**()就可以通知界面刷新了（**一般封装在set方法中，这样调用set方法就能刷新界面了**。参照上例）。

如果你的数据绑定类不能继承BaseObservable，那你就只能自己实现Observable接口，可以参考BaseObservable的实现。

**方案二、ObservableField，调用ObservableField的set方法**

Data Binding Library提供了便利类ObservableField, ObservableBoolean, ObservableByte, ObservableChar, ObservableShort, ObservableInt, ObservableLong, ObservableFloat, ObservableDouble, 和 ObservableParcelable，基本上涵盖了各种我们需要的类型。**调用ObservableField的set方法**时，Data Binding Library就会自动的帮我们通知界面刷新了

	public class User {
	    private ObservableField<String> name; //ObservableField
	    public ObservableField<String> getName() {
	        return name;
	    }
	    public void setName(ObservableField<String> name) {
	        this.name = name;
	    }
	}

	ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
    User user = new User();
    final ObservableField<String>  name = new ObservableField<String>(); //有set和get方法
    name.set("lili");
    user.setName(name);
    binding.setUser(user);
    binding.setHandlers(new Handlers() {
        @Override
        public void onClick(View view) {
            Toast.makeText(MainActivity.this,"hh",Toast.LENGTH_SHORT).show();
           name.set("hahaha"); //调用ObservableField的set方法，自动更新界面
        }
    });


## 绑定AdapterView -- binding-collection-adapter ##	
使用官方API进行AdapterView绑定不方便，下面就来介绍一个比较好用的库binding-collection-adapter

	Github地址：https://github.com/evant/binding-collection-adapter

`build.gradle`文件(module目录下）里面dependencies添加

	compile 'me.tatarka:bindingcollectionadapter:0.16' 
	如果你要是用RecyclerView，还需要添加
	compile 'me.tatarka:bindingcollectionadapter-recyclerview:0.16'

**item 布局文件（必须先建，因为Activity布局文件需要ViewModel，ViewModel需要item布局文件）**

	<layout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:app="http://schemas.android.com/apk/res-auto">
	    <data>
	        <variable name="item" type="String"/>
	    </data>
	    <TextView
	        android:id="@+id/text"
	        android:layout_width="match_parent"
	        android:layout_height="wrap_content"
	        android:text="@{item}"/>
	</layout>

**ViewModel文件**

	public class ViewModel {
	  public final ObservableList<String> items = new ObservableArrayList<>();
	  public final ItemView itemView = ItemView.of(com.example.bindadapter.BR.item, R.layout.item);
	}

**Activity布局文件 -- app:items、app:itemView、app:layoutManager**

Then bind it to the collection view with `app:items` and `app:itemView`. There are also some convience factories to attach a LayoutManager to a RecyclerView with `app:layoutManager`.

	<layout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:app="http://schemas.android.com/apk/res-auto">
	    <data>
	      <variable name="viewModel" type="com.example.ViewModel"/> 
	      <import type="me.tatarka.bindingcollectionadapter.LayoutManagers" /> //RecyclerView需要
	    </data>
	
	    <ListView
	      android:layout_width="match_parent"
	      android:layout_height="match_parent"
	      app:items="@{viewModel.items}"
	      app:itemView="@{viewModel.itemView}"/>
	
	    <android.support.v7.widget.RecyclerView
	      android:layout_width="match_parent"
	      android:layout_height="match_parent"
	      app:layoutManager="@{LayoutManagers.linear()}"
	      app:items="@{viewModel.items}"
	      app:itemView="@{viewModel.itemView}"/>
	
	    <android.support.v4.view.ViewPager
	      android:layout_width="match_parent"
	      android:layout_height="match_parent"
	      app:items="@{viewModel.items}"
	      app:itemView="@{viewModel.itemView}"/>
	
	    <Spinner
	      android:layout_width="match_parent"
	      android:layout_height="match_parent"
	      app:items="@{viewModel.items}"
	      app:itemView="@{viewModel.itemView}"
	      app:dropDownItemView="@{viewModel.dropDownItemView}"/>
	</layout>

**Activity文件**

	ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
    ViewModel viewModel = new ViewModel();
    binding.setViewModel(viewModel);
    for (int i = 0; i < 20; i++) {
        viewModel.items.add("" + i);//自动刷新界面20次
    }

## Multiple View Types ##

多种样式的布局，那么就需要把`ItemView`换成`ItemViewSelector`

	public final ItemViewSelector<String> itemView = new BaseItemViewSelector<String>() {
	    @Override
	    public void select(ItemView itemView, int position, String item) {
	        itemView.set(BR.item, position == 0 ? R.layout.item_header : R.layout.item);
	    }
	    @Override
	    public int viewTypeCount() {
	      return 2;
	    }
	};

- select方法会被多次重复调用，不要处理复杂逻辑

- viewTypeCount方法仅ListView需要复写，RecyclerView 和 ViewPager 不需要

- 不需要绑定变量到itemView布局中（如静态header/footer等），可以使用 `ItemView.BINDING_VARIABLE_NONE` 做绑定变量

## 自定义属性绑定 -- 绑定ListView EmptyView ##

正常情况下，Data Binding Library会根据属性名去找对应的set/get方法。如上面的android:text="@{user.name}"、app:items="@{viewModel.items}"。

但是我们有时候需要自定义一些属性，Data Binding Library也提供了很便利的方法让我们来实现。比如我们想在layout文件里面设置ListView的emptyView

**Activity布局文件**

	<layout xmlns:android="http://schemas.android.com/apk/res/android"
	    xmlns:app="http://schemas.android.com/apk/res-auto">
	    <data>
	        <variable
	            name="viewModel"
	            type="com.example.databinding.viewmodel.ViewAlbumsViewModel"/>
	    </data>
	    <LinearLayout
	        android:layout_width="match_parent"
	        android:layout_height="match_parent"
	        android:paddingLeft="10dp"
	        android:paddingRight="10dp"
	        android:orientation="vertical">
	        <ListView
	            android:layout_width="fill_parent"
	            android:layout_height="0px"
	            android:layout_weight="1.0"
	            app:items="@{viewModel.albums}"
	            app:itemView="@{viewModel.itemView}"
	            app:emptyView="@{@id/empty_view}" //引用了下面定义的TextView。注意这种引用方法
	            android:onItemClick="@{viewModel.viewAlbum}"
	            android:id="@+id/albumListView"/>
	        <TextView
	            android:id="@+id/empty_view" //EmptyView，定义了id
	            android:layout_width="fill_parent"
	            android:layout_height="0px"
	            android:layout_weight="1.0"
	            android:gravity="center"
	            android:text="@string/albums_list_empty" />
	    </LinearLayout>
	</layout>

**实现代码**

	@BindingAdapter("emptyView")
	public static <T> void setEmptyView(AdapterView adapterView, int viewId) {
	    View rootView = adapterView.getRootView();
	    View emptyView = rootView.findViewById(viewId);
	    if (emptyView != null) {
	        adapterView.setEmptyView(emptyView);
	    }
	}

第二个参数int viewId就是app:emptyView属性传进来的值，上面的layout可以看出来它就是R.id.empty_view，然后通过id找到控件，然后调用AdapterView原始的setEmptyView来设置

## 标准MVVM实例 ##

	MVVM设计模式及实例--查询 IP 地址归属地 https://github.com/celesteshire/MVVMDemo

**XML**

	<layout xmlns:android="http://schemas.android.com/apk/res/android">
	  <data>
	    <variable
	        name="viewModel"
	        type="com.shire.mvvmdemo.viewModel.MainViewModel"
	        />
	  </data>
	  <RelativeLayout
	      android:layout_width="match_parent"
	      android:layout_height="match_parent"
	      android:paddingBottom="@dimen/activity_vertical_margin"
	      android:paddingLeft="@dimen/activity_horizontal_margin"
	      android:paddingRight="@dimen/activity_horizontal_margin"
	      android:paddingTop="@dimen/activity_vertical_margin"
	      >
	
	    <EditText
	        android:id="@+id/et_ip"
	        android:layout_width="200dp"
	        android:layout_height="wrap_content"
	        android:hint="IP地址"
	        />
	    <Button
	        android:id="@+id/btn_search"
	        android:layout_width="200dp"
	        android:layout_height="wrap_content"
	        android:layout_toRightOf="@id/et_ip"
	        android:onClick="@{viewModel.search}"
	        android:text="查询"
	        />
	    <TextView
	        android:id="@+id/tv_msg"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	        android:layout_below="@id/et_ip"
	        />
	    <ProgressBar
	        android:id="@+id/pb_load"
	        android:layout_width="wrap_content"
	        android:layout_height="wrap_content"
	        android:layout_below="@id/btn_search"
	        android:layout_toLeftOf="@id/btn_search"
	        android:visibility="gone"
	        style="?android:attr/progressBarStyleSmall"
	        />
	  </RelativeLayout>
	</layout>

**M**

	public class SearchModel {
		public void getIPaddressInfo(final String ipAddress, final onSearchListener onSearchListener) {
		...
	}

	public interface onSearchListener {
	  void onSuccess(IPAddress ipAddress);
	  void onError();
	}

**VM**

	public  class MainViewModel implements onSearchListener {
	  private ActivityMainBinding binding;
	  private SearchModel searchModel = new SearchModel();
	  private Handler handler;
	
	  public MainViewModel(ActivityMainBinding binding) {
	    this.binding = binding;
	    handler = new Handler(Looper.getMainLooper());
	  }
	
	  public void search(View view) {
	    binding.pbLoad.setVisibility(View.VISIBLE);
	    searchModel.getIPaddressInfo(binding.etIp.getText().toString().trim(), this);
	  }
	
	  @Override public void onSuccess(final IPAddress ipAddress) {
	    handler.post(new Runnable() {
	      @Override public void run() {
	        binding.pbLoad.setVisibility(View.GONE);
	        binding.tvMsg.setText(ipAddress.toString());
	      }
	    });
	  }
	
	  @Override public void onError() {
	    handler.post(new Runnable() {
	      @Override public void run() {
	        binding.pbLoad.setVisibility(View.GONE);
	        binding.tvMsg.setText("查询失败");
	      }
	    });
	  }
	}

**VM中不能持有Context对象（否则死的很惨）。解决方案是：持有View的引用，事件总线机制框架EvenBus之类**

	再见Presenter，你好ViewModel http://www.apkbus.com/thread-245056-1-1.html
	AndroidViewModel框架 https://github.com/inloop/AndroidViewModel

**Activity**

	ActivityMainBinding binding = DataBindingUtil.setContentView(this, R.layout.activity_main);
    binding.setViewModel(new MainViewModel(binding));

## MVP MVVM 不足 ##

**MVP**

MVP的问题在于，使用接口去连接view层和presenter层，这就导致一个逻辑复杂的页面，接口会有很多，十几二十个都不足为奇。维护接口的成本就会非常的大。

这个问题的解决方案就是你得根据自己的业务逻辑去斟酌着写接口。你可以定义一些基类接口，把一些公共的逻辑，比如网络请求成功失败，toast等等放在里面，之后你再定义新的接口的时候可以继承自那些基类，这样会好不少。

**MVVM**

MVVM的问题呢，其实和MVC有一点像。data binding框架解决了数据绑定的问题，但是ViewModel引用了View，从而导致ViewModel无法重用于其他View，view层还是会过重。（最上面的例子中，Activity中实现VM，VM有Activity引用）

## mvpvm ##

	https://github.com/googlesamples/android-architecture/tree/todo-databinding

View数据绑定VM，View事件绑定Presenter。

	<data>
        <variable
            name="task"
            type="com.example.android.architecture.blueprints.todoapp.data.Task" />

        <variable
            name="presenter"
            type="com.example.android.architecture.blueprints.todoapp.taskdetail.TaskDetailContract.Presenter" />
    </data>

**MVPVM: Model**

domain logic在这层

**MVPVM: View**

View对ViewModel不需要了解太多，这样才能保持两者的解耦，两者之间的协议只需要：

	ViewModel支持View需要展示的properties。
	View实现了ViewModel的观察者模式接口（如Listener）。

所以这里ViewModel到View是一条虚线，而不是MVVM中的双向实线

**MVPVM: Presenter**

Presenter到ViewModel是有耦合的，因为Presenter需要把model更新到ViewModel中，也就是map行为，然后调用View的对应接口进行binding。

Presenter是MVPVM中唯一不需要解耦的，它紧紧地与View、ViewModel、Model层耦合。如果你的Presenter被多个View重用了，那你可能需要考虑它是不是更应该作为一个module，比如（第三方）登陆。

**MVPVM: ViewModel**

大部分ViewModel一般没有field，而是通过暴露get方法来让data binding找到对应要显示的property，get方法中直接调用持有的model的对应属性get方法