#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import time
import requests
import urllib
import os, re
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse
from threading import Thread, Lock
from settings import AGENTS
from queue import Queue
from user_agent import generate_user_agent

maxImageNum = 50
download = 30
timeout = 15
socket.setdefaulttimeout(timeout)
type_image = {'jpg', 'jpeg', 'png'}
download_dir = 'D:/pic4-10/shougou/'
link_files_dir = 'D:/pic4-10/shougou/url/'
link_files_dir_403 = 'D:/pic4-10/shougou/url_403/'
totalPageNum = 55  # 爬取页数


class HaoSuoSpider:
    __amount = 0
    __start_amount = 0
    __counter = 0

    def __init__(self):
        """
        :param totalPageNum: 下载页数
        :param image_path: 图片放置目录
        """
        self.download = download;
        self.image_path = download_dir
        self.__amount = totalPageNum * maxImageNum + self.__start_amount
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36',
        }
        self.queue = Queue()

    def parseJson(self, data, _key='thumb_bak'):
        print('json 解析：。。。' + str(data))
        img_list = []
        _indx = 0;
        while len(data) > 2 and _indx != -1:
            _indx = data.find(_key);
            data = data[_indx:];
            url_tag_index = data.find(',');
            if url_tag_index != -1:
                value = data[:url_tag_index];
                url = value.split('":"')[-1].strip('"');
                url = url.replace('\\\/', "/")
                img_list.append(url);
                data = data[url_tag_index + 1:]
        return img_list;

    def getImg(self, keyword,page=40):
        root_path = self.image_path
        print('root path:' + root_path)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        if not os.path.exists(link_files_dir):
            os.makedirs(link_files_dir)
        if not os.path.exists(link_files_dir_403):
            os.makedirs(link_files_dir_403)

        img_urls = []
        # 获取页面中的源码
        for i in range(page):
            if i==0:
                url = "http://pic.sogou.com/pics?query=%s&p=40230500&st=255&mode=255"%(keyword)
            else:
                url = "http://pic.sogou.com/pics?query=%s&mode=1&start=%d&reqType=ajax&reqFrom=result&tn=05" % (keyword,48*i)
            page = requests.get(url, headers=self.headers, timeout=20).content
            # 获取"pic_url":"http://xxxxx/x/x.jpg"图片url
            regex=r'"pic_url":"(.*?)"'
            picItems = re.findall(regex, str(page), re.S)
            # 把图片的url添加到imgUrl列表中
            for aItem in picItems:
                img_urls.append(aItem)
        link_file_path = link_files_dir + keyword + ".txt"
        with open(link_file_path, 'a', encoding='utf-8') as wf:
            for url in img_urls:
                wf.write(url + '\n')
        print('Store all the links in file {0}'.format(link_file_path))
    def download_images(self,count, download_dir, main_keyword):
        self.main_keyword=main_keyword
        headers = {}
        size=self.queue.qsize()
        count=count-size
        print('queue size:'+str(size))
        while size>0:
            try:
                link=self.queue.get()
                o = urlparse(link)
                size = self.queue.qsize()
                print('queue size:' + str(size))
                count = count - size
                ref = o.scheme + '://' + o.hostname
                # ua = random.choice(AGENTS)
                ua = generate_user_agent(os=('mac', 'linux','win'))
                headers['User-Agent'] = ua
                headers['referer'] = ref
                print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
                req = urllib.request.Request(link.strip(), headers=headers)
                response = urllib.request.urlopen(req)
                data = response.read()
                file_path = download_dir +str(count)+"-"+str(time.time())+".jpg"
                with open(file_path, 'wb') as wf:
                    wf.write(data)
                print('Process-{0} download image {1}/{2}.jpg'.format(main_keyword, main_keyword, count))
            except urllib.error.URLError as e:
                print('URLError' + str(e))
                self.queue.put(link)
                continue
            except urllib.error.HTTPError as e:
                print('HTTPError' + str(e))
                self.queue.put(link)
                continue
            except Exception as e:
                print('Unexpected Error' + str(e))
                self.queue.put(link)
                continue
            finally:
                time.sleep(1)  # 5
                print('queue size:' + str(size))
    def __del__(self):
        pass
        # print('程序退出，队列存储到403文件。。。')
        # size=self.queue.qsize()
        # link_file_path_403=link_files_dir_403+self.main_keyword+'.txt'
        # with open(link_file_path_403, 'a', encoding='utf-8') as wf:
        #     for i in range(size):
        #         wf.write(self.queue.get() + '\n')


if __name__ == '__main__':
    # fileNames = ['奶酪玉米片','冒菜(麻辣烫)',]
    # words = ['奶酪玉米片','冒菜麻辣烫)',]
    # fileNames = ['炒花生米','牛油果盖饭','烧海参','胡辣汤','木须肉']
    # words = ['炒花生米','牛油果盖饭','烧海参','胡辣汤','木须肉']
    # fileNames = ['腌萝卜','鱼馅饼','苹果派','脏脏包',]
    # words = ['腌萝卜','鱼馅饼','苹果派','脏脏包',]
    # fileNames = ['沙拉大拌菜''饭团'茶叶虾仁]
    # words = ['沙拉大拌菜''饭团'茶叶虾仁]
    # fileNames = ['羊肉泡馍','龙井虾仁',发糕'鱼饼面包','网红面包','三文鱼牛油果盖饭','果丹皮','辣炒鱿鱼','果丹卷']
    # words = ['羊肉泡馍','龙井虾仁'发糕',鱼饼面包','网红面包','三文鱼牛油果盖饭','果丹皮','辣炒鱿鱼','果丹卷']
    fileNames = ['紫菜包饭']
    words = ['紫菜包饭']

    # 获取连接
    for word in words:
        spider = HaoSuoSpider()
        spider.getImg(word);

    # 图片下载烧海参
    threads = []
    for i in range(len(fileNames)):
        link_file_path = link_files_dir + fileNames[i] + '.txt'
        # 下载路径
        download_file_path = download_dir + fileNames[i] + '/'
        if os.path.exists(download_file_path) == False:
            os.makedirs(download_file_path)
        count=0
        spider = HaoSuoSpider()
        with open(link_file_path, 'r') as file:
            count+=1
            for link in file:
                print('入队．．．'+link)
                spider.queue.put(link)
        print('入队．．．finish..............')
        for j in range(5):
            t = Thread(target=spider.download_images,
                        args=(count, download_file_path, fileNames[i]))
            threads.append(t)
        for t in threads:
            t.start()