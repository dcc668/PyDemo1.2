#!  /usr/bin/env python
# ecoding=utf-8
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from requests import Session
from selenium import webdriver
from selenium.webdriver import Chrome, PhantomJS
import time, json, random, os, re, urllib
from settings import AGENTS
from threading import Thread
import requests

class Download():
    def __init__(self,pre_index_css_urls):
        self.pre_index_css_urls=pre_index_css_urls
        self.regex='url\(\'?(.*?)\'?\)'
    def download_scripy(self, src, file_path, tag):
        headers = {}
        ua = random.choice(AGENTS)
        headers['User-Agent'] = ua
        print('\n{0}\n{1}'.format(src.strip(), ua))
        try:
            req_obj = requests.get(src.strip(), headers=headers)
        except Exception:
            print('retry..............'+str(src))
            time.sleep(2)
            req_obj = requests.get(src.strip(), headers=headers)
        time.sleep(1.2)
        if tag == 'link':
            data = req_obj.text
            urls = re.findall(self.regex, str(data), re.S)
            print('-------------tag==link-------------src---' + str(src))
            print('-------------tag==link-------------urls---' + str(urls))
            for url in urls:
                count = 1
                orga_url = url
                while orga_url.find('..') != -1:
                    orga_url = orga_url.replace('..', '')
                    count += 1
                srcs = src.strip().split('//')
                print('-------------tag==link-------------srcs---' + str(srcs))
                if len(srcs) == 2:
                    if orga_url.find("http")!=-1:
                        bg_url = orga_url
                    else:
                        srcss = srcs[1].split('/')
                        bg_url = srcs[0] + '//'
                        for k in range(len(srcss)-count):
                            if srcss[k]!='':
                                bg_url = bg_url + srcss[k] + "/"
                        if orga_url.startswith('/'):
                            orga_url=orga_url.replace('/','',1)
                        bg_url = bg_url + orga_url
                    print('-------------------after  bg_url2:' + bg_url)
                    local_url = self.pre_index_css_urls + orga_url.split('/')[-1]
                    self.download_scripy(bg_url, local_url, tag='xxx')
                    data = data.replace(url, local_url)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(data)
        else:
            try:
                with open(file_path, 'wb') as file:
                    file.write(req_obj.content)
            except Exception as e:
                print(str(e))

class Html2Local():
    def __init__(self,host_url,pre_index_path):
        self.base_url = host_url
        self.tomJsDriver = r'driver/phantomjs.exe';
        self.chromeDriver = r'driver/chromedriver.exe'
        self.session = Session()
        self.session.headers.clear()
        # self.chrome=self.tomjs_init();
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        option.add_argument('disable-infobars')
        self.chrome=Chrome(executable_path=self.chromeDriver,chrome_options=option,)
        self.pre_index_path = pre_index_path
        self.pre_index_script = pre_index_path+'/script/'
        self.pre_index_css = pre_index_path+'/css/'
        self.pre_index_img = pre_index_path+'/img/'
        self.pre_index_css_urls =pre_index_path+ '/css_urls/'
        if not os.path.exists(self.pre_index_path):
            os.makedirs(self.pre_index_path)
        if not os.path.exists(self.pre_index_script):
            os.makedirs(self.pre_index_script)
        if not os.path.exists(self.pre_index_css):
            os.makedirs(self.pre_index_css)
        if not os.path.exists(self.pre_index_img):
            os.makedirs(self.pre_index_img)
        if not os.path.exists(self.pre_index_css_urls):
            os.makedirs(self.pre_index_css_urls)

    def has_endswith(self,url):
        str=url.strip().lower()
        if str.endswith('.js'):
            return '.js'
        elif str.endswith('.css'):
            return '.css'
        elif str.endswith('.png'):
            return '.png'
        elif str.endswith('.jpg'):
            return '.jpg'
        elif str.endswith('.jpeg'):
            return '.jpeg'
        elif str.endswith('.ico'):
            return '.ico'
        else:
            return False
        # 工具方法
    # tomjs初始化
    def tomjs_init(self):
        # 引入配置对象DesiredCapabilities
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器
        agent=random.choice(AGENTS);
        dcap["phantomjs.page.settings.userAgent"] =agent
        dcap["phantomjs.page.customHeaders.User-Agent"] = agent
        # 不载入图片，爬页面速度会快很多
        dcap["phantomjs.page.settings.loadImages"] = True
        # #打开带配置信息的phantomJS浏览器
        tomJs = PhantomJS(self.tomJsDriver, desired_capabilities=dcap)
        # 隐式等待5秒，可以自己调节
        tomJs.implicitly_wait(2)
        # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项
        # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。
        tomJs.set_page_load_timeout(10)
        # 设置10秒脚本超时时间
        tomJs.set_script_timeout(10)
        return tomJs
    def get_pre(self,tag,file_name):
        if tag=='script':
            return self.pre_index_script+file_name
        elif tag=='link':
            return self.pre_index_css+file_name
        elif tag=='img':
            return self.pre_index_img+file_name
    def save_url(self,content,tag,attr,endswith):
        scripys =  self.chrome.find_elements_by_tag_name(tag)
        count = 0;
        srcss=[]
        thread_args=[]
        for script in scripys:
            if script != None and script != '':
                src = script.get_attribute(attr)
                print(src)
                if src not in srcss:
                    srcss.append(src)
                    if src!=None and src.strip() != '':
                        if self.has_endswith(src)!=False:
                            file_name = str(count) + self.has_endswith(src);
                        else:
                            file_name = str(count) +endswith
                        count += 1
                        if content.find(src)!=-1:#带有域名的url
                            content=content.replace(src,self.get_pre(tag,file_name))
                        else:
                            print('domains路径下ｕｒｌ not found：'+src)
                            sub_url=src.split(self.base_url.split('//')[1])
                            print('项目路径下ｕｒｌ：'+str(sub_url))
                            if len(sub_url)>1:
                                substr=sub_url[1]
                                content=content.replace(substr,self.get_pre(tag,file_name))
                        thread_args.append((src, self.get_pre(tag,file_name),tag))

        threads = []
        for args in thread_args:
            download=Download(self.pre_index_css_urls)
            t = Thread(target=download.download_scripy, args=args)
            threads.append(t)
        for t in threads:
            t.start()
        return content
    def html2local(self, file_name):
        self.chrome.get(self.base_url)
        content=str( self.chrome.page_source)
        content=self.save_url(content,'script','src','.js')
        content=self.save_url(content,'link','href','.css')
        content=self.save_url(content,'img','src','.png')
        with open(self.pre_index_path+file_name,'w',encoding='utf-8') as file:
            file.write(content)


if __name__ == '__main__':
#     # h2l = Html2Local("https://www.baidu.com/")
    h2l = Html2Local("http://www.wtu.edu.cn",'D:/wtu')
    h2l.html2local('/index.html')
    print('finish...')
