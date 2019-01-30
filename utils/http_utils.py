#! /usr/bin/python3
import random

import requests
from requests import Session
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Chrome,PhantomJS
from settings import AGENTS


class HttpUtils:
    def __init__(self):
        self.reponse=None
        self.tomJsDriver=r'E:\pycharm_space\Demo1.2\driver\phantomjs.exe';
        self.chromeDriver = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe'
    def get(self,url,headers):
            try:
                self.reponse = requests.get(
                    url,
                    timeout=10.0,
                    headers=headers,
                    verify=False
                )
                return self.reponse
            except Exception as e:
                print(e)
    # recursively try proxy sockets until successful GET with headers
    def get_with_proxy(self,url,headers,ip):
            proxies = {
                "http": "http://" + ip,
                "https": "https://" + ip
            }
            try:
                self.reponse = requests.get(
                    url,
                    timeout=3.0,
                    proxies=proxies,
                    headers=headers
                )
                return self.reponse
            except Exception as e:
                print(e)
    def get_with_auth(self,url,headers,user_name,password):
            try:
                self.reponse = requests.get(
                    url,
                    timeout=3.0,
                    auth=(user_name, password),
                    headers=headers
                )
                return self.reponse
            except Exception as e:
                print(e)
    # recursively try proxy sockets until successful POST with headers
    def post(self,url,data,headers):
            try:
                self.reponse = requests.post(
                    url,
                    json=data,
                    timeout=3.0,
                    headers=headers,
                )
                return self.reponse
            except Exception as e:
                print(e)
    def post_with_proxy(self,url,data,headers,ip):
            proxies = {
                "http": "http://" + ip,
                "https": "https://" + ip
            }
            try:
                self.reponse = requests.post(
                    url,
                    json=data,
                    timeout=3.0,
                    headers=headers,
                    proxies=proxies
                )
                return self.reponse
            except Exception as e:
                print(e)
    def post_with_auth(self,url,data,headers,user_name,password):
            try:
                self.reponse = requests.post(
                    url,
                    json=data,
                    timeout=3.0,
                    headers=headers,
                    auth=(user_name, password)
                )
                return self.reponse
            except Exception as e:
                print(e)

    # tomjs初始化
    def tomjs_init(self):
         # 引入配置对象DesiredCapabilities
         dcap = dict(DesiredCapabilities.PHANTOMJS)
         # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
         agent = random.choice(AGENTS);
         dcap["phantomjs.page.settings.userAgent"] = agent
         dcap["phantomjs.page.customHeaders.User-Agent"] = agent
         # 不载入图片，爬页面速度会快很多
         dcap["phantomjs.page.settings.loadImages"] = False
         # #打开带配置信息的phantomJS浏览器
         tomJs = PhantomJS(self.tomJsDriver, desired_capabilities=dcap,
                           service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
         # 隐式等待5秒，可以自己调节
         tomJs.implicitly_wait(10)
         # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
         # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
         tomJs.set_page_load_timeout(10)
         # 设置10秒脚本超时时间
         tomJs.set_script_timeout(10)
         return tomJs
    def chrome_init(self):
        session = Session()
        session.headers.clear()
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        option.add_argument('disable-infobars')
        option.add_argument('Connection="keep-alive"')
        option.add_argument('accept="application/json, text/plain, */*"')
        option.add_argument(
            'User-Agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"')
        #设置selenium自动加载flash
        prefs = {
            "profile.managed_default_content_settings.images": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        }
        option.add_experimental_option('prefs', prefs)
        chrome = Chrome(executable_path=self.chromeDriver, chrome_options=option)
        # 隐式等待5秒，可以自己调节
        chrome.implicitly_wait(130)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        chrome.set_page_load_timeout(130)
        # 设置10秒脚本超时时间
        chrome.set_script_timeout(130)
        return chrome;
    # recursively try until successful POST with file and custom headers
    # {'file': open('test.txt', 'rb')}
    def post_file_with_proxy(self,url,file_dict,headers,ip):
            proxies = {
                "http": "http://" + ip,
                "https": "https://" + ip
            }
            try:
                self.reponse = requests.post(
                    url,
                    files=file_dict,
                    timeout=3.0,
                    headers=headers,
                    proxies=proxies
                )
                return self.reponse
            except Exception as e:
                print(e)

    def get_response_headers(self):
        return self.reponse.headers

    def get_status_code(self):
        return self.reponse.status_code

    def response_to_file(self):
        from datetime import datetime
        file_name = 'proxy_requests_'
        file_name += datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        with open(file_name, 'wb') as file_out:
            file_out.write(self.reponse.content)

    def get_content(self):
        return self.reponse.content


if __name__== '__main__':
    #driver=HttpUtils().chrome_init()
    #driver.get('http://www.baidu.com')
    for i in range(127, 138):
        url = "https://gaokao.chsi.com.cn/sch/search--ss-on,searchType-1,option-qg,start-" + str(i * 20) + ".dhtml"
        header={
            'Upgrade - Insecure - Requests': '1',
            'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;Win64;x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 71.0.3578.98Safari / 537.36',
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
            'Accept - Encoding': 'gzip, deflate, br',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            'Cookie': '_ga = GA1.3.338016866.1539613769;acw_tc = 2760826515477285768641109e8d3415dbedb377d188e8d329e941b920898e;JSESSIONID = 06FF58C8F7CE6E7FD760802A0682630D',
        }
        html=HttpUtils().get(url,header).text
        print(html)