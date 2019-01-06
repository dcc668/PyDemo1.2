# coding=utf-8
import os
from 图片爬取.nowatermark.no_water_mark.WatermarkRemover import WatermarkRemover
path = '../data/'

# watermark_template_filename = path + 'anjuke-watermark-template.jpg'
watermark_template_filename = path + 'template.jpg'
remover = WatermarkRemover()
remover.load_watermark_template(watermark_template_filename)

files_path='D:/pic4-10/meishi/xiaoji/'
new_files_path='D:/pic4-10/meishi_new/xiaoji/'
if not os.path.exists(new_files_path):
    os.makedirs(new_files_path)
files=os.listdir(files_path)
for file in files:
    print('去水印．．．'+files_path + str(file))
    try:
        remover.remove_watermark(files_path + str(file), new_files_path + str(file))
    except Exception as e:
        print("发生异常..."+str(e)+str(file))
