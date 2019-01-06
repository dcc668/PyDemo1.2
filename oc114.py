#!  /usr/bin/env python
#ecoding=utf-8
import  requests
from lxml import html
import re
import pandas

url="http://shanghai.114oc.com/"
sub_url="http://shanghai.114oc.com/message/type-"
category=('cantingjiudian','paifacuxiao','qunyanbaoan','moteliyi','kefuzhanhui','jigonggongren','qitajianzhi')
names=('餐厅酒店','派发促销','群演保安','模特礼仪','客服展会','技工工人','','其他兼职')

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.3',
}
rows=[]
len=len(category)
for i in range(0,len):
    bhtml=requests.get(sub_url+category[i],headers=headers).content
    result=html.fromstring(bhtml)
    items=result.xpath('//*[@id="message_main"]/div[2]/div[58]/div');
    for item in items:
        #title
        title = item.xpath('./div[1]/div[1]')
        dateStr=title[0].xpath("string(.)")
        date=re.findall('(\d{4}.\d{1,2}.\d{1,2} \d{1,2}:\d{1,2})',dateStr)[0]
        content = item.xpath('./div[2]/pre/text()')[0]

        rows.append([date,content,names[i]])

date=pandas.DataFrame(rows)
date.to_csv('oc114.csv',header=['时间','内容','分类'])