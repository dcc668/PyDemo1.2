import requests
from urllib.parse import urlencode
from requests import RequestException
import json
import chardet


def get_page(url):
    try:
        response=requests.get(url)
        html=response.text
    except RequestException as e:
        print(e)
    return json.loads(html)
def get_img_links(offset,keyword):
    #图片信息
    url='https://www.toutiao.com/search_content?'
    params={
        'offset':offset,
        'format':'json',
        'keyword':keyword,
        'autoload':True,
        'count':20,
        'cur_tab':1,
        'from':'search_tab',
    }
    url=url+urlencode(params)
    data=get_page(url)
    print(data['data'])
    for item in data['data']:
        if 'image_url' in item.keys():
            yield 'http:'+item['image_url']
if __name__=='__main__':
    for link in get_img_links(0,'苹果'):
        print(link)