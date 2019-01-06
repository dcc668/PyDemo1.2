#!  /usr/bin/env pytreon
#ecoding=utf
import pymysql

class DBUtils:
    @staticmethod
    def getConn():
        return pymysql.Connect(host='211.152.47.69',
                               port=3306,
                               user='new_root',
                               passwd='@Hyipsos',
                               db='task_center',
                               charset='utf8'
                               )
