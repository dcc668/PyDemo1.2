#!  /usr/bin/env pytreon
#ecoding=utf
from mysql_demo.db_utils import DBUtils
from pymysql import cursors
import traceback

conn = DBUtils.getConn();
def get_data():
    try:
        cursor = conn.cursor(cursor=cursors.DictCursor)
        sql = "select a.* from t_template_url a where a.status = 0 and a.send_status=0"
        cursor.execute(sql)
        rss = cursor.fetchall()
        print('------findAll------>>>>: '+str(rss));
        return rss
    except Exception as e:
        print('error where execute fetch.......')
        traceback.print_exc()
    finally:
        conn.commit()

def update(obj):
    try:
        cursor = conn.cursor(cursor=cursors.DictCursor)
        sql = "update t_template_url  set status = 5 , send_status=2 where id ="+str(obj['id'])
        cursor.execute(sql)
    except Exception as e:
        print('error where execute fetch.......')
        traceback.print_exc()
    finally:
        conn.commit()
objs=get_data();
update(objs[0])