# -*- coding: utf-8 -*-

import pymysql.cursors
import time
from sshtunnel import SSHTunnelForwarder

class Data2MySql():
    # Connect to the MySQL database
    def __init__(self):
        self.server= SSHTunnelForwarder(
            ('39.108.122.83', 22),
            ssh_password="Dcc1234&",
            ssh_username="root",
            remote_bind_address=('172.18.150.104', 3306))
        self.server.start()  # start ssh sever
        local_port = self.server.local_bind_port
        #连接配置信息
        config = {
            'host': '127.0.0.1',
            'port': local_port,
            'user': 'cc',
            'password': '1234',
            'db': 'mydb',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        # 创建连接
        self.connection = pymysql.connect(**config)
        self.cursor= self.connection.cursor()
        # 创建数据表zhilian
        self.clean_table()

    # 创建数据表创建数据表zhilian_job_details_contents
    def clean_table(self):
        clean_sql = "truncate table t_ips;"
        self.cursor.execute(clean_sql)
        self.connection.commit()
        print('t_ips 表已经清空！')
    def process_item(self, ips):
        for ip in ips:
            # 将信息插入到数据库中
            args = (
                ip,
                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                1
            )
            newsSqlText = "insert into t_ips(" \
                          "ips,create_time," \
                          "orderBy)values(" \
                          "%s,%s,%s)"
            print(newsSqlText)
            self.cursor.execute(newsSqlText,args)
            print('执行sql  完成！')
            self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        self.server.stop()


