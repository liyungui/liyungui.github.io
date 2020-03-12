---
title: Android端架构_MVP-Clean架构
date: 2019-08-16 11:46:01
categories:
  - 编程思想
tags: 
	- 编程思想
---

# Activity跳转

Activity跳转是如何实现的

`BaseActivity` 持有 `Navigator`，Activity A 调用 Navigator 相应的跳转方法。

每个Activity 都需要提供启动自己的Intent，而不是由Navigator构造

```java
public class Navigator {
  public void navigateToUserList(Context context) {
    if (context != null) {
      Intent intentToLaunch = UserListActivity.getCallingIntent(context);
      context.startActivity(intentToLaunch);
    }
  }
}

public class UserListActivity extends BaseActivity {
  public static Intent getCallingIntent(Context context) {
    return new Intent(context, UserListActivity.class);
  }
}

navigator.navigateToUserList(this);//跳转到UserListActivity    
```

# 完整的渲染数据过程

以用户列表页为例

## presentation 表现层

### model

```java
public class UserModel {
}
```

### view

```java
public interface LoadDataView {
  void showLoading();

  void hideLoading();

  void showRetry();

  void hideRetry();

  void showError(String message);

  Context context();
}
```

```java
public interface UserListView extends LoadDataView {
  // Render a user list in the UI.
  void renderUserList(Collection<UserModel> userModelCollection);

  //View a UserModel profile/details.
  //Presenter call this when click a UserModel
  void viewUser(UserModel userModel);
}
```

```java
public class UserListFragment extends BaseFragment implements UserListView {
  UserListPresenter userListPresenter;
  
  @Override public void onViewCreated(View view, Bundle savedInstanceState) {
    super.onViewCreated(view, savedInstanceState);
    this.userListPresenter.setView(this);
    if (savedInstanceState == null) {
      this.loadUserList();
    }
  }
  
  @Override public void renderUserList(Collection<UserModel> userModelCollection) {
    if (userModelCollection != null) {
      this.usersAdapter.setUsersCollection(userModelCollection);
    }
  }

  @Override public void viewUser(UserModel userModel) {
    if (mActivity != null) {
      mActivity.navigator.navigateToUserDetails(mActivity, userModel.getUserId());
    }
  }
 
   //Loads all users.
  private void loadUserList() {
    this.userListPresenter.loadUserList();
  } 
}
```

### presenter

```java
public class UserListPresenter implements Presenter {

  private UserListView viewListView;

  private final GetUserList getUserListUseCase;
  private final UserModelDataMapper userModelDataMapper;

  public UserListPresenter(GetUserList getUserListUserCase,
      UserModelDataMapper userModelDataMapper) {
    this.getUserListUseCase = getUserListUserCase;
    this.userModelDataMapper = userModelDataMapper;
  }

  public void setView(@NonNull UserListView view) {
    this.viewListView = view;
  }
 
  private void showUsersCollectionInView(Collection<User> usersCollection) {
    final Collection<UserModel> userModelsCollection =
        this.userModelDataMapper.transform(usersCollection);
    this.viewListView.renderUserList(userModelsCollection);
  }
  
  private void getUserList() {
    this.getUserListUseCase.execute(new UserListObserver(), null);
  } 
  
  private final class UserListObserver extends DefaultObserver<List<User>> {//DisposableObserver继承rxjava2的DisposableObserver

    @Override public void onComplete() {
      UserListPresenter.this.hideViewLoading();
    }

    @Override public void onError(Throwable e) {
      UserListPresenter.this.hideViewLoading();
      UserListPresenter.this.showErrorMessage(new DefaultErrorBundle((Exception) e));
      UserListPresenter.this.showViewRetry();
    }

    @Override public void onNext(List<User> users) {
      UserListPresenter.this.showUsersCollectionInView(users);
    }
  }
}
```

## domain 领域层

### entity

```java
/**
 * Class that represents a User in the domain layer.
 */
public class User {
}
```

### interactor(use case)

```java
public class GetUserListUseCase extends UseCase<List<User>, Void> {
	//调用 data层的UserRepository
	//将可观察的用户列表，发射到上面presenter指定的观察者
}
```
 
## data 数据层

### entity

```java
/**
 * User Entity used in the data layer.
 */
public class UserEntity {
}
```

### repository

```java
/**
 * Interface that represents a Repository for getting {@link User} related data.
 */
public interface UserRepository {
}
```

#### datasource

```java
/**
 * Interface that represents a data store from where data is retrieved.
 */
public interface UserDataStore {
}

class CloudUserDataStore implements UserDataStore {
}

class DiskUserDataStore implements UserDataStore {
}

```

```java
/**
 * Factory that creates different implementations of {@link UserDataStore}.
 */
@Singleton
public class UserDataStoreFactory {
}
```

#### cache

```java
/**
 * An interface representing a user Cache.
 */
public interface UserCache {
}
```

#### net

```java
/**
 * RestApi for retrieving data from the network.
 */
public interface RestApi {
}
```

# Dagger2

是否使用，这个具体问题具体分析。更多内容参考 Dagger2 文档

# 参考&扩展

- [实例源码](https://github.com/android10/Android-CleanArchitecture)by Fernando Cejas (Fernando 大神)