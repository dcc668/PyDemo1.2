#!  /usr/bin/env python
#ecoding=utf-8
from requests import Session
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from random import randint

session = Session()
session.headers.clear()
chromePath = r'driver\chromedriver.exe'
chrome = Chrome(executable_path= chromePath)
loginUrl = 'https://login.taobao.com/member/login.jhtml'
chrome.get(loginUrl)
# 在最长 10s 内，每个 0.5 秒去检查 locator 是否存在，
# 如果存在则进入下一步
locator=(By.ID,'J_Quick2Static')
WebDriverWait(chrome, 10,
0.5).until(EC.visibility_of_element_located(locator))
chrome.find_element_by_xpath('//*[@class="iconfont static"]').click()
chrome.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys('dcc6682017')
chrome.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys('dcc19920120')
# 不停的检测，一旦当前页面URL不是登录页面URL，就说明浏览器已经进行了跳转
current_url=chrome.current_url
while(current_url=='https://login.taobao.com/member/login.jhtml'):
    current_url = chrome.current_url
    sleep(1)
    print('------------------------->>>>>>>>current_url:'+current_url)
#获取cookie，上面一跳出循环我认为就登录成功了，当然上面的判断不太严格，可以再进行修改
cookies = chrome.get_cookies()
cookieStr = "";
for cookie in cookies:
    cookieStr += cookie['name'] + "=" + cookie['value'] + "; "
with open('cookies.txt','w') as file:
    file.write(cookieStr)
chrome.quit()

import  requests
from lxml import html

url="https://www.taobao.com/"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.3',
    'Cookie':cookieStr}
bhtml=requests.get(url,headers=headers).content
result=html.fromstring(bhtml)
