#!  /usr/bin/env python
#ecoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver import PhantomJS,Chrome
from bs4 import  BeautifulSoup
import  requests,time
import traceback
import random,re
from utils.ecoding_utils import EncodingUtils
from threading import  Thread

class Spider():
    def __init__(self):
        self.tomJsDriver=r'driver\phantomjs.exe';
        self.chromeDriver=r'driver\chromedriver.exe'
        self.cookieStr=[
            "_lxsdk_cuid=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _lxsdk=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _hc.v=779de295-9cd3-45ad-a867-65458ae00ff3.1520221818; _dp.ac.v=9f06fda9-0d7b-4fec-9228-53c6a825f451; dper=3e6aae412c59c3557ed7370905e4d515a4e6f49128f520d0b281450f693bfc4a; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5123199509; ctu=64af27ffff1c544b89d50751bb4d5e9a180bc3dc00413abd29b5a7ce680ff117; uamo=17693433417; cy=1; cye=shanghai; JSESSIONID=52FDB58C61E7F7AB2453DC5D74B30CE1; s_ViewType=10; _lxsdk_s=161fb847669-98d-c32-20%7C%7C200",
            "_lxsdk_cuid=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _lxsdk=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _hc.v=779de295-9cd3-45ad-a867-65458ae00ff3.1520221818; _dp.ac.v=9f06fda9-0d7b-4fec-9228-53c6a825f451; dper=3e6aae412c59c3557ed7370905e4d515a4e6f49128f520d0b281450f693bfc4a; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5123199509; ctu=64af27ffff1c544b89d50751bb4d5e9a180bc3dc00413abd29b5a7ce680ff117; uamo=17693433417; cy=1; cye=shanghai; JSESSIONID=52FDB58C61E7F7AB2453DC5D74B30CE1; s_ViewType=10; _lxsdk_s=161fb847669-98d-c32-20%7C%7C242",
            "_lxsdk_cuid=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _lxsdk=161f4480d55c8-054b931d0d63f7-3a3e5e06-100200-161f4480d56c8; _hc.v=779de295-9cd3-45ad-a867-65458ae00ff3.1520221818; _dp.ac.v=9f06fda9-0d7b-4fec-9228-53c6a825f451; dper=3e6aae412c59c3557ed7370905e4d515a4e6f49128f520d0b281450f693bfc4a; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_5123199509; ctu=64af27ffff1c544b89d50751bb4d5e9a180bc3dc00413abd29b5a7ce680ff117; uamo=17693433417; cy=1; cye=shanghai; JSESSIONID=52FDB58C61E7F7AB2453DC5D74B30CE1; s_ViewType=10; _lxsdk_s=161fb847669-98d-c32-20%7C%7C263"
        ]
        self.headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':random.choice(self.cookieStr),
            'Host':'www.dianping.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        }
        self.ips=[]
        with open('ips/ips.txt','r',encoding='utf-8') as file:
            lines=file.readlines()
            for line in lines:
                self.ips.append(line.strip())
        print('>>>>>>>>>>>>>>>>>>>>>>>>>ips>>>>>>>>>>>>>>>>>>>>>>>>>'+str(self.ips))
        self.web='http://'+random.choice(self.ips)
        print(self.web)
        self.proxies = {
            'http':self.web,
        }
        self.change_selenium_ip_and_cookies()
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_argument('--proxy-server='+web)
        # self.tomjs = Chrome(executable_path= chromeDriver)
        # self.change_cookies()

    def change_ip(self):
        ip=random.choice(self.ips)
        self.proxies = {
            'http':ip,
        }
        print('>>>>>>>>>>>>>>>proxy ip changed!!!  '+ip+'>>>>>>>>>>>>>')
    # def change_selenium_ip_and_cookies(self):
    #     # dcap = dict(DesiredCapabilities.PHANTOMJS)
    #     dcap = DesiredCapabilities.PHANTOMJS.copy()
    #     # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
    #     agent = generate_user_agent(os=('mac', 'linux', 'win'))
    #     dcap["phantomjs.page.settings.userAgent"] = agent
    #     for key, value in self.headers.items():
    #         dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
    #     # 不载入图片，爬页面速度会快很多
    #     dcap["phantomjs.page.settings.loadImages"] = True
    #     #是否启用js
    #     dcap["phantomjs.page.settings.javascriptEnabled"] = True
    #     dcap["phantomjs.page.settings.browserName"] = 'Chrome'
    #     # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
    #     # proxy = webdriver.Proxy()
    #     # proxy.proxy_type = ProxyType.MANUAL
    #     # proxy.http_proxy = random.choice(self.ips)
    #     # proxy.add_to_capabilities(dcap)
    #     # #打开带配置信息的phantomJS浏览器
    #     # self.tomjs = PhantomJS(self.tomJsDriver, desired_capabilities=dcap)
    #     self.tomjs = PhantomJS(self.tomJsDriver)
    #     # 隐式等待5秒，可以自己调节
    #     self.tomjs.implicitly_wait(6)
    #     # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
    #     # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
    #     self.tomjs.set_page_load_timeout(10)
    #     # 设置10秒脚本超时时间
    #     self.tomjs.set_script_timeout(10)
    #     self.change_cookies()
    def change_selenium_ip_and_cookies(self,retry=False):
        if retry:
            # print(self.tomjs.page_source)
            self.tomjs.close()
        session = Session()
        session.headers.clear()
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('disable-infobars')
        option.add_argument('--proxy-server='+self.web)
        for key, value in self.headers.items():
            if 'Cookie'!=key:
                option.add_argument(
                    key+'="'+value+'"')
        self.tomjs =Chrome(executable_path=self.chromeDriver,chrome_options=option)
        self.change_cookies(session)
    def change_cookies(self,session):
        cookies=random.choice(self.cookieStr)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>change cookies>>>>>>>>>>>>>>>>>>>>>>>>>>'+str(cookies))
        for line in cookies.split(';'):
            #其设置为1就会把字符串拆分成2份
            name,value=line.strip().split('=',1)
            # session.cookies.set(name,value)
            self.tomjs.add_cookie({
                'domain': '.dianping.com',  # 服务器域名 此处xxx.com前，需要带点
                'name': name,#cookie的名称
                'value': value,#cookie对应的值，动态生成的
                "expires": "",#Cookie有效终止日期
                'path': '/',#Web服务器上哪些路径下的页面可获取服务器设置的Cookie
                'httpOnly': False,#防脚本攻击
                'HostOnly': False,#
                'Secure': False,#在Cookie中标记该变量，表明只有当浏览器和Web Server之间的通信协议为加密认证协议时
            })
    def download_page(self,main_url,retry_count=4):
        html=''
        retry=0
        while(retry<retry_count):
            try:
                print('>>>>>>>>>>>>>>>>>>>>>>>request:'+main_url+'>>>>>>>>>>>>>>>>>>>>>>>')
                if retry==0:
                    response=requests.get(main_url,headers=self.headers)
                    if 200==response.status_code:
                        return EncodingUtils.getStrNotKnowEcoding(response.content)
                response=requests.get(main_url,headers=self.headers,proxies=self.proxies)
                print(response.status_code)
                if 200==response.status_code:
                    return response.text
                else:
                    self.change_ip()
                    retry=retry+1
            except Exception as e:
                traceback.print_exc()
                self.change_ip()
                retry=retry+1
        return html
    def get_detail_links(self,main_url):
        html=self.download_page(main_url)
        bf4=BeautifulSoup(html,'lxml')
        main_links=set()
        try:
            a_eles=bf4.select('div.txt > div.tit > a')
            for a_ele in a_eles:
                h4_eles=a_ele.select('h4')
                if len(h4_eles)>0:
                    print(h4_eles[0].string)#店铺名称
                    print(a_ele['href'])#店铺链接
                    main_links.add(a_ele['href'])
        except Exception as e:
            traceback.print_exc()
        print('>>>>>>>>>>>>店铺链接数'+str(len(main_links))+'>>>>>>>>>>>>>>>')
        return main_links;
    def get_details_selenium(self,detail_urls):
        for detail_url in details_links:
            print('请求：'+detail_url)
            error_flag=0
            try:
                self.tomjs.get(detail_url)
            except Exception as e:
                # traceback.print_exc()
                error_flag=1
            # 执行js得到整个dom
            # html = self.tomjs.execute_script("return document.documentElement.outerHTML")
            if(error_flag==0):
                html=self.tomjs.page_source
                # print(html)
                ptn=re.compile('<body>(.*?)</body>',re.S)
                res=re.findall(ptn,html)
                bf4=BeautifulSoup(self.tomjs.page_source,'lxml')
                shop_name = bf4.find('h1',class_='shop-name')
            while(error_flag==1 or (len(res)>0 and res[0]=='') or shop_name==None):
                print('>>>>>>>>>>>>>>>>>Request: %s>>>>>>>>>>>>>>>>>>>>>>'%detail_url)
                self.change_selenium_ip_and_cookies(True)
                try:
                    self.tomjs.get(detail_url)
                    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>cookies:'+str(self.tomjs.get_cookies()))
                    error_flag=0
                except Exception as e:
                    traceback.print_exc()
                    error_flag=1
                self.tomjs.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                html=self.tomjs.page_source
                #body is or not null
                res=re.findall(ptn,html)
                #店铺名称
                bf4=BeautifulSoup(self.tomjs.page_source,'lxml')
                shop_name = bf4.find('h1',class_='shop-name')
            #店铺名称
            try:
                # shop_name=bf4.select('div#basic-info h1')[0].string
                shop_name = bf4.find('h1',class_='shop-name')
                ptn=re.compile('<h1 class="shop-name">(.*?)<a ',re.S)
                shop_name=re.findall(ptn,str(shop_name))[0]
                print('店铺名称:'+shop_name)
            except Exception as e:
                traceback.print_exc()
                shop_name=''
            #星级
            try:
                star=bf4.select('div.brief-info > span')[0].attrs['title']
            except Exception as e:
                traceback.print_exc()
                star=''
            print('星级:'+star)
            #评论条数
            try:
                review_str=bf4.select('span#reviewCount')[0].string
                ptn1=re.compile('(.*?)条评论',re.S)
                review_count=re.findall(ptn1,review_str)[0]
                print('评论条数:'+str(review_count))
            except Exception as e:
                review_count=''
            #人均：-
            try:
                avg_str=bf4.select('span#avgPriceTitle')[0].string
                print('人均：'+str(avg_str.split("：")[1]))
            except Exception as e:
                traceback.print_exc()
                avg_count=''
            #口味：7.6
            try:
                com_str2=bf4.select('span#comment_score span')[0].string
                print('口味：'+str(com_str2.split("：")[1]))
            except Exception as e:
                traceback.print_exc()
                env_score=''

            #环境：7.7
            try:
                com_str2=bf4.select('span#comment_score span')[1].string
                print('环境：'+str(com_str2.split("：")[1]))
            except Exception as e:
                traceback.print_exc()
                env_score=''
            #服务：7.6
            try:
                com_str3=bf4.select('span#comment_score span')[2].string
                print('服务：'+str(com_str3.split("：")[1]))
            except Exception as e:
                traceback.print_exc()
                service_score=''
            #地址：
            try:
                address=bf4.find('span',attrs={"itemprop":"street-address"}).string
                print('地址：'+address)
            except Exception as e:
                traceback.print_exc()
                address=''
            #电话：
            try:
                tel=bf4.find('span',attrs={"itemprop":"tel"}).string
                print('电话：'+tel)
            except Exception as e:
                traceback.print_exc()
                tel=''

            # 优惠促销
            # try:
            #     title=bf4.find('div',attrs={"class":"item big big-double "}).select('p')[0].string
            #     print('优惠促销：'+title)
            # except Exception as e:
            #     traceback.print_exc()
            #     title=''

            #推荐菜
            try:
                print('------------推荐菜：--------------')
                a_eles = WebDriverWait(self.tomjs, 10,0.5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.mod > div > p > a"))
                )
                for a_ele in a_eles:
                    texts=a_ele.text
                    if len(re.findall('[\s]\(',texts))>0:
                        print('推荐菜：'+str(texts))
            except Exception as e:
                # traceback.print_exc()
                pass
            try:
                items = WebDriverWait(self.tomjs, 10,0.5).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#shop-tabs > div > ul > li"))
                )
                print(len(items))
                for item in items:
                    name=item.find_element_by_css_selector('p.name').text
                    try:
                        price=item.find_element_by_css_selector('span.price').text
                    except Exception as e:
                        price=''
                    if price=='':
                        print(name)
                    else:
                        print(name+': '+price)
            except Exception as e:
                # traceback.print_exc()
                pass
            # =======================================点评==========================================
            #网友点评数量
            try:
                review=bf4.select('span.sub-title')[0].string
                ptn=re.compile('\((.*?)\)',re.S)
                review_count=re.findall(ptn,review)[0]
                print('网友点评数量:'+review_count)
            except Exception as e:
                traceback.print_exc()

            try:
                items=bf4.select('ul#reviewlist-wrapper > li')
            except Exception as e:
                traceback.print_exc()
                print(str(len(items)))
            for item in items:
                print('')
                try:
                    a_ele=item.select('p.user-info a')
                    if len(a_ele)>0:    #大众点评用户
                        #评论用户昵称
                        nice_name=a_ele[0].string
                        #评论用户链接
                        user_link='http://www.dianping.com'+a_ele[0].get('href')
                        print("评论用户昵称:"+nice_name)
                        print("评论用户链接:"+user_link)
                    else:#美团用户
                         span_ele=item.select('p.user-info > span.name')
                         #评论用户昵称
                         nice_name=span_ele[0].string
                         print("评论用户昵称:"+nice_name)
                except Exception as e:
                    traceback.print_exc()

                #评论内容
                try:
                    desc_eles=item.select('div.content > p.desc')
                    if len(desc_eles)<=0:
                        desc_eles=item.select('div.content > div > p.desc')
                    descs=desc_eles[0].strings
                    desc=''
                    for des in descs:
                        desc=desc+des.replace('\xa0',' ')
                    print('评论内容：'+desc)
                except Exception as e:
                    traceback.print_exc()
                #评论时间
                try:
                    times=item.select('div.content > div.misc-info > span.time')[0].string
                    print('评论时间：'+times)
                except Exception as e:
                    traceback.print_exc()

            #更多点评 链接
            try:
                review_link='http:'+bf4.select('p.comment-all a')[0].get('href')
                print('更多点评 链接:'+review_link)
            except Exception as e:
                review_link=''
            time.sleep(0.5)

if __name__=="__main__":
    spider=Spider()
    details_links=set()
    for i in range(1,8):
        #每一页15个店铺
        start_url='http://www.dianping.com/shengzhou/ch10/g110p'+str(i)
        links=spider.get_detail_links(start_url)
        for link in links:
            details_links.add(link)
        time.sleep(1)
        # break;
    print('>>>>>>>>>>>>店铺链接总数：'+str(len(details_links))+'>>>>>>>>>>>>>>>')
    threads_size=2
    links_size=len(details_links)
    per_thread_links_size=links_size/threads_size
    threads=[]
    for i in range(0,threads_size):
        start=int(i*per_thread_links_size)
        if i==threads_size-1:
            end=int(links_size)
        else:
            end=int(start+per_thread_links_size)
        per_thread_links=list(details_links)[start:end]
        t=Thread(target=spider.get_details_selenium,args=(per_thread_links,))
        threads.append(t)
        # spider.get_details_selenium(details_link)
        # break;
    for t in threads:
        t.start()




