import requests
import time
import base64
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LuYouReBoot():
    def __init__(self):
        self.base_url = 'http://192.168.1.1/'
        self.login_url = 'http://192.168.1.1/login.cgi?stat'
        self.user = 'user'
        self.pwd = 'cbahf'
        self.headers = {
            'Host': '192.168.1.1',
            'Connection': 'keep-alive',
            'Content-Length': '20',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://192.168.1.1',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://192.168.1.1/',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'lang=chs; sid=JRynwfqRjAqTLlKd; lsid=QjzmVVFAymqTXZxf'
        }
        session = Session()
        session.headers.clear()
        chromePath = r'C:\Users\Administrator\AppData\Local\Google\Chrome\Application\chromedriver.exe'
        self.chrome = Chrome(executable_path=chromePath)
    def login(self):
        self.chrome.delete_all_cookies()
        self.chrome.get(self.base_url)
        locator = (By.ID, 'username')
        WebDriverWait(self.chrome, 10, .5).until(EC.presence_of_element_located(locator))
        element1=self.chrome.find_element_by_xpath('.//*[@id="username"]')
        element1.clear()
        element1.send_keys(self.user);
        element2=self.chrome.find_element_by_xpath('.//*[@id="password"]')
        element2.clear()
        element2.send_keys(self.pwd);
        self.chrome.find_element_by_xpath("/html/body/form/div[1]/div[2]/table[2]/tbody/tr[4]/td[2]/input[1]").click()
        #登录成功后，将cookie存入文件
        # cookies=self.chrome.get_cookies();
        # cookie_json = {}
        # for cookie in cookies:
        #     cookie_json[cookie['name']]=cookie['value']
        # with open("D:/cookie_json.txt",'w',encoding='utf-8') as file:
        #     file.write(json.dumps(cookie_json))

    def reboot(self):
        cookieStr = '';
        # with open("D:/cookie_json.txt", 'r', encoding='utf-8') as file:
        #     cookieStr = file.readline()
        # cookies = json.loads(cookieStr);
        # self.chrome.get(self.base_url)
        # self.chrome.delete_all_cookies();
        # for key in cookies:
        #     self.chrome.add_cookie({'name':key,'value':cookies[key]});
        # self.chrome.get(self.base_url)
        self.login();
        try:
            eleme=self.chrome.find_element_by_xpath(".//a[text()='管理']")
            eleme.click();
            self.chrome.switch_to_frame("mainFrame")
            eleme2 = self.chrome.find_element_by_xpath(".//input[@value='重启']")
            eleme2.click();
        except Exception as e:
            print('需要登录')
            LuYouReBoot.logout();


        # chrome.add_cookie({
        #     'name': cookie['name'],
        #     'value': cookie['value']
        # })
    # response=requests.post(url=login_url, data={'name':user,'pswd':pwd});
    # print(response)
    @staticmethod
    def get_ip():
        url = "http://2018.ip138.com/ic.asp"
        r = requests.get(url)
        txt = r.text
        ip = txt[txt.find("[") + 1: txt.find("]")]
        return ip
    @staticmethod
    def logout():
        url = "http://192.168.1.1/login.cgi?out"
        requests.get(url)


if __name__ == "__main__":
    old_ip=LuYouReBoot.get_ip();
    print("old_ip:"+old_ip)
    LYR=LuYouReBoot();
    LYR.reboot();
    time.sleep(30)
    new_ip = LuYouReBoot.get_ip();
    print("new_ip:" + new_ip)
    retry=0
    while(retry<3 and old_ip==new_ip):
        LYR.reboot();
        retry=retry+1
        time.sleep(30)
    LYR.chrome.close();


