---
title: 使用JNI_OnLoad动态注册Native函数
date: 2019-09-05 11:39:14
categories:
  - Android
tags:
  - NDK
---

# JNI_OnLoad

加载so,虚拟机先自动执行JNI_OnLoad；

卸载so,虚拟机先自动执行JNI_UnLoad；

# 传统java Jni方式

1. 编写带有native方法的Java类
2. 使用javah命令生成.h头文件
3. 编写代码实现头文件中的方法

# RegisterNatives

使用RegisterNatives方法把c/c++中的方法映射到Java中的native方法

# 使用RegisterNatives步骤

- 在c/c++文件中定义并实现对应java中声明的本地方法，方法名称随意，但是参数类型和参数个数必须一样

- 创建声明JNINativeMethod类型的数组，值为需要动态加载映射的本地方法

- 实现JNI_OnLoad方法，主要分为下面两步：

	- 通过FindClass获取所需的映射的java类
	- 通过jint RegisterNatives(jclass clazz, const JNINativeMethod* methods, jint nMethods) 方法动态注册

# 实例

```java
public class JniOnloadTest {

    public native int  javaAdd(int x, int y);
    public native String javaSayHi();

    static {
        System.loadLibrary("test-lib");
    }
}
```

jniload.cpp

```c++
#include <jni.h>
#include <string>
#include <android/log.h>
#define  LOG_TAG    "liuhang"
#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

static jint JNICALL cAdd(JNIEnv *env, jobject jobj, jint x, jint y){
    LOGI("cAdd x is :%d  y is :%d", x, y);
    return x + y;
}

static jstring JNICALL cSayHi(JNIEnv *env, jobject jobj, jint x, jint y){
    LOGI("cSayHi runs... will return a string in c");
    return env->NewStringUTF("hello from cSayHi");
}

/**
   第一个参数：javaAdd 是java中的方法名称
   第二个参数：(II)I  是java中方法的签名，可以通过javap -s -p 类名.class 查看
   第三个参数： (jstring *)cSayHi  （返回值类型）映射到native的方法名称

*/
static const JNINativeMethod gMethods[] = {
        {"javaAdd", "(II)I", (jint *)cAdd},
        {"javaSayHi","()Ljava/lang/String;",(jstring *)cSayHi}
};


static jclass myClass;
// 这里是java调用C的存在Native方法的类路径
static const char* const className="com/jni/test/JniOnloadTest";
JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved){
    LOGI("jni onload called");
    JNIEnv* env = NULL; //注册时在JNIEnv中实现的，所以必须首先获取它
    jint result = -1;
    if(vm->GetEnv((void **) &env, JNI_VERSION_1_4) != JNI_OK) { //从JavaVM获取JNIEnv，一般使用1.4的版本
        return -1;
    }
    // 获取映射的java类
    myClass = env->FindClass(className);
    if(myClass == NULL)
    {
      printf("cannot get class:%s\n", className);
      return -1;
    }
    // 通过RegisterNatives方法动态注册
    if(env->RegisterNatives(myClass, gMethods, sizeof(gMethods)/sizeof(gMethods[0])) < 0)
    {
      printf("register native method failed!\n");
      return -1;
    }
    LOGI("jni onload called end...");
    return JNI_VERSION_1_4; //这里很重要，必须返回版本，否则加载会失败。
}    
```	

java端调用

```java
JniOnloadTest jniOnloadTest = new JniOnloadTest();
Log.d("liuhang", "jnionload add result is :"+jniOnloadTest.javaAdd(1, 2)+" sayhi is :"+jniOnloadTest.javaSayHi());
```

{% asset_img 结果.png %}
# 参考&扩展

- [使用JNI_OnLoad动态注册函数](https://www.jianshu.com/p/f4b4b9006742)