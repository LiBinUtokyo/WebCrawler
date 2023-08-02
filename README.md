# WebCrawler
Let's learn it  
来学习爬虫吧  

适用人群：希望跟踪最新校内公告的东大新领域创成研究科在校生  
本项目核心功能：监视目标网页的公告栏。有新的公告刊载的话，就向你指定的邮箱发送通知邮件

- `main_wiout_login.py`: 普通网页的内容爬取（东大官网）
- `main_with_login.py`: 带有登陆页面的揭示板公告爬取（东大新领域人间环境揭示板）
- `send_email.py`: 发送邮件的函数  
- `news.csv`: 存储东大官网ADMISSIONS部分公告的数据库
- `news_GSFS`: 存储东大新领域人间环境校内公告的数据库


## 注意：需要自己定义config.py，news_GSFS.csv文件和设置while True循环
在开始运行`main_wiout_login.py`或`main_with_login.py`之前：
- 自行创建config.py文件并在其中定义如下内容
```python
info = {
'msg_from': '', #设置了SMTP的发送者的邮箱地址
'passwd': '', #发送者SMTP的授权码
'to': '', #接受通知的邮箱地址
'agent1': '', #用于main_no_login.py的User-Agent信息(请自行在希望监测的目标网页的网页检查器中找到它)
'agent2': '', #用于main_with_login.py的agent信息(请自行在希望监测的目标网页的网页检查器中找到它)
'cookie':'', #用于main_with_login.py的cookie信息(请自行在希望监测的目标网页的网页检查器中找到它)
'urls': [] #用于main_with_login.py，可以填：'soumu','kyoumu','yosan','kenkyu','keiyaku','ilo'及其中的任意子集
}
```
- 自行创建news_GSFS.csv文件并在第一行加入如下表头：  
`Category,Date,Title,Link`

- 如果希望周期性自动运行脚本，请自行对整个脚本设置while True循环