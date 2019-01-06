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

import os, random,re
import json,requests
import time,requests
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


class DownLoad():

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
        with open(link_file_path, 'r',encoding='utf-8') as rf:
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
    def bing_gen_query_url(keywords, face_only=False):
        query_url = "https://image.baidu.com/search/index?ct=201326592&cl=2" \
                    "&st=-1&lm=-1&nc=1&ie=utf-8&tn=baiduimage&ipn=r&rps=1&pv=&fm=rs6" \
                    "&word=%s&oriquery=%s&ofr=%s&sensitive=0"\
                    %(keywords,keywords,keywords,)
        return query_url

    @staticmethod
    def bing_image_url_from_webpage(driver):
        image_urls = list()
        time.sleep(3)       # default 10
        img_count = 0
        retry_count=0
        while True:
            regex=r'<a href="(.*?)"(.|\\n|\s)[^>]{1,2500}><img(.|\\n|\s){1,3}class="main_img img-hover"'
            image_elements=re.findall(regex,driver.page_source,re.S)
            print('------------------>>>>>image_elements:'+str(len(image_elements)))
            # image_elements = driver.find_elements_by_class_name("iusc")
            if len(image_elements) > img_count:
                img_count = len(image_elements)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
            else:
                retry_count+=1
                if retry_count>=10:#重试
                    break
                else:
                    print('重试.....')
                    continue
            time.sleep(2)#default 3
        for image_element in image_elements:
            print('------------------>>>>>image_element:' + str(image_element))
            image_urls.append(image_element)
        return image_urls
    @staticmethod
    def down_page(url):
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                   # 'Cookie': PHOTO_COOKIE
                   }
        html = requests.get(url,headers=headers).text
        return html

class Google():
    def __init__(self):
        chromePath = r'J:\lib\driver\chromedriver.exe'
        os.environ["webdriver.chrome.driver"] = chromePath
        chrome_options = webdriver.ChromeOptions()
        user_data = r"C:\Users\Administrator\AppData\Local\Google\Chrome\User Data"
        chrome_options.add_argument(
            "user-data-dir=" + os.path.abspath(user_data))
        self.driver = webdriver.Chrome(executable_path=chromePath,
                                       chrome_options=chrome_options)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        self.driver.maximize_window()

    def get_image_links(self, main_keywords, pre_link_path, fileNames, num_requested=4000):
        """get image links with selenium

        Args:
            main_keyword (str): main keyword
            supplemented_keywords (list[str]): list of supplemented keywords
            link_file_path (str): path of the file to store the links
            num_requested (int, optional): maximum number of images to download

        Returns:
            None
        """
        number_of_scrolls = int(num_requested / 400) + 1
        # number_of_scrolls * 400 images will be opened in the browser
        for i in range(len(main_keywords)):
            search_query = main_keywords[i]
            link_file_path = pre_link_path + fileNames[i] + ".txt"
            url = DownLoad.bing_gen_query_url(search_query)
            self.driver.get(url)
            image_urls=DownLoad.bing_image_url_from_webpage(self.driver)
            print('KeyWords {0} , got {1} image urls so far'.format(main_keywords[i], len(image_urls)))
            with open(link_file_path, 'a',encoding='utf-8') as wf:
                for url in image_urls:
                    if len(re.findall('^/search(.*?)',url[0],re.S))!=0:
                        img_url='https://image.baidu.com'+str(url[0])
                        img_url=img_url.replace('amp;','')
                        html2 = DownLoad.down_page(img_url)
                        url2 = re.findall(r'class="currentImg"(.|\n|\s){1,235}src="(.*?)"', html2, re.S)
                        print('---------------img url:' + str(url2[0][1]))
                        wf.write(url2[0][1] + '\n')
            print('Store all the links in file {0}'.format(link_file_path))


if __name__ == "__main__":
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
    # main_keywords = ['奶酪玉米片','盖饭', '馅饼', '胡辣汤', '炒海参', '木耳炒肉',
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
    #     '炒花生米',
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
    #     "银耳羹"
    # ]
    # main_keywords = ['银耳羹']

    # fileNames = [
    #     "重庆火锅","酸辣土豆丝",
    #     "基辅炸鸡",'龙井虾仁','脏脏包','梅菜扣肉'
    # ]
    # keywords = ["重庆火锅","酸辣土豆丝",'鸡肉排','龙井虾仁','脏脏包','梅菜扣肉']
    fileNames = [
       '牛油果盖饭',

    ]
    keywords = ['牛油果盖饭',]


    download_dir = 'D:/pic4-10/baidu_test/'
    link_files_dir = 'D:/pic4-10/baidu_test/url/'
    log_dir = 'D:/pic4-10/bing/logs/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(link_files_dir):
        os.makedirs(link_files_dir)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # fileNames1=['']
    # main_keywords1=['果脯蜜饯']
    # supplemented_keywords1=['果脯蜜饯']
    ###################################
    # get image links and store in file
    ###################################

    # single process
    google = Google()
    google.get_image_links(keywords, link_files_dir, fileNames)



    ###################################
    # download images with link file
    ##################################
    #
    # # multiple process
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    threads = []
    for i in range(len(fileNames)):
        link_file_path = link_files_dir + fileNames[i]+'.txt'
        #下载路径
        download_file_path = download_dir + fileNames[i]+'/'
        if os.path.exists(download_file_path)==False:
            os.makedirs(download_file_path)
        with open(link_file_path,'r',encoding='utf-8') as file:
            lines=file.readlines()
        per_t=20# num of link per thread
        for j in range(len(lines)):
            if j%per_t==1 and j!=(len(lines)/per_t)*per_t+1:#not last
                t = Thread(target=DownLoad.download_images,
                        args=(j,j+per_t,link_file_path, download_file_path,log_dir,fileNames[i]))
                t.start()
            elif j%per_t==1 and j==(len(lines)/per_t)*per_t+1:
                t = Thread(target=DownLoad.download_images,
                        args=(j, len(lines), link_file_path, download_file_path, log_dir, fileNames[i]))
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
