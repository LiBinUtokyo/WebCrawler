'''
本脚本用于对存在登陆验证的网页使用爬虫
目前似乎不需要使用cookie了
从东大新领域揭示板https://gsfs-portal.k.u-tokyo.ac.jp/中提取新通知

'''
import csv #用于把爬取的数据存成CSV格式
import time #用于对请求加延时以避免被反爬
from time import sleep #同上
import random #用于对延时设置随机数
import requests #用于向网站发送请求
from lxml import etree #网页解析库lxml
import os
import send_email #自定义函数，用于发送邮件
from config import info
count = 0
while True:
    #构造请求url和头部信息headers
    for url in info['urls']:
        url = 'https://gsfs-portal.k.u-tokyo.ac.jp/'+url+'/news/'
        # url = 'https://gsfs-portal.k.u-tokyo.ac.jp/soumu/news/'
        # print(url)
        # headers = {'User-Agent':info['agent2'],
        #         'Cookie': info['cookie']}
        headers = {'User-Agent':info['agent2']}

        #通过rquestes获取网页信息
        response = requests.get(url, headers = headers, timeout = 10)
        # response.encoding = response.apparent_encoding
        html = response.text
        # print(html)

        #解析网页，对html文本使用 etree.HTML(html)解析，得到Element对象
        parse = etree.HTML(html)
        #提取news_web，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
        # print(parse.xpath('/html/body/div/div/div/div/div/div/section'))

        # news_web = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div/ul/li')
        news_web = parse.xpath('/html/body/div/div/div/div/div/div/section')

        #判断能否正常连接，不能的话就发送警告消息
        if not news_web:
            # print('网页不对')
            send_email.send('来自main_with_login.py的报告','温馨提示：该检查程序了。  它打不开目标网页啦！')
            break

        #通过xpath获取需要的信息，包括标签内的text和herf（超链接）
        news = []
        for section in news_web:
            # print(section)
            # print(section.xpath('./div/h3/text()'))
            # for item in section.xpath('.//*[class="c-list-5__item"]'):
            for item in section.xpath('./div/div/div/div/div/ul/li'):
                # print(item)
                # print(item.xpath('./a/p[1]/text()'))
                news.append({
                    'Category': ''.join(section.xpath('./div/h3/text()')),
                    'Date': ''.join(item.xpath('./a/p[2]/text()')).split(' ')[0],
                    'Title': ''.join(item.xpath('./a/p[1]/text()')),
                    'Link': ''.join(['https://gsfs-portal.k.u-tokyo.ac.jp',item.xpath('./a/@href')[0]])
                })
                # print(news[-1])

        #将news存到csv文件里
        #news_GSFS.csv文件不存在则创建，并写入Category-Date-Title-Link数据
        #存在的话，提取里面的内容，如果内容不一致，则表明通知更新
        with open('news_GSFS.csv','a+',encoding='utf_8_sig',newline='') as f:
            # a+为读写模式
            # utf_8_sig格式导出csv不乱码
            # 从头到尾对比news.csv文件与爬到的文件是否有一致的条目，没有的话就添加并提示
            # fieldnames = ['Category','Date','Title','Link']
            header = list(news[0].keys())
            writer = csv.DictWriter(f,header)
            # writer.writeheader()
            for i in range(len(news)):
                flag = False
                #设置文件读取指针到开头
                f.seek(0,0)
                reader = csv.DictReader(f)
                for row in reader:
                    # print(type(row),row)
                    if news[i] == row:
                        flag = True
                        break
                if not flag:
                    f.seek(0,2)
                    writer.writerow(news[i])
                    #获取新通知内容,还没写完，不过感觉不是很有必要
                    # response = requests.get(news[i]['Link'], headers = headers, timeout = 10)
                    # html = response.text
                    # # print(html)
                    # #解析网页，对html文本使用 etree.HTML(html)解析，得到Element对象
                    # parse = etree.HTML(html)
                    # #提取news_web，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
                    # # print(parse.xpath('/html/body/div/div/div/div/div/div/section'))
                    # news_web = parse.xpath('/html/body/div/div/div/div/div/div/section') 
                    Content=''
                    text = 'Date: %s \r\n Title: %s \r\n Link: %s \r\n Content: %s' %(news[i]['Date'],news[i]['Title'],news[i]['Link'],Content)
                    send_email.send(news[i]['Category']+': '+news[i]['Date']+'-'+news[i]['Title'],text)
                    print(text)
                    time.sleep(5*random.random())
        # time.sleep(5*random.random())
    #每隔一天检查一次
    count += 1
    print(count)
    time.sleep(86400-10*random.random())
    














