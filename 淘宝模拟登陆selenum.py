#!  /usr/bin/env python
#ecoding=utf-8
from requests import Session
from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium import webdriver
from random import randint

session = Session()
session.headers.clear()
# chromePath = r'J:\lib\driver\chromedriver.exe'
chromeDriver = r'zhihu4/zhihu/driver/chromedriver.exe'
session = Session()
session.headers.clear()
option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('disable-infobars')
option.add_argument('Host="www.zhihu.com"')
option.add_argument('Referer="https://www.zhihu.com/people"')
option.add_argument('Connection="keep-alive"')
option.add_argument('X-API-VERSION="3.0.40"')
option.add_argument('X-UDID="ALDrFjeREg2PTthA-cVwHI6iT6deB87yN68="')
option.add_argument('accept="application/json, text/plain, */*"')
option.add_argument(
    'Cookie="q_c1=62643b38b6ef4d9fa32698ee1cbdbe24|1515657103000|1515657103000; _zap=d0932210-e19f-415b-9827-4e6737484716; l_cap_id="MWU1YzNkYmViNzlhNDc4ZGE0MTViODM0ZTVmNzg2ODE=|1515937552|dbe6ae7a4c5fe1fd6ba79711d42ba4aaf46987da"; r_cap_id="NjRkYTI0NjlmY2RmNDkzY2FiM2UyZjg2YmM0YjliNGQ=|1515937552|5a5dd08fbedfe0820e16e6f6cefec65702dfd403"; cap_id="ZmNjZTk4MzZiMDAwNDA3MDkyNzU1MmYxZWYzNWY3MTk=|1515937552|7b9eb122b440d4fa19d18d2a9eba4e06f23ea1b3"; aliyungf_tc=AQAAABdmGgxxiwMAxLnidPuEfUG4qxe1; d_c0="ALDrFjeREg2PTthA-cVwHI6iT6deB87yN68=|1517364326"; anc_cap_id=e9deafb94edd42a0849fbf6b53bf5a5d; capsion_ticket="2|1:0|10:1517364450|14:capsion_ticket|44:ZDlhMjIwY2IyYTFiNDc0MWE2ZmNjNGI0NDU2NDUwOGE=|f7a809f2756e9281adb4a6b34da6b08f80a70513cc4a9b0fe81cc23930d89805"; z_c0="2|1:0|10:1517364658|4:z_c0|92:Mi4xc3d5V0J3QUFBQUFBc09zV041RVNEU1lBQUFCZ0FsVk5zbk5lV3dBUC1XV3ZicGRyUE5HRE02R1hCZEkxZU96NkNB|5e7a9d1b4745a92a2afff3206d593fb922760d333cc9baab4c90998a4d5be082"; __utma=155987696.1641113454.1517364861.1517364861.1517364861.1; __utmb=155987696.0.10.1517364861; __utmc=155987696; __utmz=155987696.1517364861.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _xsrf=852354d4-a878-4dac-b0fd-ac3f74edfa5b"')
option.add_argument(
    'authorization="Bearer 2|1:0|10:1517364658|4:z_c0|92:Mi4xc3d5V0J3QUFBQUFBc09zV041RVNEU1lBQUFCZ0FsVk5zbk5lV3dBUC1XV3ZicGRyUE5HRE02R1hCZEkxZU96NkNB|5e7a9d1b4745a92a2afff3206d593fb922760d333cc9baab4c90998a4d5be082"')
option.add_argument(
    'User-Agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"')
chrome =Chrome(executable_path=chromeDriver,chrome_options=option,)
loginUrl = 'https://login.taobao.com/member/login.jhtml'
chrome.get(loginUrl)
# 在最长 10s 内，每个 0.5 秒去检查 locator 是否存在，
# 如果存在则进入下一步
locator=(By.ID,'J_Quick2Static')
WebDriverWait(chrome, 10,
0.5).until(EC.visibility_of_element_located(locator))
chrome.find_element_by_xpath('//*[@class="iconfont static"]').click()
sleep(3)
chrome.find_element_by_xpath('//*[@id="TPL_username_1"]').send_keys('dcc6682017')
sleep(1)
chrome.find_element_by_xpath('//*[@class="static-form "]').click()#模拟点击，随便点
sleep(1)
chrome.find_element_by_xpath('//*[@id="TPL_password_1"]').send_keys('dcc19920120')

action = ActionChains(chrome);
#获取滑动滑块的标签元素
source=chrome.find_element_by_id("nc_1_n1z")
huakuai=chrome.find_element_by_id("nocaptcha")
display=huakuai.value_of_css_property("display")
print('==========display:'+display)
if display!='none':
    print(huakuai.size)
    #确保每次拖动的像素不同，故而使用随机数
    action.click_and_hold(source).move_by_offset(randint(1,50), 0.5).perform()
    sleep(0.7)
    action.click_and_hold(source).move_by_offset(randint(50,150), 0.3).perform()
    sleep(0.8)
    action.click_and_hold(source).move_by_offset(randint(150,200), 0.1).perform()
    sleep(0.9)
    action.click_and_hold(source).move_by_offset(randint(200,270), 0.3).perform()
    sleep(0.4)
    action.click_and_hold(source).move_by_offset(randint(270,290), 1).perform()
    sleep(1)
    action.click_and_hold(source).move_by_offset(randint(290,300), 2).perform()
    sleep(1.7)
    action.click_and_hold(source).move_by_offset(300, 1).perform()
    sleep(1.7)
    # try:
    #     refresh = chrome.find_element_by_xpath('//*[@id="nocaptcha"]/div/span/a')
    # except Exception:
    #     print("There is no refresh text..3...")
    # else:
    #     print('refresh click....3...')
    # refresh.click()
    # action.click_and_hold(source).move_by_offset(260, 0).perform()
    action.release()
    #拖动完释放鼠标
    #组织完这些一系列的步骤，然后开始真实执行操作
    # action.move_to_element(source).perform()

chrome.find_element_by_xpath('//*[@id="J_SubmitStatic"]').submit()
sleep(5)#等待买过的商品验证
sleep(5)#等待Cookies加载
cookies = chrome.get_cookies()
for cookie in cookies:
    session.cookies.set(cookie['name'],cookie['value'])
