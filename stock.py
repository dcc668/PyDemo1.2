import requests
import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import Chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LuYouReBoot():
    def __init__(self):
        pass;
    def login(self):
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
            eleme2 = self.chrome.find_element_by_xpath(".//input[@id='Restart_button']")
            eleme2.click();
        except Exception as e:
            print('需要登录')


        # chrome.add_cookie({
        #     'name': cookie['name'],
        #     'value': cookie['value']
        # })
    # response=requests.post(url=login_url, data={'name':user,'pswd':pwd});
    # print(response)
    def getPage(self,url,headers):
        res=requests.get(url,headers=headers);
        pprint.pprint(res.json())


if __name__ == "__main__":
    url='http://upos-hz-mirrorkodo.acgvideo.com/dspxcode/i181206ws3idr6yxt878k82bqo555js3-1-56.mp4?um_deadline=1546796180&rate=500000&oi=3083024301&um_sign=df58bd3824b0e06e911654033c1980a6&gen=dsp&wsTime=1546796180&platform=html5';
    lyrb=LuYouReBoot()
    headers={
        'User - Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    res=requests.get(url,headers=headers,stream=True);
    if res.status_code==200:
        for item_data in res.iter_content(chunk_size=1024):
            with open('C:/cc.mp4',mode='ab') as file:
                file.write(item_data);
                file.flush()
