#!  /usr/bin/env python
#ecoding=utf-8
import requests
import chardet
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
    'Cookie':'login_sid_t=cff0772f23d4e36463b4143f23d6196b; _s_tentry=www.google.co.jp; Apache=1124296278023.551.1505877017253; SINAGLOBAL=1124296278023.551.1505877017253; ULV=1505877017261:1:1:1:1124296278023.551.1505877017253:; cross_origin_proto=SSL; crossidccode=CODE-gz-1DUzYz-28JwTf-VusLs6zTBi7JFlOe7285d; SSOLoginState=1505894613; SUB=_2A250xlCFDeThGeNL71cY8ifIzzSIHXVXssVNrDV8PUNbmtBeLWf-kW8TWPRxsmR0QL7Z_tF3mlg8IhzNsg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-N7N1zLYZaUg_e_UmziNJ5JpX5KzhUgL.Fo-fSh-4eo.XShn2dJLoI7y2BXec1hBR15tt; SUHB=0KAhVNzENTWEf7; ALF=1537430612; wvr=6; UOR=www.csto.com,widget.weibo.com,graph.qq.com'
};
url="https://weibo.com/u/5545929448/home?wvr=5&sudaref=graph.qq.com"
html=requests.get(url,headers=headers).content #type(html)  : bytes
print(html)
json=chardet.detect(html);
print(json)
print(json["encoding"])
if "gb2312"==json["encoding"]:
    bhtml=html.decode("gb2312").encode("utf-8")    #gb2312--->utf-8

elif "utf-8"==json["encoding"]:
    htmlStr = str(html, "utf-8")  # toString
    print(htmlStr)
else:
    print("不可处理编码！！")
