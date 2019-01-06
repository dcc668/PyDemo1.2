#!  /usr/bin/env python
#ecoding=utf-8

def quickSort(li):
    if len(li)<=0:
        return []
    mid=li[0]
    left=quickSort([x for x in li[1:] if x<mid])
    right=quickSort([y for y in li[1:] if y>=mid])
    return left+[mid]+right

if __name__=="__main__":
    li=[123,44,55,32,2,5,333,66,543,786,99,95]
    soLi=quickSort(li)
    print(soLi)