#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
from threading import Thread
import requests,time

class Downloader():
    @staticmethod
    def down_page(url):
        html = requests.get(url).text
        return html

    @staticmethod
    def down_pic(url):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        return requests.get(url, headers=headers, stream=True, timeout=20).content


class UrlManager():
    def __init__(self):
        self.page_urls = set()

    def gen_urls(self, word, pages):
        for page in range(0,pages):
            url = self.__gen_url__(word, page)
            self.page_urls.add(url)
        print('------word----'+word+'----url count---'+str(len(self.page_urls)))
    def __gen_url__(self, word, page):
        return 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%s&gsm=3c&ct=&ic=0&lm=-1&width=0&height=0' % (
            word, page)

    def has_new_url(self):
        return len(self.page_urls) > 0

    def get_craw_url(self):
        return self.page_urls.pop()


class Parser():
    def parse(self, html):
        print()
        urls=re.findall(r'objURL":"(.*?)"', html, re.S)
        new_urls=[]
        for url in urls:
            print('----img-url:'+url)
            test = re.findall(r'//(.*?)thumb.jpg', url)
            if len(test)==0:
                new_urls.append(url)
            else:
                print('end thumb.jpg'+str(test))
        urls2=re.findall(r'data-thumburl=(.*?)', html, re.S)
        for url in urls2:
            print('----img-url2:' + url)
            new_urls.append(url)
        return new_urls

class Output():
    def __init__(self):
        self.result_dir = 'D:/pic4-10/baidu/'
        self.__check_dir__(self.result_dir)

    def save(self, file_name, pic_content):
        with open(os.path.join(self.result_dir, file_name), 'wb') as result_file:
            result_file.write(pic_content)

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

    def general_urls(self,word,fileName, page):
        self.output.result_dir = self.output.result_dir + fileName + '/'
        self.output.__check_dir__(self.output.result_dir)
        self.__check_params__(word, page)
        self.urls.gen_urls(word, page)
    def crawl(self):
        count = 0
        while self.urls.has_new_url():
            page_url = self.urls.get_craw_url()
            html = self.downloader.down_page(page_url)
            pic_urls = self.parser.parse(html)
            for pic_url in pic_urls:
                try:
                    count += 1
                    file_name = '%s_%s' % (count, pic_url[pic_url.rindex("/") + 1:])
                    pic_content = self.downloader.down_pic(pic_url)
                    self.output.save(file_name, pic_content)
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
    # fileNames=[
    #     "墨西哥玉米片(奶酪玉米片)",
    #     "三文鱼牛油果盖饭",
    #     "苹果派(苹果馅饼)",
    #     "酸辣汤(胡辣汤)",
    #     "烧海参(焖海参，炒海参)",
    #     "木须肉",
    #     "冒菜",
    #     "重庆火锅"
    # ]
    # keywords=[
    #     "玉米片",
    #     "三文鱼牛油果盖饭",
    #     "苹果派(苹果馅饼)",
    #     "酸辣汤(胡辣汤)",
    #     "烧海参(焖海参，炒海参)",
    #     "木须肉",
    #     "冒菜",
    #     "重庆火锅"
    # ]
    # fileNames = [
    #     "墨西哥玉米片",
    #     "三文鱼牛油果盖饭",
    #     "苹果派(苹果馅饼)",
    #     "酸辣汤(胡辣汤)",
    #     "烧海参(焖海参，炒海参)",
    #     "木须肉",
    #     "重庆火锅",
    #     "冒菜"
    # ]
    # keywords = ['奶酪玉米片','盖饭', '馅饼', '胡辣汤', '炒海参', '木耳炒肉',
    #                  '火锅', '冒菜']

    # fileNames = [
    #     '鲫鱼汤',
    #     '绿豆糕',
    #     '脏脏包',
    #     '萝卜泡菜',
    #     '日式咖喱饭',
    #     '糖葫芦',
    #     '饭团',
    #     '大拌菜',
    #     '糖炒栗子',
    #     '炒花生',
    # ]
    # keywords = [
    #     '鲫鱼汤',
    #     '绿豆糕',
    #     '脏脏包',
    #     '萝卜泡菜',
    #     '日式咖喱饭',
    #     '糖葫芦',
    #     '饭团',
    #     '大拌菜',
    #     '糖炒栗子',
    #     '炒花生米',
    # ]
    # fileNames = [
    #     '牛油果盖饭',
    # ]
    # keywords = [
    #     '牛油果盖饭',
    # ]
    fileNames = [
        "发糕", "羊肉泡膜","印度咖喱羊肉煲",
    ]
    keywords = ['发糕', "羊肉泡膜","羊肉煲", ]
    start_time = time.time()
    threads=[]
    for i in range(len(keywords)):
        spider=Spider_Main()
        page=1500
        spider.general_urls(keywords[i], fileNames[i], page)
        for i in range(3):
            t1 = Thread(target=spider.crawl)
            threads.append(t1)
    for t in range(len(threads)):
        threads[t].start()
    # for t in range(4,8):
    #     threads[t].start()
    # threads[t].join()
    # for t in range(8,10):
    #     threads[t].start()
    # threads[t].join()
    end_time = time.time()

    print("Total time: {}".format(end_time - start_time))