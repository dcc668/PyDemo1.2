#!  /usr/bin/env python
#ecoding=utf-8

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from http.client import HTTPConnection
import threading
import random
from settings import AGENTS
import  re
import time
from utils.ecoding_utils import EncodingUtils
import redis


needIp = open('ips.txt','w',encoding='utf-8')
lock = threading.Lock()
urls=set()#ip去重复
ips = []
rds = redis.StrictRedis(host='39.108.122.83', port=6379, decode_responses=True)
def init():
    #redish获取可用
    ips_str = rds.get('ips')
    ipss = ips_str.split('||')
    for ip in ipss:
        if ip == '':
            ipss.remove(ip)
        else:
            urls.add(ip)
    print('redis.....get.....ips'+str(ipss))
'''
验证代理的有效性
'''
def verifyProxyList(v_url):
    while True:
        if len(urls) == 0: break
        lock.acquire()
        ll = urls.pop()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split(':')
        protocol = 'http'
        ip = line[0]
        port = line[1]
        myurl=protocol+"://"+ip+":"+port

        try:
            start=time.time()
            proxies = {
                'http': myurl,
            }
            res=requests.get(url=v_url, headers={'User-Agent': random.choice(AGENTS)},proxies=proxies,timeout=3.0)
            end=time.time()
            print("验证代理的有效性:"+myurl+"--->>use time:"+str(end-start))
            #响应时间小于1.5秒
            useTime=end-start
            if res.status_code==200 and useTime<2:
                print("+++Success:" + ip + ":" + port)
                print(str(res.text))
                lock.acquire()
                print("--------存文件--------->>>>>:"+myurl)
                needIp.write(str(ll + "\n",'utf-8'))
                ips.append(ip+":"+port)
                lock.release()
        except Exception as e:
            print("---Failure:" + ip + ":" + port+str(e))
if __name__ == '__main__':
    init()
    v_url='http://www.zhihu.com'
    # v_url = 'http://www.baidu.com'
    print(u"\n验证代理的有效性：")
    all_thread = []
    for i in range(30):
        t = threading.Thread(target=verifyProxyList,args=(v_url,))
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()
    needIp.close()#所有线程操作完文件后，在关闭
    print("All Done.")

