#!  /usr/bin/env python
#ecoding=utf-8

def outfunc(func):
    def wrapper():
        print("add ....")
        func()
        print("end ....")
    return wrapper

@outfunc
def mainfunc():
    print("Hi,good afternoon")

mainfunc();

'''
mainfunc=
       def wrapper():
           print("add ....")
           func()
           print("end ....")
'''

#---------------------------------------------------------------------------
'''
单例
'''

def singleton(cls,*args,**kwargs):
    instances={}
    def getInstance():
        if cls not in instances:
            instances[cls]=cls(*args,*kwargs)
            return instances[cls]
    return getInstance

@singleton
class MyClass:
    pass