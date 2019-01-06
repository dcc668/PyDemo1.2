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


lock = threading.Lock()
urls=set()#ip去重复
urls2=set()#ip去重复
ips = []
def get_bhtml(url):
    user_agent = random.choice(AGENTS)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    bhtml = s.get(url, headers={'User-Agent': user_agent},timeout=10).content
    html_doc = EncodingUtils.getStrNotKnowEcoding(bhtml)
    return BeautifulSoup(html_doc, "html.parser")

def daiLi66(targetUrl):
    soup = get_bhtml(targetUrl)
    tbs=soup.find_all("table")
    trs=tbs[2].find_all("tr")
    for tr in trs[1:]:
        tds=tr.find_all("td")
        ip = tds[0].text.strip()
        port= tds[1].text.strip()
        locate = tds[2].text.strip()
        time = tds[4].text.strip()
        urls.add("|".join(("", ip, port, locate, "", "http", "", "")))
        print("%s:%s %s %s"%(ip,port,locate,time))
    print('获取url总数-----------〉〉' + str(len(urls)))
    return len(urls)

def data5u(targetUrl):
    soup = get_bhtml(targetUrl)
    tbs=soup.select("ul.l2")
    for tr in tbs:
        spans=tr.select("span")
        ip=spans[0].select("li")[0].text
        port=spans[1].select("li")[0].text
        protocal=spans[3].select("li")[0].text
        url=protocal+"://"+ip+":"+port
        print(str(ip))
        urls2.add(url);
    print('获取url总数-----------〉〉' + str(len(urls2)))
    return len(urls2)


'''
验证代理的有效性
'''
def verifyProxyList():
    while True:
        if len(urls) == 0: break
        lock.acquire()
        ll = urls.pop()
        lock.release()
        if len(ll) == 0: break
        line = ll.strip().split('|')
        protocol = line[5]
        ip = line[1]
        port = line[2]
        myurl=protocol+"://"+ip+":"+port

        try:
            conn = HTTPConnection(ip, port, timeout=3.0)
            start=time.time()
            conn.request(method='GET', url="http://www.baidu.com", headers={'User-Agent': random.choice(AGENTS)})
            res = conn.getresponse()
            end=time.time()
            print("验证代理的有效性:"+myurl+"--->>use time:"+str(end-start))
            #响应时间小于1.5秒
            useTime=end-start
            if res.status==200 and useTime<2:
                print("+++Success:" + ip + ":" + port)
                lock.acquire()
                print("--------存文件--------->>>>>:"+myurl)
                with open('guowai_ip.txt','w',encoding='utf-8') as needIp:
                    needIp.write(str(myurl + "\n",'utf-8'))
                ips.append(ip+":"+port)
                lock.release()
        except Exception as e:
            print(e)
            print("---Failure:" + ip + ":" + port)
def verifyProxyList2():
    while True:
        if len(urls2) == 0: break
        lock.acquire()
        ll = urls2.pop()
        lock.release()
        if len(ll) == 0: break
        type=ll.split("://")[0]
        url=ll.split("://")[1]
        ip=url.split(":")[0]
        try:
            start=time.time()
            proxies = {
                type:ip
            }
            print("验证代理的有效性,请求:"+ll)
            res=requests.get(url="https://www.google.com",headers={'User-Agent': random.choice(AGENTS)},proxies=proxies,timeout=10)
            end=time.time()
            print("验证"+ll+"--->>use time:"+str(end-start))
            #响应时间小于1.5秒
            useTime=end-start
            if res.status_code==200 and useTime<3:
                print("+++Success:" + ll)
                lock.acquire()
                print("--------存文件--------->>>>>:"+ll)
                with open('guowai_ip.txt','w',encoding='utf-8') as needIp:
                    needIp.write(str(ll + "\n",'utf-8'))
                ips.append(ll)
                lock.release()
        except Exception as e:
            # print(e)
            print("---Failure:" + ll)
if __name__ == '__main__':
    print('-----------------------------------------------------3--------从http://www.66ip.cn/areaindex_2/1.html获取-----------')
    for i in range(33,35):
        try:
            daiLi66("http://www.66ip.cn/areaindex_"+str(i)+"/1.html");
        except Exception as e:
            print(u"66ip发生异常" + str(e))
    # countrys=["美国","英国","法国","加拿大","澳大利亚","香港","澳门"]
    # for i in countrys:
    #     url="http://www.data5u.com/free/country/"+i+"/index.html"
    #     data5u(url)

    print(u"\n验证代理的有效性：")
    all_thread = []
    for i in range(10):
        t = threading.Thread(target=verifyProxyList)
        all_thread.append(t)
        t.start()
    # for i in range(10):
    #     t = threading.Thread(target=verifyProxyList2)
    #     all_thread.append(t)
    #     t.start()
    for t in all_thread:
        t.join()
    print("All Done.")

