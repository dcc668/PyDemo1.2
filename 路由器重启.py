import requests
import time
import base64
import re


base_url = 'http://192.168.0.1'
pwd = 'Dcc1234&'#路由器管理密码

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
    'Referer': base_url + '/userRpm/StatusRpm.htm',
    'Cookie': 'Authorization=Basic ' + base64.b64encode(("admin:"+pwd).encode(encoding='utf-8')).decode(encoding='utf-8')
}


def get_ip():
    url = "http://2018.ip138.com/ic.asp"
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    return ip


def get_ip_status():
    url = base_url + "/userRpm/StatusRpm.htm"
    r = requests.get(url=url, headers=headers)
    pattern = re.compile('(\d+\.\d+\.\d+\.\d+)')
    ip = re.findall(pattern, r.text)
    return ip[3]


def change_ip():
    url = base_url + '/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'
    res=requests.get(url=url, headers=headers)
    print(res)
    while True:
        new_ip = get_ip_status()
        if new_ip != '0.0.0.0':
            break
        time.sleep(5)


if __name__ == "__main__":
    change_ip()