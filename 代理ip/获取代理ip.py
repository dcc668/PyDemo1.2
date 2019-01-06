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
import queue
from 代理ip.dao.save2mysql import Data2MySql


urls=set()#ip去重复
q = queue.Queue()
def get_bhtml(url):
    user_agent = random.choice(AGENTS)
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    bhtml = s.get(url, headers={'User-Agent': user_agent},timeout=10).content
    html_doc = EncodingUtils.getStrNotKnowEcoding(bhtml)
    return BeautifulSoup(html_doc, "html.parser")

def getXiciProxy(targeturl):
    count=0
    for page in range(1, 10):
        url = targeturl + str(page)
        soup=get_bhtml(url)
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            # 国家
            if tds[0].find('img') is None:
                nation = '未知'
                locate = '未知'
            else:
                nation = tds[0].find('img')['alt'].strip()
                locate = tds[3].text.strip()
            ip = tds[1].text.strip()
            port = tds[2].text.strip()
            anony = tds[4].text.strip()
            protocol = tds[5].text.strip().lower()
            speed = tds[6].find('div')['title'].strip()
            time = tds[8].text.strip()
            urls.add(ip+':'+port)
            print('%s=%s:%s' % (protocol, ip, port))
            count+=1
    print('获取url总数-----------〉〉'+str(count))
    return len(urls)


def getHttpDailiProxy(targeturl):
    soup=get_bhtml(targeturl)
    tabs=soup.find_all('table')
    print("tabs:"+str(len(tabs)))
    for tab in tabs:
        trs=tab.find_all('tr')
        for tr in trs[1:]:
            tds=tr.find_all('td')
            ip=tds[0].text.strip()
            port=tds[1].text.strip()
            locate=tds[3].text.strip()
            urls.add(ip+':'+port)
            print("%s:%s %s"%(ip,port,locate))
    print('获取url总数-----------〉〉' + str(len(urls)))
    return len(urls)

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
        urls.add(ip+':'+port)
        print("%s:%s %s %s"%(ip,port,locate,time))
    print('获取url总数-----------〉〉' + str(len(urls)))
    return len(urls)

def kuaiDaiLi(targetUrl):
    soup = get_bhtml(targetUrl)
    tabs=soup.find_all('table')
    while len(tabs)<=0:#报错时再请求
        soup = get_bhtml(targetUrl)
        tabs = soup.find_all('table')
    trs=tabs[0].find_all('tr')
    for tr in trs[1:]:
        tds=tr.find_all("td")
        speed = tds[5].text.strip()
        res=re.search("(.*?)秒",speed).group(1)
        try:
            if float(res)<=1:
                ip=tds[0].text.strip()
                port = tds[1].text.strip()
                locate = tds[4].text.strip()
                protocol = tds[3].text.strip().lower()
                urls.add(ip+':'+port)
                print("%s:%s %s %s" % (ip, port, locate, speed))
        except Exception:
            pass
    print('获取url总数-----------〉〉' + str(len(urls)))
    return len(urls)
"""
从www.kxdaili.com抓取免费代理
"""
def fetch_kxdaili(targetUrl):
    try:
        soup = get_bhtml(targetUrl)
        table_tag = soup.find("table", attrs={"class": "segment"})
        trs = table_tag.tbody.find_all("tr")
        print(len(trs))
        for tr in trs:
            tds = tr.find_all("td")
            ip = tds[0].text
            port = tds[1].text
            gaoni = tds[2].text.strip().lower()
            latency = tds[4].text.split(" ")[0]
            print("%s:%s %s %s" % (ip, port, latency, gaoni))
            if float(latency) < 1: # 输出延迟小于1秒的代理
                urls.add(ip+':'+port)
    except Exception as e:
        print(e)
        print("fail to fetch from kxdaili")
    print('获取url总数-----------〉〉' + str(len(urls)))
    return len(urls)

'''
验证代理的有效性
'''
def verifyProxyList(v_url,urls):
        while len(urls) > 0:
            myurl = 'http://'+urls.pop()
            try:
                start=time.time()
                print(myurl)
                proxies = {
                    'http': myurl,
                }
                res=requests.get(url=v_url,proxies=proxies,timeout=3.0)
                end=time.time()
                print("验证代理的有效性:"+myurl+"--->>use time:"+str(end-start))
                #响应时间小于1.5秒
                useTime=end-start
                if res.status_code==200 and useTime<3:
                    print("+++Success:" + myurl)
                    print("--------存文件--------->>>>>:"+myurl)
                    q.put(myurl)
            except Exception as e:
                print("---Failure:" + myurl+str(e))
if __name__ == '__main__':

    print('-----------------------------------------------------１--------从xici获取获取-----------')
    # try:
    #     proxynum = getXiciProxy("http://www.xicidaili.com/nn/")
    # except Exception as e:
    #     print(u"国内高匿：发生异常" +str(e))
    # try:
    #     proxynum = getXiciProxy("http://www.xicidaili.com/nt/")
    # except Exception as e:
    #     print(u"国内透明：发生异常" + str(e))
    # try:
    #     proxynum = getXiciProxy("http://www.xicidaili.com/wn/")
    # except Exception as e:
    #     print(u"国外高匿：发生异常" + str(e))
    # try:
    #     proxynum = getXiciProxy("http://www.xicidaili.com/wt/")
    # except Exception as e:
    #     print(u"国外透明：发生异常" + str(e))
    # print('-----------------------------------------------------2----从www.httpdaili.com获取-----------')
    # try:
    #     getHttpDailiProxy("http://www.httpdaili.com/#c-4");
    # except Exception as e:
    #     print(u"httpdaili发生异常" + str(e))
    # print('-----------------------------------------------------3--------从http://www.66ip.cn/areaindex_2/1.html获取-----------')
    # for i in range(1,300):
    #     try:
    #         daiLi66("http://www.66ip.cn/areaindex_2/"+str(i)+".html");
    #     except Exception as e:
    #         print(u"66ip发生异常" + str(e))
    # print('-----------------------------------------------------4--------从kuaidaili获取-----------')
    # for i in range(1,60):
    #     try:
    #         kuaiDaiLi("http://www.kuaidaili.com/free/inha/"+str(i))
    #     except Exception as e:
    #         print(u"kuaidaili发生异常" + str(e))
    print('-----------------------------------------------------5--------从kxdaili获取-----------')
    for i in range(1, 10):
        try:
            fetch_kxdaili("http://www.kxdaili.com/dailiip/1/%d.html" % i)
        except Exception as e:
            print(u"kxdaili发生异常" + str(e))


    print(u"\n验证代理的有效性：")
    v_url='https://www.baidu.com/'
    thread_size=30
    pre_thread_ips=int(len(urls)/thread_size)
    all_thread = []
    for i in range(thread_size):
        start=int(i*pre_thread_ips)
        if i==thread_size-1:
            sub_urls=list(urls)[start:len(urls)]
        else:
            end=int(i*pre_thread_ips+pre_thread_ips)
            sub_urls=list(urls)[start:end]
        t = threading.Thread(target=verifyProxyList,args=(v_url,sub_urls))
        all_thread.append(t)
        t.start()

    for t in all_thread:
        t.join()
    print('Total count:'+str(q.qsize()))
    print("--------存文件--------->>>>>:")
    ips_str=''
    ips=[]
    with open('ips.txt','w',encoding='utf-8') as file:
        while q.qsize()>0:
            use_ip=q.get()
            ips.append(use_ip)
            file.write(use_ip+'\n')
    print('--------存文件---------全部成功:')
    print("--------存mysql数据库--------->>>>>:")
    mysql=Data2MySql()
    mysql.process_item(ips)
    print('--------存mysql数据库---------全部成功:'+str(len(ips)))

    print("All Done.")

