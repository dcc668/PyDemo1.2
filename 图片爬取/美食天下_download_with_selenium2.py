# -*- coding: utf-8 -*-
# @Author: WuLC
# @Date:   2017-09-27 23:02:19
# @Last Modified by:   LC
# @Last Modified time: 2017-09-30 10:54:36


####################################################################################################################
# Download images from google with specified keywords for searching
# search query is created by "main_keyword + supplemented_keyword"
# if there are multiple keywords, each main_keyword will join with each supplemented_keyword
# Use selenium and urllib, and each search query will download any number of images that google provide
# allow single process or multiple processes for downloading
# Pay attention that since selenium is used, geckodriver and firefox browser is required
####################################################################################################################

import os, random
import json, re, requests
import time
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse
from urllib.parse import unquote, quote

from multiprocessing import Pool
from threading import Thread
from settings import AGENTS
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from user_agent import generate_user_agent
from queue import Queue


class DownLoad():
    @staticmethod
    def down_page(url):
        html = requests.get(url).text
        return html

    @staticmethod
    def download_images(start, end, link_file_path, download_dir, log_dir, main_keyword):
        # start 从第几个开始爬
        """download images whose links are in the link file

        Args:
            link_file_path (str): path of file containing links of images
            download_dir (str): directory to store the downloaded images

        Returns:
            None
        """
        print('Start downloading with link file {0}'.format(link_file_path))
        log_file = log_dir + 'download_selenium_{0}.log'.format(main_keyword)
        logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+",
                            format="%(asctime)-15s %(levelname)-8s  %(message)s")
        count = start  ## 从第start个开始爬
        show = start
        headers = {}
        # start to download images
        with open(link_file_path, 'r') as rf:
            index = 0
            for link in rf:
                index += 1;
                if index >= start and index < end:  ## 从第start个开始爬
                    show += 1
                    print('---------------->>>>link to num:' + str(show))
                    try:
                        o = urlparse(link)
                        ref = o.scheme + '://' + o.hostname
                        # ref = 'https://www.google.com'
                        ua = random.choice(AGENTS)
                        headers['User-Agent'] = ua
                        headers['referer'] = ref
                        print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
                        req = urllib.request.Request(link.strip(), headers=headers)
                        response = urllib.request.urlopen(req)
                        data = response.read()
                        file_path = download_dir + '{0}.jpg'.format(count)
                        with open(file_path, 'wb') as wf:
                            wf.write(data)
                        print('Process-{0} download image {1}/{2}.jpg'.format(main_keyword, main_keyword, count))
                        count += 1
                        if count % 10 == 0:
                            print('Process-{0} is sleeping'.format(main_keyword))
                            # time.sleep(1)  #5

                    except urllib.error.URLError as e:
                        print('URLError')
                        logging.error('URLError while downloading image {0}reason:{1}'.format(link, e.reason))
                        continue
                    except urllib.error.HTTPError as e:
                        print('HTTPError')
                        logging.error(
                            'HTTPError while downloading image {0}http code {1}, reason:{2}'.format(link, e.code,
                                                                                                    e.reason))
                        continue
                    except Exception as e:
                        print('Unexpected Error')
                        logging.error(
                            'Unexpeted error while downloading image {0}error type:{1}, args:{2}'.format(link, type(e),
                                                                                                         e.args))
                        continue

    @staticmethod
    def bing_gen_query_url(keywords, page):
        base_url = "http://home.meishichina.com/search/%s/page/%d/" % (keywords, page)
        return base_url

    @staticmethod
    def bing_image_url_from_webpage(url):
        image_elements = list()
        regex = r'<div class="pic">(.|\\n|\s){1,5}<a(.|\\n|\s){1,5}href="(.*?)"'
        retry=0
        while len(image_elements) == 0 and retry<=9:
            retry=retry+1
            html = DownLoad.down_page(url)
            image_elements = re.findall(regex, html, re.S)
            print('------------------>>>>>image_elements:' + str(len(image_elements)))
            # time.sleep(1)
        image_urls = []
        for image_element in image_elements:
            print('------------------>>>>>image_element:' + str(image_element[2]))
            html = DownLoad.down_page(image_element[2])
            regex = r'<a class="J_photo"[^>]{1,555}><span>(.|\\n|\s){0,333}</span><img src="(.*?)"'
            image_elements2 = re.findall(regex, html, re.S)
            if len(image_elements2) > 0:
                print('------------------>>>>>image_element2:' + str(image_elements2[0][1]))
                image_urls.append(image_elements2[0][1])
        return image_urls


maxImageNum = 50
download = 30
timeout = 15
type_image = {'jpg', 'jpeg', 'png'}
download_dir = 'D:/pic4-10/meishi/'
link_files_dir = 'D:/pic4-10/meishi/url/'
link_files_dir_403 = 'D:/pic4-10/meishi/url_403/'
totalPageNum = 55  # 爬取页数


class Google():
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

    def get_image_links(self, main_keywords, pre_link_path, fileNames, page=10):
        for i in range(len(main_keywords)):
            search_query = main_keywords[i]
            link_file_path = pre_link_path + fileNames[i] + ".txt"
            image_urls_count = set()
            for j in range(page):
                url = DownLoad.bing_gen_query_url(search_query, j)
                image_urls = DownLoad.bing_image_url_from_webpage(url)
                for img_link in image_urls:
                    image_urls_count.add(img_link)
                # time.sleep(1)
            print('KeyWords {0} , got {1} image urls so far'.format(main_keywords[i], len(image_urls_count)))
            with open(link_file_path, 'a', encoding='utf-8') as wf:
                for iu in image_urls_count:
                    wf.write(iu + '\n')
            print('Store all the links in file {0}'.format(link_file_path))

    def download_images(self, count, download_dir, main_keyword):
        self.main_keyword = main_keyword
        headers = {}
        size = self.queue.qsize()
        count = count - size
        print('queue size:' + str(size))
        while size > 0:
            try:
                link = self.queue.get()
                o = urlparse(link)
                size = self.queue.qsize()
                print('queue size:' + str(size))
                count = count - size
                ref = o.scheme + '://' + o.hostname
                # ua = random.choice(AGENTS)
                ua = generate_user_agent(os=('mac', 'linux', 'win'))
                headers['User-Agent'] = ua
                headers['referer'] = ref
                print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
                req = urllib.request.Request(link.strip(), headers=headers)
                response = urllib.request.urlopen(req)
                data = response.read()
                file_path = download_dir + str(count) + "-" + str(time.time()) + ".jpg"
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
                time.sleep(0.5)  # 5
                print('queue size:' + str(size))


if __name__ == "__main__":
    fileNames = [
         '龙井虾仁',
    ]
    keywords = ['龙井虾仁', ]
    download_dir = 'D:/pic4-10/meishi/'
    link_files_dir = 'D:/pic4-10/meishi/url/'
    log_dir = 'D:/pic4-10/meishi/logs/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(link_files_dir):
        os.makedirs(link_files_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    ###################################
    # get image links and store in file
    ###################################

    # single process
    google = Google()
    google.get_image_links(keywords, link_files_dir, fileNames)



    ###################################
    # download images with link file
    ##################################

    # multiple process
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    threads = []
    for i in range(len(fileNames)):
        link_file_path = link_files_dir + fileNames[i] + '.txt'
        # 下载路径
        download_file_path = download_dir + fileNames[i] + '/'
        if os.path.exists(download_file_path) == False:
            os.makedirs(download_file_path)
        count = 0
        spider = Google()
        with open(link_file_path, 'r') as file:
            count += 1
            for link in file:
                print('入队．．．' + link)
                spider.queue.put(link)
        print('入队．．．finish..............')
        for j in range(3):
            t = Thread(target=spider.download_images,
                       args=(count, download_file_path, fileNames[i]))
            threads.append(t)
    for t in threads:
        t.start()





            # multiple processes   暂时不能用
            # 浏览器的 C:\Users\Administrator\AppData\Local\Google\Chrome\User Data
            # p = Pool(3) # default number of process is the number of cores of your CPU, change it by yourself
            # for i in range(len(main_keywords)):
            #     p.apply_async(get_image_links, args=(main_keywords[i], supplemented_keywords, link_files_dir + fileNames[i]))
            # p.close()
            # p.join()
            # print('Fininsh getting all image links')




            # if not os.path.exists(log_dir):
            #     os.makedirs(log_dir)
            # threads = []
            # for fileName in fileNames:
            #     link_file_path = link_files_dir + fileName+".txt"
            #     # 下载路径
            #     download_file_path = download_dir + fileName + '/'
            #     if os.path.exists(download_file_path) == False:
            #         os.makedirs(download_file_path)
            #     t = Thread(target=DownLoad.download_images,
            #                args=(link_file_path, download_file_path, log_dir, fileName))
            #     threads.append(t)
            # for t in threads:
            #     t.start()


            # multiple processes
            # p = Pool() # default number of process is the number of cores of your CPU, change it by yourself
            # for keyword in main_keywords:
            #     p.apply_async(download_images, args=(link_files_dir + keyword, download_dir, log_dir))
            # p.close()
            # p.join()
            # print('Finish downloading all images')
