from keras.preprocessing.image import ImageDataGenerator
import os,shutil


def generage_imgs(sub_path):
    PATH='class2/'+sub_path
    SAVE_PATH='class2/'+sub_path
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    img_width, img_height = 60, 30
    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,#对图片的每个像素值均乘上这个放缩因子
        shear_range=0.2,#错切变换
        zca_whitening=True,
        zoom_range=0.1,#在长或宽的方向进行放大(0-1，放大，>1，缩小)
        horizontal_flip=False)#随机对图片执行水平翻转操作
    # this is the augmentation configuration we will use for testing:
    # only rescaling
    train_generator = train_datagen.flow_from_directory(
        PATH,
        target_size=(img_width, img_height),
        batch_size=100,
        save_to_dir=SAVE_PATH,
        save_prefix='gen',
        color_mode='grayscale',
        class_mode='categorical')
    return train_generator
def move1():
    # #移动子目录
    for sub_path in mapList:
        path='class2/'+sub_path+'/'+(sub_path+sub_path)
        path2='class2/'+sub_path
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path2):
            os.makedirs(path2)
        for file in os.listdir(path2):
            file=path2+'/'+file
            if os.path.isfile(file):
                shutil.move(file,path)
def move2():
    #移动子目录
    for sub_path in mapList:
        path='class2/'+sub_path+'/'+(sub_path+sub_path)
        path2='class2/'+sub_path
        path3='class4/'+sub_path
        if not os.path.exists(path3):
            os.makedirs(path3)
        for file in os.listdir(path):
            file=path+'/'+file
            if os.path.isfile(file):
                shutil.move(file,path3)
        for file in os.listdir(path2):
            file=path2+'/'+file
            shutil.move(file,path3)
        #删除空目录
        for file in os.listdir(path3):
            file=path3+'/'+file
            if os.path.isdir(file):
                os.rmdir(file) #只能删除空目录

mapList = ['3','5','6','7','8','9','A','B','D','E','F','G','H','J','K','M','N','P','R','S','T','U','V','X','Y']
move1()
# 生成9张图
for sub_path in mapList:
    print('generate:'+sub_path)
    train_generator=generage_imgs(sub_path)
    for i in range(5):
        train_generator.next()
move2()





