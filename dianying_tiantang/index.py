#!/usr/bin/env Python
# coding=utf-8
import requests
import re
from requests import RequestException
from utils.ecoding_utils import EncodingUtils
from pandas import DataFrame,ExcelWriter
from multiprocessing import Pool
def get_page(url):
    try:
        response=requests.get(url,timeout=10)
        if response.status_code==200:
            return EncodingUtils.getStrNotKnowEcoding(response.content)
        else:
            print('request error  .....  status:'+str(response.status_code))
            return None
    except RequestException as e:
        print(e)
        return None

def parse_html(page):
    url='http://www.dytt8.net/html/gndy/dyzz/list_23_'+str(page)+'.html'
    html=get_page(url)
    pattern=re.compile('<b>.*?<a href="(.*?)" class="ulink">(.*?)</a>',re.S)
    items=re.findall(pattern,html)
    for item in items:
        yield {
            'name':item[1],
            'url':'http://www.dytt8.net'+item[0]
        }


#获取下载连接
def parse_link(url):
    html=get_page(url)
    pattern=re.compile('bgcolor="#fdfddf"><a href="(.*?)"',re.S)
    link=re.findall(pattern,html)
    if len(link)>0:
        return link[0]
    else:
        return None

def parse(page):
    res=[]
    print('.......get page.........'+str(page))
    for item in parse_html(page):
        link=parse_link(item['url'])
        res.append(item['name']+","+link)
    print('write to file.......')
    with open('dianying.txt','a',encoding='utf-8') as file:
        for line in res:
            file.write(str(line)+'\n')
if __name__=='__main__':
    pool=Pool(3)
    pool.map(parse,[x for x in range(1,10)])

