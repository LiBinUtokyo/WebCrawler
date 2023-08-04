'''
爬取globalkomaba的通知
globalkomaba网址：https://www.globalkomaba.c.u-tokyo.ac.jp
直接从数据库爬取信息
https://www.globalkomaba.c.u-tokyo.ac.jp/json/nabi00000028.json?build=20230516123344
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
import json

#构造请求url和头部信息headers
url = 'https://www.globalkomaba.c.u-tokyo.ac.jp/json/nabi00000028.json?build=20230516123344'
headers = {'User-Agent': info['agent1']}

#通过rquestes获取网页信息，使用apparent来解决返回乱码的问题
response = requests.get(url, headers = headers, timeout = 10)
# #保存网页文件
# html = response.content
# with open('globalkomaba.html','wb') as f:
#     f.write(html)

#这里直接从数据库直接获取所有data，不需要解析网页了
response.encoding = response.apparent_encoding
data_all = response.text
# print(type(data_all))
data_all = json.loads(data_all) #将json字符串解析为字典列表
# print(type(data_all),data_all[0])
# #解析网页，对html文本使用 etree.HTML(html)解析，得到Element对象
# parse = etree.HTML(html)

# #提取news_web，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
# # all_tr = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div')
# #                     //*[@id="content"]/div[4]/div/div/div[2]/div/ul/li[1]/a/p[2]
# news_web = parse.xpath('//*[@id="tab01_content"]/div/div/news-all-493/div/news-li-item-28')

# # print(len(news_web))

# 获取标签内的text和herf（超链接）
news = []
for item in data_all:
    news.append({
        'Date': item['display_date'],
        'Title': item['title'],
        'Link': 'https://www.globalkomaba.c.u-tokyo.ac.jp/news/nid'+str(item['cms_news_id']).rjust(8,'0')+'.html',
        'Description':item['description']
    })

# print(news)

#将news存到csv文件里
# # #存在的话，提取里面的内容，如果内容不一致，则表明通知更新

with open('news_golobalkobama.csv','a+',encoding='utf_8_sig',newline='') as f:
    # a+为读写模式
    # utf_8_sig格式导出csv不乱码
    # 从头到尾对比news.csv文件与爬到的文件是否有一致的条目，没有的话就添加并提示
    fieldnames = ['Date','Title','Link','Description']
    for i in range(20):
        flag = False
        #设置文件读取指针到开头
        f.seek(0,0)
        reader = csv.DictReader(f)
        for row in reader:
            # print(type(row),row)
            if news[i] == row:
                flag = True
                # print('The Same')
                # print(news[i])
                # print(row)
                # print(flag)
            # if news[i] != row:
                # differ = set(row.items())^set(news[i].items())
                # print(differ)
                # print(news[i])
                # print(row)
        if not flag:
            f.seek(0,2)
            writer = csv.DictWriter(f,fieldnames)
            writer.writerow(news[i])
            content = 'Date: %s \r\n Title: %s \r\n Link: %s \r\n Note: %s' %(news[i]['Date'],news[i]['Title'],news[i]['Link'],news[i]['Description'])
            send_email.send(news[i]['Date']+': '+news[i]['Title'],content)
            time.sleep(2)

















