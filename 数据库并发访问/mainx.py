#!  /usr/bin/env python
#ecoding=utf-8
from pymysql import Connection, cursors

from 数据库并发访问.user_eo import UserEO
from 数据库并发访问.utils.db_utils import DBUtils
from 数据库并发访问.utils.dict2obj_utils import Dict2Obj
import time;

class BaseDao:
    conn:Connection;
    def __init__(self):
        self.conn =DBUtils.getConn();
        # 关闭自动commit
        self.conn.autocommit(False)

    def findById(self,id):
        #return dict
        cursor = self.conn.cursor(cursor=cursors.DictCursor)
        sql = "select a.* from users a where a.id="+str(id)
        cursor.execute(sql)
        rs = cursor.fetchone()
        # print('------findById------>>>>return dict '+str(rs));
        user=Dict2Obj(rs);
        cursor.close();
        return user;

    #乐观锁
    def updateUserNoLock(self, user):
        try:
            cursor = self.conn.cursor(cursor=cursors.DictCursor)
            newVal=user.status+1;
            sql = "select status from users where id = %d;" \
                  "update users set status = %d" \
                  ",userName = '%s'" \
                  ",password = '%s'" \
                  ",email = '%s'," \
                  "money=%d," \
                  "status=%d where id=%d and status=%d;" \
                  % (
                  user.id, user.status, user.userName, user.password, user.email, user.money, newVal, user.id,
                  user.status)
            res=cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback();
            print('更新失败发生冲突')
            raise;
        finally:
            cursor.close()
        print('....execute...sql...end..')

    def updateUser(self,user):
        cursor = self.conn.cursor(cursor=cursors.DictCursor)
        sql  = "start transaction; "\
                "select status from users where id = %d for update;" \
                "update users set status = %d" \
                                    ",userName = %s" \
                                   ",password = %s" \
                                    ",email = %s,money=%d;"\
               %(user.id,user.status,user.userName,user.password,user.email,user.money)
        try:
            cursor.execute(sql)
            self.conn.commit();
        except Exception as e:
            self.conn.rollback();
            print('error where execute update.......')
            raise ;
        finally:
            cursor.close()

    #测试，更新后不提交事务
    def updateUserTestNoCommit(self,user):
        cursor = self.conn.cursor(cursor=cursors.DictCursor)
        sql  = "start transaction; "\
                "select status from users where id = %d for update;" \
               "update users set status = %d" \
               ",userName = '%s'" \
               ",password = '%s',money=%d" \
               %(user.id,user.status,user.userName,user.password,user.money)
        # ",email = %s ;"\
        try:
            cursor.execute(sql)
            self.conn.commit();
        except Exception as e:
            self.conn.rollback();
            raise ;
        finally:
            cursor.close()


if __name__ == "__main__":
    base=BaseDao();
    user = base.findById(1);
    # print('第1次更新前.....  用户名:' + user.userName);
    user.userName='zhangsan111'
    # base.updateUserTestNoCommit(user)
    # user = base.findById(1);
    # print('第1次更新后.....  用户名:'+user.userName);
    # print('第2次更新前.....  用户名:' + user.userName);
    # user.userName='lisi222'
    # base.updateUser(user)
    # user = base.findById(1);
    # print('第2次更新后.....  用户名:' + user.userName);

    user = base.findById(1);
    print('----------->>>>>before:status:'+str(user.status))
    for i in range(9):
        print('execute.........'+str(i))
        base.updateUserNoLock(user)
    user = base.findById(1);
    print('----------->>>>>after:status:' + str(user.status))