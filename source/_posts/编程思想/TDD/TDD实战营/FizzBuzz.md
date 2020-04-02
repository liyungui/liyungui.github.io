---
title:  FizzBuzz
date: 2020-03-31 22:36:53
categories:
  - TDD
tags:
  - TDD
---

# 项目介绍

FizzBuzz是个非常简单的数字游戏题。

通过对简单题目的多次练习，帮助学员逐渐养成正确的开发习惯，形成刻意练习的节奏。

# 教学目标

- 掌握测试驱动开发基本节奏
- 至少练习3遍FizzBuzz题目
- 能在10分钟内完成FizzBuzz题目

# 能力目标

- 键盘编程（不准动鼠标）。掌握IDE的快捷键操作，充分利用代码生成
- 用JUnit编写单元测试
- 测试驱动开发。编写失败的测试，驱动出产品代码
- 刻意练习的节奏

# JUnit

## Test

```java
@Test
public void testN() {
    assertEquals("1", FizzBuzz.printValue(1));
}
```

## 测试异常    

### `try-catch`

```java
@Test
public void testN() {
    try {
        FizzBuzz.printValue(0);
        fail("No exception thrown.");//没有抛出异常，使测试失败
    } catch (Exception e) {
	 	//断言异常类型
        assertTrue(e instanceof IllegalArgumentException);
        //断言异常message
        assertTrue(e.getMessage().contains("input must be > 0"));
    }
}
```

**缺陷** ：给出的**失败提示不够直接**，需要分析堆栈，测试方法在哪一行失败了

```
没有如预期抛出异常，提示信息：
java.lang.AssertionError: No exception thrown.
	at org.junit.Assert.fail(Assert.java:91)
	at com.lyg.fizz.FizzBuzzTest.testN(FizzBuzzTest.java:13)
------------------------
异常的message 不符合预期，提示信息：
java.lang.AssertionError: 
	at org.junit.Assert.fail(Assert.java:91)
	at org.junit.Assert.assertTrue(Assert.java:43)
	at org.junit.Assert.assertTrue(Assert.java:54)
	at com.lyg.fizz.FizzBuzzTest.testN(FizzBuzzTest.java:16)
```

### Test expected 异常类型

```java
@Test(expected = IllegalArgumentException.class)
public void testN() {
    FizzBuzz.printValue(0);
}
```

报错很清晰 

`java.lang.AssertionError: Expected exception: java.lang.IllegalArgumentException`

**缺陷** ：**无法断言异常信息** （即异常的message）


### Rule 断言异常类型和异常信息

JUnit 4.7 新特性

```java
public class FizzBuzzTest {
    @Rule
    public ExpectedException mExpectedException = ExpectedException.none();

    @Test
    public void testN() {
        mExpectedException.expect(IllegalArgumentException.class);
        mExpectedException.expectMessage("input must be > 0");
        FizzBuzz.printValue(0);
    }
}
```

```
没有如预期抛出异常，提示信息：
java.lang.AssertionError: 
Expected test to throw (exception with message a string containing "input must be > 0" and an instance of java.lang.IllegalArgumentException)
------------------------
异常的message 不符合预期，提示信息：
java.lang.AssertionError: 
Expected: (exception with message a string containing "input must be > 0" and an instance of java.lang.IllegalArgumentException)
     got: <java.lang.IllegalArgumentException: input must be > 1>
```

## ParameterizedTest 和 CsvSource

JUnit 5 新特性；Gradle 4.6 开始支持 JUnit 5

AS 默认使用 JUnit 4

```java
@ParameterizedTest
@CsvSource({
	"1,1",
	"3,Fizz",
	"5,Buzz",
	"15,FizzBuzz"
})
public void testN(int number, String value) {
    assertEquals(value, FizzBuzz.printValue(number));
}
```

# 任务

写一个程序，打印出从1到100的数字，将其中3的倍数替换成“Fizz”，5的倍数替换成“Buzz”。既能被3整除、又能被5整除的数则替换成“FizzBuzz”。

# TDD流程

- **Red**。write a test that fails
- **Green**。make the code work
- **Refactor**。eleminate redundancy [ɪˈlɪmɪneɪt rɪˈdʌndənsi] 消除重复

## 写测试

```java
public class FizzBuzzTest {
    @Test
    public void testN() {
        assertEquals("1", FizzBuzz.printValue(1));
    }
}    
```

测试报错找不到 `FizzBuzz.printValue` ，使用IDE自动生成

```java
public class FizzBuzz {
    public static String printValue(int input) {
        return null;
    }
}
```

试运行测试，不通过；预期返回1，实际返回null

## 使测试通过

```java
public class FizzBuzz {
    public static String printValue(int input) {
        return String.valueOf(input);
    }
}
```

重复上面的步骤一和步骤二，逐个增加测试用例并使之通过

```java
public class FizzBuzzTest {
    @Test
    public void testN() {
        assertEquals("1", FizzBuzz.printValue(1));
        assertEquals("Fizz", FizzBuzz.printValue(3));
        assertEquals("Buzz", FizzBuzz.printValue(5));
        assertEquals("FizzBuzz", FizzBuzz.printValue(15));
    }
}
```

```java
public class FizzBuzz {
    public static String printValue(int input) {
        String result = "";
        if (input < 1) throw new IllegalArgumentException("input must be > 0");
        if (input % 3 == 0) result += "Fizz";
        if (input % 5 == 0) result += "Buzz";
        if (result.isEmpty()) result += input;
        return result;
    }
}
```

## 重构，消除重复

使用 JUnit 5 新特性 ParameterizedTest 和 CsvSource，消除重复断言代码

```java
@ParameterizedTest
@CsvSource({
	"1,1",
	"3,Fizz",
	"5,Buzz",
	"15,FizzBuzz"
})
public void testN(int number, String value) {
    assertEquals(value, FizzBuzz.printValue(number));
}
```






  



