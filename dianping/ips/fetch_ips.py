#!  /usr/bin/env python
#ecoding=utf-8
from dianping.ips.db_utils import DBUtils
import  traceback
from pymysql import cursors
import threading,time,requests
import queue
q = queue.Queue()
class FetchIPs():
    def __init__(self):
        self.lock=threading.Lock
    def findIds(self,orderby=2):
        #return dict
        conn = DBUtils.getConn();
        ips=set()
        try:
            cursor = conn.cursor(cursor=cursors.DictCursor)
            sql = "select a.* from t_ips a where a.orderby <= "+str(orderby)
            cursor.execute(sql)
            rss = cursor.fetchall()
            print('------findIds------>>>>: '+str(len(rss)));
            for ip_dict  in rss:
                ips.add(ip_dict['ips'])
        except Exception as e:
            print('error where execute fetch.......')
            traceback.print_exc()
        finally:
            conn.commit()
        return ips;

    def verifyProxyList(self,v_url,urls):
        while len(urls) > 0:
            myurl = urls.pop()
            try:
                start=time.time()
                proxies = {
                    'http': myurl,
                }
                res=requests.get(url=v_url,proxies=proxies,timeout=3.0)
                end=time.time()
                print("验证代理的有效性:"+myurl+"--->>use time:"+str(end-start))
                #响应时间小于1.5秒
                useTime=end-start
                if res.status_code==200 and useTime<2:
                    print("+++Success:" + myurl)
                    print("--------存文件--------->>>>>:"+myurl)
                    q.put(myurl)
            except Exception as e:
                print("---Failure:" + myurl)
    def execute(self,schedule, sch_times):
        ips=self.findIds()
        v_url='http://www.dianping.com'
        # v_url = 'http://www.baidu.com'
        print(u"\n验证代理的有效性：")
        thread_size=30
        pre_thread_ips=len(ips)/thread_size
        all_thread = []
        for i in range(thread_size):
            start=int(i*pre_thread_ips)
            if i==thread_size-1:
                urls=list(ips)[start:len(ips)]
            else:
                end=int(i*pre_thread_ips+pre_thread_ips)
                urls=list(ips)[start:end]
            t = threading.Thread(target=self.verifyProxyList,args=(v_url,urls))
            all_thread.append(t)
            t.start()

        for t in all_thread:
            t.join()
        print('Total count:'+str(q.qsize()))
        with open('ips.txt','w',encoding='utf-8') as file:
            while q.qsize()>0:
                file.write(q.get()+'\n')
        print("All Done.")

        # 安排inc秒后再次运行自己，即周期运行
        schedule.enter(sch_times, 0, self.execute, (schedule, sch_times))

import time, sched
if __name__=="__main__":
    fet=FetchIPs()
    # 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
    # 第二个参数以某种人为的方式衡量时间
    schedule = sched.scheduler(time.time, time.sleep)
    # 安排inc秒后再次运行自己，即周期运行
    sche_times=5*60 #6min
    schedule.enter(0, 0, fet.execute, (schedule,sche_times))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()
