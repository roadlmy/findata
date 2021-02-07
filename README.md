
## 金融爬虫项目

### 项目简介

该项目通过对东方财富和网易财经网站爬虫，获取个股日线数据并存入Mysql数据库。通过Python调用数据并进行基础金融数据分析，在Jupyter Notebook进行展示。代码通过下文项目说明的简单修改，可以直接在Macos，Linux操作系统的Server上直接使用。

### 项目使用说明

1.修改文件保存路径：文件结构需要与本仓库保持一致<br>
<br>
      get_data_sh_ORG.py line 40,56,70,75 改到自己文件所在路径下 <br>
      get_data_sz_ORG.py line 42,60,74,80 改到自己data_sz所在文件路径下 <br>
<br>
2.修改个股数据开始和结束日期,如 &start=20060101&end=20210204&  <br>
<br>
      get_data_sh_ORG.py line 45<br>
      get_data_sz_ORG.py line 48<br>
<br>
3.终端输入 python3 get_data_sh_ORG.py 和 python3 get_data_sz_ORG.py<br>
<br>
这两个文件只需要在初始时候执行一次即可，之后无需再次执行，将个股数据存入mysql数据库<br>

4.终端输入 crontab -e <br>
将crontab文件的内容拷贝进去保存，update.py,update_new_stock_sh.py,update_new_stock_sz.py自动定时执行<br>
意思分别是每天21:30更新数据库信息，每天21:40更新股票池，每天22:30数据库备份 <br>
可以使用 crontab -l 查看 <br>
Macos:<br>
sudo /usr/sbin/cron start<br>
sudo /usr/sbin/cron restart<br>
sudo /usr/sbin/cron stop<br>

Ubuntu:
sudo /etc/init.d/cron start<br>
sudo /etc/init.d/cron stop<br>
sudo /etc/init.d/cron restart<br>

Centos:
/sbin/service crond start //启动服务 <br>
/sbin/service crond stop //关闭服务  <br>
/sbin/service crond restart //重启服务  <br>
/sbin/service crond reload //重新载入配置<br>

### 项目文件介绍

文件：<br>
get_data_sh_ORG.py:获取沪A个股数据，并存入数据库（只需要执行一次）<br>
get_data_sz_ORG.py:获取深A个股数据，并存入数据库（只需要执行一次）<br>
log.txt:项目个人编写日志，记录及时想法 <br>
sha_list.csv:爬取沪A的个股股票代码，便于直接查询使用，数据库也有 <br>
sza_list.csv:爬取深A的个股股票代码，便于直接查询使用，数据库也有 <br>
update.py:每日数据库数据更新 <br>
update_new_stock_sh.py:每日沪A股票池更新 <br>
update_new_stock_sz.py:每日深A股票池更新 <br>
crontab:linux crontab命令 <br>

<br>

文件夹：<br>
data_sh:网易财经下载的沪A个股数据，存入数据库后可删除，初始为空 <br>
data_sz:网易财经下载的深A个股数据，存入数据库后可删除，初始为空 <br>
save:存放一些测试代码 <br>
backup:数据库备份文件存放位置 <br>

### 项目更新以及想法

1.爬虫多线程

2.数据库存储缓存参数设置my.cnf
