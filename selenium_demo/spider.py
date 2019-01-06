#!  /usr/bin/env python
#ecoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import PhantomJS,Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import re,time
from user_agent import generate_user_agent

class Spider():
    def __init__(self):
        self.tomJsDriver=r'driver\phantomjs.exe';
        self.chromeDriver=r'driver\chromedriver.exe'
        self.headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        }

        # self.tomjs_init()
        self.chrome_init()

    def tomjs_init(self,retry=False):
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
        self.tomjs.implicitly_wait(10)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        self.tomjs.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        self.tomjs.set_script_timeout(15)
    def chrome_init(self,retry=False):
        self.tomjs =Chrome(executable_path=self.chromeDriver)
    def close(self):
        self.tomjs.close()
    def download(self,template_url):
        detail_url=template_url['url']
        print('请求：'+detail_url)
        try:
            self.tomjs.get(detail_url)
            return self.tomjs.page_source
        except Exception as e:
            print('>>>>>>>>>>>>>>>>>Request: %s>>>>>>>>>>>>>>>>>>>>>'%detail_url)
            traceback.print_exc()
            template_url['html_request_status']=6
            raise Exception('>>>>>>>>>error occured in spider download>>>>>>>>>>>>')

spider=Spider()
spider.tomjs.get("https://www.zhihu.com/topic/19559450/hot")
for i in range(10):
    spider.tomjs.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(1)
