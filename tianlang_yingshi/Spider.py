#!  /usr/bin/env python
#ecoding=utf-8
from utils.http_utils import HttpUtils
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TianLang():
    def __init__(self):
        self.index_href='http://www.tlyy.tv/dy';
        self.index_header = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN, zh;q=0.9',
            'Cookie':'ASPSESSIONIDSSRQCCDD=IGDJPNHCPEGHKKAPOAGBAJEP; ASPSESSIONIDSSTSCDCC=NAEDBOHCDPIKCCMDEOLMAPMC; ASPSESSIONIDSSTRDDDC=GJDJPNHCOALEFONGIOHBNIHF; MAX_HISTORY={video:[{"name":"北海食神","link":"http://www.tlyy.tv/dy/dy2/beihaishishen/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/20191251614941288.jpg"},{"name":"极线杀手","link":"http://www.tlyy.tv/dy/dy1/jixianshashou/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/201912018543495353.jpg"},{"name":"大侦探霍桑","link":"http://www.tlyy.tv/dy/dy5/dazhentanhuosang/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/2019126956181452.jpg"},{"name":"唐伯虎点秋香2019","link":"http://www.tlyy.tv/dy/dy2/tangbohudianqiuxiang2019/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/201912515574423544.jpg"},{"name":"宝塔镇河妖2绝世妖龙","link":"http://www.tlyy.tv/dy/dy6/baotazhenheyao2jueshiyaolong/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/201912216332031157.jpg"},{"name":"大人物2019","link":"http://www.tlyy.tv/dy/dy1/darenwu2019/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/2019152313783687.jpg"},{"name":"贼王2019","link":"http://www.tlyy.tv/dy/dy1/zeiwang2019/","pic":"http://pic.jxncpw.cn/uploadimg/2019-1/201912110281691828.jpg"}]}'
        }
    def index(self):
        httpU=HttpUtils();
        response=httpU.get(self.index_href,self.index_header);
        if(response is not None and response.status_code==200):
            html=response.text;
            print(html)

#88影视网
#https://www.88ys.cn/vod-play-id-53326-src-1-num-3.html
class YingShiWang():
    def __init__(self):
        self.host='https://www.88ys.cn/'
    def getXmlUrl(self):
        url=self.host+'vod-play-id-53326-src-1-num-1.html'
        httpUitls=HttpUtils();
        chrome=httpUitls.chrome_init();
        chrome.get(url)
        wait=WebDriverWait(chrome, 10, 0.5)
        # flash_url="http://www.macromedia.com/go/getflashplayer"
        # chrome.get(flash_url)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="a1"]/a')))
            ele=chrome.find_element_by_xpath('//*[@id="a1"]/a')
            ele.click();
        except Exception as e:
            print("点击flash插件异常！",e)
        print(chrome.page_source)

if __name__=='__main__':
    yingShi=YingShiWang();
    yingShi.getXmlUrl();