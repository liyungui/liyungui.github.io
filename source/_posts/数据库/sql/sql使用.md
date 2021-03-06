---
title: SQL使用
date: 2018-12-20 15:47:53
categories:
  - 数据库
tags:
  - SQL
---

# SQL
 
**Structured Query Language**, 结构化查询语言

操作 关系型数据库（用表存储数据）的 标准 非过程性语言。

为加强SQL的语言能力，各厂商在实现标准中增加了过程性语言的特征。如Oracle的PL/SQL 过程性处理能力，SQL Server、Sybase的T-SQL
	
# 语法

	不区分大小写。推荐关键字大写，自定义的小写
	每条语句以分号结尾
	注释符号是 #

# 数据库服务器--数据库--表

数据库服务器有多个数据库组成，每个数据库有多个表。表中存储着数据。

一般一个工程项目对应一个数据库，一个JavaBean对应一个表。

元数据：数据库，表，列的定义信息

# 数据库服务器--mysql

要特别注意连接，备份命令是在cmd窗口执行，要注意和sql语句区分，是没有分号的。特别注意！！

## CentOS安装MySQL

CentOS 7上把MySQL从默认软件列表中移除了，用MariaDB来代替，所以我们必须要去官网上进行下载

	wget http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm 
	
	rpm -ivh mysql-community-release-el7-5.noarch.rpm
	
	yum -y install mysql mysql-server mysql-devel

## 启动MySQL

	service mysqld start
	
## 设置MySQL数据库服务器密码

	mysqladmin -u root password dbroot@quanlist2018
	
## 连接MySQL数据库服务器

	mysql -u root -p
	密码默认为空
	
## 允许用户远程连接

登录MySQL后

	grant all privileges on *.* to 'root'@'%' identified by 'dbroot@quanlist2018' with grant option;
	FLUSH PRIVILEGES;
	exit
	
	'root'@'%' identified by 'dbroot@quanlist2018'
	表示root用户可以在任意地址用密码dbroot@quanlist2018登录
	
		
## 备份与恢复数据库

- 备份数据库：连接mysql服务器前
	
		mysqldump -u root -p db_name>c:/1.sql

- 恢复数据库：必须要先创建数据库，然后导入备份的sql文件
				
		备份。在cmd窗口
			mysql -u root -p db_name<c:/1.sql
		恢复。在mysql窗口中（连接mysql服务器后）
			use db_name;
			source c:/1.sql;

## mysql中乱码的原因与解决

### 原因

客户端发送数据时使用的编码和服务器处理数据时使用的编码不相同

`show variables like 'character%';` 可以获得服务器使用的编码。%表示任意个字符，下划线_表示一个字符。 模糊匹配like。
			
### 解决方法

```
(1)set names xxxx; --- 连接后通知服务器和当前客户端进行交互时使用的编码集（每个客户端连接后都需要设置）
(2)修改服务器中的my.ini配置文件，修改服务器默认的客户端的编码
```
					
# 数据库

	1.创建数据库
		create database [if not exists] db_name [character set xxx] [collate xxx]
		*创建一个名称为mydb1的数据库。
			create database mydb1;
		*创建一个使用utf8（中间没有杆）字符集的mydb2数据库。
			create database mydb2 character set utf8;
		*创建一个使用utf8字符集，并带校对规则（校对规则是下划线连接）的mydb3数据库。
			create database mydb3 character set utf8 collate utf8_bin ;
	2.查看数据库
		show databases;查看所有数据库
		show create database db_name; 查看数据库的创建方式
	3.修改数据库
		alter database db_name [character set xxx] [collate xxxx]
	4.删除数据库
		drop database [if exists] db_name;
	5.使用数据库
		切换使用的数据库 use db_name; （数据库特有关键字，不用加database）
		查看当前使用的数据库 select database();注意不要忘了括号

# 表

## 创建表

```
create table tab_name(
	field1 type,
	field2 type,
	...
	fieldn type
)[character set xxx][collate xxx];
```

### 数据类型
		
java和mysql的数据类型比较

```
String  ----------------------  char(n) varchar(n) 注意是var+char。 
	定长是固定长度，自动补齐。变长是根据存储内容决定长度。
	但都不能超过定义长度n.定长胜在效率，变长胜在节省空间。
byte short int long float double -------------- tinyint  smallint int bigint float double。
	长度分别	1		2		4	8		4		8字节
boolean ------------------ bit 0/1
Date ------------------ Date、Time、DateTime、timestamp
FileInputStream FileReader  ------------------------------ 大数据类型 Blob Text
字符和日期型数据应包含在单引号中
```

### 实例
				
创建一个员工表employee

```
create table employee(
	id int primary key auto_increment ,
	name varchar(20),
	gender bit default 1,
	birthday date,
	entry_date date,
	job varchar(20),
	salary double,
	resume text
);
```
				
### 约束

```
primary key 主键，不空切唯一。一般其后都紧跟着auto_increment 主键字段必须是数字类型(非数字无法自增长)。主键无法更改（更改主键，插入数据库就无法知道修改的列）
auto_increment只有主键可以自动增长	
unique
not null
外键约束，一般是和多表设计一起理解。看后面
```

## 查看表信息

```
show tables 查看当前数据库中的所有的表
show create table tab_name	查看当前数据库表建表语句 
desc tab_name 查看表结构。（表特有关键字，所以不用加table）
```

## 修改表

```
alter table add列/drop列/change列名/modify列类型/character set
rename table to  重命名表(不要忘记了to)
```

### 实例

```
*在上面员工表的基本上增加一个image列。
	alter table employee add image blob;
*修改job列，使其长度为60。
	alter table employee modify job varchar(60);
*删除gender列。
	alter table employee drop gender;
*表名改为user。
	rename table employee to user;
*修改表的字符集为utf8
	alter table user character set gbk; 
*列名name修改为username	
	alter table user change name username varchar(20);
```
				
### 删除表

`drop table tab_name;`
			
# 表记录(数据)

## 新增

增加一条记录 insert into values  其实可以用逗号分隔一次性插入多条记录。

```
insert into tab_name [(field1,filed2,.......)] 
values (value1,value2,.......)[,(value1,value2,...)];
	*values中的数据必须与列的排列位置相对应。
	*插入空值：不要把该列加入列列表  或  值写为null
	*如果要插入所有字段可以省写列列表，直接按表中字段顺序写值列表
		insert into tab_name values(value1,value2,......);
	*字符和日期型数据应包含在单引号中'zhang' '2013-04-20'

```

实例

使用insert语句向表中插入四个员工的信息

```
insert into emp (name,birthday,entry_date,job,salary) values ('张飞','1990-09-09','2000-01-01','打手',999);
insert into emp values (null,'黄忠',1,'1970-05-05','2001-01-01','战神',1000,null);
insert into emp values ('关羽','1989-08-08','2000-01-01','财神',9999)
	,('赵云','1991-07-07','2000-01-02','保安',888);
```

## 修改

修改表列记录 update  set

```
update tab_name set field1=expr1 [,field2=expr1] [where 语句]
	*SET子句指示要修改哪些列和要给予哪些值（可以是表达式，比如field+10，表示增加10）。
	*WHERE子句指定应更新哪些行。如没有WHERE子句，则更新所有的行。
	*where字句中可以使用：
		*比较运算符：	
			= > < >= <= <>  （不等于是<>,特别注意）
			between 10 and 20 值在10到20之间  
			in(10,20,3)值是10或20或30
			like '张pattern' pattern可以是%或者_，如果是%则表示任意多字符，此例中张三丰 张飞 张abcd ，如果是_则表示一个字符张_，张飞符合。
			is null		
		*逻辑运算符
			多个条件可以使用逻辑运算符 and or not
```

实例

```	
~将所有员工薪水修改为5000元。
	update employee set salary=5000;
~将姓名为’张飞’的员工薪水修改为3000元。
	update employee set salary=3000 where name = '张飞';
~将姓名为’关羽’的员工薪水修改为4000元,job改为ccc。
	update employee set salary=4000,job='ccc' where name='关羽';
~将刘备的薪水在原有基础上增加1000元。	
	update employee set salary=salary+1000 where name='刘备';
```

## 删除
			
删除表行操作 delete

```
delete from tab_name [where ....]
	*如果不跟where语句则删除整张表中的数据
	*delete只能用来删除一行记录，不能值删除一行记录中的某一列值（这是update操作）。
	*delete是删除表中选中的数据，表还在。删除表要 drop table
	truncate是删除表中所有数据。直接删除表，然后创建一张结构一样（具有相同列）的新表。这种删除不能在事务中恢复。
		当删除表中所有数据时，truncate比delete更高效。
```

实例

```
~删除表中名称为’张飞’的记录。
	delete from employee where name='张飞';
~删除表中所有记录。
	delete from employee;
~使用truncate删除表中记录。
	truncate employee;
```

## 查询
		
select 操作

### 基本查询

```
select [distinct] *|field1 [,field2] from tab_name

*表示查找所有列，也可以指定一个列列表明确指定要查找的列，
from指定从哪里筛选
distinct用来剔除重复行。

查询表中所有学生的信息。
select * from exam;
查询表中所有学生的姓名和对应的英语成绩。
select name,english from exam;
过滤表中重复数据。
select distinct english from exam;
```

### 使用表达式和别名

select 也可以使用表达式，并且可以使用 as 别名 。（as可以省略，直接空格跟别名）

```
在所有学生分数上加10分特长分显示。
select name,english+10,chinese+10,math+10 from exam;
统计每个学生的总分。
select name,english+chinese+math from exam;
使用别名表示学生总分。
select name,english+chinese+math as 总成绩 from exam;
select name,english+chinese+math 总成绩 from exam;
select name english from exam;这个很容易出错。其实是省略as的别名。
```

### where过滤

使用where子句，进行过滤查询。

实际应用中，where子句都是动态构造的。

多条件查询构造sql技巧，where 1=1 and ......

```
~查询英语成绩大于90分的同学
	select name,english from exam where english > 90;
~查询总分大于230分的所有同学
	select name 姓名,english+chinese+math 总成绩 from exam where english+chinese+math>230;
~查询英语分数在 80－100之间的同学。
	select * from exam where english between 80 and 100;
~查询数学分数为75,76,77的同学。
	select * from exam where math in(75,76,77);
~查询所有姓张的学生成绩。
	select * from exam where name like '张%';
	select * from exam where name like '张_';
	select * from exam where name like '张__';
~查询数学分>70，语文分>80的同学。
	select * from exam where math>70 and chinese>80;
~查找缺考数学的学生的姓名
	select name from exam where math is null;
```

### order排序
			
`order by field [asc|desc]` 按指定列排序，可以是别名。
			
Asc 升序()默认、Desc 降序
			
```
对数学成绩排序后输出。
select * from exam order by math desc;
对总分排序按从高到低的顺序输出
select name ,(ifnull(math,0)+ifnull(chinese,0)+ifnull(english,0)) 总成绩 from exam order by 总成绩 desc;
对姓张的学生成绩排序输出
select name ,(ifnull(math,0)+ifnull(chinese,0)+ifnull(english,0)) 总成绩 from exam where name like '张%' order by 总成绩 desc;
```

null和任何数运算结果都为null

`ifnull(col,0)` 如果某列的值为null，用0替代

### 聚合

先不要管聚合函数要干嘛，先把要求的内容查出来再包上聚合函数即可。

```
~1.count(列) -- 统计符合条件的记录共有几条
	~统计一个班级共有多少学生？
		select count(*) from exam;
	~统计数学成绩大于70的学生有多少个？
		select count(*) from exam where math>70;
	~统计总分大于230的人数有多少？
		select count(name) from exam where math+english+chinese>230;
~2.sum(列) --Sum函数返回满足where条件的行的和
	~统计一个班级数学总成绩？
		select sum(math) from exam;	
	~统计一个班级语文、英语、数学各科的总成绩
		select sum(chinese),sum(english),sum(math) from exam;
	~统计一个班级语文、英语、数学的成绩总和
		select sum(ifnull(chinese,0)+ifnull(english,0)+ifnull(math,0)) 班级总分 from exam;
	~统计一个班级语文成绩平均分
		select sum(chinese)/count(name) from exam
~3.AVG --函数返回满足where条件的一列的平均值
	~求一个班级数学平均分？
		select avg(math) from exam;
	~求一个班级总分平均分？			
	select avg(ifnull(chinese,0)+ifnull(english,0)+ifnull(math,0)) 班级总分 from exam;
~4.MAX/MIN--函数返回满足where条件的一列的最大/最小值	
	~求班级最高分和最低分
	select max(ifnull(chinese,0)+ifnull(english,0)+ifnull(math,0)) 班级总分 from exam;
	select min(ifnull(chinese,0)+ifnull(english,0)+ifnull(math,0)) 班级总分 from exam;
```
	
### 分组 GROUP

```
~对订单表中商品归类后，显示每一类商品的总价
	select id,product,sum(price) from orders group by product;
```

### 分组后过滤 having

where 在最前面进行过滤，不能使用别名和聚合函数

having 在分组之后进行过滤，可以使用别名和聚合函数，having中用到的列，必须在前面使用过才可以用

```
~查询购买了几类商品，并且每类总价大于100的商品
	select product,sum(price) from orders group by product having sum(price)>100;
~查询单价小于100 但是总价大于100的商品。
	select product from orders where price<100 group by product having sum(price)>100;
```		

### 执行优先级

Mysql在执行sql语句时的执行顺序：**from where select group having order**

关于这个顺序，我们可以用**别名**来做一个判断

实例

```	
select math+english+chinese as 总成绩 from exam where 总成绩 >250; ---- 不成功
select math+english+chinese as 总成绩 from exam having 总成绩 >250; --- 成功
select math+english+chinese as 总成绩 from exam group by 总成绩 having 总成绩 >250; ----成功
select  math+english+chinese as 总成绩 from exam order by 总成绩;----成功
select * from exam as 成绩 where 成绩.math>85; ---- 成功
```		

# 嵌套查询

SQL语言中，一个 SELECT-FROM-WHERE 语句称为一个查询块。

**嵌套查询**：将一个查询块嵌套在另一个查询块的 WHERE 子句或 HAVING 短语的条件中的查询 

SQL语言允许多层嵌套查询，即一个子查询中还可以嵌套其他子查询。

注意：子查询的SELECT语句中不能使用 ORDER BY 子句，因为 ORDER BY 子句只能对最终查询结果排序。

## 带有IN谓词的子查询

查询与“刘晨”在同一个系学习的学生

`SELECT Sno,Sname,Sdept FROM Student WHERE Sdept IN (SELECT Sdept FROM Student WHERE Sname='刘晨');`

## 带有 EXISTS 谓词的子查询

带有EXISTS 谓词的子查询不返回任何数据，只产生逻辑真值“true”或逻辑假值“false”。

查询所有选修了1号课程的学生姓名

`SELECT Sname FROM Student WHERE EXISTS (SELECT * FROM SC WHERE Sno=Student.Sno AND Cno='1');`

# 多表设计 -- 外键约束
		
{% asset_img 外键.png %}

	1.创建表时指定约束：foreign key (dept_id) references dept(id)
			create table dept(
			id int primary key auto_increment,
			name varchar(30)
		);
		insert into dept values(null,'财务部');
		insert into dept values(null,'人事部');
		insert into dept values(null,'销售部');
		insert into dept values(null,'科技部');

		create table emp(
			id int primary key auto_increment,
			name varchar(30),
			dept_id int,
			foreign key (dept_id) references dept(id)
		);
		insert into emp values (null,'奥巴马',1);
		insert into emp values (null,'乔峰',2);	
		insert into emp values (null,'哈利波特',3);
		insert into emp values (null,'朴乾',4);
		insert into emp values (null,'萨达姆',4);

			

	2.外键约束：
			（1）增加外键：
				可以明确指定外键的名称，如果不指定外键的名称,mysql会自动为你创建一个外键名称。
				RESTRICT : 只要本表格里面有指向主表的数据， 在主表里面就无法删除相关记录。
				CASCADE : 如果在foreign key 所指向的那个表里面删除一条记录，那么在此表里面的跟那个key一样的所有记录都会一同删掉。
				alter table book add [constraint FK_BOOK] foreign key(pubid) references pub_com(id) [on delete restrict] [on update restrict];
			
			（2）删除外键
				alter table 表名 drop foreign key 外键（区分大小写，外键名可以desc 表名查看）;
				
				
	3.主键约束：
			（1）增加主键（自动增长，只有主键可以自动增长）primary key(id)
				Alter table tb add primary key(id) [auto_increment];
			（2）删除主键
				alter table 表名 drop primary key
			（3）增加自动增长
				Alter table employee modify id int auto_increment;
			（4）删除自动增长
				Alter table tb modify id int;		
	
	
	
--------------------------------------------------------------------------------------------------

# 多表设计

{% asset_img 多表设计.png %}

	一对一（311教室和20130405班级，两方都是一）:在任意一方保存另一方的主键
	一对多、多对一（班级和学生，其中班级为1，学生为多）：在多的一方保存一的一方的主键
	多对多（教师和学生，两方都是多）：使用中间表，保存对应关系
	
			create table orderitem(
				order_id varchar(100),
				product_id varchar(100),
				buynum int ,
				primary key(order_id,product_id), #联合主键,两列的值加在一起作为这张表的主键使用
				foreign key(order_id) references orders(id),
				foreign key(product_id) references products(id)
			);


--------------------------------------------------------------------------------------------------

# 多表查询

		create table dept(
				id int primary key auto_increment,
				name varchar(30)
			);
			insert into dept values(null,'caiwu');
			insert into dept values(null,'renshi');
			insert into dept values(null,'xingzheng');

			create table emp(
				id int primary key auto_increment,
				name varchar(30),
				dept_id int
			);
			insert into emp values (null,'cw',1);
			insert into emp values (null,'rs',2);	
			insert into emp values (null,'xx',5);
		
		
		mysql> select * from dept;
			+----+-----------+
			| id | name      |
			+----+-----------+
			|  1 | caiwu     |
			|  2 | renshi    |
			|  3 | xingzheng |
		mysql> select * from emp;
			+----+------+---------+
			| id | name | dept_id |
			+----+------+---------+
			|  1 | cw   |       1 |
			|  2 | rs   |       2 |
			|  3 | xx   |       5 |
			+----+------+---------+
	
		1.笛卡尔积查询：两张表中一条一条对应的记录，m条记录和n条记录查询，最后得到m*n条记录，其中很多错误数据
			select * from dept,emp;
		
			mysql> select * from dept,emp;
					+----+-----------+----+------+---------+
					| id | name      | id | name | dept_id |
					+----+-----------+----+------+---------+
					|  1 | caiwu     |  1 | cw   |       1 |
					|  2 | renshi    |  1 | cw   |       1 |
					|  3 | xingzheng |  1 | cw   |       1 |
					|  1 | caiwu     |  2 | rs   |       2 |
					|  2 | renshi    |  2 | rs   |       2 |
					|  3 | xingzheng |  2 | rs   |       2 |
					|  1 | caiwu     |  3 | xx   |       5 |
					|  2 | renshi    |  3 | xx   |       5 |
					|  3 | xingzheng |  3 | xx   |       5 |
					+----+-----------+----+------+---------+
		2.内连接：查询两张表中都有的关联数据,相当于利用条件从笛卡尔积结果中筛选出了正确的结果。
		inner join on
			select * from dept,emp      	  where dept.id=emp.dept_id;
			select * from dept inner join emp on dept.id=emp.dept_id;
		
			mysql> select * from dept,emp where dept.id=emp.dept_id;
					+----+--------+----+------+---------+
					| id | name   | id | name | dept_id |
					+----+--------+----+------+---------+
					|  1 | caiwu  |  1 | cw   |       1 |
					|  2 | renshi |  2 | rs   |       2 |
			mysql> select * from dept inner join emp on dept.id=emp.dept_id;
					+----+--------+----+------+---------+
					| id | name   | id | name | dept_id |
					+----+--------+----+------+---------+
					|  1 | caiwu  |  1 | cw   |       1 |
					|  2 | renshi |  2 | rs   |       2 |
					+----+--------+----+------+---------+
		3.外连接
			（1）左外连接：在内连接的基础上增加左边有右边没有的结果
			left join on
						mysql> select * from dept left join emp on dept.id=emp.dept_id;
								+----+-----------+------+------+---------+
								| id | name      | id   | name | dept_id |
								+----+-----------+------+------+---------+
								|  1 | caiwu     |    1 | cw   |       1 |
								|  2 | renshi    |    2 | rs   |       2 |
								|  3 | xingzheng | NULL | NULL |    NULL |
								+----+-----------+------+------+---------+
			（2）右外连接：在内连接的基础上增加右边有左边没有的结果
			right join on
						mysql> select * from dept right join emp on dept.id=emp.dept_id;
								+------+--------+----+------+---------+
								| id   | name   | id | name | dept_id |
								+------+--------+----+------+---------+
								|    1 | caiwu  |  1 | cw   |       1 |
								|    2 | renshi |  2 | rs   |       2 |
								| NULL | NULL   |  3 | xx   |       5 |
								+------+--------+----+------+---------+
				
			（3）全外连接：在内连接的基础上增加左边有右边没有的和右边有左边没有的结果
			full join on  --mysql不支持全外连接
				left join on
				union
				right join on ;--mysql可以使用此种方式间接实现全外连接
				
				mysql> select * from dept left join emp on dept.id=emp.dept_id
					-> union
					-> select * from dept right join emp on dept.id=emp.dept_id;
						+------+-----------+------+------+---------+
						| id   | name      | id   | name | dept_id |
						+------+-----------+------+------+---------+
						|    1 | caiwu     |    1 | cw   |       1 |
						|    2 | renshi    |    2 | rs   |       2 |
						|    3 | xingzheng | NULL | NULL |    NULL |
						| NULL | NULL      |    3 | xx   |       5 |
						+------+-----------+------+------+---------+


# 分页查询 limit

		逻辑分页：检索出所有数据存到集合中，需要时从集合中拿
			优点：一次查询，多次使用。减少数据库访问
			缺点：数据过大占内存，数据更新有延迟
		物理分页：只检索需要的数据
					不同数据库有不同的物理分页指令，mysql是limit startIndex,count （索引编号从0开始）
							select * from customer limit 0,1; 从表中第一条数据开始取一条记录。
							
# 创建用户

				create user estore identified by 'estore';
			授权：
				grant all on estore.* to estore;