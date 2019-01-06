#!  /usr/bin/env python
#ecoding=utf-8
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import Chrome

from settings import AGENTS
import random

tomJsDriver=r'J:\lib\driver\phantomjs.exe';
base_url='https://wx2.qq.com/?&lang=zh_CN';
cookieStr="webwxuvid=bd2a6d577d3e5a497c2ec36c562a3b111d81e1e0311d65fdad5d14ee8d4f2a49950af8eaa5aa8d7e85ded3f943c724b0; webwx_auth_ticket=CIsBEMbl7hIagAEi+BM6jGIGp/yTjZOwTvt2/gnw4SlAIsWTTWwddO0alA0dGKF7dWGBBpPzSxbx1HJSH6/Kl0rUuTlFBBCDuiXW1GoVnf20ZyuNxS3ASvLtsmoKxCwiQu8UZO9DZTbhX5drgz0NKPDetNImLv0oifb3xBy50RAT578qZ5KnrP4wMA==; login_frequency=1; last_wxuin=1874818113; wxloadtime=1512975906_expired; wxpluginkey=1512954002; wxuin=1874818113; wxsid=CBktnMZBq1zxZXHc; webwx_data_ticket=gSc62p27ViXvMe+wyJ9au+fB; mm_lang=zh_CN; MM_WX_NOTIFY_STATE=1; MM_WX_SOUND_STATE=1"
session = Session()
session.headers.clear()
chromePath = r'J:\lib\driver\chromedriver.exe'
chrome = Chrome(executable_path= chromePath)
for line in cookieStr.split(';'):
    cookie={}
    #其设置为1就会把字符串拆分成2份
    name,value=line.strip().split('=',1)
    cookie['name'] = name
    cookie['value'] = value
    chrome.add_cookie({
        'domain': '.zhihu.com',  # 此处xxx.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })
chrome.get(base_url)

#
#
# # 引入配置对象DesiredCapabilities
# dcap = dict(DesiredCapabilities.PHANTOMJS)
# #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
# # dcap["phantomjs.page.settings.userAgent"] = (random.choice(AGENTS))
# # 不载入图片，爬页面速度会快很多
# dcap["phantomjs.page.settings.loadImages"] = False
# #打开带配置信息的phantomJS浏览器
# driver = webdriver.PhantomJS(tomJsDriver, desired_capabilities=dcap)
# print(cookies);
# driver.add_cookie(cookie_dict=cookies)
# # 隐式等待5秒，可以自己调节
# driver.implicitly_wait(5)
# # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
# # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
# driver.set_page_load_timeout(10)
# # 设置10秒脚本超时时间
# driver.set_script_timeout(10)
# print(driver.find_element_by_id("content").text)



