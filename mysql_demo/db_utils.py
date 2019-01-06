#!  /usr/bin/env pytreon
#ecoding=utf
import pymysql

class DBUtils:
    @staticmethod
    def getConn():
        return pymysql.Connect(host='rds29oh57jzmb8qv9ry4.mysql.rds.aliyuncs.com',
                               port=3306,
                               user='ebin',
                               passwd='hcr123',
                               db='hcj',
                               charset='utf8'
                               )
