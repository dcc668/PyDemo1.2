#! /usr/bin/python
from threading import Thread
import time

def my_counter():
    print("--------->>time:"+str(time.time()))
    i = 0
    for _ in range(1000000000):
        i = i + 1
    return True
def main():
    start_time = time.time()
    for tid in range(2):
        t = Thread(target=my_counter)
        t.start()
    t.join()#join的作用是保证当前线程执行完成后，再执行其它线程。
    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))
if __name__ == '__main__':
    main()

# --------->>time:1506676940.6625316
# --------->>time:1506676940.6675317    同时运行，--多线程
# Total time: 186.60267305374146

# --------->>time:1506677496.7693388
# --------->>time:1506677573.5737321〉 分别运行，--〉单线程
# Total time: 151.4936649799347

#结论：
#threadingcpu密集型 多线程慢
