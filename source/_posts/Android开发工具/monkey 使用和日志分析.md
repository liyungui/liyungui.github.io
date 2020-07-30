	Monkey测试之monkey测试策略 http://www.51testing.com/html/68/245968-822552.html
	Monkey日志自动分析脚本 http://www.cnblogs.com/findyou/p/4106285.html

## 单一apk ##

| 类型  | 命令 |
| --- | --- |
| 不忽略异常  | monkey -p com.android.mms --throttle 1000 -s 100 -v -v -v 15000 > /mnt/sdcard/monkey_test.txt & |
| 忽略异常 | monkey -p com.android.mms --throttle 1000 -s 100 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-carshes --monitor-native-crashes -v -v -v 15000 > /mnt/sdcard/monkey_test.txt & |

## APK集合 ##

| 类型  | 命令 |
| --- | --- |
| 不忽略异常 | monkey --pkg-whitelist-file /data/whitelist.txt --throttle 1000 -s 100 -v -v -v 15000 > /mnt/sdcard/monkey_test.txt & | 
| 忽略异常 | monkey --pkg-whitelist-file /data/whitelist.txt --throttle 1000 -s 100 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-carshes --monitor-native-crashes -v -v -v 15000 > /mnt/sdcard/monkey_test.txt & |
