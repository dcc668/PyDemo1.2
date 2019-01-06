#!  /usr/bin/env python
#ecoding=utf-8
from lxml import html
import requests
import json
from multiprocessing.dummy import Pool

def getContent(url):
    bhtml=requests.get(url).content
    content=html.fromstring(str(bhtml,"utf-8"))
    items=content.xpath('//div[@class="l_post j_l_post l_post_bright  "]')
    print("items:"+str(len(items)))
    for item in items:
        lists=item.xpath("@data-field")
        if len(lists)>0:
            jsons=lists[0]
            dics=json.loads(jsons)  #json--->dic
            userName=dics["author"]["user_name"]
            sex=str(dics["author"]["user_sex"])
            date=dics["content"]["date"]
            #内容
            objs=item.xpath('div[@class="d_post_content_main"]/div/cc/div')
            reps=objs[0].xpath("string(.)")
            print(userName+"---"+sex+"---"+date+"---"+reps)
            line={}
            line["userName"]=userName
            line["sex"]=sex
            line["date"]=date
            line["content"]=reps
            _writeFile(line)
def _writeFile(line):
    file.writelines("时间："+line["date"]+"\n")
    file.writelines("用户："+ line["userName"]+"\n")
    file.writelines("性别："+ line["sex"]+"\n")
    file.writelines("回复："+ line["content"]+"\n")


if __name__=="__main__":
    file = open("D:/baidu.txt",'a')
    urls=[]
    for i in range(1,10):
        url="http://tieba.baidu.com/p/5286628155?pn=%d"%i
        urls.append(url)
    pool=Pool()
    pool.map(getContent,urls)
    pool.close()
    pool.join()
    file.close()