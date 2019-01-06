from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential,load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense


img_width, img_height = 60, 30
batch_size=32 #每次将batch_size的数据通过PCI总线传到GPU，然后进行预测。
epochs=150  #total number of iterations on the data.
steps_per_epoch= 400    #当生成器返回steps_per_epoch次数据时计一个epoch结束，执行下一个epoch
validation_steps = 200

def CNN(trainDir, validationDir, classNum):
    model = Sequential()
    # layer    60*30
    model.add(Conv2D(4, (3, 3), input_shape=(img_width, img_height, 1))) #filter个数为4个，filter大小3*3，
    model.add(Activation('relu'))
    # layer2   30*15
    model.add(Conv2D(4, (3, 3)))#卷积层,(输出高度,卷积核的大小,strides)
    model.add(Activation('relu'))#激励层
    model.add(MaxPooling2D(pool_size=(2, 2)))#池化层
    # layer3   30*15
    model.add(Conv2D(8, (3, 3)))
    model.add(Activation('relu'))
    # layer4    15*7=106
    model.add(Conv2D(8, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    # model.add(Conv2D(16, 3, 3))
    # model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())#Flatten层用来将输入“压平”，即把多维的输入一维化，常用在从卷积层到全连接层的过渡。Flatten不影响batch的大小。
    model.add(Dense(64))#对上一层的神经元进行全部连接，实现特征的非线性组合,     64:输出高度
    model.add(Activation('relu'))
    # model.add(Dropout(0.5))# 在每次训练的时候，每个神经元有百分之50的几率被移除，这样可以让一个神经元的出现不应该依赖于另外一个神经元
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dropout(0.6))
    model.add(Dense(classNum))
    model.add(Activation('softmax'))#分成16类
    # test
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    # this is the augmentation configuration we will use for training
    train_datagen = ImageDataGenerator(
            rescale=1./255,#对图片的每个像素值均乘上这个放缩因子
            shear_range=0.2,#错切变换
            zca_whitening=True,
            zoom_range=0.2,#在长或宽的方向进行放大(0-1，放大，>1，缩小)
            horizontal_flip=False)#随机对图片执行水平翻转操作
    # this is the augmentation configuration we will use for testing:
    # only rescaling
    test_datagen = ImageDataGenerator(rescale=1./255, zca_whitening=True)
    train_generator = train_datagen.flow_from_directory(
            trainDir,
            target_size=(img_width, img_height),
            batch_size=100,
            color_mode='grayscale',
            class_mode='categorical')
    validation_generator = test_datagen.flow_from_directory(
            validationDir,
            target_size=(img_width, img_height),
            batch_size=batch_size,
            color_mode='grayscale',
            class_mode='categorical')
    #从节省内存的角度，通过生成器的方式来训练
    model.fit_generator(
        train_generator,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_steps)
    return model

if __name__ == '__main__':
    train_data_dir='train'
    validation_data_dir='train'
    train_class='class3'
    validation_class='class'
    # cropModel = CNN(train_data_dir, validation_data_dir, 2)
    # cropModel.save_weights('temp/cropWeights2.h5')
    # cropModel.save('temp/cropModel2.h5')
    classModel = CNN(train_class, validation_class, 25)
    classModel.save_weights('temp/classWeights2.h5')
    classModel.save('temp/classModel2.h5')