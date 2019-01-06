#!  /usr/bin/env python
#ecoding=utf-8
#yield  迭代器，迭代的时候才执行（类似懒加载）

def alexReadLine():
    while True:
        seek=0  #开始位置
        with open("D:/baidu.txt","r") as file: #自动关闭
            file.seek(seek) #调到开始读取位置
            data=file.readline()
            if data:
                seek=file.tell() #已经读取的位置
                yield data  #返回读取的一行，下次遍历时继续循环
            else:
                return

if __name__=="__main__":
    i=0
    for line in alexReadLine():
        print("------"+str(i)+"-------")
        i=i+1
        print(line)

