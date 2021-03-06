import requests
import pandas as pd
import re
import pymysql
import tushare as ts
import datetime
import numpy as np

# 更新每日个股信息
# 获取交易日期，并判断今日是否为交易日


def is_trade_day():
    a = datetime.date.today()
    d = datetime.timedelta(days=31)
    prem = a-d
    a = a.__format__('%Y%m%d')
    prem = prem.__format__('%Y%m%d')

    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=prem, end_date=a)

    s = (df[df['cal_date'] == a])
    jud = (s['is_open'] == 1)
    return jud.iloc[0]


def get_trade_day():
    a = datetime.date.today()
    d = datetime.timedelta(days=31)
    prem = a-d
    a = a.__format__('%Y%m%d')
    prem = prem.__format__('%Y%m%d')
    pro = ts.pro_api()
    df = pro.trade_cal(exchange='', start_date=prem, end_date=a)

    trade_day = df[df['is_open'] == 1]
    return trade_day


# 获取交易日当日每只股票数据


def get_data(csvfile):
    if not is_trade_day():
        return
    else:
        sl = pd.read_csv(csvfile, header=None, dtype=str)
        idx = sl.iloc[1:, 1]
        a = datetime.date.today()
        # d=datetime.timedelta(days=1)
        # a=a-d
        a = a.__format__('%Y-%m-%d')
        td = get_trade_day()
        pretd = td.iloc[-2, 1]
        pretd = datetime.datetime.strptime(pretd, "%Y%m%d")
        pretd = pretd.__format__('%Y-%m-%d')

        daily_data = pd.DataFrame(columns={})
        for code in idx:
            # print(code)
            url = 'http://quotes.money.163.com/trade/ls\
            jysj_' + str(code) + '.html#'
            wbdata = requests.get(url).text
            sa = re.findall(a+"(.*?)"+pretd, wbdata)
            if sa:
                num = re.findall(">(.*?)<", sa[0], re.S)
                num = [x for x in num if x != '']
                daily_data.loc[:, str(code)] = num

        daily_data = daily_data.T
        return daily_data

# 将最新数据存入数据库


def save_data(csvfie):
    if not is_trade_day():
        return
    else:
        data = get_data('sha_list.csv')
        print(data)
        idx = data.index
        sl = pd.read_csv('sha_list.csv', header=None, dtype=str)
        sl = sl.iloc[1:, 1:3]
        sl = sl.set_index(1)

        db = pymysql.connect(
            host='localhost', port=3306,
            charset='utf8',
            user='root', password='lmy6571495')
        cursor = db.cursor()
        cursor.execute("use stockdata")

        for code in idx:
            save = data.loc[code]
            dt = datetime.date.today().__format__('%Y/%m/%d')
            co = '\''+str(code)
            name = str(sl.loc[code, 2])
            spj = np.float64(save[3])
            zgj = np.float64(save[1])
            zdj = np.float64(save[2])
            kpj = np.float64(save[0])
            qsp = np.float64(1)
            zde = str(save[4])
            zdf = str(save[5])
            hsl = np.float64(save[9])
            cjl = save[6]
            cjl = cjl.replace(',', '')
            cjl = np.int64(cjl)
            cje = save[7]
            cje = cje.replace(',', '')
            cje = np.float64(cje)
            record = (
                dt, co, name, spj, zgj, zdj, kpj,
                qsp, zde, zdf, hsl, cjl, cje)

            #  插入数据语句
            try:
                print('正在存储stock_%s' % str(code))
                sqlSentence4 = "insert into stock_%s" % str(code) + " (日期, 股票代码, 名称, 收盘价, 最高价, 最低价, 开盘价,\
                前收盘, 涨跌额, 涨跌幅, 换手率, 成交量, 成交金额) \
                values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
                sqlSentence4 = sqlSentence4.replace('nan', 'null').replace('None', 'null').replace('none', 'null')
                cursor.execute(sqlSentence4)
                db.commit()
            except:  # 如果以上插入过程出错，跳过这条数据记录，继续往下进行
                db.rollback()
                break
        cursor.close()
        db.commit()
        db.close()


if __name__ == '__main__':
    save_data('sha_list.csv')
    save_data('sza_list.csv')
