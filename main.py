'''
本内容参考自网页https://cloud.tencent.com/developer/article/1932575
用于学习网络爬虫
从东京大学官网检测最新通知并存储起来，当有新通知的时候发送邮件
'''
import csv #用于把爬取的数据存成CSV格式
import time #用于对请求加延时以避免被反爬
from time import sleep #同上
import random #用于对延时设置随机数
import requests #用于向网站发送请求
from lxml import etree #网页解析库lxml
import os
import send_email #自定义函数，用于发送邮件

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

#提取news_web，对Element对象使用xpath筛选，返回一个列表（里面的元素也是Element）
# all_tr = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div')
#                     //*[@id="content"]/div[4]/div/div/div[2]/div/ul/li[1]/a/p[2]
news_web = parse.xpath('//*[@id="content"]/div[4]/div/div/div[2]/div/ul/li')

# print(len(all_tr))

#通过xpath获取标签内的text和herf（超链接）
news = []
for item in news_web:
    news.append({
        'date': ''.join(item.xpath('./a/p[1]/text()')).strip(),
        'title': ''.join(item.xpath('./a/p[2]/text()')).strip(),
        # 'link': ''.join(['https://www.u-tokyo.ac.jp/',tr.xpath('./a/@href')]).strip()
        'link': 'https://www.u-tokyo.ac.jp'+item.xpath('./a/@href')[0]
    })

print(news)

#将news存到csv文件里
# #判断news.txt文件是否存在，不存在则创建，并写入date-title-link数据
# if not os.path.isfile('news.txt'):
#     f = open(news.txt,'w')



#     f.close()
# #存在的话，提取里面的内容，如果内容不一致，则表明通知更新

with open('news.csv','a+',encoding='utf_8_sig',newline='') as f:
    # a+为读写模式
    # utf_8_sig格式导出csv不乱码
    # 从头到尾对比news.csv文件与爬到的文件是否有一致的条目，没有的话就添加并提示
    fieldnames = ['date','title','link']
    for i in range(len(news)):
        flag = False
        #设置文件读取指针到开头
        f.seek(0,0)
        reader = csv.DictReader(f)
        for row in reader:
            # print(type(row),row)
            if news[i] == row:
                flag = True
        if not flag:
            f.seek(0,2)
            writer = csv.DictWriter(f,fieldnames)
            writer.writerow(news[i])
            send_email.send(news[i])
            time.sleep(2)




    # fieldnames = ['date','title','link']
    # writer = csv.DictWriter(f,fieldnames)
    # for i in range(len(news)):
    #     writer.writerow(news[i])


