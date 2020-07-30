## 资源重复 ##

	Error:Execution failed for task ':app:mergeDebugResources'.
	>[declare-styleable/ViewPagerIndicator] C:\workspace\KuaiHappy1\app\src\main\res\values\attrs.xml	
	 [declare-styleable/ViewPagerIndicator] C:\workspace\KuaiHappy1\app\src\main\res\values\viewpager_indicator_attrs.xml: 
	Error: Duplicate resources

这是因为eclipse支持同一个资源名称可以出现在多个xml文件中，eclipse生成R时会自动合并，而android studio不支持。把两个文件中的资源合并即可

	\res\values\viewpager_indicator_attrs.xml中
	<resources>
	    <attr name="item_count" format="integer"></attr>
	    <declare-styleable name="ViewPagerIndicator">
	        <attr name="item_count" />
	        <attr name="vpiTabPageIndicatorStyle" format="reference" />
	    </declare-styleable>
	</resources>

	\res\values\attrs.xml中
	<resources>
	    <declare-styleable name="ViewPagerIndicator">
	    </declare-styleable>
	</resources>

	把两个资源定义合并一下就解决了

ava.lang.UnsatisfiedLinkError: dlopen failed: "/data/app/net.zuixi.peace-1/lib/x86/libk1.so" has unexpected e_machine: 40

