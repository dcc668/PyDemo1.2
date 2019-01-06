#!  /usr/bin/env python
#ecoding=utf-8

import pandas
import numpy
import jieba
import fasttext

from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.optimizers import RMSprop
from utils.ecoding_utils import EncodingUtils
def group_history2excel_pandas():
    result=[['时间', '内容', '用户', '群名']]
    with open('room_history.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().split('##$##')
            if len(line)>=4:
                roomname = line[0]
                username =  line[1]
                text = line[2]
                msgtime =  line[3]
                result.append([msgtime,text,username,roomname])
            else:
                print('该数据不完整!\n'+str(line))
    #save to excel
    data=pandas.DataFrame(result)
    writer=pandas.ExcelWriter('Result.xlsx')
    data.to_excel(writer)
    writer.save()

#pandas 读取excel
def read_excel(path):
    xls_file=pandas.ExcelFile(path)
    col_valss=[]
    for name in xls_file.sheet_names:#显示出读入excel文件中的表名字
        print('+++++++++++++++++++++++++++++sheet name:'+name+'+++++++++++++++++++++++++++++')
        sheet1=xls_file.parse(name)
        col_names=sheet1.keys()#第一行作为key
        for col_name in col_names:
            col_vals=[]
            for col_val in sheet1.pop(col_name):
                if '测试结果'==col_name.strip():
                    if type(col_val)!=float:
                        col_vals.append('__lable__0')
                    else:
                        col_vals.append('__lable__1')
                else:
                    col_vals.append(col_val)

            col_valss.append(col_vals)
        break;
    col_valss=numpy.reshape(col_valss,(3,-1)).T#列变行
    return col_valss


if __name__=='__main__':
    items=read_excel('2w条数据.xlsx')
    x_data=[]
    y_data=[]
    content=""
    for item in items:
        x_item=''.join(item[:2]);
        seg_list = jieba.cut(x_item)# 默认模式
        line=" ".join(seg_list);
        content=content+line+" "+item[2]+"\n";
    saveDataFile='train_data.txt'
    with open(saveDataFile,'w',encoding='utf-8') as file:
        file.write(content);

    # print("read from excel x length:%d"%len(x_data))
    # print("read from excel y length:%d"%len(y_data))
    # x_train=numpy.reshape(x_data[:18000],(-1,2))
    # y_train=numpy.reshape(y_data[:18000],(-1,1))
    # print(x_train)
    # print(y_train)
    # x_test=x_data[18000:]
    # y_test=y_data[18000:]


# Another way to build your neural net
# model = Sequential([
#     Dense(32, input_dim=2),
#     Activation('relu'),
#     Dense(1),
#     Activation('softmax'),
# ])
#
#
# model.compile(loss='binary_crossentropy',
#               optimizer='rmsprop',
#               metrics=['accuracy'])
# # training
# print('Training -----------')
# for step in range(301):
#     cost = model.train_on_batch(x_train, y_train)
#     if step % 100 == 0:
#         print('train cost: ', cost)
# print('\nTesting ------------')
# # Evaluate the model with the metrics we defined earlier
# loss, accuracy = model.evaluate(x_test, y_test)
#
# print('test loss: ', loss)
# print('test accuracy: ', accuracy)

    #fasttext.supervised():有监督的学习
    classifier=fasttext.supervised(saveDataFile,'classifier.model')
    result = classifier.test(saveDataFile)
    print("P@1:",result.precision)    #准确率
    print("R@2:",result.recall)    #召回率
    print("Number of examples:",result.nexamples)    #预测错的例子


