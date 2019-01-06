#!  /usr/bin/env python
#ecoding=utf-8
import re

if __name__=="__main__":
    strs='';
    with open('cc.txt', 'r',encoding='UTF-8') as file:
        lines=file.readlines();

    for line in lines:
        strs+=line
    # insert[\s]{1,}into(.|\\n|\s){3,50}\([^)]{1,11500}
    pattern = "insert[\t\n\v\f\r ]{1,}into([^\n\r\x85\u2028\u2029]|\\n|[\t\n\v\f\r ]){3,50}\([^)]{1,11500}";
    res=re.finditer(pattern, strs, flags=0)
    for it in res:
        print('------>>>res:'+str(it.group()))