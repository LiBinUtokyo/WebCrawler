import csv #用于把爬取的数据存成CSV格式
import time #用于对请求加延时以避免被反爬
from time import sleep #同上
import random #用于对延时设置随机数
import requests #用于向网站发送请求
from lxml import etree #网页解析库lxml
import os
import send_email #自定义函数，用于发送邮件
from config import info
import re
news = []
headers = {'User-Agent':info['agent2'],
        'Cookie': info['cookie']}


news.append({'Link': 'https://gsfs-portal.k.u-tokyo.ac.jp/keiyaku/news/keiyaku-notice/2936/'})


#获取新通知内容,还没写完，不过感觉不是很有必要
response = requests.get(news[0]['Link'], headers = headers, timeout = 10)
html = response.text
# print(html)
#解析网页，对html文本使用 etree.HTML(html)解析，得到Element对象
parse = etree.HTML(html)
cont = parse.xpath('/html/body/div/div/div/div/div/div/article/div/div')
# print(cont)
# print(type(cont))
Content=''
# for i in cont[0].iter('p','strong','href','li'):
#     if i.text:
#         Content += i.text+' /r/n '
#         print(i.text)
#     if i.get('href'):
#         Content += i.get('href')+'/r/n'
#         print(i.get('href')) 

Content = ' \n '.join(cont[0].itertext())

Content = re.sub(r'\n+', '\n', Content)
    # if i.iter('a'):
    #     for j in i.iter('a'):
    #         Content += j.get('href')+'/r/n'
    #         print(j.get('href')) 

print(Content)
    # print(i.attrib)
# for i in cont[0].iter('a'):
#     print(i.get('href'))


#提取news_web，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
# print(parse.xpath('/html/body/div/div/div/div/div/div/article/div/div'))
# news_web = parse.xpath('/html/body/div/div/div/div/div/div/section') 
