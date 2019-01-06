#!  /usr/bin/env python
#ecoding=utf-８
from queue import Queue
from threading import Thread
import random

qu=Queue(100)
class Product(Thread):
    def run(self):
        while True:
            prod=1;
            qu.put(prod)
            msg="生产者{}生产,库存{}".format(self.name,qu.qsize())
            print(msg)
class Consumer(Thread):
    def run(self):
        while True:
            res=qu.get()
            msg="消费者{}消费,库存{}".format(self.name,qu.qsize())
            print(msg)


if __name__=='__main__':
    for i in range(3):
        pro=Product()
        pro.start()
    for i in range(2):
        pro=Consumer()
        pro.start()
