#!  /usr/bin/env python
#ecoding=utf-8
from lxml import etree
import requests

url="http://blog.csdn.net/"
resp=requests.get(url)
html=etree.HTML(resp.content) #将列表中的元素逐个用引号连接成字符串
title=html.xpath('//*[@id="feedlist_id"]/li[1]/div/div[1]/h2/a/text()')
print("title-->%s"%title)
