---
title: CleanCode
date: 2019-01-14 08:56:53
categories:
  - 编程思想
tags:
  - 编程思想
---
## 第一章、 整洁代码 ##

我们一直需要整洁代码。 可预见的未来，自动化产生代码无法替代人工编写。

## 第二章、 有意义的命名 ##

## 2.2 名副其实 ##

名称应该答复了所有大问题。 为何存在，何用，如何用

如果名称需要注释类补充，就不是名副其实

实例： 消逝的时间，以日记

	elapsedTimeInDay;
	daysSinceCreation
	fileAgeInDay

## 2.3 避免误导 ##

- 避免留下误导的错误仙索。

	实例： 一组账号
		
		accountList 最好别用，即使真是List<Account>。List对程序员有特殊含义
		accounts 推荐使用

- 避免使用不同之处较小的名称

	现代IDE都能自动提示自动补全，假如相似的名称放在一起，不同之处较小，分清楚得花多少时间
	
## 2.4 做有意义的区分 ##

错误示例：

- a,b,c
- list1,list2
- Product,ProductInfo,ProductData
- name,nameString

## 使用读得出来的名称 ##

方便交流

## 2.6 使用可搜索的名称 ##

单字母名称和数字常量，都是无法搜索

MAX_COLUM_PER_PAGE 能搜索出来，常量 7 麻烦了

## 2.7 避免使用编码 ##

现在语言中使用编码，纯属多余的负担

### 2.7.1 匈牙利命名法 ###

windows c 语言 API 时代，程序员需要匈牙利命名法来帮助自己记住类型。

- 类型不好区分：整数句柄，长指针，void指针，string的几种实现（不同属性/用途）
- 编译器不做类型检查

### 2.7.2 成员前缀 ###

类和函数足够小，自然不需要 m_ 前缀来表明成员变量

现代IDE 都自动用高亮来 标识成员变量

### 2.7.3 接口和实现 ###

用户根本不需要知道这个是接口。

我说如果，一定要选一个编码的话，宁愿选择给实现编码。

## 2.8 避免思维映射 ##

不要让读者非得把你的名称映射/翻译为他们熟知的名称。 明确是王道

## 2.9 类名 ##

- 类名应是名词/名词短语。

		Address，AddressParser

- 避免使用Manager，Processor，Data，Info。 出现说明类过大/命名不明确

## 2.10 方法名 ##

- 方法名应是动词

		deletePage，save

- 重载构造器是，使用静态工厂方法名

		Message.fromType(1) 好过 new Message(1);

## 2.11 别扮可爱 ##

别为了扮可爱，用一些不好理解的词命名

## 2.12 每个概念对应一个词 ##

给每个抽象概念选一个词，并一以贯之。

错误范例： 

- 使用 `fetch` , `retrive`, `find`, `get` 来给查询命名，怎么记得住哪个类中用哪个方法呢
- `controller` , `manager` , `driver`

## 2.13 别用双关语（一个词用于多个概念/目的） ##

`add` 用于多个场景/目的：

- 连接两个字符串。 `append` 就挺好
- 将一个对象放到集合中。 `insert` 可以

## 2.14 使用解决方案领域名称 ##

只有程序员才会读你的代码，放心地使用解决方案领域名称吧。

使用问题领域名称，难道你指望你的客户会跟你讨论代码。

## 2.15 使用源自所涉问题领域的名称 ##

如果实在不能用解决方案领域名称命名，那就用所涉问题领域名称吧。至少，负责维护的程序员就能去请教领域专家了。

## 2.16 添加有意义的语境 ##

多数名称都不能自我说明，需要良好命令的类、函数、名称空间来提供语境。如果没有，给名称添加前缀是最后一招了。

addressFirstName，addressState

# 第三章、函数 #

## 3.1 短小 ##

### 代码块和缩进 ###

代码块(if/else,while等)应该只有一行（调用函数），缩进层级不该多于两层。

## 3.2 只做一件事 ##

判断函数是否只做了一件事：能否再拆出一个函数

## 3.3 每个函数一抽象层级 ##

如何确保函数只做一件事：函数中的语句都在同一抽象层级上。

### 自顶向下 ###

每个函数后面紧跟位于下一抽象层级的函数（被调用的函数）

## 3.4 [switch语句](http://feikiss.iteye.com/blog/1454010) ##

即使只有两种条件的switch语句也比我想要的单个代码块或函数大得多。而switch天生要做N件事。

不幸我们总无法避开switch语句，我们可以**利用多态来确保每个switch都埋藏在较低的抽象层级，且永不重复**。

	public Money calculatePay(Employee e) thorws InvalidEmployeeType {  
	    switch(e.type)  {  
	       case COMMISSIONED:  
	            return calculateCommissionedPay(e);  
	       case HOURLY:  
	            return calculateHourlyPay(e);  
	       case SALARIED:  
	             return calculateSalariedPay(e);  
	       default:  
	             throw new InvalidEmployeeType(e.type);  
    }  

该函数问题：

- 首先，太长，当出现新的雇员时，它还会更长
- 其次，明显做了不止一件事。
- 第三，违反了单一权责原则，因为有好几个修改它的理由。
- 第四，违反了开-关原则，因为每当添加新的雇员类型时，就必须修改它。
- 最麻烦的，可能是到处皆有类似结构的函数。都需要重复同样的switch结构

	例如，可能会有： 

		isPayday(Employ e, Date date)  
		deliverPay(Employee e, Money pay)

解决方案：

将switch语句埋到抽象工厂底下，不让任何人看到。

使用switch语句为Employee的派生类创建适当的实体，而不同的函数，如calculatePay、isPayday和deliverPay等，则由Employee接口动态的调用相应子类方法。 

	public interface Employee{  
	    public boolean isPayday();  
	    public Money calculatePay();  
	    public void deliverPay(Money pay);  
	      
	} 
 
	public interface EmployeeFactory{  
	    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType;  
	} 
 
	public class EmployeeFactoryImpl implements EmployeeFactory{  
	    public Employee makeEmployee(EmployeeRecord r) throws InvalidEmployeeType{  
	        switch(r.type){  
	        case COMMISSIONED:  
	            return new CommissionedEmployee(r);  
	        case HOURLY:  
	            return new HourlyEmployee(r);  
	        case SALARIED:  
	            return new SalariedEmployee(r);  
	        default:  
	            throw new InvalidEmployeeType(r.type);  
	        }  
	    }  
	} 

## 3.5 使用描述性的名称  ##

名称描述函数做的事

## 3.6 函数参数 ##

尽量避免三个参数，有足够特殊的理由才能使用多参函数（三个参数以上）。

### 3.6.1 一元函数的普遍形式 ###

### 3.6.2 标识参数 ###

标识参数大声宣布，本函数不止做一件事。一定要避免。

### 3.6.3 二元函数 ###

### 3.6.4 三元函数 ###

### 3.6.5 参数对象 ###

如果函数确实需要两个以上的参数，说明应将一些参数封装为类了。

### 3.6.6 参数列表 ###

同类型的可变参数列表，其实可以算作一个参数（List类型的参数）

	public static String format(String format, Object... args)  二元函数

### 3.6.7 动词与关键词 ###

好名字的函数，能很好的解释函数意图、参数顺序和意图

- 动词

	一元函数。 函数名和参数名形成一种非常好的动词/名词形式

	- write(name) write的对象是name
	- writeField(name) 更好的名词，同时声明name是一个field

- 关键词

	把参数名称编码成函数名一部分，大大减轻记忆参数顺序的负担

	- assertExpectedEquasActual(expected，actual）

### 输出参数 ###

绝对不要使用输出参数。那是面向对象编程之前远古岁月的一个不得而为之的手段

## 3.7 无副作用 ##
 
副作用是一种谎言。做了函数名说明的事情之外的事，就是副作用。

函数承诺只做一件事，做其他被藏起来的事，这是破坏性的，会导致时序性耦合和顺序依赖

- 对类变量做出未能预期的改动
- 把变量搞成向函数传递的参数/系统全局变量

`public boolean checkPassword(userName, password)` 函数名只是校验密码，但是内部，当密码错误，却调用Session.initalize，这是非常致命的副作用。调用者冒着丢失现有会话数据的风险。时序性耦合令人迷惑，躲在函数副作用之后，就更难排查了。

## 3.8 分隔指令与查询 ##

函数只做一件事：

- 指令。修改对象
- 查询。查询对象

实例：

	public boolean set(key,value) 设置某个属性，成功返回true

	从读者角度考虑一下，if(set("username","bob")) 是什么含义：
		1. username属性值之前是否已经设置为bob
		2. username属性值设置为bob是否执行成功

	作者本意，set是动词，是指令函数。但在if语句块中，set像个形容词

解决方案：分隔指令与查询

	if(keyExists("username")){
		setKeyValue("username","bob");
	}

## 3.9 使用异常代替返回错误码 ##

指令函数返回错误码，违反分隔指令与查询规则。

返回错误码弊端：

- 要求调用者立刻处理错误
- 造成异常处理代码与正常逻辑混合在一起
- 导致多层嵌套
- 依赖磁铁。错误码通常是一个类，许多地方都导入和使用，该类修改会影响所有使用该类的类。使用异常码，新异常可以直接从异常基类派生出来

### 3.9.1 抽离 try/catch 代码块 ###

try/catch 把 错误处理代码与正常逻辑混合在一起

	try {
		deletePage(page);
		registry.deleteReference(page.name);
		configKeys.deleteKey(page.name.makeKey());
	}
	catch (Exception e) {
		logger.log(e.getMessage());
	}

抽离后

	public void delete(Page page) {
        try {
            deletePageAndAllReferences(page);
        } catch (Exception e) {
            logErrot(e);
        }
    }

    private void deletePageAndAllReferences(Page page) {
		deletePage(page);
		registry.deleteReference(page.name);
		configKeys.deleteKey(page.name.makeKey());
    }

    private void logErrot(Exception e) {

    }

### 3.9.2 错误处理就是一件事 ###

## 3.10 别重复自己 ##

消除系统中的重复代码。

重复代码导致一个改变影响多处代码，修改过程中非常有可能遗漏


# 第四章、 注释 #

注释承认自己代码表达能力的失败

注释不能美化糟糕的代码。

代码维护过程中，注释和代码分离是很常见的，大家维护的焦点就是代码，这时错误过时的注释，反而误导对代码的理解

## 第五章、格式 ##

## 第六章、 对象和数据结构 Objects and Data Structures ##

私有变量的理由：

- 保护数据
- 不被外部依赖，修改并不影响其他类

但是，为什么有那么多程序员给对象添加 setter和getter，就如同公共变量一般？

## 6.1 数据抽象 ##

抽象：隐藏实现。并不是简单的在变量间放上一个函数层（setter/getter），而是暴露抽象接口，以便用户无需了解数据的实现就能操作数据

实例：机动车燃料层

	public interface Vehicle {
        double getFuelTankCapacityInGallons(); //油箱容量，单位加仑
        double getGallonsOfGasoline(); //汽油量，加仑
    }
    
    public interface Vehicle{
        double getFuelRemainingPercent(); //燃料剩余百分比
    }

采用百分比抽象，无法确定Vehicle类中数据形态。

抽象并不是简单的setter/getter，而是以最好的方式呈现对象的数据

## 6.2 数据、对象的反对称性 Anti-Symmetry ##

数据结构和对象时对立的。

**对象和数据结构间的二分原理：**

- 数据结构：

	- 暴露数据，不提供有意义的函数。
	- **面向过程/方法**，不改动既有数据结构即可**添加新函数**，添加新数据结构得修改所有函数。（本身无方法，方法都在另一个类中）
	
- 对象：

	- 隐藏数据，暴露行为。
	- **面向对象**，不改动既有函数即可**添加新对象**，添加新函数所有对象都得修改。

优秀的开发者不带成见地了解两者，依据工作性质选择其中一种手段

代码：

- 数据结构-面向过程

		public class Square{
			public point topLeft;
			public double side;
		}
	
		public class Rectangle{
			public point topLeft;
			public double height;
			public double width;
		}
	
		public class Geometry{//几何
			public double area(Object shape){
				if(shape instanceOf Square){
					Square s = (Square) shape;
					return s.side * s.side;
				}else if(shape instanceOf Rectangle){
					Rectangle r = (Rectangle) shape;
					return r.height * r.width;
				}
				throw new NoSuchShapeException();
			}
		}

	- 想增加一个函数 perimeter 求周长，原有数据结构完全不受影响
	- 想添加一个新数据结构，就得修改 所有已有函数来处理新数据结构

- 对象-面向对象

		public interface Shape{
			double area();
		}

		public class Square implements Shape{
			public point topLeft;
			public double side;

			public double area(){
				return side * side;
			}
		}

		public class Rectangle implements Shape{
			public point topLeft;
			public double height;
			public double width;
			
			public double area(){
				return height * width;
			}
		}

	- 想增加一个函数 perimeter 求周长，原有对象都得修改实现该函数
	- 想添加一个新对象，原有函数都不会受影响

## 6.3 Law of Demeter ##

迪米特法则（Law of Demeter 简写LoD）又叫作最少知道原则（Least Knowledge Principle 简写LKP），就是说一个对象应当对其他对象尽可能少的了解,不和陌生人说话。talk only to your immediate friends

### “朋友”类型： ###

1. 当前对象本身（this）
2. 方法参量对象
3. 实例变量对象
4. 实例变量如果是一个聚集，那么聚集中的元素也都是朋友
5. 当前对象所创建的对象

[实例：老师让体育委员清点女生人数](http://www.cnblogs.com/silentjesse/p/3510966.html)

	public class Teacher{
		public void command(GroupLeader groupLeader）{
			List<Girl> girls = new ArrayList();
			for(int i = 0; i<20; i++){
				girls.add(new Girl());
			}
	
			groupLeader.countGirls(girls);
		}
	}

	public class GroupLeader{
		public void countGirls(List<Girl> girls){
			System.out.println("女生数量是：" + girls.size());
		}
	}

	public class Girl{}

	public class Client{
		public static void main(String[] args){
			Teacher teacher = new Teacher();
			teacher.commond(new GroupLeader());
		}
	}

存在的问题：

- Teacher 只有一个朋友类 GroupLeader。 Teacher 完全不知道自己依赖Girl，这违反LoD，应该把 List<Girl> girls 声明为成员变量
- Teacher 最少知道原则，完全不需要知道 Girl，所以即使 List<Girl> girls 声明为成员变量，还是违反 最少知道原则

修改：

	public class Teacher{
		public void command(GroupLeader groupLeader）{
			groupLeader.countGirls();
		}
	}

	public class GroupLeader{
		private List<Girl> girls
		
		public GroupLeader（List<Girl> girls）{
			this.girls = girls;
		}

		public void countGirls(){
			System.out.println("女生数量是：" + girls.size());
		}
	}

	public class Girl{}

	public class Client{
		public static void main(String[] args){
			List<Girl> girls = new ArrayList();
			for(int i = 0; i<20; i++){
				girls.add(new Girl());
			}

			Teacher teacher = new Teacher();
			teacher.commond(new GroupLeader(girls));
		}
	}

### [LoD 在设计中的应用](http://blog.csdn.net/lovelion/article/details/7563445) ###

最少知道原则：

- 尽量减少对象间的交互。 

	- 类耦合度越低，越利于复用
	- 可以通过引入一个合理的第三者来降低对象间的耦合度
	
- 尽量减少类的公共变量和公共方法。 处在松耦合中的类修改，不会对关联的类造成太大波及

实例：单击按钮(Button)，列表框(List)、组合框(ComboBox)、文本框(TextBox)、文本标签(Label)发生改变

- 存在的问题： 四个朋友类。扩展性差，不便于增加/删除控件
- 重构方案： 引入控件交互的中间类(Mediator调解人中介物)来降低界面控件之间的耦合度

![](http://my.csdn.net/uploads/201205/14/1336930673_6550.jpg)

## 6.4 数据传送对象 Data Transfer Objects ##

Data Transfer Objects（简写 DTO）：只有公共变量，没有方法的类，是最精练的数据结构。

非常有用的结构，尤其在通信场景中（数据库，网络等）

DTO 比 常用的 javaBean 更简洁

# 第七章、错误处理 #

## 7.1 使用异常而非返回码 ##

抛出异常代替返回错误码，这样调用代码很整洁，逻辑不会被错误错误处理搞乱

## 7.2 先写 Try—Catch-Finally 语句 ##

能帮你定义代码应该期待什么

## 7.3 使用不可控异常 unchecked exception ##

可控异常--每个方法的签名声明可能抛出的异常

可控异常违反 开放/闭合原则，低层方法异常的修改必将影响高层方法的签名。如果catch语句在抛出异常的方法三个层级之上，catch语句和抛出异常处之间的每个方法签名中声明该异常，这成本太高，不值票价。

## 7.4 给出异常发生的环境说明 ##

抛出的每个异常，须提供足够的环境说明，以便判断错误来源和处所

java的stack trace 无法告知异常的初衷

## 7.5 `依调用者需要`定义异常类 ##

定义异常类最重要的考虑：**异常该如何被捕获**

`没太理解` 例子是 封装一个抛出多种异常的三方API为一个自定义异常，从而整洁代码

## 7.6 定义常规流程 ##

遵循前文的建议，业务逻辑和错误处理会良好分离。

却把错误处理推到的程序边缘地带。封装三方API而抛出自定义的异常，只在最顶层处理错误。

但有时候，你可以不用抛出异常

下面的笨代码，计算 工资总数: `如果有餐食花费，计入总额，如果没有则获得每日标准餐补，计入总额`。

	try{
		MealExpenses expenses = expensesDAO.getMeals(employeeId);
		total += expenses.getTotal();
	}catch(MealExpensesNotFound e){
		total += getMealPerDiem(); //PerDiem allowance 按日补贴
	}

异常打断了义务逻辑。如果不用处理特殊情况，代码会整洁很多

实现方法是使用 **特例模式（Special Case Pattern）**。使用一个特例类封装异常，客户代码就不用处理异常了

具体到上例：expensesDAO.getMeals 总是返回 MealExpenses。若没有餐食花费，返回一个 餐食补贴的 MealExpenses 对象

	public class PerDiemMealExpenses implements MealExpenses{}

## 7.7 别返回null ##

随处可见的 null 检查，代码糟糕透了。

返回null，不如抛出异常。

特例对象是爽口良药。

如果三方API可能返回null，考虑重新封装，在新方法中抛异常或返回特例对象。

## 7.8 别传递null ##

返回null很糟糕，传递null更糟糕。

在定义方法时，使用@NotNull 注解

## 7.9 总结 ##

整洁代码要可读，也要强固。

可读与强固并不冲突。

分离业务逻辑和错误处理，就能写出可读而强固的整洁代码

# 第八章、边界 #

## 8.1 使用第三方代码 ##

接口提供者和接口使用者之间，存在与生俱来的张力。提供者追求普适性以吸引广泛用户，使用者追求集中满足特定需求。这种张力会导致系统边界上出现问题。

**以java.util.Map为例**

Map提供了丰富灵活的方法，但也要付出代价。

- Map中可以存放任何类型对象，访问对象时需要判断与转换类型。 `Sensor s = (Sensor) sensors.get(sendorId)`
- 当Map被修改时，所有用到Map的地方都要跟着修改。Java 5 加入泛型支持，的确见到很多系统都要做大量改动才能
- 超出控制。我们初衷可能不允许删除Map中的任何对象，但Map提供了删除接口

整洁方式

public class sensors{
	private Map<string,Sendor> sensors = new HashMap();
	
	public Sensor getById(String id){
		return sensors.get(id);
	}
}

边界接口（Map）是隐藏的。该接口封装后能适应业务的需要，易于理解，难以误用

## 8.2 浏览和学习边界 ##

学习第三方代码很难。整合第三方代码也很难。同时做这两件事难上加难。

更好的做法是，不要在生产代码中实验新东西，而是编写测试来遍览和理解第三方代码。即**学习型测试**。

## 8.3 学习log4j ##

Log4j是一个功能强大的日志组件,提供方便的日志记录

## 8.4 学习性测试的好处不只是免费 ##

学习性测试不光免费，还在投资上有正面的回报。

当第三方程序包发布了新版本，我们可以运行学习性测试，看看程序包的行为有没有改变。

无论你是否通过学习型测试来学习，总要有与生产代码调用方式一直的测试来支持整洁的边界。边界测试是减轻迁移劳力的有效方法。

## 8.5 使用尚不存在的代码 ##

还有另一种边界，那种将已知和未知分隔开的边界。在代码中总有许多地方是我们的知识未及之处。有时，边界那边就是未知的（至少目前未知）。有时，我们并不往边界那边看过去。

工作中，并发编程总是在边界接口未实现的情况下开始工作。自定义接口（模拟对依赖接口的封装）就很有用了

## 8.6 整洁的边界 ##

依赖你能控制的东西，好过依赖你控制不了的东西，免得日后受它控制。

可以像上文对象Map那样**包装**他们，也可以使用 **适配器模式（Adapter Pattern）**将我们的接口转换为第三方接口。

# 第十章、类 #

## 10.1 类的组织 ##

遵循自顶向下原则，让程序读起来像一篇报纸。

顺序：先静态，后实体；先公有，后私有；

私有函数应紧跟调用它的公有函数。

## 10.2 类应该短小 ##

**函数大小标准：代码行数；类大小标准：权责（Responsibility）数量**

**类名应当描述其权责**。命名正是帮组判断类长度的一个手段。如果无法为类精确命名，这个类大概就太长了。类中包括含义模糊的词（如Processor、Manager，Super）,说明有不恰当的权责聚集

### 10.2.1 单一权责原则 SRP ###

**类或模块应且只有一条加以修改的理由**。

鉴别权责（修改理由）常常帮助我们认识并创建更好的抽象

很多开发者害怕数量巨大的短小类会导致难以一目了然抓住全局。常常为了搞清一个功能而在类间跳来跳去。

问题是：抽屉中有许多定义和标记良好的小箱子，还是把工具随便扔到抽屉中，更容易组织管理呢？

**系统应由许多短小的类组成，而不是少量巨大的类组成。每个小类封装一个权责，只有一个修改的理由，并与其他类一起协同完成系统行为**

### 10.2.2 内聚 ###

类应该只有少量实体变量。通常而言，方法操作的变量越多，就越黏聚到类上。如果一个类中的每个变量都被每个方法所使用，则该类具有最大的内聚性。

一般来说，创建极大化内聚类是既不可取也不可能的；另一方面，我们希望内聚性保持在较高位置。

内聚性高，意味着类中的方法和变量互相依赖、互相结合成一个逻辑整体。

保持函数参数列表短小，有时会导致类实体变量增多。这时往往意味着需要拆分类，提高内聚性。

### 10.2.3 保持内聚性就会得到许多短小的类 ###

仅仅简单将大函数切割为小函数，而且保持函数参数简洁，会导致实体变量增多。比如，大函数用到4个变量，函数拆分后就得变成四个实体变量。

而这4个变量可能就2个方法使用了，这意味着丧失了内聚性。

如果就这2个方法需要共享变量，为什么不让它们拥有自己的类呢？当丧失了内聚性，就拆分它们为单独的类。将大函数拆分为小函数，往往也是拆分为小类的时机。程序会更多有组织结构。

#### 打印质数实例重构 ####

原程序只有一个大行数，简直一团糟。很深的缩进结构，冗余的变量，紧密耦合的结构

重构和原程序采用同样算法和机制，重构后程序被拆分为3个权责：

- PrimePrinter 主程序，权责是处理执行环境，因调用方式而改变，例如程序被转换为SOAP服务，该类会被影响
- PrimeGenerator 权责是生成质数列表，因质数算法而改变
- RowColumnPagePrinter 权责是格式化数字列表成固定行列的列表，因输出格式而改变

代码如下：

- PrimePrinter

		public class PrimePrinter {
		  public static void main(String[] args) {
		    final int NUMBER_OF_PRIMES = 1000;
		    int[] primes = PrimeGenerator.generate(NUMBER_OF_PRIMES);
		
		    final int ROWS_PER_PAGE = 50;
		    final int COLUMNS_PER_PAGE = 4;
		    RowColumnPagePrinter tablePrinter =
		      new RowColumnPagePrinter(ROWS_PER_PAGE,
		                               COLUMNS_PER_PAGE,
		                               "The First " + NUMBER_OF_PRIMES +
		                                 " Prime Numbers");
		
		    tablePrinter.print(primes);
		  }
		}

- PrimeGenerator

		public class PrimeGenerator {
		  private static int[] primes;
		  private static ArrayList<Integer> multiplesOfPrimeFactors;
		
		  protected static int[] generate(int n) {
		    primes = new int[n];
		    multiplesOfPrimeFactors = new ArrayList<Integer>();
		    set2AsFirstPrime();
		    checkOddNumbersForSubsequentPrimes();
		    return primes;
		  }
		
		  private static void set2AsFirstPrime() {
		    primes[0] = 2;
		    multiplesOfPrimeFactors.add(2);
		  }
		
		  private static void checkOddNumbersForSubsequentPrimes() {
		    int primeIndex = 1;
		    for (int candidate = 3;
		         primeIndex < primes.length;
		         candidate += 2) {
		      if (isPrime(candidate))
		        primes[primeIndex++] = candidate;
		    }
		  }
		
		  private static boolean isPrime(int candidate) {
		    if (isLeastRelevantMultipleOfNextLargerPrimeFactor(candidate)) {
		      multiplesOfPrimeFactors.add(candidate);
		      return false;
		    }
		    return isNotMultipleOfAnyPreviousPrimeFactor(candidate);
		  }
		
		  private static boolean
		  isLeastRelevantMultipleOfNextLargerPrimeFactor(int candidate) {
		    int nextLargerPrimeFactor = primes[multiplesOfPrimeFactors.size()];
		    int leastRelevantMultiple = nextLargerPrimeFactor * nextLargerPrimeFactor;
		    return candidate == leastRelevantMultiple;
		  }
		
		  private static boolean
		  isNotMultipleOfAnyPreviousPrimeFactor(int candidate) {
		    for (int n = 1; n < multiplesOfPrimeFactors.size(); n++) {
		      if (isMultipleOfNthPrimeFactor(candidate, n))
		        return false;
		      }
		    return true;
		  }
		
		  private static boolean
		  isMultipleOfNthPrimeFactor(int candidate, int n) {
		    return
		      candidate == smallestOddNthMultipleNotLessThanCandidate(candidate, n);
		  }
		
		  private static int
		  smallestOddNthMultipleNotLessThanCandidate(int candidate, int n) {
		    int multiple = multiplesOfPrimeFactors.get(n);
		    while (multiple < candidate)
		      multiple += 2 * primes[n];
		    multiplesOfPrimeFactors.set(n, multiple);
		    return multiple;
		  }
		}

- RowColumnPagePrinter

		public class RowColumnPagePrinter {
		  private int rowsPerPage;
		  private int columnsPerPage;
		  private int numbersPerPage;
		  private String pageHeader;
		  private PrintStream printStream;
		
		  public RowColumnPagePrinter(int rowsPerPage,
		                              int columnsPerPage,
		                              String pageHeader) {
		    this.rowsPerPage = rowsPerPage;
		    this.columnsPerPage = columnsPerPage;
		    this.pageHeader = pageHeader;
		    numbersPerPage = rowsPerPage * columnsPerPage;
		    printStream = System.out;
		  }
		  public void print(int data[]) {
		    int pageNumber = 1;
		    for (int firstIndexOnPage = 0;
		         firstIndexOnPage < data.length;
		         firstIndexOnPage += numbersPerPage) {
		      int lastIndexOnPage =
		        Math.min(firstIndexOnPage + numbersPerPage - 1,
		                 data.length - 1);
		      printPageHeader(pageHeader, pageNumber);
		      printPage(firstIndexOnPage, lastIndexOnPage, data);
		      printStream.println("\f");
		      pageNumber++;
		    }
		  }
		
		  private void printPage(int firstIndexOnPage,
		                         int lastIndexOnPage,
		                         int[] data) {
		    int firstIndexOfLastRowOnPage =
		      firstIndexOnPage + rowsPerPage - 1;
		    for (int firstIndexInRow = firstIndexOnPage;
		         firstIndexInRow <= firstIndexOfLastRowOnPage;
		         firstIndexInRow++) {
		      printRow(firstIndexInRow, lastIndexOnPage, data);
		      printStream.println("");
		    }
		  }
		
		  private void printRow(int firstIndexInRow,
		                        int lastIndexOnPage,
		                        int[] data) {
		    for (int column = 0; column < columnsPerPage; column++) {
		      int index = firstIndexInRow + column * rowsPerPage;
		      if (index <= lastIndexOnPage)
		        printStream.format("%10d", data[index]);
		    }
		  }
		
		  private void printPageHeader(String pageHeader,
		                               int pageNumber) {
		    printStream.println(pageHeader + " --- Page " + pageNumber);
		    printStream.println("");
		  }
		
		  public void setOutput(PrintStream printStream) {
		    this.printStream = printStream;
		  }
		}

## 10.3 为了修改而组织 ##

修改将一直持续。每次修改（打开类）都让系统冒着其他部分不能如期望工作的风险。整洁系统必须优化类的组织，降低修改带来的风险

### Sql类实例重构 ###

	public class Sql {
	  public Sql(String table, Column[] columns);
	  public String create();
	  public String insert(Object[] fields);
	  public String selectAll();
	  public String findByKey(String keyColumn, String keyValue);
	  public String select(Column column, String pattern);
	  public String select(Criteria criteria);
	  public String preparedInsert();
	  private String columnList(Column[] columns) 
	  private String valuesList(Object[] fields, final Column[] columns)
	  private String selectWithCriteria(String criteria) 
	  private String placeholderList(Column[] columns) 
	}

原程序存在的问题：

- 存在两个修改的理由，说明违反了SRP原则

	每当需要新增支持一种语句（如 update），必须“打开”类进行修改，风险随之而来，可能破坏类中其他代码，必须全面重新测试。

	每当需要更改select查询，也必须“打开”类进行修改。

- 内聚性不足

	存在类似 `selectWithCriteria`等 只与 `select` 有关的是有方法

如果该类无需增加update功能，就该不动Sql类。但是一旦打开了类，就应该马上修正设计方案

重构方案：

- 每个功能拆分为一个权责类。Sql为基类，每个功能都是一个子类。
- 私有方法放到被使用的类。valuesList方法只在insert中使用了，放到InsertSql中
- 公共私有方法放到工具类。Where 和 ColumnList

代码如下：

- Sql

		abstract public class Sql {
		   public Sql(String table, Column[] columns) {};
		   abstract public String generate();
		}

- CreateSql
		
		class CreateSql extends Sql {
		   public CreateSql(String table, Column[] columns) { super(table, columns); }
		   @Override public String generate() { return ""; }
		}

- InsertSql

		class InsertSql extends Sql {
		   public InsertSql(String table, Column[] columns, Object[] fields) { super(table, columns); }
		   @Override public String generate() { return ""; }
		   private String valuesList(Object[] fields, final Column[] columns) { return ""; }
		}

- Where
				
		class Where {
		   public Where(String criteria) {}
		   public String generate() { return ""; }
		}

- ColumnList
				
		class ColumnList {
		   public ColumnList(Column[] columns) {}
		   public String generate() { return ""; }
		}

当需要增加update是，只需新建UpdateSql类。

重构后的系统，符合单一权责原则SRP，符合 开闭原则OCP


### 隔离修改 ###

借助接口和抽象类隔离细节修改带来的影响。

依赖倒置原则DIP：类应当依赖于抽象，而不是依赖于具体细节。

# 第十一章、 系统 #

## 11.1 如何建造一个城市 ##

城市能够正常运转是因为城市演化出恰当的抽象等级和模块（供水系统、供电系统、交通、执法、立法等），各组件即便在不了解全局时，都能有效转转

本章讨论的就是如何在较高的抽象层级-系统层级 上保持整洁

## 11.2 将系统的构造和使用分开 ##

Separate Constructing a System from Using It

酒店建设时，先搭个框架，起重机升降机附着在外面，工人忙碌其间。建成后，起重机升降机都会消失，酒店变得整洁

