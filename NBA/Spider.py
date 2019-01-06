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
import random,re,json
from utils.ecoding_utils import EncodingUtils
from threading import  Thread
from user_agent import generate_user_agent
class Spider():
    def __init__(self):
        self.tomJsDriver=r'driver\phantomjs.exe';
        self.chromeDriver=r'driver\chromedriver.exe'
        self.cookieStr=[
            "_ga=GA1.2.84436129.1521881685; _gid=GA1.2.1440645970.1521881685; _fssid=8a4e90bc-343d-46e6-9728-9d955405cc8b; _fsloc=?i=CN&c=U2hhbmdoYWk=; _fsuid=104e95e8-cfbe-4366-acfd-30aa0a1dfccc; sr_note_box_countdown=71; auth_checked=true; srcssfull=yes; is_live=true; __qca=P0-54633894-1521881694127; __gads=ID=1124b4286712ad10:T=1521881691:S=ALNI_Ma_Bq2xuvw0kRfwb6sQul9AyLlACw; SR_user=",
        ]
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': random.choice(self.cookieStr),
            'Host': 'www.basketball-reference.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        }

        self.ips=[]
        with open('ips/ips.txt','r',encoding='utf-8') as file:
            lines=file.readlines()
            for line in lines:
                self.ips.append(line.strip())
        print('>>>>>>>>>>>>>>>>>>>>>>>>>ips>>>>>>>>>>>>>>>>>>>>>>>>>'+str(self.ips))
        self.web=random.choice(self.ips)
        self.proxies = {
            'http':self.web,
        }
        self.change_ip_and_cookies_tomjs()

    def change_ip(self):
        ip=random.choice(self.ips)
        self.proxies = {
            'http':ip,
        }
        print('>>>>>>>>>>>>>>>proxy ip changed!!!  '+ip+'>>>>>>>>>>>>>')
    def change_ip_and_cookies_tomjs(self,retry=False):
        if retry:
            self.tomjs.close()
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap = DesiredCapabilities.PHANTOMJS.copy()
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        agent = generate_user_agent(os=('mac', 'linux', 'win'))
        dcap["phantomjs.page.settings.userAgent"] = agent
        for key, value in self.headers.items():
            dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
        # 不载入图片，爬页面速度会快很多
        dcap["phantomjs.page.settings.loadImages"] = False
        #是否启用js
        dcap["phantomjs.page.settings.javascriptEnabled"] = True
        dcap["phantomjs.page.settings.browserName"] = 'Chrome'
        # 利用DesiredCapabilities(代理设置)参数值，重新打开一个sessionId，我看意思就相当于浏览器清空缓存后，加上代理重新访问一次url
        # proxy = webdriver.Proxy()
        # proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = random.choice(self.ips)
        # proxy.add_to_capabilities(dcap)
        # #打开带配置信息的phantomJS浏览器
        # self.tomjs = PhantomJS(self.tomJsDriver, desired_capabilities=dcap)
        self.tomjs = PhantomJS(self.tomJsDriver)
        # 隐式等待5秒，可以自己调节
        self.tomjs.implicitly_wait(6)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self.tomjs.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        self.tomjs.set_script_timeout(10)
        self.change_cookies()
    def change_ip_and_cookies_chrome(self,retry=False):
        if retry:
            self.tomjs.close()
        session = Session()
        session.headers.clear()
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('disable-infobars')
        # option.add_argument('--proxy-server='+self.web)
        for key, value in self.headers.items():
            if 'Cookie'!=key:
                option.add_argument(
                    key+'="'+value+'"')
        self.tomjs =Chrome(executable_path=self.chromeDriver,chrome_options=option)
        self.change_cookies()
    def change_cookies(self):
        cookies=random.choice(self.cookieStr)
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>change cookies>>>>>>>>>>>>>>>>>>>>>>>>>>'+str(cookies))
        for line in cookies.split(';'):
            #其设置为1就会把字符串拆分成2份
            name,value=line.strip().split('=',1)
            self.tomjs.add_cookie({
                'domain': '.basketball-reference.com',  # 服务器域名 此处xxx.com前，需要带点
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
    def get_schedule_selenium(self,links):
        for detail_url in links:
            print('请求：'+detail_url)
            error_flag=0
            html=''
            try:
                html=self.tomjs.get(detail_url)
            except Exception as e:
                error_flag=1
            if(error_flag==0):
                ptn=re.compile('<body>(.*?)</body>',re.S)
                html=self.tomjs.page_source;
                res=re.findall(ptn,)
            while(error_flag==1 or (len(res)>0 and res[0]=='')):
                print('>>>>>>>>>>>>>>出错了：return>>>>>>>>'+html)
                print('>>>>>>>>>>>>>>>>>Request: %s>>>>>>>>>>>>>>>>>>>>>'%detail_url)
                self.change_ip_and_cookies_tomjs(True)
                try:
                    self.tomjs.get(detail_url)
                    html=self.tomjs.page_source;
                    res=re.findall(ptn,html)
                    if (len(res)>0 and res[0]==''):
                        error_flag=1
                    else:
                        error_flag=0
                except Exception as e:
                    traceback.print_exc()
                    error_flag=1
            lines=WebDriverWait(self.tomjs,10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="schedule"]/tbody/tr')))
            for line in lines:
                item={}
                dateObj=line.find_element_by_xpath('./th/a')#没有/tbody
                date=dateObj.text
                # //客场球队
                visitorObj=line.find_element_by_xpath('./td[2]/a')
                visitor = visitorObj.text
                # //主场球队
                homeObj = line.find_element_by_xpath('./td[4]/a')
                home = homeObj.text

                item['date']=date if date else ""
                item['visitor']=visitor if visitor else ""
                item['home']=home if home else ""
                json_str = json.dumps(item, default=lambda o: o.__dict__, sort_keys=True)
                print((detail_url,json_str))
                if not date or not visitor or not home:
                    print("有空字段！！该条数据不完整！",date,visitor,home)

if __name__=="__main__":
    preUrl='https://www.basketball-reference.com/leagues/NBA_2018_games-'
    months=['october','november','december','january','february','march','april']
    links=[]
    for month in months:
        link=preUrl+month+'.html'
        links.append(link)
    threads_size=3
    links_size=len(links)
    per_thread_links_size=int(links_size/threads_size)
    threads=[]
    for i in range(0,threads_size):
        spider=Spider()
        start=int(i*per_thread_links_size)
        if i==threads_size-1:
            end=int(links_size)
        else:
            end=int(start+per_thread_links_size)
        per_thread_links=list(links)[start:end]
        t=Thread(target=spider.get_schedule_selenium,args=(per_thread_links,))
        threads.append(t)

    for t in threads:
        t.start()
        time.sleep(1)




