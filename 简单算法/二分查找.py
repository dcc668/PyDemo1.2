#!  /usr/bin/env python
#ecoding=utf-8

def binarySearch(li,key):
    left,right=0,len(li)-1
    while left<=right:
        mid=(left+right)//2
        if key<li[mid]:
            right=mid-1
        elif key==li[mid]:
            return True
        else:
            left=mid+1
    return False

if __name__=="__main__":
    li=[2,4,5,6,76,77,87,89,342,432,444,555,666]
    res=binarySearch(li,444)
    print(res)


