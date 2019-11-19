# SSTAP_ip_crawl_tool
一个自动获取游戏远程ip，并自动写成SSTAP规则文件的脚本。

此脚本由python3编写，版本为3.7，其他版本未验证。

依赖的第三方库为psutil。

使用方法：
-------
启动程序(ip_crawl_tool.py)后输入需要抓取IP的程序名，然后根据提示输入游戏英文名、中文名随即进入抓取状态。

进入抓取状态后开启SSTAP全局进入游戏即可自动抓取ip并填写入规则文件。

获取到ip后关闭窗口即可退出程序。

为确保获取规则的完整性，务必保证多运行几分钟（也就是开着全局和工具多玩一会）

规则文件在程序当前目录中。

不会python可以选择下载release中打包好的exe可执行文件https://github.com/oooldtoy/SSTAP_ip_crawl_tool/releases/download/v3.0/ip_crawl_tool.v3.0.exe

规则更新快速版网页：
-------
http://23.101.14.221:5001

使用3.0版本创建的规则均会在此显示

更新说明：
-------
v3.0<br>
1.增加自动上传规则功能<br>
2.增加快速规则预览网页服务<br>
3.修复ipv6规则相关问题

v2.0<br>
1.更新同时抓取多个进程的功能<br>
2.更新规则写入模式，使其覆盖IP段更加全面

关于如何获取程序名称：
-------

首先打开游戏，然后打开任务管理器，找到游戏进程

![查找程序名第一步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/1.png)

然后右键点击该进程属性

![查找程序名第二步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/2.png)

然后在红框位置的即为程序名称：

![查找程序名第三步](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/3.png)

![查找程序名总览](https://raw.githubusercontent.com/oooldtoy/SSTAP_ip_crawl_tool/master/MD_IMG/4.png)
