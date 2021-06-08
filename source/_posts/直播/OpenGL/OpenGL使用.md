---
title: OpenGL使用
date: 2020-04-02 14:52:14
categories:
  - OpenGL
tags:
  - OpenGL
---

# 什么是OpenGL

Open Graphics Library

开放图形库

跨语言、跨平台的 渲染2D、3D矢量图形的 应用程序编程接口（API）

**OpenGL ES**：OpenGL for Embedded Systems

# OpenGL ES 版本

OpenGL ES 1.x的版本和2.0基本是两套框架，许多东西不兼容而且过时

现在比较新的OpenGL ES 3.x的版本是兼容和复用2.0的接口的

所以一般以2.0版本作为切入点

# 关于EGL

OpenGL ES定义了平台无关的GL绘图指令

EGL则定义了统一的平台接口：

- **Display(EGLDisplay)** 实际显示设备的抽象
- **Surface(EGLSurface)** 存储图像的内存区域 FrameBuffer 的抽象
	- 包括：
		- Color Buffer
		- Stencil Buffer
		- Depth Buffer 
- **Context(EGLContext)** 存储OpenGL ES绘图的一些状态信息

## 使用EGL的绘图的一般步骤

- 获取EGLDisplay对象
- 初始化与EGLDisplay 之间的连接。
- 获取EGLConfig对象
- 创建EGLContext 实例
- 创建EGLSurface实例
- 连接EGLContext和EGLSurface.
- 使用GL指令绘制图形
- 断开并释放与EGLSurface关联的EGLContext对象
- 删除EGLSurface对象
- 删除EGLContext对象
- 终止与EGLDisplay之间的连接。

一般来说，Android平台大部分OpenGL ES开发，无需直接按照上述步骤来使用OpenGL ES绘制图形。

Android平台中 类 **GLSurfaceView**，提供了对Display,Surface,Context 的管理，大大简化了OpenGL ES的程序框架

# 第一个Android实例

实例：显示红色背景

要在Android应用程序中使用OpenGL ES绘制图形，必须为它们创建一个视图容器。其中一种比较直接的方法是实现一个 GLSurfaceView(视图容器)和一个GLSurfaceView.Renderer(控制将什么内容显示在GLSurfaceView上)

GLSurfaceView 适合全屏或近全屏图形视图。想要在布局的一小部分中加入OpenGL ES图形可以使用TextureView 或 SurfaceView，这样更灵活但这需要编写相当多的额外代码。

## 添加声明

必须在manifest中添加以下声明：

```
<uses-feature android:glEsVersion="0x00020000" android:required="true" />
```

## 构建视图容器 GLSurfaceView

```
public class CameraView extends GLSurfaceView {

    public CameraView(Context context) {
        super(context);

        // 使用 OpenGL ES 2.0
        setEGLContextClientVersion(2);

        // 设置渲染器
        // setRenderer() 内部 会 开启线程 GLThread
        // 所有 GL API 都必须在 GLThread线程 调用，否则崩溃
        // CameraRender implements GLSurfaceView.Renderer
        CameraRender render = new CameraRender();
        setRenderer(render);

        // 设置渲染模式
        // RENDERMODE_WHEN_DIRTY 手动调用 requestRender() 刷新
        // RENDERMODE_CONTINUOUSLY 自动刷新 大概16ms回调一次 onDraw()
        // 必须在 setRenderer 之后
        setRenderMode(GLSurfaceView.RENDERMODE_WHEN_DIRTY);
        requestRender();
    }
}    
```

## 构建渲染器 GLSurfaceView.Renderer

显示红色背景

```
public class CameraRender implements GLSurfaceView.Renderer {

	// GLSurfaceView创建时被回调
	public void onSurfaceCreated(GL10 unused, EGLConfig config) {
		// 设置背景颜色为红色(rgba)
		GLES20.glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
	}
	
	// GLSurfaceView视图改变时回调，第一次创建时也会被回调
	public void onSurfaceChanged(GL10 unused, int width, int height) {
		// 设置渲染的位置和大小
		GLES20.glViewport(0, 0, width, height);
	}
	
	// 每一帧绘制时被回调	
	public void onDrawFrame(GL10 unused) {
		// 绘制前，清空 Color 和 Depth Buffer
		GLES20.glClear(GLES20.GL_COLOR_BUFFER_BIT | GLES20.GL_DEPTH_BUFFER_BIT);
	}
}

```

## Activity使用视图容器

```
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //全屏
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);

        CameralView cameralView = new CameralView(getBaseContext());
        setContentView(cameralView);
    }
}
```

# OpenGL ES API 命名习惯

Android OpenGL ES 实现上是使用Java 语言对底层的C接口进行了封装，因此类和方法带有很强的C语言色彩

```
常量都以 GL_ 为前缀。比如 GLES20.GL_COLOR_BUFFER_BIT
指令都以 gl 开头 ，比如 GLES20.glClearColor()

某些指令以 数字fixv 结尾
	数字 代表参数的个数
	fivx 代表参数类型
		f 代表参数类型为 浮点数, 如 GLES20.glUniform3f
		i,x 代表参数类型为 int, 如 GLES20.glUniform2i
		v 代表参数类型为 向量(Vector), 如 GLES20.glUniformMatrix4fv

所有8-bit整数对应到byte 类型，16-bit 对应到short类型,32-bit整数(包括GLFixed)对应到int类型，而所有32-bit 浮点数对应到float 类型。
GL_TRUE,GL_FALSE 对应到boolean类型
C字符串((char*)) 对应到Java 的 UTF-8 字符串。
```

# 管线(渲染流程)

管线 这个术语 描述了 OpenGL 完整的 **渲染流程**

OpenGL采用**cs模型**：c是cpu，s是GPU。c给s的输入是vertex信息和Texture信息，s的输出是显示器上显示的图像。

{% asset_img OpenGL绘制流程.png %}

# 可编程管线

固定管线是没有shader参与的绘制管线，OpenGL3.0已经废除了这个功能

# 着色器

## VertexShader 顶点着色器

**画形状**：处理顶点信息(**VBO/VAO**提供的)、法线

每个顶点(**Attribute**不同，**Uniforms**和**Samples**相同)，执行一遍顶点着色器，输出变量(**Varying**)N个、`gl_Position`、`gl_PointSize`

{% asset_img 顶点着色器.png %}

## FragmentShader 片段着色器

**上色、贴图**：处理片段信息(光栅化输出的，信息包括光、阴影、遮挡、环境等)

每个片段(**Varying**不同，**Uniforms**和**Samples**相同，`gl_FragCoord`、`gl_FrontFacing`、`gl_PointCoord `)，执行一遍片段着色器，输出颜色(**Color**)一个或多个（多重渲染）、`gl_FragDepth`

{% asset_img 片段着色器.png %}

# 程序 Program

用于：
- 加载 着色器
- 编译 着色器
- 附加 着色器 到 Program
- 链接 Program
- 使用 Program 绘制形状

# 坐标

{% asset_img 世界坐标.png %}

规范化：值为[-1,1]

- **世界坐标(xy)**：左手坐标系，以矩形**中心**为原点
- **纹理坐标(st,或uv)**：左手坐标系，以矩形**左下角**为原点

## 纹理坐标和OpenGL世界坐标

由于对一个OpenGL纹理来说，它没有内在的方向性，因此我们可以使用不同的坐标把它定向到任何我们喜欢的方向上，然而大多数计算机图像都有一个默认的方向，它们通常被规定为**y轴向下**，y的值随着向图像的底部移动而增加。

这就跟OpenGL世界坐标的y方向相反，想用正确的方向观看图像，那纹理坐标的u也必须要向下(即跟上面独立的纹理坐标u反向，左上角变为原点)

{% asset_img 纹理坐标和世界坐标.png %}

# 数据类型

```
void
int float 整数 浮点数
bool 布尔值

===Vectors 向量(vector 的复数)===
vec2 vec3 vec4 浮点数容器(后面的数字表示容量) Matrices
ivec2 ivec3 ivec4 整数容器
bvec2 bvec3 bvec4 布尔容器

===Matrices 矩阵(matrix 的复数)===
mat2 mat3 mat4 矩阵(行列数相同，后面数字表示行列数)

===Sampler 采样器===
sampler2D 2D纹理指针
samplerCube 立方体纹理指针

===Structures 结构体===
struct light{
	float intensity;
	vec3 position;

} lightVar; 结构体

===Arrays 数组===
float num[3]; 数组
```

# 作用域 Scopes

GLSL ES使用了静态嵌套范围，允许在着色器内**重定义一个变量**。

```
默认，本地变量
const 本地变量

attribute 属性变量
	仅可用于顶点着色器
	声明通过OpenGL ES应用程序传递到顶点着色器中的变量值 
	不能声明 数组或结构体
	在顶点着色器被程序使用之前，attribute变量是只读的
	
	OpenGL ES中，可以使用的属性变量个数是有限制的，
	如果超过这个限制，将会引起链接错误。
	声明了但没有使用的属性变量不会受到这个限制。
	浮点数属性也要受到这个限制，所以尽量将四个毫不相关的float变量打包成一个pack
	一个mat4和使用4个vec4变量是一致的
	
uniform
	修饰在整个图元被处理的过程中保持不变的全局变量。
	所有的uniform变量都是只读的
	可以通过应用程序调用API命令初始化，或者通过OpenGL ES间接初始化。
	
	每种类型的着色器的uniform变量的存储数量是有限制
	
Varying	
	提供了顶点着色器，片元着色器和二者 通讯控制模块之间的接口。
	顶点着色器写到varying变量中，片段着色器从varying变量中读值。必须 同名同类型同精度
	不能声明 结构体
```

# 第一个实例

抖音上下两分屏特效

## 原理

{% asset_img 抖音分屏.png %}

原理：截取垂直正中间一半，分别贴到上下两个区域

## 代码

顶点着色器

```
attribute vec4 aPosition; // 一个顶点坐标，java传过来
attribute vec2 aTextureCoord; // 一个纹理坐标，java传过来
varying vec2 vTextureCoord; // 一个纹理坐标，输出到片段着色器

void main() {
	gl_Position = aPosition;
	vTextureCoord = aTextureCoord;
}
```

片段着色器

```
// 摄像头数据 扩展纹理
#extension GL_OES_EGL_image_external : require

precision mediump float; // 数据精度

varying vec2 vTextureCoord; // 一个纹理坐标，片段着色器传过来
uniform samplerExternalOES vTexture;

void main() {
	// gl_FragColor = texture2D(vTexture, vTextureCoord); // 原样输出摄像头数据
	// 开始抖音分屏特效
	float x = vTextureCoord.x;
	if(x < 0.5){
		x += 0.25
	} else {
		x -= 0.25
	}
	gl_FragColor = texture2D(vTexture, vec2(x, vTextureCoord.y));
}
```

# 基本几何图形定义

## 三种基本几何图形

OpenGL ES 支持绘制的基本几何图形分为三类：

- 点
- 线段
- 三角形

也就是说OpenGL ES 只能绘制这三种基本几何图形。

任何复杂的2D或是3D图形都是通过这三种几何图形构造而成的。

## 顶点解释的七种模式

三种基本几何图形，都是通过 **顶点数组** 来定义

点(Point)，可以两个连接成线段(Line Segment) ，也可以三个连成三角形(Triangle)。

这些对一组顶点的不同解释就定义了Android OpenGL ES可以绘制的基本几何图形


- `GL_POINTS` 绘制独立的点
- `GL_LINES` 绘制线段(`0-1,2-3`)。即两两连接，构成多条线段。
- `GL_LINE_STRIP` 绘制连续线段(`0-1-2-3`)。每相邻两个点组成线段
- `GL_LINE_LOOP` 绘制首尾相连的封闭线段(`0-1-2-3-0`)
- `GL_TRIANGLES` 绘制三角形(`0-1-2,3-4-5`)
- `GL_TRIANGLE_STRIP` 绘制连续三角形(`0-1-2,1-2-3,2-3-4，3-4-5`)。每相邻两个点组成线段
- `GL_TRIANGLE_FAN` 绘制共顶点三角形(`0-1-2,0-2-3,0-3-4，0-4-5`)。

## 绘图API

OpenGL ES提供了两个方法来绘制一个空间几何图形

```
glDrawArrays(int mode, int first, int count) 使用VetexBuffer 来绘制，顶点的顺序由vertexBuffer中的顺序指定。mode 为解释顶点的模式
glDrawElements(int mode, int count, int type, Buffer indices) ，可以重新定义顶点的顺序，顶点的顺序由indices Buffer 指定。
```

# 绘制三角形

绘制一个红色的三角形

绘制基本流程：

- 定义顶点，一般用FloatBuffer
- 编写着色器代码
- 传递Java值初始化着色器中的变量(顶点坐标、颜色等)
- 创建 Program，加载编译添加链接着色器
- 绘制图形

```
public class Triangle {
    private String TAG = "Triangle";

    // 顶点着色器 代码
    private final String vertexShaderCode =
            "attribute vec4 vPosition;" +
                    "void main() {" +
                    "  gl_Position = vPosition;" +
                    "}";
    // 片段着色器 代码
    private final String fragmentShaderCode =
            "precision mediump float;" +
                    "uniform vec4 vColor;" +
                    "void main() {" +
                    "  gl_FragColor = vColor;" +
                    "}";

    // 数组 存储 三个顶点
    private float triangleCoords[] = {  // 按逆时针顺序
            0.0f, 0.622008459f, 0.0f, // 上
            -0.5f, -0.311004243f, 0.0f, // 左下
            0.5f, -0.311004243f, 0.0f  // 右下
    };
    // FloatBuffer 存储 三个顶点，更加高效
    // 内存拷贝。Java层 到 Native层。可抽取为模板代码
    private FloatBuffer vertexBuffer = ByteBuffer
            .allocateDirect(triangleCoords.length * 4)// 分配一块 Native 内存，不会被 Java 的垃圾回收器管理
            .order(ByteOrder.nativeOrder())// 缓冲区读取顺序使用设备硬件的本地字节读取顺序
            .asFloatBuffer()// 从ByteBuffer创建一个浮点缓冲区，避免直接操作字节
            .put(triangleCoords);// 将坐标点加到FloatBuffer中。从 Java 层内存复制到 Native 层

    // 数组 存储颜色(rgba)，红色
    private float color[] = {1.0f, 0.0f, 0.0f, 1.0f};

    private final int mProgram;
    private int mPositionHandle;
    private int mColorHandle;

    public Triangle() {
        mProgram = loadProgram(vertexShaderCode, fragmentShaderCode);
        // 使用着色器程序
        GLES20.glUseProgram(mProgram);

        // 获取顶点着色器vPosition属性的句柄
        mPositionHandle = GLES20.glGetAttribLocation(mProgram, "vPosition");
        // 启用三角形顶点的句柄
        GLES20.glEnableVertexAttribArray(mPositionHandle);
        // 设置缓冲区开始读取位置，这边设置为从头开始读取
        vertexBuffer.position(0);
        // 准备三角坐标数据
        // size: 每个顶点坐标维数，可以为2，3，4。
        // type: 顶点的数据类型，可以为GL_BYTE, GL_SHORT, GL_FIXED,或 GL_FLOAT，缺省为浮点类型GL_FLOAT。
        // stride: 每个相邻顶点之间在数组中的间隔（字节数），缺省为0，表示顶点存储之间无间隔。
        // pointer: 存储顶点的数组。
        GLES20.glVertexAttribPointer(mPositionHandle, 3, GLES20.GL_FLOAT, false, 3 * 4, vertexBuffer);

        // 获取片段着色器vColor成员（颜色）的句柄
        mColorHandle = GLES20.glGetUniformLocation(mProgram, "vColor");
        //设置绘制三角形的颜色
        GLES20.glUniform4fv(mColorHandle, 1, color, 0);
    }

    public void draw() {
        // 绘制三角形
        // count 3个顶点
        GLES20.glDrawArrays(GLES20.GL_TRIANGLES, 0, 3);
    }

    /**
     * 加载编译着色器
     *
     * @param type
     * @param shaderCode
     * @return
     */
    public int loadAndCompileShader(int type, String shaderCode) {
        // 创建着色器
        // 顶点着色器类型（GLES20.GL_VERTEX_SHADER）
        // 片段着色器类型（GLES20.GL_FRAGMENT_SHADER）
        int shader = GLES20.glCreateShader(type);
        if (shader == 0) {
            Log.e(TAG, "创建着色器失败 " + type);
            return shader;
        }
        // 将源代码添加到着色器
        GLES20.glShaderSource(shader, shaderCode);
        // 编译着色器
        GLES20.glCompileShader(shader);
        // 验证编译结果
        final int[] compileStatus = new int[1];
        GLES20.glGetShaderiv(shader, GLES20.GL_COMPILE_STATUS, compileStatus, 0);
        if (compileStatus[0] == 0) {
            Log.d(TAG, "Compile Shader Failed\n" + GLES20.glGetShaderInfoLog(shader));
            // 失败则删除
            GLES20.glDeleteShader(shader);
            return 0;
        }
        return shader;
    }

    /**
     * 加载着色器程序
     *
     * @param vertexShaderCode
     * @param fragmentShaderCode
     * @return
     */
    public int loadProgram(final String vertexShaderCode, final String fragmentShaderCode) {
        int vertexShader;
        int fragmentShader;
        int program;

        vertexShader = loadAndCompileShader(GLES20.GL_VERTEX_SHADER, vertexShaderCode); // 顶点着色器
        if (vertexShader == 0) {
            Log.d(TAG, "Load Program: Vertex Shader Failed");
            return 0;
        }
        fragmentShader = loadAndCompileShader(GLES20.GL_FRAGMENT_SHADER, fragmentShaderCode); // 片元着色器
        if (fragmentShader == 0) {
            Log.d(TAG, "Load Program: Fragment Shader Failed");
            return 0;
        }

        // 创建着色器程序
        program = GLES20.glCreateProgram();

        // 附加 顶点着色器 和 片元着色器
        GLES20.glAttachShader(program, vertexShader);
        GLES20.glAttachShader(program, fragmentShader);

        // 链接着色器程序
        GLES20.glLinkProgram(program);

        // 验证program的链接结果
        int[] linkStatus = new int[1];
        GLES20.glGetProgramiv(program, GLES20.GL_LINK_STATUS, linkStatus, 0);
        if (linkStatus[0] <= 0) {
            Log.d(TAG, "Load Program: Link Failed");
            // 失败则删除 OpenGL 程序
            GLES20.glDeleteProgram(program);
            return 0;
        }

        // 删除着色器
        GLES20.glDeleteShader(vertexShader);
        GLES20.glDeleteShader(vertexShader);

        //验证着色器程序
        GLES20.glValidateProgram(program);
        final int[] validateStatus = new int[1];
        GLES20.glGetProgramiv(program, GLES20.GL_VALIDATE_STATUS, validateStatus, 0);
        if (validateStatus[0] <= 0) {
            Log.d(TAG, "Load Program: Validate Failed");
            // 失败则删除 OpenGL 程序
            GLES20.glDeleteProgram(program);
            return 0;
        }

        return program;
    }
}
```

在Render的`onDrawFrame(GL10 gl)` 创建`Triangle`实例，调用`Triangle.draw()`即可

# 投影和相机矩阵变换

上面已经初步将三角形显示在屏幕上了，但明显可以看到存在问题。

首先按照前面三角形的坐标，应该是一个等边三角形。

其次，这个三角形竖屏和横屏拉伸方向都存在 **变形拉伸**

这是因为 OpenGL采用 **方形均匀的坐标系统**

要解决此问题，可以应用OpenGL**投影模式和摄像机视图来转换坐标**，以便图形对象在任何显示上都具有正确的比例。

这边就涉及到一个**视见体(frustum 椎体)**的概念，其实OpenGL图形所处与于一个三维的世界，可以想象一下在屏幕上显示的其实是一个图像的投影，而屏幕可以理解为一块投影幕布，这样就可以通过改变相机的坐标和旋转移动投影来达到显示在投影上的物体的形状的拉伸与缩放。

投影矩阵重新计算图形的坐标，以便它们正确映射到Android设备屏幕。摄像机视图矩阵创建一个变换，从特定的眼睛位置渲染对象。

## 投影矩阵

此矩阵根据绘制对象的显示位置的宽度和高度调整绘制对象的坐标。

如果没有这个变换，OpenGL ES绘制的对象会因视图窗口的不等比例而拉伸。

通常只需要在onSurfaceChanged()渲染器的方法中建立或更改OpenGL视图的宽高比例，计算投影矩阵。

```
private final float[] mProjectionMatrix = new float[16];// 投影矩阵
private final float[] mViewMatrix = new float[16];// 视图矩阵
private final float[] mMVPMatrix = new float[16];// 模型视图投影矩阵(Model View Projection Matrix)
@Override
public void onSurfaceChanged(GL10 gl, int width, int height) {
	// Sets the current view port to the new size.
	gl.glViewport(0, 0, width, height);
        
	// 计算宽高比
	float ratio = (float) width / height;
	    
	// 使用其宽高来计算投影矩阵。frustum 椎体
	// mProjectionMatrix 输出的投影矩阵
	// offset 从输出的数组的什么位置开始写入
	// left, right, bottom, top
	// 投影矩阵对应于OpenGL ES世界坐标的对应上限的映射关系
	// 即 宽*ratio; left=1*ratio, right=1*ratio
	// near,fart 有点抽象，用于显示图像的前面和背面
	// 需要结合假想摄相机即观察者眼睛的位置来设置
	// near必须大于setLookAtM()中设置eyeZ，才可以看得到绘制的图像。否则图像就会处于观察者眼睛的后面，绘制的图像就会消失在镜头前
	// far参数影响的是立体图形的背面，一般会设置得比较大(一定比near大)。如果设置的比较小，投影矩阵就没法容纳图形全部的背面，这样3D图形的背面会有部分无法显示。
	Matrix.frustumM(mProjectionMatrix, 0, -ratio, ratio, -1, 1, 3, 7);
```

## 摄像机视图矩阵

此变换根据假想摄像机位置调整绘制对象的坐标。

注意OpenGL ES不定义实际的相机对象，而是提供通过转换绘制对象的显示来模拟相机的效果。

建立摄像机转换时，可能只计算一次 GLSurfaceView，或者也可能会根据用户操作或应用程序的功能动态更改。

```
@Override
public void onDrawFrame(GL10 gl) {
	// 设置相机的位置 (View matrix)
	// mViewMatrix 输出的视图矩阵
	// offset 从输出的数组的什么位置开始写入
	// eyeX、eyeY、eyeZ 摄相机即观察者眼睛的位置
	// centerX、centerY、centerZ 目标视图中心位置
	// upX、upY、upZ相机角度
	Matrix.setLookAtM(mViewMatrix, 0, 0, 0, -3, 0f, 0f, 0f, 0f, 1.0f, 0.0f);
	
	// 计算投影和视图转换（Model View Projection Matrix）
	// 矩阵相乘的顺序会影响结果。即 AB 和 BA 得到的是不同的矩阵
	// mMVPMatrix 输出的模型视图投影矩阵
	// offset 从输出的数组的什么位置开始写入
	Matrix.multiplyMM(mMVPMatrix, 0, mProjectionMatrix, 0, mViewMatrix, 0);
	
	mTriangle.draw(mMVPMatrix);
}
```

## 使用模型视图投影矩阵

```
// 顶点着色器 代码
private final String vertexShaderCode =
        "attribute vec4 vPosition;" +
                "uniform mat4 uMVPMatrix;" + // 提供了一个矩阵来变换顶点着色器对象的坐标
                "void main() {" +
                "  gl_Position = uMVPMatrix * vPosition;" + // uMVPMatrix因子必须在*前面才能使矩阵乘法乘积正确。
                "}";
                
public void draw(float[] mvpMatrix) {
    // 获取形状变换矩阵的具柄
    mMVPMatrixHandle = GLES20.glGetUniformLocation(mProgram, "uMVPMatrix");
    // 将模型视图投影矩阵传递给着色器
    GLES20.glUniformMatrix4fv(mMVPMatrixHandle, 1, false, mvpMatrix, 0);

    // 绘制三角形
    // count 3个顶点
    GLES20.glDrawArrays(GLES20.GL_TRIANGLES, 0, 3);
}    
```

# 添加动画

动画和上面所述的图像修正的核心原理是一样的，都是通过对图像进行矩阵变换来实现。

实例：旋转绘图对象

创建另一个变换矩阵（旋转矩阵），然后将其与投影和摄像机视图变换矩阵组合

```
public void onDrawFrame(GL10 gl) 中
// 创建旋转矩阵。
// angel 角度，跟随系统时间递增
float[] rotationMatrix = new float[16];
Matrix.setRotateM(rotationMatrix, 0, 0.090f * ((int) SystemClock.uptimeMillis() % 4000L), 0, 0, -1.0f);

//计算旋转，mMVPMatrix因子必须在*前面才能使矩阵乘法乘积正确。
float[] scratch = new float[16];
Matrix.multiplyMM(scratch, 0, mMVPMatrix, 0, rotationMatrix, 0);

mTriangle.draw(scratch);
```

如果设置过 `setRenderMode(RENDERMODE_CONTINUOUSLY);`先注释，然后就能看到不断旋转的三角形了

# 渲染一张图片

```
public class Image2D {
    // 顶点着色器 代码
    public static final String vertexShaderCode = "" +
            "attribute vec4 position;\n" + // 顶点着色器的顶点坐标,由外部程序传入
            "attribute vec4 inputTextureCoordinate;\n" + // 传入的纹理坐标
            " \n" +
            "varying vec2 textureCoordinate;\n" +
            " \n" +
            "void main()\n" +
            "{\n" +
            "    gl_Position = position;\n" +
            "    textureCoordinate = inputTextureCoordinate.xy;\n" + // 最终顶点位置
            "}";
    // 片段着色器 代码
    public static final String fragmentShaderCode = "" +
            "varying highp vec2 textureCoordinate;\n" + // 最终顶点位置，上面顶点着色器的varying变量会传递到这里
            " \n" +
            "uniform sampler2D inputImageTexture;\n" + // 外部传入的图片纹理 即代表整张图片的数据
            " \n" +
            "void main()\n" +
            "{\n" +
            "     gl_FragColor = texture2D(inputImageTexture, textureCoordinate);\n" +  // 调用函数 进行纹理贴图
            "}";

    // 原始的矩形区域的顶点坐标
    static final float CUBE[] = {
            -1.0f, -1.0f, // v1 左下
            1.0f, -1.0f,  // v2 右下
            -1.0f, 1.0f,  // v3 左上
            1.0f, 1.0f,   // v4 右上
    };
    // 纹理坐标系，称UV坐标，或者ST坐标。UV坐标定义为左上角（0，0），右下角（1，1）
    // 每个坐标的纹理采样对应上面顶点坐标。
    public static final float TEXTURE_NO_ROTATION[] = {
            0.0f, 1.0f, // v1 左下
            1.0f, 1.0f, // v2 右下
            0.0f, 0.0f, // v3 左上
            1.0f, 0.0f, // v4 右上
    };
    private FloatBuffer mGLCubeBuffer = ByteBuffer
            .allocateDirect(CUBE.length * 4)
            .order(ByteOrder.nativeOrder())
            .asFloatBuffer();

    private FloatBuffer mGLTextureBuffer = ByteBuffer
            .allocateDirect(TEXTURE_NO_ROTATION.length * 4)
            .order(ByteOrder.nativeOrder())
            .asFloatBuffer()
            .put(TEXTURE_NO_ROTATION);

    protected int mGLProgId;
    protected int mGLAttribPosition;
    protected int mGLAttribTextureCoordinate;
    protected int mGLUniformTexture;

    private int mImageWidth, mImageHeight; // bitmap图片实际大小
    private int mGLTextureId = OpenGLUtil.NO_TEXTURE; // 纹理id

    public Image2D(Context context) {
        // 需要显示的图片
        Bitmap bitmap = BitmapFactory.decodeResource(context.getResources(), R.drawable.bg_clazz_preview_result);
        mImageWidth = bitmap.getWidth();
        mImageHeight = bitmap.getHeight();
        // 把图片数据加载进GPU，生成对应的纹理id
        mGLTextureId = OpenGLUtil.loadTexture(bitmap, mGLTextureId, true); // 加载纹理

        mGLProgId = OpenGLUtil.loadProgram(vertexShaderCode, fragmentShaderCode); // 编译链接着色器，创建着色器程序
        GLES20.glUseProgram(mGLProgId);

        mGLAttribPosition = GLES20.glGetAttribLocation(mGLProgId, "position"); // 顶点着色器的顶点坐标
        mGLAttribTextureCoordinate = GLES20.glGetAttribLocation(mGLProgId, "inputTextureCoordinate"); // 顶点着色器的纹理坐标
        mGLUniformTexture = GLES20.glGetUniformLocation(mGLProgId, "inputImageTexture"); // 传入的图片纹理
        // 顶点着色器的纹理坐标
        mGLTextureBuffer.position(0);
        GLES20.glVertexAttribPointer(mGLAttribTextureCoordinate, 2, GLES20.GL_FLOAT, false, 0, mGLTextureBuffer);
        GLES20.glEnableVertexAttribArray(mGLAttribTextureCoordinate);
        // 传入的图片纹理
        if (mGLTextureId != OpenGLUtil.NO_TEXTURE) {
            GLES20.glActiveTexture(GLES20.GL_TEXTURE0);
            GLES20.glBindTexture(GLES20.GL_TEXTURE_2D, mGLTextureId);
            GLES20.glUniform1i(mGLUniformTexture, 0);
        }
    }

    public void draw() {
        // 绘制顶点
        GLES20.glDrawArrays(GLES20.GL_TRIANGLE_STRIP, 0, 4);
    }

    // 调整图片显示大小为居中显示
    public void adjustImageScaling(float outputWidth, float outputHeight) {
        float ratio1 = outputWidth / mImageWidth;
        float ratio2 = outputHeight / mImageHeight;
        float ratioMax = Math.min(ratio1, ratio2);
        // 居中后图片显示的大小
        int imageWidthNew = Math.round(mImageWidth * ratioMax);
        int imageHeightNew = Math.round(mImageHeight * ratioMax);

        // 图片被拉伸的比例
        float ratioWidth = outputWidth / imageWidthNew;
        float ratioHeight = outputHeight / imageHeightNew;
        // 根据拉伸比例还原顶点
        float[] cube = new float[]{
                CUBE[0] / ratioWidth, CUBE[1] / ratioHeight,
                CUBE[2] / ratioWidth, CUBE[3] / ratioHeight,
                CUBE[4] / ratioWidth, CUBE[5] / ratioHeight,
                CUBE[6] / ratioWidth, CUBE[7] / ratioHeight,
        };

        mGLCubeBuffer.clear();
        mGLCubeBuffer.put(cube).position(0);

        // 顶点着色器的顶点坐标
        GLES20.glVertexAttribPointer(mGLAttribPosition, 2, GLES20.GL_FLOAT, false, 0, mGLCubeBuffer);
        GLES20.glEnableVertexAttribArray(mGLAttribPosition);
    }
}
```
在Render的`onSurfaceChanged(GL10 gl, int width, int height)` 创建`Image2D `实例，调用`Image2D.adjustImageScaling()`调整图片居中显示，然后在Render的`onDrawFrame(GL10 gl)` 调用`Image2D.draw()`即可

# 参考&扩展

- [Android OpenGL ES 开发教程(5)：关于EGL](http://www.guidebee.info/wordpress/?p=1873) EGL绘图步骤
- [OpenGL 学习系列--基础的绘制流程](https://juejin.cn/post/6844903603115671566) 结构清晰易懂
- [OpenGL渲染流程](https://www.pianshen.com/article/5565670467/)
- [OpenGL ES着色器语言之变量和数据类型（一）（官方文档第四章）](https://blog.csdn.net/wangyuchun_799/article/details/7744620)
- [Android OpenGL ES 开发教程(8)：基本几何图形定义](http://www.guidebee.info/wordpress/?p=1938)
- [OpenGL ES 2.0 显示图形（上）](https://www.jianshu.com/p/b2a9c83c2256) 显示三角形和正方形
- [OpenGL ES 2.0 显示图形（下）](https://www.jianshu.com/p/2c94427418ba) 解决变形拉升问题
- [从显示一张图片开始学习OpenGL ES](https://juejin.cn/post/6844903682413182984) 
- [OpenGL ES 3.0（四）矩阵变换](https://www.jianshu.com/p/3bae907f353a)
- [android平台下OpenGL ES 3.0从零开始](https://blog.csdn.net/byhook/article/details/83715360)
