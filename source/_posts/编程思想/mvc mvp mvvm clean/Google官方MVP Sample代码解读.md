---
title: Google官方MVP Sample代码解读
date: 2019-01-14 09:07:56
categories:
  - 编程思想
tags:
  - 编程思想
---

[Google官方MVP Sample代码解读](http://www.cnblogs.com/mengdd/p/5988104.html)

[Android官方MVP架构解读](http://blog.csdn.net/ljd2038/article/details/51477475)

[一个简单项目（反馈页面）搞定 MVP + Mockito进行单元测试 + Espresso进行UI测试，配详细介绍文档](https://github.com/boredream/DesignResCollection/tree/master/DesignResCollection_MVP)



# 项目结构分析 #

项目是一个备忘录。添加任务到待办任务列表。列表中标记任务已完成，任务详细页面修改任务内容，统计已完成的任务和未完成的任务数量。 

![](http://img.blog.csdn.net/20160522165007677)

- 一个源码目录 `mian` ，四个测试目录 `androidTest` `androidTestMock` `mock` `test` 。

- 代码分包结构

	- 四个功能包：
		- 任务的添加编辑(addedittask)。包内一般有类：xxActivity,xxFragment,xxPresenter,xxContract。`Presenter层`与`View层`
		- 任务完成情况的统计(statistics)
		- 任务的详情(taskdetail)
		- 任务列表的显示(tasks)。
	- data包。数据源，数据库读写，网络请求，MVP架构中的 `Model层`。
	- util包。工具类。
	- 在最外层存放了两接口BasePresenter和BaseView。Presenter层接口和View层接口的基类，项目中所有的Presenter接口和View层接口都继承自这两个接口。 

# MVP架构实现 #

## Model层的实现 ##

### public interface TasksDataSource ###
	
	/**
	 * For simplicity, only getTasks() and getTask() have callbacks.Consider adding callbacks to other methods
	 */
	public interface TasksDataSource {
		void getTasks(@NonNull LoadTasksCallback callback);
		void getTask(@NonNull String taskId, @NonNull GetTaskCallback callback);
		void saveTask(@NonNull Task task);
		void completeTask(@NonNull Task task);//标记为已完成
		void completeTask(@NonNull String taskId);
		void activateTask(@NonNull Task task);//标记为进行中
		void activateTask(@NonNull String taskId);
		void clearCompletedTasks();
		void refreshTasks();
		void deleteAllTasks();
		void deleteTask(@NonNull String taskId);

### local数据源 ###

	/**
	 * Concrete implementation of a data source as a db.
	 */
	public class TasksLocalDataSource implements TasksDataSource {

### remote数据源 ###

	/**
	 * Implementation of the data source that adds a latency simulating network.
	 */
	public class TasksRemoteDataSource implements TasksDataSource {


### 数据三级缓存 ###

	/**
	 * Concrete implementation to load tasks from the data sources into a cache.
	 * 
	 * For simplicity, this implements a dumb synchronisation between locally persisted data and data
	 * obtained from the server, by using the remote data source only if the local database doesn't
	 * exist or is empty.
	 */
	public class TasksRepository implements TasksDataSource {
		Map<String, Task> mCachedTasks;
		boolean mCacheIsDirty = false;

		/**
	     * Gets tasks from cache, local data source (SQLite) or remote data source, whichever is available first.
	     * 
	     * LoadTasksCallback#onDataNotAvailable() is fired if all data sources fail to get the data.
	     */
	    @Override
	    public void getTasks(@NonNull final LoadTasksCallback callback) {
	        checkNotNull(callback);
	
	        // Respond immediately with cache if available and not dirty
	        if (mCachedTasks != null && !mCacheIsDirty) {
	            callback.onTasksLoaded(new ArrayList<>(mCachedTasks.values()));
	            return;
	        }
	
	        if (mCacheIsDirty) {
	            // If the cache is dirty we need to fetch new data from the network.
	            getTasksFromRemoteDataSource(callback);
	        } else {
	            // Query the local storage if available. If not, query the network.
	            mTasksLocalDataSource.getTasks(new LoadTasksCallback() {
	                @Override
	                public void onTasksLoaded(List<Task> tasks) {
	                    refreshCache(tasks);
	                    callback.onTasksLoaded(new ArrayList<>(mCachedTasks.values()));
	                }
	
	                @Override
	                public void onDataNotAvailable() {
	                    getTasksFromRemoteDataSource(callback);
	                }
	            });
	        }
	    }

		private void getTasksFromRemoteDataSource(@NonNull final LoadTasksCallback callback) {
	        mTasksRemoteDataSource.getTasks(new LoadTasksCallback() {
	            @Override
	            public void onTasksLoaded(List<Task> tasks) {
	                refreshCache(tasks);
	                refreshLocalDataSource(tasks);
	                callback.onTasksLoaded(new ArrayList<>(mCachedTasks.values()));
	            }
	
	            @Override
	            public void onDataNotAvailable() {
	                callback.onDataNotAvailable();
	            }
	        });
	    }
	
	    private void refreshCache(List<Task> tasks) {
	        if (mCachedTasks == null) {
	            mCachedTasks = new LinkedHashMap<>();
	        }
	        mCachedTasks.clear();
	        for (Task task : tasks) {
	            mCachedTasks.put(task.getId(), task);
	        }
	        mCacheIsDirty = false;
	    }
	
	    private void refreshLocalDataSource(List<Task> tasks) {
	        mTasksLocalDataSource.deleteAllTasks();
	        for (Task task : tasks) {
	            mTasksLocalDataSource.saveTask(task);
	        }
	    }

实际使用的就是带三级缓存的数据源，它由手动实现的注入类Injection（该类在mock目录）提供:

	public class Injection {
	    public static TasksRepository provideTasksRepository(@NonNull Context context) {
	        checkNotNull(context);
	        return TasksRepository.getInstance(FakeTasksRemoteDataSource.getInstance(),
	                TasksLocalDataSource.getInstance(context));
	    }
	}

## contract ##

	public interface BasePresenter {
	    void start();
	}
	
	public interface BaseView<T> {
	    void setPresenter(T presenter);
	}
	
	public interface AddEditTaskContract {
	
	    interface View extends BaseView<Presenter> {
	
	        void showEmptyTaskError();
	
	        void showTasksList();
	
	        void setTitle(String title);
	
	        void setDescription(String description);
	
	        boolean isActive();
	    }
	
	    interface Presenter extends BasePresenter {
	
	        void createTask(String title, String description);
	
	        void updateTask( String title, String description);
	
	        void populateTask();
	    }
	}

## Presenter层的实现 ##

	/**
	 * Listens to user actions from the UI ({@link AddEditTaskFragment}), retrieves the data and updates the UI as required.
	 */
	public class AddEditTaskPresenter implements AddEditTaskContract.Presenter, TasksDataSource.GetTaskCallback {

## View层的实现 ##

- View的实现是在Fragment中
- 而在Activity中则是完成对Fragment的添加，Presenter的创建

		// Create the presenter
        mAddEditTaskPresenter = new AddEditTaskPresenter(
                taskId,
                Injection.provideTasksRepository(getApplicationContext()),
                addEditTaskFragment,
                shouldLoadDataFromRepo);

- 官方对于采用Fragment的原因给出了两种解释。
	- 通过Activity和Fragment分离非常适合对于MVP架构的实现。Activity作为全局控制者将Presenter与View联系在一起。
	- 采用Fragment更有利于平板电脑的布局或者是多视图屏幕。

# 单元测试 #

- MVP模式的主要优势就是便于为业务逻辑加上单元测试.

- 本例子中的单元测试是给TasksRepository和四个feature的Presenter加的.

- 单元测试的目录是  `mock` `test`

- 单元测试使用的是 Junit + [mockito](http://site.mockito.org/)

依赖配置

	repositories { jcenter() }
	dependencies { testCompile "org.mockito:mockito-core:1.+" }

Presenter的单元测试, Mock了View和Model, 测试调用逻辑, 如:

	/**
	 * Unit tests for the implementation of {@link AddEditTaskPresenter}.
	 */
	public class AddEditTaskPresenterTest {
	
	    @Mock
	    private TasksRepository mTasksRepository;
	
	    @Mock
	    private AddEditTaskContract.View mAddEditTaskView;
	
	    /**
	     * {@link ArgumentCaptor} is a powerful Mockito API to capture argument values and use them to
	     * perform further actions or assertions on them.
	     */
	    @Captor
	    private ArgumentCaptor<TasksDataSource.GetTaskCallback> mGetTaskCallbackCaptor;
	
	    private AddEditTaskPresenter mAddEditTaskPresenter;
	
	    @Before
	    public void setupMocksAndView() {
	        // Mockito has a very convenient way to inject mocks by using the @Mock annotation. To
	        // inject the mocks in the test the initMocks method needs to be called.
	        MockitoAnnotations.initMocks(this);
	
	        // The presenter wont't update the view unless it's active.
	        when(mAddEditTaskView.isActive()).thenReturn(true);
	    }
	
	    @Test
	    public void saveNewTaskToRepository_showsSuccessMessageUi() {
	        // Get a reference to the class under test
	        mAddEditTaskPresenter = new AddEditTaskPresenter(
	                null, mTasksRepository, mAddEditTaskView, true);
	
	        // When the presenter is asked to save a task
	        mAddEditTaskPresenter.saveTask("New Task Title", "Some Task Description");
	
	        // Then a task is saved in the repository and the view updated
	        verify(mTasksRepository).saveTask(any(Task.class)); // saved to the model
	        verify(mAddEditTaskView).showTasksList(); // shown in the UI
	    }

# UI 测试 #

Espresso，Google官方提供的Android UI自动化测试的框架
