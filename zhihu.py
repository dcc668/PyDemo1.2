#!  /usr/bin/env python
#ecoding=utf-8

import  requests
from lxml import html

url="https://www.zhihu.com"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.3',
    'Cookie':'q_c1=2feb42d6aa8d480185b54cf011575ffd|1513656706000|1513656706000; _zap=5bbb9c08-9d62-44eb-8b47-080516a4c57f; d_c0="ACACZul03AyPTu7dQ6jPwt5e8MMclcX75iI=|1513733027"; r_cap_id="Y2IyYzJmZmQ4ZTQ5NDJiNzkyZmZkMTcyODNmMDIyZTc=|1513825424|6436c4dcf09d816849e73f557b87e1af087861a0"; cap_id="YjkzYzg4N2E2MjU2NDljNThkMGUyODdhMjM3NmE4YmU=|1513825424|866a2412bafe546d1b2d9c87094c39eaf1c65e2e"; __utma=51854390.1043173927.1513825481.1513825481.1513825481.1; __utmb=51854390.0.10.1513825481; __utmc=51854390; __utmz=51854390.1513825481.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20171221=1; z_c0=Mi4xbVBTMUJRQUFBQUFBSUFKbTZYVGNEQmNBQUFCaEFsVk5tbklvV3dCemEyT3NOX2VwUWlybWNwTGVNNmthU3lyc0Jn|1513825434|2bc8e12ff610d0591ee71386b6204f032fcd610d; _xsrf=007947a5-3ee6-4b6e-954b-70531a8445d0'
}
bhtml=requests.get(url,headers=headers).content

result=html.fromstring(bhtml)
items=result.xpath('//*[@id="root"]/div/main/div/div/div[1]/div[2]/div/div');
for item in items:
    #获取来源
    froms = item.xpath('./div/div[1]/div')
    if len(froms)>0:
        comeFrom=froms[0].xpath('string(.)')
        print("from:"+comeFrom);
    #获取标题
    titles = item.xpath('./div/div[2]/h2/div/a')
    if len(titles)>0:
        title=titles[0].xpath('string(.)')
        print("title:"+title);
    #获取内容
    contents = item.xpath('./div/div[2]/div[2]/div[1]/span/text()')
    if len(contents)==0:
        contents = item.xpath('./div/div[2]/div[2]/div[2]/span/text()')
    if len(contents) >0:
        print("content:"+contents[0]);
