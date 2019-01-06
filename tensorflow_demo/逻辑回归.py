#!  /usr/bin/env python
#ecoding=utf-8
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as  plt


def add_lay(inputs,in_size,out_size,activation_func=None):
    Weight=tf.Variable(tf.random_normal([in_size,out_size]))
    baises=tf.Variable(tf.zeros([1,out_size])+0.1)
    wei_ba=tf.matmul(inputs,Weight)+baises
    if activation_func==None:
        return  wei_ba
    else:
        return activation_func(wei_ba)

#真实数据
x_data=np.linspace(-1,1,300)[:,np.newaxis]
noise=np.random.normal(0,0.05,x_data.shape)
y_data=np.square(x_data)-0.5+noise
#图像显示真实数据
fig=plt.figure()
sub=fig.add_subplot(1,1,1)
sub.scatter(x_data,y_data)
plt.ion()#block:False
plt.show()

#-----------------------训练-----------------------
#define placeholder for inputs
with tf.name_scope('inputs'):
    x_input=tf.placeholder(tf.float32,[None,1],name='x_input')
    y_input=tf.placeholder(tf.float32,[None,1],name='y_input')
lay=add_lay(x_input,1,10,tf.nn.relu)#add hidden lay
predict=add_lay(lay,10,1)#add output lay
loss= tf.reduce_mean(tf.reduce_sum(np.square(y_input-predict),reduction_indices=[1]))

train=tf.train.GradientDescentOptimizer(0.1).minimize(loss)

#变量初始化
ini=tf.initialize_all_variables()
session=tf.Session()
session.run(ini)

for _ in range(1000):
    session.run(train,feed_dict={x_input:x_data,y_input:y_data})
    if _%20==0:
        res=session.run(loss,feed_dict={x_input:x_data,y_input:y_data})
        while len(sub.lines)>0:
            sub.lines.remove(sub.lines[0])
        predict_val=session.run(predict,feed_dict={x_input:x_data})
        lines=sub.plot(x_data,predict_val,'r-',lw=5)#线宽5
        plt.pause(0.1)
        print(res)