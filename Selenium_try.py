"""
尝试使用Selenium完成网页的谷歌登陆操作从而可以持续地爬取校内通知
但是使用webdriver登陆Gmail似乎违反了网站的使用条款，所以只能放弃了
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
# driver.get("https://gsfs-portal.k.u-tokyo.ac.jp/")
driver.get('https://www.selenium.dev/zh-cn/documentation/webdriver/getting_started/first_script/')
title = driver.title
print(title)

