#ecoding=utf-8

import  requests
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import Chrome,PhantomJS
import time,json,random
from settings import AGENTS


class ZhiHuSelenum():
    def __init__(self):
        self.base_url="https://www.zhihu.com"
        self.login_url='https://www.zhihu.com/#signin';
        self.tomJsDriver=r'J:\lib\driver\phantomjs.exe';
        self.chromeDriver = r'J:\lib\driver\chromedriver.exe'
        self.session = Session()
        self.session.headers.clear()

    #工具方法
    #tomjs初始化
    def tomjs_init(self):
        # 引入配置对象DesiredCapabilities
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        agent=random.choice(AGENTS);
        dcap["phantomjs.page.settings.userAgent"] =agent
        dcap["phantomjs.page.customHeaders.User-Agent"] = agent
        # 不载入图片，爬页面速度会快很多
        dcap["phantomjs.page.settings.loadImages"] = False
        # #打开带配置信息的phantomJS浏览器
        tomJs = PhantomJS(self.tomJsDriver, desired_capabilities=dcap)
        # 隐式等待5秒，可以自己调节
        tomJs.implicitly_wait(5)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        tomJs.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        tomJs.set_script_timeout(10)
        return tomJs
    def addCookies(self, driver,cookies_list):
        for cookie in cookies_list:
            driver.add_cookie({
                'domain': '.zhihu.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })
    def startRun(self):
        tomJs=self.tomjs_init();
        #从文件读取cookie
        cookieStr=''
        try:
            with open('cookies.json', 'r') as file:
                cookieStr =file.read();
        except Exception as e:
            pass;
        print('从文件中获取cookies-----------'+cookieStr);
        if cookieStr!=''and cookieStr!=None:
            tomJs.delete_all_cookies()
            cookies_list=json.loads(cookieStr)
            if len(cookies_list)>0:
                self.addCookies(tomJs, cookies_list)
        #登陆主页
        tomJs.get(self.base_url)
        try:
            div=tomJs.find_element_by_name('password')
        except Exception as e:
            div=''
        #文件cookie登录失败，模拟登录------------------=---------------------------start----------
        if div!='':
            print('--------文件cookie登录失败，模拟登录--------')
            chrome = Chrome(executable_path=self.chromeDriver)
            chrome.get(self.login_url)
            try:
                div = chrome.find_element_by_name('password')
            except Exception as e:
                div = ''
            # 不停的检测，没有password就说明浏览器已经进行了跳转
            while(div!=''):
                try:
                    div = chrome.find_element_by_name('password')
                except Exception as e:
                    div = ''
                time.sleep(1)
            #获取cookie，上面一跳出循环我认为就登录成功了，当然上面的判断不太严格，可以再进行修改
            cookies = chrome.get_cookies()
            print('--------------登陆成功，获取cookies--------------'+json.dumps(cookies))
            if len(cookies)>0:
                cookies_list = json.dumps(cookies)
                # 登录完成后，将cookie保存到本地文件
                with open('cookies.json', 'w') as f:
                    f.write(cookies_list)
                    self.addCookies(tomJs, cookies)
                print('-----------------模拟登录finish-----------------')
        # 登陆主页
        tomJs.get(self.base_url)
        print(tomJs.page_source)



if __name__=='__main__':
    zhihu=ZhiHuSelenum()
    zhihu.startRun()
