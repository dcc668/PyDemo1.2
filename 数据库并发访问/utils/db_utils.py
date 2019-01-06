#!  /usr/bin/env pytreon
#ecoding=utf
import pymysql
import PyQt5.QtSql as sql

class DBUtils:
    @staticmethod
    def getConn():
        return pymysql.Connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               passwd='1234',
                               db='test',
                               charset='utf8'
                               )

    @staticmethod
    def getConn2():
        db = sql.QSqlDatabase.addDatabase('QMYSQL')
        db.setDatabaseName('test')
        db.setUserName('root')
        db.setPassword('1234')
        db.open()
        return db;