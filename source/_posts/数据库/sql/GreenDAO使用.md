---
title: GreenDAO使用
date: 2018-12-21 09:04:53
categories:
  - 数据库
tags:
  - ORM
---

greendao
	orm--object relation mapping
	javabean -- orm -- sqlite
	
	官方Demo里共有六个工程目录，分别为：
	(1).DaoCore：库目录，即jar文件greendao-1.3.0-beta-1.jar的代码；
	(2).DaoExample：android范例工程；
	(3).DaoExampleGenerator：DaoExample工程的DAO类构造器，java工程；
	(4).DaoGenerator：DAO类构造器，java工程；
	(5).DaoTest、PerformanceTestOrmLite：其他测试相关的工程。
	我们关心的只是2和3.
	
	1.新建java工程（数据模型和dao 生成 工程）
	
	2.导入jar
		greendao-generator.jar
		freemarker.jar模版文件
	
	3.设计表结构
	
	4.数据模型化 和 生成dao
		实例化 schema
		创建添加entity  -- 可持久化的对象，一个实体关联 一张表
		为entity添加属性(关于主键，一般是自己指定一个任意类型属性。不想指定就用addIdProperty())
		生产 new DaoGenerator().generateAll()
			Schema schema = new Schema(1, "com.baiyz.medicchat.dao"); 
			//Schema(int version, String defaultJavaPackage) version用于标识更新db，package是生产的Java文件所在包名
			//还可以设置（dao和test单独放于一个包下，默认是放在schema定义的实体包下）
				schema.setDefaultJavaPackageDao(defaultJavaPackageDao)
				schema.setDefaultJavaPackageTest(defaultJavaPackageTest)
				schema.enableKeepSectionsByDefault();//设置可以在实体中保留自定义代码
				
			Entity note= schema.addEntity("Note");
			
			note.addIdProperty(); //hospital.addIdProperty().autoincrement().primaryKey();一般加上主键和自增长属性
			note.addStringProperty("text").notNull();
			note.addStringProperty("comment");
			note.addDateProperty("date");
			
			new DaoGenerator().generateAll("../medichat/src", schema); 
			//generateAll(Schema schema, String outDir) 输出到那个文件目录（一般写我们使用该dao的Android工程目录，不用自己手动拷贝）
		
	5.把greendao.jar，生成的object和objectDao 拷贝到Android工程 （example是 Note.java 和 NoteDao.java ）
	6.开始使用
		使用前先了解一下 核心类
			DaoMaster：以一定的模式持有数据库对象（SQLiteDatabase）并管理一些DAO类（而不是对象）。
			DaoSession：管理指定模式下所有可用的DAO对象，你可以通过某个get方法获取到。
				DaoSession提供一些通用的持久化方法，比如对实体进行插入，加载，更新，刷新和删除。
				最后DaoSession对象会跟踪identity scope，更多细节，可以参看 session文档。
			DAOs（Data access objects）: 数据访问对象，用于实体的持久化和查询。
				对于每一个实体，greenDao会生成一个DAO，相对于DaoSession它拥有更多持久化的方法，比如：加载全部，插入
			Beans，每个实体都会生成一个bean
			
		DevOpenHelper helper = new DaoMaster.DevOpenHelper(this, "notes-db", null); //"notes-db"会作为数据库名字，
        db = helper.getWritableDatabase();		
        daoMaster = new DaoMaster(db);
		
        daoSession = daoMaster.newSession();
		
        noteDao = daoSession.getNoteDao();
		
		1.添加一个新的note到数据库中：
			Note note = new Note(null, noteText, comment, new Date());
			noteDao.insert(note);
			Log.d("DaoExample", "Inserted new note, ID: " + note.getId());
			该示例只是创建并插入了一个java对象。但insert方法返回的时候，数据库的ID已经分发到了刚插入的Note对象上了。在log中可以看到。

		2.删除一条note：非常简单明，在onListItemClick方法中可以看到
			noteDao.deleteByKey(id);
		3.你也可以看一下其它的DAO方法：loadAll、update。
			
		4.条件查询	
		注意：每次查询必须新建一个queryBuilder，否则会导致数据不更新的bug（数据一直不变）
			QueryBuilder.where(WhereCondition arg0, WhereCondition... arg1)
			 /**通过医院name获得医院id 失败返回-1*/
			public int getHospitalIdByName(String name){
				QueryBuilder<Hospital> qb=this.queryBuilder();
				qb.where(Properties.HospitalName.eq(name));
				if(qb.list().size()>0){
					return qb.list().get(0).getHospitalId();
				}
				return -1;
			}
	
	继承类和接口、序列化
		greendao的 实体 也支持 继承、接口、序列化
		实体可以继承其他类和接口。
		但是千万不要试图 继承另一个实体，期望获得另一个实体的字段，
		这会造成跨表，需要到父实体表中查询字段
		通常，使用接口作为实体属性和行为的通用基类是比较好的。
		比如：一个实体A和B共享了一套属性，这些属性可以定义在C中。下面是一个序列化B的列子：
		其父类可以通过setSuperclass，其父类可以通过setSuperclass(String)方法指定，
			myEntity.setSuperclass("MyCommonBehavior");

			entityA.implementsInterface("C");
			entityB.implementsInterface("C");
			
			entityB.implementsSerializable();

	保持段落独（Keep sections 保持自定义的代码不会被覆盖，只在实体中有效，实体dao不会起效，没有keep段）
		实体类在每一次生成器运行的时候都会被覆盖。
		greenDao允许添加自定义的代码到实体，通过“keep” 
		schema.enableKeepSectionsByDefault()设置对所有实体有效，允许保留自定义的代码不被覆盖
		或者hospital.setHasKeepSections(new Boolean(true))。对该实体单独生效，设置有保留段落为true
		一旦使用，3个独立的部分会在实体中生成：

		// KEEP INCLUDES - put your custom includes here
		// KEEP INCLUDES END
		...
		// KEEP FIELDS - put your custom fields here
		// KEEP FIELDS END
		...
		// KEEP METHODS - put your custom methods here
		// KEEP METHODS END

	注意，不要修改KEEP注释。在该范围的代码会在代码重新生成的时候不被覆盖。
	这个功能实在鸡肋，dao本来就功能少，还不能保留自定义代码，只能定义在实体中（不合封装逻辑）
	
	表在什么时候如何创建？
		OpenHelper extends SQLiteOpenHelper的onCreate()中创建所有的表