# -*- coding:utf-8 -*-

import urllib.request, re, os
import pandas as pd
from datetime import datetime


def get_url(id):#获取页面
    url = 'http://quote.eastmoney.com/sz%s.html' % id
    req = urllib.request.Request(url)
    f = open('log.txt', 'a')
    try:
        data = urllib.request.urlopen(req).read().decode('gb18030')#网页的编码是gb2312，但是部分网页报编码错误，因此使用gb18030
        return data
    except UnicodeDecodeError:
        print(id, '编码错误')
        f.write('%s编码错误\n' % id)
        f.close()
        data = 0
        return data
    except urllib.error.HTTPError:
        try:
            data = urllib.request.urlopen(urllib.request.Request('http://quote.eastmoney.com/sh%s.html' % id)).read().decode('gb18030')
            return data
        except urllib.error.HTTPError:
            print(id, '股票页面未找到')
            f.write('%s页面不存在\n' % id)
            f.close()
            data = 0
            return data



def check_Quartile_info(Quartile,rank):#检查四分位属性是否为8个
    for i in range(len(rank)):
        if rank[i] == '—|—':#只要在评分相应位置检测出'—|—'，即代表该项无数据
            Quartile.insert(i, '无数据')
    return Quartile

def get_info(idlist):#获取信息
    all_info = []
    for id in idlist:
        data = get_url(id)
        if data != 0:
            print('正在获取%s的报表' % id)
            infomation = re.findall(r'<tbody>\s*(.*基准.</span></div>)', data)#匹配数据板块
            detail = re.findall(r'<td>(.{0,14})</td>', infomation[0])#详细信息
            industry = re.findall(r'target="_blank">(.{2,8})</a>', infomation[0])#行业
            name = detail[0].strip('<>/b')#名称
            name_info = detail[1:9]#名称信息
            level_info = detail[9:17]#行业平均
            rank_info = detail[18:27]#行业排名
            Quartile_info = re.findall(r'<p>(..?)</p>', infomation[0])#四分位属性
            if len(Quartile_info)<8:
                Quartile_info = check_Quartile_info(Quartile_info, rank_info)#检查四分位属性
            detail_info = []#59~72行  插入所获取id的报表
            detail_info.append(name)
            detail_info.append(industry[0])
            error = 1
            for i in range(8):
                try:
                    detail_info.append(name_info[i])
                    detail_info.append(rank_info[i])
                    detail_info.append(Quartile_info[i])
                except IndexError:#如果部分数据为空，则需要单独分析
                    f = open('log.txt', 'a')
                    f.write('%s需要单独分析\n' % id)
                    f.close()
                    error = 0
            if error:#若没有报错，就添加该列数据
                detail_info.append(id)#在列表末尾添加股票号码，代码中未使用，留作检查备用
                all_info.append(detail_info)
                #print(all_info)
    return all_info



def main(idlist):
    f = open('log.txt', 'wb')
    f.truncate()
    f.close()
    infomation = get_info(idlist)
    detail_info = {}
    detail_info['名称'] = []
    detail_info['行业'] = []
    detail_info['总市值'] = []
    detail_info['总市值排名'] = []
    detail_info['总市值四分位'] = []
    detail_info['净资产'] = []
    detail_info['净资产排名'] = []
    detail_info['净资产四分位'] = []
    detail_info['净利润'] = []
    detail_info['净利润排名'] = []
    detail_info['净利润四分位'] = []
    detail_info['市盈率'] = []
    detail_info['市盈率排名'] = []
    detail_info['市盈率四分位'] = []
    detail_info['市净率'] = []
    detail_info['市净率排名'] = []
    detail_info['市净率四分位'] = []
    detail_info['毛利率'] = []
    detail_info['毛利率排名'] = []
    detail_info['毛利率四分位'] = []
    detail_info['净利率'] = []
    detail_info['净利率排名'] = []
    detail_info['净利率四分位'] = []
    detail_info['ROE'] = []
    detail_info['ROE排名'] = []
    detail_info['ROE四分位'] = []
    for i in range(len(infomation)):
        #添加信息
        detail_info['名称'].append(infomation[i][0])
        detail_info['行业'].append(infomation[i][1])
        detail_info['总市值'].append(infomation[i][2])
        detail_info['总市值排名'].append(infomation[i][3])
        detail_info['总市值四分位'].append(infomation[i][4])
        detail_info['净资产'].append(infomation[i][5])
        detail_info['净资产排名'].append(infomation[i][6])
        detail_info['净资产四分位'].append(infomation[i][7])
        detail_info['净利润'].append(infomation[i][8])
        detail_info['净利润排名'].append(infomation[i][9])
        detail_info['净利润四分位'].append(infomation[i][10])
        detail_info['市盈率'].append(infomation[i][11])
        detail_info['市盈率排名'].append(infomation[i][12])
        detail_info['市盈率四分位'].append(infomation[i][13])
        detail_info['市净率'].append(infomation[i][14])
        detail_info['市净率排名'].append(infomation[i][15])
        detail_info['市净率四分位'].append(infomation[i][16])
        detail_info['毛利率'].append(infomation[i][17])
        detail_info['毛利率排名'].append(infomation[i][18])
        detail_info['毛利率四分位'].append(infomation[i][19])
        detail_info['净利率'].append(infomation[i][20])
        detail_info['净利率排名'].append(infomation[i][21])
        detail_info['净利率四分位'].append(infomation[i][22])
        detail_info['ROE'].append(infomation[i][23])
        detail_info['ROE排名'].append(infomation[i][24])
        detail_info['ROE四分位'].append(infomation[i][25])
    #print('输出的字典为',detail_info)
    a = pd.DataFrame(detail_info, columns=['名称', '行业', '总市值', '总市值排名', '总市值四分位', '净资产',
                                            '净资产排名', '净资产四分位', '净利润', '净利润排名', '净利润四分位',
                                            '市盈率', '市盈率排名', '市盈率四分位', '市净率', '市净率排名',
                                            '市净率四分位', '毛利率', '毛利率排名', '毛利率四分位', '净利率',
                                            '净利率排名', '净利率四分位', 'ROE', 'ROE排名', 'ROE四分位'])
    t = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    path = './金融报表/'
    if not os.path.exists(path):#判断路径是否存在
        os.makedirs(path)
    a.to_csv('%s%s金融报表.csv' % (path, t))
    print('输出成功')




if __name__ == '__main__':
    f = open('id.txt')#读取id.txt中的信息(可直接复制pdf至id.txt)
    str = str(f.readlines())
    f.close()
    list = re.findall(r'[0-9]{6}', str)
    main(list)