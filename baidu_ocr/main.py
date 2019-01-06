#!  /usr/bin/env python
#ecoding=utf-8
from aip import AipOcr
import json

# 定义常量
APP_ID = '10537247'
APP_ID2 = '10606299'

API_KEY = 'btKfUNPK4da6E8e2fRFaeQYq'
API_KEY2 = 'cp4kNQMFqnq7uF8TqL5VuVCj'

SECRET_KEY = 'ZK4tVualOAXQXgYaAGRvQnQaQv1PZZ4n'
SECRET_KEY2 = '1P6aqP8ZkSUDY5Sb8kaTpSxOXowsZMZk '

# 初始化AipFace对象
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
filePath = "image/3.jpg"
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
        # 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

# 调用通用文字识别接口
result = aipOcr.basicGeneral(get_file_content(filePath), options)
num=result['words_result_num']
all=result['words_result']
words=''
for item in all:
    word=item['words']
    words=words+word+'\n'
print(words)