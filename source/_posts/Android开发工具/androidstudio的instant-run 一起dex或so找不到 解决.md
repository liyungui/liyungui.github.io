	http://stackoverflow.com/questions/35792459/java-lang-unsatisfiedlinkerror-com-android-tools-fd-runtime-incrementalclassloa 
报错如下：

	java.lang.UnsatisfiedLinkError: com.android.tools.fd.runtime. IncrementalClassLoader$DelegateClassLoader nativeLibraryDirectories=[/data/data/com.catcry.ffmpeg/lib, /vendor/lib,/system/lib]]] couldn't find "libffmpeg-jni.so"

解决方案：

关闭instant-run

	Just turn off instant-run from Setting/Preferences -> Build,Execution,Deployment -> Instant Run and uncheck the first two check-boxes. This error is because of instant-run feature.