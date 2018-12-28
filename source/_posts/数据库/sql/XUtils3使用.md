---
title: XUtils3使用
date: 2018-12-21 09:00:53
categories:
  - 数据库
tags:
  - ORM
---

# 使用步骤 #
1. application中初始化框架 

		x.Ext.init(this);//初始化xutils
2. 获取DbManager.DaoConfig 对象

		DaoConfig daoConfig=XUtil.getDaoConfig();//默认DaoConfig
3. 获取DbManager对象，**操作数据库的对象**

		DbManager db = x.getDb(daoConfig); 

数据库里表的创建的时间，在涉及到这张表的操作时，会先判断当前的表是否存在，如果不存在，创建一张表，如果存在，进行相应的CRUD操作

	DbManager.DaoConfig daoConfig = new DbManager.DaoConfig()
            .setDbName(dbName)
            .setDbVersion(1)
            .setDbOpenListener(new DbManager.DbOpenListener() {
                @Override
                public void onDbOpened(DbManager db) {
                    db.getDatabase().enableWriteAheadLogging();// 开启WAL, 对写入加速提升巨大
                }
            })
            .setDbUpgradeListener(new DbManager.DbUpgradeListener() {
                @Override
                public void onUpgrade(DbManager db, int oldVersion, int newVersion) {
                }
            });

    dbManager = x.getDb(daoConfig);

## DbManager操作 ##
1. getDaoConfig 获取数据库的配置信息 
2. getDatabase 获取数据库实例 
3. saveBindingId、saveOrUpdate、save 插入数据的3个方法(保存数据) 

		如果主键id是自增长模式
		save完，object的id不改变（还是默认0），只有数据库中id自增长了
		saveBindingId，obje的id会自动赋值为数据库中的id值
		saveOrUpdate，判断id，如果一致就update，否则save
4. replace 只有存在唯一索引时才有用 慎重 
5. delete操作的4种方法(删除数据) 
6. update操作的2种方法(修改数据) 
7. find操作6种方法(查询数据) 
8. dropTable 删除表 
9. addColumn 添加一列 
10. dropDb 删除数据库

## 必须有主键 ##

**没有主键构建sql会报空指针**

	@Column(name = "id", isId = true)
    public long id;

**主键默认自动增长，无法赋值。若要赋值，将自动增长属性设为false**

	@Column(name = "taskId", isId = true, autoGen = false, property = "UNIQUE")
    public int taskId;

## 除了主键，至少需要另外一个列 ##

 	Caused by: android.database.sqlite.SQLiteException: near ")": syntax error (code 1): , while compiling: CREATE TABLE IF NOT EXISTS "followedquestion" ( "_id"INTEGER PRIMARY KEY, )

看到这个异常，逗号，想到可能是需要主键外的另一个列，加了一列，果然可以

## 多条件查询 ##

	communityMessage = DBHelp.getInstance().getDbManager().selector(CommunityMessage.class).where("communityId", "=", communityId).and(WhereBuilder.b("atUserId", "=", UserData.getUserId()).or("atUserId", "=", -1)).limit(1).orderBy(orderByColumName, true).findFirst();

	查找CommunityMessage表中指定communityId，而且(atUserId=本人id或=-1)的一条消息

## 实体支持继承 ##

实体 Animal

	@Table(name = "animal")
	public class Animal implements Serializable {
	    @Column(name = "id", isId = true, autoGen = true)
	    protected long id;
	
	    @Column(name = "name")
	    protected String name;
	
	    @Column(name = "type")
	    private String type;
	
	    public long getId() {
	        return id;
	    }
	
	    public void setId(long id) {
	        this.id = id;
	    }
	
	    public String getName() {
	        return name;
	    }
	
	    public void setName(String name) {
	        this.name = name;
	    }
	
	    public String getType() {
	        return type;
	    }
	
	    public void setType(String type) {
	        this.type = type;
	    }
	}

实体 Dog extends Animal
 
	@Table(name = "dog")
	public class Dog extends Animal {
	    @Column(name = "age")
	    private int age;
	
	    public int getAge() {
	        return age;
	    }
	
	    public void setAge(int age) {
	        this.age = age;
	    }
	}

代码

	DbManager.DaoConfig daoConfig = new DbManager.DaoConfig()
            .setDbName("test.db")
            .setDbVersion(1)
            .setDbOpenListener(new DbManager.DbOpenListener() {
                @Override
                public void onDbOpened(DbManager db) {
                    db.getDatabase().enableWriteAheadLogging();// 开启WAL, 对写入加速提升巨大
                }
            });
    DbManager dbManager = x.getDb(daoConfig);

	Animal animal = new Animal();//存入Animal表
    animal.setName("animal");
    animal.setType("small");

    Dog dog = new Dog();//存入Dog表
    dog.setName("dog");
    dog.setAge(13);
    dog.setType("big");

    Animal animalDog = new Dog();//存入Dog表
    animalDog.setName("animalDog");
    animalDog.setType("big");

    try {
        dbManager.save(animal);
        dbManager.save(animalDog);
        dbManager.save(dog);

        List<Animal> animals = dbManager.findAll(Animal.class);
        for (Animal a :
                animals) {
            Log.d("lyg", a.getName() + " " + a.getType());
        }


        List<Dog> dogs = dbManager.findAll(Dog.class);
        for (Dog d :
                dogs) {
            Log.d("lyg", d.getName() + " " + d.getType() + " " + d.getAge());
        }

    } catch (DbException e) {
        e.printStackTrace();
    }

结果：

	10-25 09:24:17.979 30810-30810/com.xuehu365.test D/lyg: animal small
	10-25 09:24:17.979 30810-30810/com.xuehu365.test D/lyg: animalDog big 0
	10-25 09:24:17.979 30810-30810/com.xuehu365.test D/lyg: dog big 13

结论：

	能多态将实体存入正确的表中。
	父类中所有字段都能继承下来（包括private字段）

# 常见错误

## 删除对象id为空异常

this entity's id value is null

报错如下：

	org.xutils.ex.DbException: this entity[class com.xuehu365.xuehu.model.BroadcastMessage]'s id value is null
       	at org.xutils.db.sqlite.SqlInfoBuilder.buildDeleteSqlInfo(SqlInfoBuilder.java:128)
       	at org.xutils.db.DbManagerImpl.delete(DbManagerImpl.java:253)
		at com.xuehu365.xuehu.utils.DBHelp.delete(DBHelp.java:103)

查看源码：

	public static SqlInfo buildDeleteSqlInfo(TableEntity<?> table, Object entity) throws DbException {
        SqlInfo result = new SqlInfo();

        ColumnEntity id = table.getId();
        Object idValue = id.getColumnValue(entity);

        if (idValue == null) {
            throw new DbException("this entity[" + table.getEntityType() + "]'s id value is null");
        }
        StringBuilder builder = new StringBuilder("DELETE FROM ");
        builder.append("\"").append(table.getName()).append("\"");
        builder.append(" WHERE ").append(WhereBuilder.b(id.getName(), "=", idValue));

        result.setSql(builder.toString());

        return result;
    }

原因：

	是从服务器返回的message对象，并没有id字段（json解析值为null）

解决方案：

	先用该对象的msgId从数据库查询到message对象，然后再调用delete方法