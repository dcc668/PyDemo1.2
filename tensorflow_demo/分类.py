#!  /usr/bin/env python
#ecoding=utf-8
import tensorflow as tf
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

def add_lay(inputs,in_size,out_size,activation_func=None):
    #因为我们要学习 W 和 b 的值，它们的初值可以随意设置
    Weight=tf.Variable(tf.random_normal([in_size,out_size]))
    baises=tf.Variable(tf.zeros([1,out_size])+0.1)
    wei_ba=tf.matmul(inputs,Weight)+baises
    if activation_func==None:
        return  wei_ba
    else:
        return activation_func(wei_ba)
#评估 模型数据（计算准确度）
def computer_accuracy(x_data,y_data):
    global prediction
    y_prediction_val=session.run(prediction,feed_dict={x_input:x_data})
    # 预测是否=真实
    correct_prediction = tf.equal(tf.argmax(y_data,1), tf.argmax(y_prediction_val,1))
    #计算所学习到的模型在测试数据集上面的正确率
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result=session.run(accuracy, feed_dict={x_input: mnist.test.images, y_input: mnist.test.labels})
    return result
#-----------------------训练-----------------------
#define placeholder for inputs
with tf.name_scope('inputs'):
    x_input=tf.placeholder(tf.float32,[None,784],name='x_input')
    y_input=tf.placeholder(tf.float32,[None,10],name='y_input')
#add output layer
prediction=add_lay(x_input,784,10,tf.nn.softmax)#add hidden lay
#the error between predict and real,
cross_entropy= tf.reduce_mean(
        -tf.reduce_sum(
            y_input*tf.log(prediction),reduction_indices=[1]))

train=tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

#变量初始化
ini=tf.initialize_all_variables()
session=tf.Session()
session.run(ini)

for i in range(1000):
    x_data, y_data = mnist.train.next_batch(100)
    res = session.run(train, feed_dict={x_input: x_data, y_input: y_data})
    if i%20==0:
        print(computer_accuracy(
            mnist.test.images, mnist.test.labels))