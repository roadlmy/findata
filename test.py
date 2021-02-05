import requests
# from spider.UA import agents
import random
import time
import json
# from spider.stock_queue import StockMongo
from lxml import html
import multiprocessing
from thread_pool import ThreadPool#自己写的线程池

import requests
import re
import pandas as pd

import urllib
import re
import pandas as pd
import pymysql
import os

def get_indi():
    ticker = pd.DataFrame(columns={})
    for i in range(1,124):
        url = 'http://19.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405729827281650932_1612450709581&pn='+str(i)+'&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1612450709582'
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
    save_sza = ticker.reset_index(drop=True)
    print(save_sza)
    save_sza.to_csv('sza_list.csv')
def list_crawler():
    pool=ThreadPool(6)
    for i in range(1,3):
        pool.run(func=get_indi,args=(i,))  ###124页



    # url = 'http://73.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408013832830150123_1612441015559&pn='+str(i)+'&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1612441015560'
if __name__ == '__main__':
    process=[]
    num_cups=multiprocessing.cpu_count()
    print('将会启动的进程数为',num_cups)
    for i in range(int(num_cups)-2):
        p=multiprocessing.Process(target=get_indi)#创建进程
        p.start()
        process.append(p)
        for p in process:
            p.join()
    # list_crawler()
    # ticker = ticker.T
    # print(ticker)
