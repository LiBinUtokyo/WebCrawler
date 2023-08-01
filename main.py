'''
本内容参考自网页https://cloud.tencent.com/developer/article/1932575
用于学习网络爬虫

'''
import csv #用于把爬取的数据存成CSV格式
import time #用于对请求加延时以避免被反爬
from time import sleep #同上
import random #用于对延时设置随机数
import requests #用于向网站发送请求
from lxml import etree #网页解析库lxml

#构造请求url和头部信息headers
url = 'https://www.u-tokyo.ac.jp/ja/index.html'
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

#通过rquestes获取网页信息，使用apparent来解决返回乱码的问题
response = requests.get(url, headers = headers, timeout = 10)
response.encoding = response.apparent_encoding
html = response.text
# print(html)

#解析网页，对html文本使用 etree.HTML(html)解析，得到Element对象
parse = etree.HTML(html)

#提取tr，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
# all_tr = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div')
#                     //*[@id="content"]/div[4]/div/div/div[2]/div/ul/li[1]/a/p[2]
all_tr = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div/ul/li')

# print(len(all_tr))


for tr in all_tr:
    tr = {
        'date': ''.join(tr.xpath('./a/p[1]/text()')).strip(),
        'title': ''.join(tr.xpath('./a/p[2]/text()')).strip()
    }
    print(tr)
    # print(tr.tag, tr[0][0].tag)
    # print(tr.text, tr[0][0].text)






