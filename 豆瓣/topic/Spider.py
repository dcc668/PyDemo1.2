# coding=utf-8
import pandas,re,random
import json,requests
import time,traceback
from bs4 import BeautifulSoup
from threading import  Thread

class Spider():
    def __init__(self):
        pass;
    def download_page(self,url,headers):
        print("请求>>>>>>>>>>>>>>>>>>>>url："+url)
        html = requests.get(url, headers=headers,timeout=10).text
        return html
    def download_page_return_response(self,url,headers):
        print("请求>>>>>>>>>>>>>>>>>>>>url："+url)
        return requests.get(url, headers=headers,timeout=10)
    def get_topic(self,category,word):
        url='https://www.douban.com/search?q='+word
        header = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.douban.com/search?q=%E6%96%97%E7%A0%B4%E8%8B%8D%E7%A9%B9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cookie': 'bid=SoBiHhlar8Q; ll="108296"; ps=y; dbcl2="174614892:GF90ovKw+Kw"; ck=8iVS; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1519826123%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DC2x0PH5GAyL88YpYczrEH8mpIDU5OTQGI8d44oBeeaGijWBd59mrDTxItFISG4IT%26wd%3D%26eqid%3Df46ebebf000052c2000000045a93a7c3%22%5D; __utmt_douban=1; __utmt=1; _vwo_uuid_v2=DFF7717729FFC540EBF34EA210F443F6A|9538e9984c82c31180c8f74d23162e95; _pk_id.100001.8cb4=eb706e343404c65b.1516618304.4.1519827044.1519626862.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.413610095.1519273954.1519626183.1519826126.4; __utmb=30149280.24.10.1519826126; __utmc=30149280; __utmz=30149280.1519626183.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.17461; ap=1',
        }
        html=self.download_page(url,header)
        regex='['+category+'].*?<a href="(.*?)"'
        print(regex)
        ptn=re.compile(regex,re.S)
        links=re.findall(ptn,html)
        if len(links)<1:
            print(html)
        details_link=''
        for link in links:
            print(link)
            if link.find('link2')!=-1:
                details_link=link;
                break;
        if details_link!='':
            time.sleep(0.7)
            print('>>>>>>>>>>>>>>>>>>>>获取详细页数据>>>>>>>>>>>>>>>>>>>>>>>')
            print('>>>>>>>>>>>>>>>>>>>>详细页>>>>>>>>>>>>>>>>>>：'+details_link)
            response=self.download_page_return_response(details_link,header)
            html=response.text
            # ['类别','key','产品ID','评分','想看数','看过数','短评数','长评数','链接']
            #'产品ID',
            id=re.split('/',response.url)[-2]
            if '电影'==category or '电视剧'==category:
                # #'评分',
                bs=BeautifulSoup(html,'lxml')
                score_ele=bs.find('strong',attrs={'property':'v:average'})
                score=score_ele.get_text()
                # #'想看数',# #'看过数',
                want_ele=bs.select('div.subject-others-interests-ft')[0].children
                print('=================================================')
                ptn1=re.compile('(.*?)人想看',re.S)
                ptn2=re.compile('(.*?)人看过',re.S)
                ptn3=re.compile('全部 (.*?) 条',re.S)
                for ele in want_ele:
                    want=re.findall(ptn1,ele.string)
                    watch=re.findall(ptn2,ele.string)
                    if len(want)>0:
                         want_count=want[0]
                         print('想看:'+want_count)
                    if len(watch)>0:
                        watch_count=watch[0]
                        print('看过:'+watch_count)
                # #'短评数',
                short=bs.select('div#comments-section div.mod-hd h2 span.pl a')
                if len(short)>0:
                    short_co=re.findall(ptn3,short[0].string)
                    if len(short_co)>0:
                        short_count=short_co[0]
                        print('短评数:'+short_count)
                else:
                    print('！！！！！！！！！！电影 短评数节点为空！！！！！！！！！')
                # #'长评数',
                long=bs.select('header h2 span.pl a')
                if len(long)>0:
                    long_co=re.findall(ptn3,long[0].string)
                    if len(long_co)>0:
                        long_count=long_co[0]
                        print('长评数:'+long_count)
                else:
                    print('！！！！！！！！！！电影 短评数节点为空！！！！！！！！！')
                # #'链接'
                link=response.url
                #['类别','key','产品ID','评分','想看数','看过数','短评数','长评数','链接']
                excel1=[category,word,id,score,want_count,watch_count,short_count,long_count,link]
            if '书籍'==category:
                print('书籍')
                # #'评分',
                bs=BeautifulSoup(html,'lxml')
                score_ele=bs.find('strong',attrs={'property':'v:average'})
                score=score_ele.get_text()
                #'想看数',# #'看过数',
                want_ele=bs.select('div#collector p')
                print('================================================='+str(len(want_ele)))
                ptn1=re.compile('(.*?)人想读',re.S)
                ptn2=re.compile('(.*?)人读过',re.S)
                ptn3=re.compile('全部 (.*?) 条',re.S)
                watch_str=want_ele[1].select('a')[0].string
                want_str=want_ele[2].select('a')[0].string
                want=re.findall(ptn1,want_str)
                watch=re.findall(ptn2,watch_str)
                if len(want)>0:
                    want_count=want[0]
                    print('想读:'+want_count)
                if len(watch)>0:
                    watch_count=watch[0]
                    print('读过:'+watch_count)
                # #'短评数',
                short=bs.select('div.mod-hd h2 span.pl a')
                if len(short)>0:
                    short_co=re.findall(ptn3,short[0].string)
                    if len(short_co)>0:
                        short_count=short_co[0]
                        print('短评数:'+short_count)
                        if int(short_count.strip())>0:
                            short_link=short[0]['href']
                            print('>>>>>>>>>>>>>短评链接>>>>>>>>>>>'+short_link)
                            # 用户昵称	评分星级	评论有用数	评论无用数	评论回应数	评论时间	评论内容	评论链接
                            time.sleep(0.8)
                            short_response=self.download_page_return_response(short_link,header)
                            bf4=BeautifulSoup(short_response.text,'lxml')
                            items=bf4.select('ul li.comment-item div.comment')
                            for item in items:
                                #评论有用数
                                youyong_count=item.select('h3 span.comment-vote span')[0].string
                                print('评论有用数：'+str(youyong_count))
                                #用户昵称
                                nice_name=item.select('h3 span.comment-info a')[0].string
                                print('用户昵称：'+nice_name)
                                #评分星级
                                try:
                                    score=item.select('h3 span.comment-info span')[0].get('title')
                                    print('评分星级:'+score)
                                except Exception as e:
                                    traceback.print_exc()
                                    print("没有评分星级")
                                # 1: "很差",
                                # 2: "较差",
                                # 3: "还行",
                                # 4: "推荐",
                                # 5: "力荐"
                                #评论无用数
                                #评论回应数
                                #评论时间
                                #评论内容
                                #评论链接
                else:
                    print('！！！！！！！！！！电影 短评数节点为空！！！！！！！！！')
                #'长评数',
                long=bs.select('header h2 span.pl a')
                if len(long)>0:
                    long_co=re.findall(ptn3,long[0].string)
                    if len(long_co)>0:
                        long_count=long_co[0]
                        print('长评数:'+long_count)
                else:
                    print('！！！！！！！！！！书籍 短评数节点为空！！！！！！！！！')
                # #'链接'
                link=response.url
                #['类别','key','产品ID','评分','想看数','看过数','短评数','长评数','链接']
                excel1=[category,word,id,score,want_count,watch_count,short_count,long_count,link]

        else:
            with open('log.txt','a') as file:
                file.write(category+'-'+word+"     detail_link  not found")
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>detail_link  not found>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        excel1=[]
        excel2=[]
        time.sleep(1)
        return excel1,excel2

    #存excel
    def to_excel(self,content,path):
        data=pandas.DataFrame(content)
        writer=pandas.ExcelWriter(path)
        data.to_excel(writer)
        writer.save()
    def all_to_excel(self,excels1,excels2,file1,file2):
        self.to_excel(excels1,file1)
        self.to_excel(excels2,file2)
    def process(self,words,file1,file2):
        excels1=[]
        excels2=[]
        for word in words:
            excel1,excel2=spider.get_topic(category,word)
            excels1.append(excel1)
            for ele in excel2:
                excels2.append(ele)
            time.sleep(1)
        # self.all_to_excel(self,excels1,excels2,file1,file2)
    #读取excel
    def read_excel(self,path):
        xls_file=pandas.ExcelFile(path)
        result={}
        for name in xls_file.sheet_names:#显示出读入excel文件中的表名字
            # print('+++++++++++++++++++++++++++++sheet name:'+name+'+++++++++++++++++++++++++++++')
            sheet1=xls_file.parse(name)
            col_name=sheet1.keys()[1]#每一列的第一行为键
            col_vals=[col_name]
            for col_val in sheet1.pop(col_name):
                col_vals.append(col_val)
            print(col_vals)
            result[name]=col_vals;
        return xls_file.sheet_names,result
    #时间搓转换成字符串
    def stamp2time(self,st):
        timeStamp = int(st)
        timeArray = time.localtime(timeStamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

titles1=[['类别','key','产品ID','评分','想看数','看过数','短评数','长评数','链接']]
titles2=[['类别','key','产品ID','用户昵称','评分星级','评论有用数','评论无用数','评论回应数','评论时间','评论内容','评论链接']]
titles3=[['类别','key','产品ID','用户昵称','评分星级','评论有用数','评论无用数','评论回应数','评论时间','评论内容','评论链接','评论标题']]
file1='产品信息.xlsx'
file2='短评采集.xlsx'
file3='长评采集.xlsx'
spider = Spider()
sheet_names,result=spider.read_excel('file/采集频道总表.xlsx')
for category in sheet_names:
    if '书籍'==category:
        print('+++++++++++++++++++++++++++++sheet name:'+category+'+++++++++++++++++++++++++++++')
        words=result[category]
        print('+++++++++++++++++++++++++++++keyword count:'+str(len(words))+'+++++++++++++++++++++++++++++')
        #每爬取一个分类存一次文件
        t=Thread(target=spider.process,args=(words,file1,file2))
        t.start();
        break;

