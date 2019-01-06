#!  /usr/bin/env python
#ecoding=utf-8
import time, sched


def execute(schedule, sch_times):
    print('execute.........')
    # 安排inc秒后再次运行自己，即周期运行
    schedule.enter(sch_times, 0, execute, (schedule, sch_times))


if __name__=="__main__":
    # 第一个参数确定任务的时间，返回从某个特定的时间到现在经历的秒数
    # 第二个参数以某种人为的方式衡量时间
    schedule = sched.scheduler(time.time, time.sleep)
    # 安排inc秒后再次运行自己，即周期运行
    sche_times=6 #/s
    schedule.enter(0, 0, execute, (schedule,sche_times))
    # 持续运行，直到计划时间队列变成空为止
    schedule.run()
