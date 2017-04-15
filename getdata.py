# -*- coding:utf-8 -*-

import urllib.request, re, csv, os
import pandas as pd


def get_url(id):#获取页面
    url = 'http://quote.eastmoney.com/sz%s.html' % id
    req = urllib.request.Request(url)
    print(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Mobile Safari/537.36')
    f = open('log.txt', 'a')
    try:
        data = urllib.request.urlopen(req).read().decode('gb2312')
        return data
    except UnicodeDecodeError:
        print('编码错误')
        f.write('%s编码错误\n' % id)
        f.close()
        data = 0
        return data
    except Exception:
        print('股票页面未找到')
        f.write('%s页面不存在\n' % id)
        f.close()
        data = 0
        return data

def dict(n,m):
    property = {}
    property[n] = {}
    property[n]['总市值'] = [m[0]]
    property[n]['净资产'] = [m[1]]
    property[n]['净利润'] = [m[2]]
    property[n]['市盈率'] = [m[3]]
    property[n]['市净率'] = [m[4]]
    property[n]['毛利率'] = [m[5]]
    property[n]['净利率'] = [m[6]]
    property[n]['ROE'] = [m[7]]
    return property


def get_info(idlist):#获取信息
    detail_info = {}
    for id in idlist:
        data = get_url(id)
        if data != 0:
            infomation = re.findall(r'<tbody>\s*(.*基准.</span></div>)',data)#匹配数据板块
            detail = re.findall(r'<td>(.{2,14})</td>', infomation[0])#详细信息
            industry = re.findall(r'target="_blank">(.{2,8})</a>',infomation[0])#行业
            name = detail[0].strip('<>/b')#名称
            name_info = detail[1:9]#名称信息
            level_info = detail[9:17]#行业平均
            rank_info = detail[18:27]#行业排名
            Quartile_info = re.findall(r'<p>(..?)</p>', infomation[0])#四分位属性
            #check_Quartile_info(Quartile_info,infomation[0])#检查四分位属性
            check_industry_exsit(industry,level_info)
            detail_info[name] = []
            for i in range(8):
                detail_info[name].append(name_info[i])
                detail_info[name].append(rank_info[i])
                detail_info[name].append(Quartile_info[i])
            print(detail_info)
    a = pd.DataFrame(detail_info)
    a.to_csv('ll.csv')




if __name__ == '__main__':
    with open('id.txt') as f:
        str = str(f.readlines())
    list = re.findall(r'[0-9]{6}', str)
    with open('log.txt', 'wb') as fe:
        fe.truncate()
    get_info(list)