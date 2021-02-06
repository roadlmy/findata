

import requests
import re
import pandas as pd

import urllib
import re
import pandas as pd
import pymysql
import os
import tushare as ts
import datetime
import numpy as np
def get_data(csvfile):
    # if not is_trade_day():
    #     return
    # else:
        sl = pd.read_csv(csvfile,header=None,dtype = str)
        idx = sl.iloc[1:,1]
        a=datetime.date.today()
        d=datetime.timedelta(days=1)
        a=a-d
        a=a.__format__('%Y-%m-%d')
        td = get_trade_day()
        pretd = td.iloc[-2,1]
        pretd =datetime.datetime.strptime(pretd, "%Y%m%d")
        pretd=pretd.__format__('%Y-%m-%d')

        daily_data = pd.DataFrame(columns={})
        for code in idx[0:4]:
            # print(code)
            url = 'http://quotes.money.163.com/trade/lsjysj_'+str(code)+'.html#'
            wbdata = requests.get(url).text
            sa = re.findall(a+"(.*?)"+pretd, wbdata)
            if sa:
              num = re.findall(">(.*?)<", sa[0],re.S)
              num = [x for x in num if x != '']
              daily_data.loc[:,str(code)]=num
              # print(num)
        daily_data = daily_data.T
        return daily_data
data = get_data('sha_list.csv')
print(data)
idx = data.index
sl = pd.read_csv('sha_list.csv',header=None,dtype = str)
sl = sl.iloc[1:,1:3]
sl =sl.set_index(1)

db = pymysql.connect(host='localhost', port=3306,
                       charset='utf8',
                      user='root', password='lmy6571495')
cursor = db.cursor()
cursor.execute("use stockdata")

for code in idx[0:3]:
            print(code)
            save = data.loc[code]
            dt=datetime.date.today().__format__('%Y/%m/%d')
            # print(type(dt))
            co = '\''+str(code)
            name = str(sl.loc[code,2])
            spj = np.float64(save[3])
            zgj = np.float64(save[1])
            zdj = np.float64(save[2])
            kpj = np.float64(save[0])
            qsp = np.float64(1)
            zde = str(save[4])
            zdf = str(save[5])
            hsl = np.float64(save[9])
            cjl = save[6]
            cjl = cjl.replace(',','')
            cjl = np.int64(cjl)
            cje = save[7]
            cje = cje.replace(',','')
            cje = np.float64(cje)
            record = (dt,co,name,spj,zgj,zdj,kpj,qsp,zde,zdf,hsl,cjl,cje)

            #插入数据语句
            try:
                print(record)
                print('正在存储stock_%s'% str(code))
                sqlSentence4 = "insert into stock_%s" % str(code) + " (日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价,\
                前收盘, 涨跌额, 涨跌幅, 换手率, 成交量, 成交金额) \
                values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null')
                # print(sqlSentence4)
                cursor.execute(sqlSentence4)
                db.commit()
            except:#如果以上插入过程出错，跳过这条数据记录，继续往下进行
                db.rollback()
                break
cursor.close()
db.commit()
db.close()
