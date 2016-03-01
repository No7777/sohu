# sohu
题目2：写一个python脚本main.py，使用方式如下：
main.py -d 60 -u http://m.sohu.com -o /tmp/backup 

功能要求：
1、每60秒备份一次http://m.sohu.com这个页面，并按时间分隔保存在/tmp/backup目录下，如/tmp/backup/201603011020/；
2、用浏览器打开保存的页面时效果需要和线上的一致；
3、所有内容，包括图片，js，css等都需要存储在本地；
4、代码以github地址方式提交。

/tmp/backup/201603011020/这个目录的结构如下：
index.html  #html内容
images/  # 存放图片
js/  # 存放js
css/  # 存放css 
