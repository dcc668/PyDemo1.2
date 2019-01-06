from user_agent import generate_user_agent
import requests,re,os
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver


class DownLoad():
    @staticmethod
    def down_page(url):
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Cookie':'zh_choose=n; __jsluid=86f5e976583dae4c5ac9d6255270294c; JSESSIONID=BE927F9BF6BEB6B9991923EEC36520D7; Hm_lvt_525b7a4b6599566fc46ec53565d28557=1519714387,1519717052; Hm_lpvt_525b7a4b6599566fc46ec53565d28557=1519725696',
            'Host':'www.coinw.com',
            'Referer':'https://www.coinw.com/newService/ourService.html?id=1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        }
        html = requests.get(url, headers=headers).text
        return html
class Spider():
    def get_links(self,url):
        self.driver.get(url)
        a_eles=self.driver.find_elements_by_class_name('link-1');
        hrefs=set()
        for  ele in a_eles:
            href=ele.get_attribute('href')
            hrefs.append(href);

        return hrefs;
    def get_content(self,url):
        self.driver.get(url)
        a_eles=self.driver.find_elements_by_class_name('link-1');
        hrefs=set()
        for  ele in a_eles:
            href=ele.get_attribute('href')
            hrefs.append(href);


url='https://www.coinw.com/newService/ourService.html?id=1&currentPage=3'
html=DownLoad.down_page(url)
bs=BeautifulSoup(html,'lxml')
# print(bs.prettify())
a_eles=bs.find_all(attrs={'class':'link-1'})
for a_ele in a_eles:
    # print(a_ele['href'])
    url='https://www.coinw.com'+a_ele['href']
    print(url)
    html2=DownLoad.down_page(url)
    bs2=BeautifulSoup(html2,'lxml')
    pattern=re.compile('<h3 class="mb5 fs-20 color-dark">(.*?)</h3>',re.S)
    res=re.findall(pattern,bs2.prettify())
    print(res[0])
    break;