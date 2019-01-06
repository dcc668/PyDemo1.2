# ecoding=utf-8

import requests, os, urllib
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium.webdriver import Chrome, PhantomJS
import time, json, random
from threading import Thread

# http://www.everystockphoto.com/
PHOTO_COOKIE = '__unam=2e3b66d-160a6f74a5e-1fa554e4-3; AWSELB=97878D2104732ADDF38D4DE7A65BEF917616C430B4A0D48C19E26F35B9D6DED2917AEF283E48299E086FD716BD3B94D5F5F33C9FFE3F4B2D726BB7D3A8FDBBEAAB7B06ED63; __utmt=1; PHPSESSID=hiula5k4qagot5uth6mctla0f0; ESPTOK=e5be800434bb850101a9cbe78651e929; __utma=67133509.1092402433.1514627847.1514640320.1514768886.3; __utmb=67133509.8.10.1514768886; __utmc=67133509; __utmz=67133509.1514627847.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'


class Downloader():
    @staticmethod
    def down_pic(url):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        return requests.get(url, headers=headers, stream=True, timeout=20).content

DETAIL_URLS_DIR = 'D:/pic3/photo/url/'
if os.path.exists(DETAIL_URLS_DIR) == False:
    os.makedirs(DETAIL_URLS_DIR)
DIRS = 'D:/pic3/photo/'
if os.path.exists(DIRS) == False:
   os.makedirs(DIRS)

class ZhiHuSelenum():
    def __init__(self):
        self.chromePath = r'J:\lib\driver\chromedriver.exe'
        os.environ["webdriver.chrome.driver"] = self.chromePath
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            "user-data-dir=" + os.path.abspath(r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"))
        self.driver = webdriver.Chrome(executable_path=self.chromePath,
                                       chrome_options=chrome_options)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        self.driver.maximize_window()
        # 记录下载过的图片地址，避免重复下载

    def execute_url(self, keyword, page_num):
        for page in range(page_num):
            url = 'http://www.everystockphoto.com/search.php?&oSort=desc&sSort=1&sField=' \
                  + keyword + '&sLayout=1&sBool=and&sLicense%5B%5D=4&sLicense%5B%5D=6&sLicense%5B%5D=2&sLicense%5B%5D=3&sLicense%5B%5D=1&sLicense%5B%5D=5&sLicense%5B%5D=7&sLicense%5B%5D=99&multiselect_sLicense=4&multiselect_sLicense=6&multiselect_sLicense=2&multiselect_sLicense=3&multiselect_sLicense=1&multiselect_sLicense=5&multiselect_sLicense=7&multiselect_sLicense=99&restrict%5B%5D=none&restrict%5B%5D=account&restrict%5B%5D=restrict&sSource%5B%5D=1&sSource%5B%5D=5&sSource%5B%5D=4&sSource%5B%5D=2&sSource%5B%5D=8&sSource%5B%5D=11&sSource%5B%5D=3&sSource%5B%5D=7&sSource%5B%5D=6&safeSearch=1&sPortrait=on&sLandscape=on&sSquare=on&sMinW=&sMinH=&sDispRes=on&sDispLic=on&sDispSrc=on&perPage=100&currentPage=' \
                  + str(page)
            # 浏览器打开爬取页面
            self.driver.get(url)
            img_url_eles = self.driver.find_elements_by_xpath('//a[@class="img"]')
            print('----%s------size:%d-----img_urls:%s' % (keyword,len(img_url_eles), str(img_url_eles)))
            img_urls = []
            for img_url_ele in img_url_eles:
                try:
                    img_url = img_url_ele.get_attribute('href')
                    print('------->img_url  1 :' + img_url)
                    if img_url != None and (img_url not in img_urls):
                        img_urls.append(img_url)
                except Exception as e:
                    print('------->img_url  1 发生异常:' + str(e))
                    continue
            detail_img_urls = []
            for img_url in img_urls:
                self.driver.get(img_url)
                url2 = self.driver.find_elements_by_xpath('//a[@class="photo"]')
                for element in url2:
                    try:
                        detail_img_url = element.get_attribute('href')
                        if detail_img_url != None and (detail_img_url not in detail_img_urls):
                            print('获取图片详细url:' + detail_img_url)
                            detail_img_urls.append(detail_img_url)
                    except Exception as e:
                        print('获取图片详细url 发生异常:' + str(e))
                        continue
            print('图片详细url存文件')
            with open(DETAIL_URLS_DIR + keyword + '.txt', 'a') as file:
                for detail_url in detail_img_urls:
                    file.write(detail_url+'\n')
            if len(img_url_eles) < 100:  # 不取下一页
                break

    @staticmethod
    def save_imgs(detail_img_url, index):
        # 保存图片到指定路径
        file_name = '%s_%s' % (index, detail_img_url[detail_img_url.rindex("/") + 1:])
        # 保存图片数据
        print('保存图片数据 :' + detail_img_url)
        data = Downloader.down_pic(detail_img_url)
        with open(DIRS + file_name, 'wb') as f :
            f.write(data)


if __name__ == '__main__':
    zhihu = ZhiHuSelenum()
    keywords = ['rice with meat', 'Apple pie', 'Sour Soup', 'Braised sea cucumber',
                'hotpot']
    start_time = time.time()
    threads = []
    page_num = 15
    for keyword in keywords:
        t = Thread(target=zhihu.execute_url, args=(keyword, page_num))
        threads.append(t)
    for t in threads:
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))

    # -----------------------download img---------------------------------------------
    # for keyword in keywords:
    #     detail_file = DETAIL_URLS_DIR + keyword + '.txt'
    #     print('download img:   '+detail_file)
    #     with open(detail_file, 'r') as file:
    #         lines = file.readlines()
    #     for i in range(len(lines)):
    #         try:
    #             ZhiHuSelenum.save_imgs(lines[i], i)
    #             print('保存图片成功。。。')
    #         except Exception as e:
    #             print('保存图片数据 发生异常:'+str(lines[i]) + str(e))
    #             continue
