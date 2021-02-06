
##沪A股
import requests
import re
import pandas as pd

import urllib
import re
import pandas as pd
import pymysql
import os
###################获取股票代码#######################
def get_stocklist():
    ticker = pd.DataFrame(columns={})
    for i in range(1,96):  ###96页

        url = 'http://73.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408013832830150123_1612441015559&pn='+str(i)+'&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1612441015560'
        wbdata = requests.get(url).text
        # print (re.findall("f12\"\:\"(.*?)\"\,", wbdata,re.M))
        stock_id = re.findall("f12\"\:\"(.*?)\"\,", wbdata,re.M)
        # print (re.findall("f14\"\:\"(.*?)\"\,", wbdata,re.M))
        stock_name = re.findall("f14\"\:\"(.*?)\"\,", wbdata,re.M)
        # ticker.loc[len(ticker),'stock_id']=l1
        # ticker.loc[len(ticker),'stock_name']=l2
        df = pd.DataFrame([stock_id,stock_name])
        # ticker =ticker.append(df,ignore_index=True)
        ticker = pd.concat([ticker,df],axis=1)


    ticker = ticker.T
    save_sha = ticker.reset_index(drop=True)
    print(save_sha)
    save_sha.to_csv('sha_list.csv')
    # type(wbdata)

###################获取个股数据#######################
def get_indiv_stock():
    sha_list =pd.read_csv('sha_list.csv',header=None)
    idx = sha_list.iloc[1:,1]
    filepath = r'/Users/lmy/Desktop/findata/data_sh/'
    print(idx)
    for code in idx:
        try:
            print('正在获取股票%s数据'%code)
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+str(code)+'&start=20060101&end=20210204&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'   ####TODO:每日更新日期
            urllib.request.urlretrieve(url, filepath+str(code)+'.csv')
        except:
            continue



###################数据库存储#######################
def save_db():
    sza_list =pd.read_csv('sha_list.csv',header=None,dtype = str)
    idx = sza_list.iloc[1:,1]
    filepath = r'/Users/lmy/Desktop/findata/data_sh/'

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
        try:
            data = pd.read_csv(r'/Users/lmy/Desktop/findata/data_sh/'+str(code)+'.csv', encoding="gbk")
        except FileNotFoundError:
            print('正在获取股票%s数据'%code)
            url = 'http://quotes.money.163.com/service/chddata.html?code=0'+str(code)+'&start=20060101&end=20210204&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'   ####TODO:每日更新日期
            urllib.request.urlretrieve(url, filepath+str(code)+'.csv')
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
                continue

    cursor.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    get_stocklist()
    get_indiv_stock()
    save_db()
