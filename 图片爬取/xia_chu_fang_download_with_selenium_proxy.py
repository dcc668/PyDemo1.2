# -*- coding: utf-8 -*-
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
import redis

ip= 'http://118.114.77.47:8080'
# ip= 'http://113.200.159.155:9999'
# ip= 'http://118.178.124.33:3128'


class DownLoad():
    @staticmethod
    def get_proxies():
        proxies = {
            'http':ip,
        }
        return proxies
    @staticmethod
    def down_page(url):
        ua = generate_user_agent(os=('mac', 'linux', 'win'))
        headers={'User-Agent':ua}
        retry=0
        while retry<3:
            try:
                html = requests.get(url, headers=headers,proxies=DownLoad.get_proxies(),timeout=9).text
                break
            except Exception as e:
                retry+=1
                print('请求发生异常，重试%d。。。。%s%s'%(retry,url,str(e)))
                time.sleep(1)
                continue
        return html

    @staticmethod
    def down_page_return_url(url):
        ua = generate_user_agent(os=('mac', 'linux', 'win'))
        headers = {'User-Agent': ua}
        retry = 0
        while retry < 3:
            try:
                response = requests.get(url, headers=headers, proxies=DownLoad.get_proxies(), timeout=9);
                break
            except Exception as e:
                retry += 1
                print('请求发生异常，重试%d。。。。%s%s' % (retry, url, str(e)))
                time.sleep(1)
                continue
        html = response.text
        return (html,response.url)
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
        base_url = "http://www.xiachufang.com/search/?keyword=%s&cat=1001&page=%d" % (keywords, page)
        return base_url

    @staticmethod
    def bing_image_url_from_webpage(html):
        regex = r'<a href="/recipe/(.*?)/"'
        image_elements = re.findall(regex, html, re.S)
        image_urls = []
        details_urls= []
        for image_element in image_elements:
            print('------------------>>>>>image_element:' + str(image_element))
            details_url='http://www.xiachufang.com/recipe/' + image_element
            details_urls.append(details_url)
            html = DownLoad.down_page(details_url)
            regex = r'<div class="cover image expandable block-negative-margin"(.|\n|\s){1,300}<img(.|\\n|\s){1,5}src="(.*?)"'
            image_elements2 = re.findall(regex, html, re.S)
            if len(image_elements2) > 0:
                ele=image_elements2[0][2]
                if ele.find('<')==-1:
                    print('------------------>>>>>image_element2:' + str(image_elements2))
                    image_urls.append(ele)
            time.sleep(1)
        return (image_urls,details_urls)#详细页图片，详细页
    @staticmethod
    def bing_image_details_url_from_webpage(url):
        image_elements = list()
        regex = r'<a href="/dish/(.*?)/"'
        retry = 0
        while len(image_elements) == 0 and retry < 2:
            retry = retry + 1
            html = DownLoad.down_page(url)
            image_elements = re.findall(regex, html, re.S)
            print('------------------>>>>>details image_elements:' + str(image_elements))
            if retry == 2:
                return []
            time.sleep(1)
        image_urls = []
        elements = set()
        for image_element in image_elements:
            elements.add(image_element)
        for image_element in elements:
            print('------------------>>>>> details image_element:' + str(image_element))
            details_url = 'http://www.xiachufang.com/dish/' + image_element
            html = DownLoad.down_page(details_url)
            regex = r'<div class="dish-cover block-negative-margin">(.|\n|\s){1,30}<img(.|\\n|\s){1,5}src="(.*?)"'
            image_elements2 = re.findall(regex, html, re.S)
            if len(image_elements2) > 0:
                print('------------------>>>>> details image_element2:' + str(image_elements2))
                image_urls.append(image_elements2[0][2])
            time.sleep(1)
        return image_urls  # 详细页图片
    @staticmethod
    def bing_image_details_url_from_webpage_with_selenium(urls):
        image_urls=[]
        for details_url in urls:
            try:
                html = DownLoad.down_page(details_url)
            except Exception as e:
                print(str(e))
                time.sleep(1)
                continue
            regex = r'<div class="dish-cover block-negative-margin">(.|\n|\s){1,30}<img(.|\\n|\s){1,5}src="(.*?)"'
            image_elements2 = re.findall(regex, html, re.S)
            if len(image_elements2) > 0:
                print('------------------>>>>> details image_element2:' + str(image_elements2))
                image_urls.append(image_elements2[0][2])
            time.sleep(random.randrange(1,2))
        return image_urls  # 详细页图片

maxImageNum = 50
download = 30
timeout = 15
type_image = {'jpg', 'jpeg', 'png'}
download_dir = 'D:/pic4-10/xiachufang/'
link_files_dir = 'D:/pic4-10/xiachufang/url/'
link_files_dir_403 = 'D:/pic4-10/xiachufang/url_403/'
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
        self.rds = redis.StrictRedis(host='39.108.122.83', port='6379', decode_responses=True)
        self.q_details = 'myspider:details_links'

    def driver_init(self,is_with_proxy=False):
        chromePath = r'J:\lib\driver\chromedriver.exe'
        if is_with_proxy:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--proxy-server='+ip)
            self.driver = webdriver.Chrome(executable_path=chromePath,chrome_options=chrome_options)
        else:
            self.driver = webdriver.Chrome(executable_path=chromePath)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        self.driver.maximize_window()
    def get_image_links(self, main_keywords, pre_link_path, fileNames, page=20):
        for i in range(len(main_keywords)):
            search_query = main_keywords[i]
            link_file_path = pre_link_path + fileNames[i] + ".txt"
            details_file_path = pre_link_path +'details_'+fileNames[i] + ".txt"
            image_urls_count = set()
            details_urls_count = set()
            for j in range(1,page):
                #详细页图片，详细页
                if j==1:
                    url = DownLoad.bing_gen_query_url(search_query, 1)
                    html,res_url = DownLoad.down_page_return_url(url)
                elif j==2:
                    if res_url.find('category')!=-1:
                        res_url = res_url+'?page=2'
                    else:
                        res_url = res_url + '&page=2'
                    html = DownLoad.down_page(res_url)
                else:
                    res_url=res_url.replace('page='+str(j-1),'page='+str(j))
                    print('---#详细页图片，详细页----'+res_url)
                    html=DownLoad.down_page(res_url)
                image_urls,details_urls = DownLoad.bing_image_url_from_webpage(html)
                for img_link in image_urls:
                    image_urls_count.add(img_link)
                for img_link1 in details_urls:
                    details_urls_count.add(img_link1)
                    # time.sleep(1)
            print('KeyWords {0} , got {1} image urls so far'.format(main_keywords[i], len(image_urls_count)))
            with open(link_file_path, 'a', encoding='utf-8') as wf:
                for iu in image_urls_count:
                    wf.write(iu + '\n')
            with open(details_file_path, 'a', encoding='utf-8') as wf:
                for iu in details_urls_count:
                    wf.write(iu + '\n')
            print('Store all the links in file {0}'.format(link_file_path))

    def get_details_links(self, main_keywords, pre_link_path, fileNames):
        self.driver_init(True)
        for i in range(len(main_keywords)):
            link_file_path = pre_link_path + fileNames[i] + ".txt"
            link_file_beifen_path = pre_link_path+'beifen/' + fileNames[i] + ".txt"
            if not os.path.exists(pre_link_path+'beifen/'):
                os.makedirs(pre_link_path+'beifen/')
            details_file_path = pre_link_path + 'details_' + fileNames[i] + ".txt"
            with open(details_file_path,'r',encoding='utf-8') as file:
                lines=file.readlines()
            links=set()
            for link in lines:
                links.add(link)
            #使用redis 队列 存储要爬取的详细页连接
            # self.rds.lrem(self.q_details)#清空队列
            for link in links:
                self.rds.lpush(self.q_details, str(link))
            while self.rds.llen(self.q_details)>0:
                link=self.rds.rpop(self.q_details)
                print('浏览器访问url：'+link)
                current_url=str(link).replace('\n','')+'/dishes/'
                self.driver.get(current_url)
                img_links = set()
                # 详细页图片，详细页
                img_count = 0
                retry_count = 0
                while True:
                    try:
                        image_elements = self.driver.find_elements_by_class_name('cover-link')
                        if len(image_elements) > img_count:
                            retry_count = 0
                            img_count = len(image_elements)
                            self.driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)  # default 3
                        else:
                            time.sleep(2)
                            retry_count += 1
                            if retry_count >= 10:  # 连续重试15（根据网速）次时，退出
                                break
                            else:
                                continue
                    except Exception as e:
                        print(str(e))
                        time.sleep(2)
                        continue
                for img_ele in image_elements:
                    try:
                        img_link=img_ele.get_attribute('href')
                    except Exception as e:
                        print(str(e))
                        continue
                    print('-----href--------'+str(img_link))
                    img_links.add(img_link)
                #备份待爬连接
                print('----备份待爬连接----size:'+str(len(img_links)))
                with open(link_file_beifen_path, 'w', encoding='utf-8') as wf:
                    for iu in img_links:
                        wf.write(iu + '\n')
                self.__image_urls_save__(img_links, link_file_path)
    def get_details_links_from_beifen(self, main_keywords, pre_link_path, fileNames):
        for i in range(len(main_keywords)):
            link_file_beifen_path = pre_link_path + 'beifen/' + fileNames[i] + ".txt"
            link_file_path = pre_link_path + fileNames[i] + ".txt"
            # 备份待爬连接
            with open(link_file_beifen_path, 'r', encoding='utf-8') as wf:
                img_links=wf.readlines()
            img_links_set=set()
            for link in img_links:
                img_links_set.add(link)
            print('----待爬连接----size:' + str(len(img_links_set)))
            self.__image_urls_save__(img_links_set, link_file_path)

    def __image_urls_save__(self,img_links,link_file_path):
        # 50个，保存一次
        sub_links = []
        count = 0
        for i in range(1, len(img_links) + 1):
            sub_links.append(img_links.pop().replace('\n', ''))
            if i % 50 == 0:
                count += 1
                print('save..........%d.......%s' % (len(sub_links), str(sub_links)))
                image_urls_count = DownLoad.bing_image_details_url_from_webpage_with_selenium(sub_links)
                sub_links = []
                with open(link_file_path, 'a', encoding='utf-8') as wf:
                    for iu in image_urls_count:
                        wf.write(iu + '\n')
            if i == len(img_links)+1:
                print('save..........%d.......%s' % (len(sub_links), str(sub_links)))
                image_urls_count = DownLoad.bing_image_details_url_from_webpage_with_selenium(sub_links)
                with open(link_file_path, 'a', encoding='utf-8') as wf:
                    for iu in image_urls_count:
                        wf.write(iu + '\n')
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
    # fileNames = [
    #      '脏脏包', '果丹皮','辣炒鱿鱼','羊肉泡馍','美式炒蛋','三文鱼牛油果拌饭','苹果派',
    # ]
    # keywords = ['脏脏包', '果丹皮','辣炒鱿鱼','羊肉泡馍','美式炒蛋','三文鱼牛油果拌饭','苹果派',]
    fileNames = [
         '油炸花生米',
    ]
    keywords = ['油炸花生米', ]
    download_dir = 'D:/pic4-10/xiachu/'
    link_files_dir = 'D:/pic4-10/xiachu/url/'
    log_dir = 'D:/pic4-10/xiachu/logs/'
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
    #1.获取详细页面图片链接
    # google.get_image_links(keywords, link_files_dir, fileNames)
    # 2.获取详细页面下评论网页链接
    # google.get_details_links(keywords, link_files_dir, fileNames)
    # google.get_details_links_from_beifen(keywords, link_files_dir, fileNames)
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
