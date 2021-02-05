import requests
import re
import pandas as pd
import urllib
import re
import pandas as pd
import pymysql
import os
sha_list =pd.read_csv('sha_list.csv',header=None)
idx = sha_list.iloc[1:,1]
filepath = r'/Users/lmy/Desktop/findata/data/'
db = pymysql.connect(host='localhost', port=3306,
                           charset='utf8',
                          user='root', password='lmy6571495')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
cursor.execute("drop database if exists stockdata")
cursor.execute("CREATE DATABASE stockdata")
cursor.execute("use stockdata")

#获取本地文件列fileList = os.listdir(filepath)#依次对每个数据文件进行存储
for code in idx:
    data = pd.read_csv(r'/Users/lmy/Desktop/findata/data_sh/'+str(code)+'.csv', encoding="gbk")
    # print(data)
   #创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName[0:6])
    sqlSentence3 = "create table if not exists stock_%s" % str(code) + "(日期 date, 股票代码 VARCHAR(10), 名称 VARCHAR(10), 收盘价 float,\
    最高价 float, 最低价 float, 开盘价 float, 前收盘 float, 涨跌额 float, 涨跌幅 float, 换手率 float,\
    成交量 bigint, 成交金额 bigint)"
    cursor.execute(sqlSentence3)#迭代读取表中每行数据，依次存储（整表存储还没尝试过）
    db.commit()
    print('正在存储stock_%s'% str(code))
    length = len(data)
    for i in range(0, length):
        record = tuple(data.iloc[i])
        # print(record[0:13])
        r = record[0:13]
        #插入数据语句
        try:
            sqlSentence4 = "insert into stock_%s" % str(code) + "(日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价,\
            前收盘, 涨跌额, 涨跌幅, 换手率, 成交量, 成交金额) \
            values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % r
            #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            # print(sqlSentence4)
            sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null')
            cursor.execute(sqlSentence4)
            db.commit()
        except:#如果以上插入过程出错，跳过这条数据记录，继续往下进行
            break

cursor.close()
db.commit()
db.close()
