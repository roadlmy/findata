import requests
import pandas as pd
import urllib
import re
import pandas as pd
import pymysql
import os
from multiprocessing import Process, Lock
import time


def get_ini(code):
    filepath = r'/Users/lmy/Desktop/findata/data_sz/'
    url = 'http://quotes.money.163.com/service/chddata.html?code=1'+str(code)+'&start=20160101&end=20210204&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'   ####TODO:每日更新日期

    urllib.request.urlretrieve(url, filepath+str(code)+'.csv')


if __name__ == '__main__':
    sza_list =pd.read_csv('sza_list.csv',header=None,dtype = str)
    idx = sza_list.iloc[:,1]
    filepath = r'/Users/lmy/Desktop/findata/data_sz/'
    # print(idx)

    process=[]
    for i in range(100,len(idx)):

        code = idx[i]

        print('正在获取股票%s数据,第%s个'% (code,i))
        p = Process(target=get_ini,args=(code,))
        p.start()
        process.append(p)
        for p in process:
            p.join()
