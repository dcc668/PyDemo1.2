#!  /usr/bin/env python
# ecoding=utf-8
import numpy as np
import sys
import re
import os
import cv2
from aip import AipOcr
import shutil
from threading import Thread

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
try:
    from pyocr import pyocr
    from PIL import Image
except ImportError:
    print('模块导入错误,请使用pip安装,pytesseract依赖以下库：')
    print('http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil')
    print('http://code.google.com/p/tesseract-ocr/')
    raise SystemExit


class OCR():
    def __init__(self):
        # baidu api 定义常量
        APP_ID = '10537247'
        APP_ID2 = '10606299'
        API_KEY = 'btKfUNPK4da6E8e2fRFaeQYq'
        API_KEY2 = 'cp4kNQMFqnq7uF8TqL5VuVCj'
        SECRET_KEY = 'ZK4tVualOAXQXgYaAGRvQnQaQv1PZZ4n'
        SECRET_KEY2 = '1P6aqP8ZkSUDY5Sb8kaTpSxOXowsZMZk '

        # baidu api 初始化AipFace对象
        self.aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        # baidu api 定义参数变量
        self.options = {
            'detect_direction': 'true',
            'language_type': 'CHN_ENG',
        }

    def preprocess(self, gray):
        # 1. Sobel算子，x方向求梯度
        sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)

        # x = cv2.Sobel(gray, cv2.CV_8U, 1, 0, ksize=3)
        # y = cv2.Sobel(gray, cv2.CV_8U, 0, 1, ksize=3)
        # sobel = cv2.addWeighted(x, 0.5, y, 0.5, 0)

        # 2. 图像二值化
        ret, binary = cv2.threshold(sobel, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

        # 3. 腐蚀和膨胀的处理 设置结构元素
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (24, 6))
        # 4. 膨胀一次，让轮廓突出
        dilation = cv2.dilate(binary, element2, iterations=1)
        # 5. 腐蚀一次，去掉细节，如表格线等。注意这里去掉的是竖直的线
        erosion = cv2.erode(dilation, element1, iterations=1)
        # 6. 再次膨胀，让轮廓明显一些
        dilation2 = cv2.dilate(erosion, element2, iterations=3)
        # 7. 存储中间图片
        cv2.imwrite("binary.png", binary)
        cv2.imwrite("dilation.png", dilation)
        cv2.imwrite("erosion.png", erosion)
        cv2.imwrite("dilation2.png", dilation2)
        return dilation2

    def findTextRegion(self, img):
        region = []

        # 1. 轮廓检测
        img, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 2. 筛选那些面积小的
        for i in range(len(contours)):
            cnt = contours[i]
            # 计算该轮廓的面积
            area = cv2.contourArea(cnt)

            # 面积小的都筛选掉
            if (area < 1500):
                continue

            # 轮廓近似，作用很小
            epsilon = 0.001 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            # 找到最小的矩形，该矩形可能有方向
            rect = cv2.minAreaRect(cnt)

            # box是四个点的坐标
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            # print(box)

            # 计算高和宽
            height = abs(box[0][1] - box[2][1])
            width = abs(box[0][0] - box[2][0])

            # 筛选那些太细的矩形，留下扁的
            if (height > width * 1.2 or height <= 15):
                continue
            region.append(box)

        return region

    def detect(self, img, im, path):
        try:
            # print('1.  转化成灰度图')
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # print('2. 形态学变换的预处理，得到可以查找矩形的图片')
            dilation = self.preprocess(gray)
            # print('3. 查找和筛选文字区域')
            region = self.findTextRegion(dilation)
            # 4. 用绿线画出这些找到的轮廓
            # a = 0
            # print('5.拼接一个json对象')
            result = []
            for box in region:
                minleft = min(box[0][0], box[1][0], box[2][0], box[3][0])
                mintop = min(box[0][1], box[1][1], box[2][1], box[3][1])
                maxleft = max(box[0][0], box[1][0], box[2][0], box[3][0])
                maxtop = max(box[0][1], box[1][1], box[2][1], box[3][1])
                box1 = (minleft, mintop, maxleft, maxtop)
                if box[0][0] * box[1][1] * box[2][0] * box[0][1] != 0:
                    png = im.crop(box1)
                    res = self.Imgprint(png)
                    if len(res) != 0:
                        a = {}
                        a['name'] = ''.join(res);
                        a['top'] = str(box[1][1]);
                        a['left'] = str(box[1][0]);
                        result.append(a)
                cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
            # 删除有文字的
            if len(result) > 1:
                new_path = ''
                pre_path = ''
                pas = path.split('/');
                for i in range(len(pas)):
                    if i == len(pas) - 1:
                        new_path = new_path + 'delete_file/' + pas[i]
                        pre_path = new_path + 'delete_file/'
                    else:
                        new_path = new_path + pas[i] + '/'
                exist = os.path.exists(pre_path);
                if exist == False:
                    os.makedirs(pre_path)
                cv2.imwrite(new_path, img)
                print('删除有文字的.....' + path)
                os.remove(path)
            else:
                print('没有文字的.....' + path)
        except Exception as e:
            print('该图ocr 识别发生异常' + path + str(e))

    def Imgprint(self, img):
        tools = pyocr.get_available_tools()[:]
        if len(tools) == 0:
            print("No OCR tool found")
            sys.exit(1)
        res = tools[0].image_to_string(img, lang='chi_sim')
        res = re.findall(r"[\u4e00-\u9fa5]", res, re.S)
        return res

    def hasWord(self, filePath):
        try:
            # 调用通用文字识别接口
            result = self.aipOcr.basicGeneral(self.get_content(filePath), self.options)
            all = result['words_result']
            words = []
            has_word = False
            for item in all:
                word = item['words']
                if word:
                    has_word = True
                words.append(word)
            print('识别结果：' + str(words))
        except Exception as e:
            print('识别api---excep:'+str(e))
        return has_word

    def get_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()



            # im = Image.open(path)
            # img = cv2.imread(path)
            # ocr = OCR()
            # ocr.detect(img,im,path)
            # break;
            # t = Thread(target=ocr.detect, args=(img,im,path))
            # threads.append(t)
            #
            # count=0;
            # while count<len(threads):
            #     #一次执行n个线程
            #     n=3
            #     print('一次执行%d个线程---start'%n)
            #     if len(threads)>=n:
            #         for t in range(count,count+n):
            #             threads[t].start()
            #         count=count+n;
            #     else:
            #         for t in range(0, len(threads)):
            #             threads[t].start()
            #         break;
            #     threads[t].join()
            #     print('一次执行三个线程---end')

    def is_img(self, path):
        path = path.lower()
        ext = os.path.splitext(path)[1]
        print('--------->>>>>>type:' + ext)
        if ext == '.jpg':
            return True
        # elif ext == '.png':
        #     return True
        # elif ext == '.jpeg':
        #     return True
        # elif ext == '.bmp':
        #     return True
        else:
            return False

    def deal_with_ocr(self, path):
        print('识别文字。。。。。' + path)
        if ocr.hasWord(path):
            del_file = os.path.join(has_word_dir, list[i])
            print('有文字图片。。。存储中' + del_file)
            shutil.move(path, del_file)
            print('有文字图片。。。删除中' + path)


if __name__ == '__main__':
    rootdir = 'D:/pic4-10/test/'
    rootdir2 = 'D:/pic4-10/test/'
    has_word_dir = rootdir2 + 'delete/has_word/'  # 有文字图片
    small_img_dir = rootdir2 + 'delete/small_img/'  # 小于300图片
    if not os.path.exists(has_word_dir):
        os.makedirs(has_word_dir)
    if not os.path.exists(small_img_dir):
        os.makedirs(small_img_dir)

    listss = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for predir in listss:
        try:
            list = os.listdir(rootdir + predir)  # 列出文件夹下所有的目录与文件
            threads = []
            for i in range(0, len(list)):
                ocr = OCR()
                path = os.path.join(rootdir + predir + '/', list[i])
                if ocr.is_img(path) == True:
                    is_open = False;
                    try:
                        fp = open(path, 'rb')
                        im = Image.open(fp)
                        fp.close()
                        x, y = im.size
                        is_open = True;
                    except Exception as e:
                        fp.close()
                        print('打不开的图片。。。删除中' + path)
                        os.remove(path)
                    if is_open and (x < 300 or y < 300):
                        print('小于300*300图片。。。删除中' + path)
                        file_path=small_img_dir + predir + '/';
                        if not os.path.exists(file_path):
                            os.makedirs(file_path)
                        small_file = file_path+list[i]
                        try:
                            shutil.move(path, small_file)
                        except Exception as e:
                            print('删除失败。。。'+str(file_path)+str(e))
                    elif is_open:
                        pass
                        # t=Thread(target=ocr.deal_with_ocr,args=(path,))
                        # threads.append(t)
                else:
                    if not os.path.isdir(path):
                        print('空白图片。。。删除中' + path)
                        os.remove(path)
        except Exception as e:
            print("不是目录文件。。。")
            continue
        # for th in threads:
        #     th.start()
