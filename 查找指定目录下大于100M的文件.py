import os;
from os.path import getsize

def getFiles(dirs):
    for root, current_dirs, files in os.walk(dirs):
        print("current_dirs:"+str(current_dirs))
        if(root[len(root)-1]!="/"):continue;
        if(len(current_dirs)<=0 or current_dirs[0][0]=='_'):
            continue;
        print(root+"  files:"+str(len(files)))
        for name in files:
            if name[0]=='.':continue;
            file=root+name;
            size=getsize(file);
            if size>=100*1024:#记录大于100M的文件
                with open("C://max_files.txt",'a',encoding="utf-8",) as fle:
                    fle.write(str(file)+"  size:"+str(size)+"\n")
        for dir in current_dirs:
            temp=dir[0];
            if dir[0]=='.' or  temp=='_':continue;
            getFiles(dirs+dir+"/")



if __name__=='__main__':
    getFiles("./");