#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re,urllib
from threading import Thread
import requests,time
import settings

# http://www.everystockphoto.com/
PHOTO_COOKIE='__unam=2e3b66d-160a6f74a5e-1fa554e4-3; AWSELB=97878D2104732ADDF38D4DE7A65BEF917616C430B4A0D48C19E26F35B9D6DED2917AEF283E48299E086FD716BD3B94D5F5F33C9FFE3F4B2D726BB7D3A8FDBBEAAB7B06ED63; __utmt=1; PHPSESSID=hiula5k4qagot5uth6mctla0f0; ESPTOK=e5be800434bb850101a9cbe78651e929; __utma=67133509.1092402433.1514627847.1514640320.1514768886.3; __utmb=67133509.8.10.1514768886; __utmc=67133509; __utmz=67133509.1514627847.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
class Downloader():
    @staticmethod
    def down_page(url):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Cookie': PHOTO_COOKIE
                   }
        html = requests.get(url,headers=headers).text
        return html

    @staticmethod
    def down_pic(url,save_dir):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   'Cookie':PHOTO_COOKIE
                   }
        req = urllib.request.Request(url.strip(), headers=headers)
        response = urllib.request.urlopen(req)
        data = response.read()
        temp_file = open(save_dir, 'wb')
        temp_file.write(data)
        temp_file.close()


class UrlManager():
    def __init__(self):
        self.page_urls = set()

    def gen_urls(self, word, pages):
        for page in range(pages):
            url = self.__gen_url__(word,page)
            self.page_urls.add(url)

    def __gen_url__(self, word,page):
        return 'http://www.everystockphoto.com/search.php?&oSort=desc&sSort=1&sField='+word+'&sLayout=1&sBool=and&sLicense%5B%5D=4&sLicense%5B%5D=6&sLicense%5B%5D=2&sLicense%5B%5D=3&sLicense%5B%5D=1&sLicense%5B%5D=5&sLicense%5B%5D=7&sLicense%5B%5D=99&multiselect_sLicense=4&multiselect_sLicense=6&multiselect_sLicense=2&multiselect_sLicense=3&multiselect_sLicense=1&multiselect_sLicense=5&multiselect_sLicense=7&multiselect_sLicense=99&restrict%5B%5D=none&restrict%5B%5D=account&restrict%5B%5D=restrict&sSource%5B%5D=1&sSource%5B%5D=5&sSource%5B%5D=4&sSource%5B%5D=2&sSource%5B%5D=8&sSource%5B%5D=11&sSource%5B%5D=3&sSource%5B%5D=7&sSource%5B%5D=6&safeSearch=1&sPortrait=on&sLandscape=on&sSquare=on&sMinW=&sMinH=&sDispRes=on&sDispLic=on&sDispSrc=on&perPage=100&currentPage='+str(page)

    def has_new_url(self):
        return len(self.page_urls) > 0

    def get_craw_url(self):
        return self.page_urls.pop()


class Parser():
    def parse(self, html):
        img_urls= re.findall(r'class="img"\s{1,}href="(.*?)"', html, re.S)
        print('----------size:%d-----img_urls:%s'%(len(img_urls),str(img_urls)))
        urls=[]
        for i in range(len(img_urls)):
            if i<=3:
                try:
                    url = 'http://www.everystockphoto.com'+img_urls[i]
                    html2 = Downloader.down_page(url)
                    url2 = re.findall(r'class="photo"(.|\n|\s){1,35}href="(.*?)"', html2, re.S)
                    print('---------------img url:' + str(url2[0][1]))
                    time.sleep(0.3)
                    urls.append(url2[0][1])
                except Exception as e:
                    print(str(e))
                    continue
            else:
                break;
        return urls;

class Output():
    def __init__(self):
        self.result_dir = 'D:/pic/nitu3/'
        self.__check_dir__(self.result_dir)

    def __check_dir__(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def show(self):
        print("result dir: %s" % os.path.abspath(self.result_dir))


class Spider_Main():
    def __init__(self):
        self.urls = UrlManager()
        self.downloader = Downloader()
        self.parser = Parser()
        self.output = Output()


    def crawl(self, word):
        self.output.result_dir =self.output.result_dir+word+'/'
        self.output.__check_dir__(self.output.result_dir)
        self.__check_params__(word, 20)#page  100 per page
        self.urls.gen_urls(word, 20)

        count = 0
        while self.urls.has_new_url():
            page_url = self.urls.get_craw_url()
            html = self.downloader.down_page(page_url)
            pic_urls = self.parser.parse(html)
            while len(pic_urls)==0:
                print('pic_urls 为空，重新获取。。。。')
                print(html)
                pic_urls = self.parser.parse(html)
                time.sleep(0.5)
            for pic_url in pic_urls:
                try:
                    count += 1
                    file_name = '%s_%s' % (count, pic_url[pic_url.rindex("/") + 1:])
                    print('----------->>>download:'+pic_url)
                    save_dir=os.path.join(self.output.result_dir, file_name)
                    self.downloader.down_pic(pic_url,save_dir)
                    print( "crawl %s url=%s" % (count, pic_url))
                except Exception as e:
                    print("failed %s url=%s, e=%s" % (count, pic_url, e))
        self.output.show()

    @staticmethod
    def __check_params__(word, pages):
        if word is None:
            raise Exception('关键字不能为空')
        if pages <= 0:
            raise Exception('页数必须大于0')


if __name__ == '__main__':
    keywords=['rice served with meat', 'Apple pie', 'Hot and Sour Soup', 'Braised sea cucumber', '木须肉',
                     'Instant Spicy Steampot', 'hotpot']
    start_time = time.time()
    threads=[]
    for keyword in keywords:
        spider=Spider_Main()
        t = Thread(target=spider.crawl,args=(keyword,))
        threads.append(t)
    for t in threads:
        t.start()
        t.join()
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))