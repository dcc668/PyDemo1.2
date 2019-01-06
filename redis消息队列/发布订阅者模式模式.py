#!  /usr/bin/env python
# ecoding=utf-8

import redis

class Task():
    def __init__(self):
        self.rcon = redis.StrictRedis(host='localhost', db=5)
        #发布订阅者模式
        self.ps = self.rcon.pubsub()
        self.redis_sub=self.ps.subscribe('task:pubsub:channel')
    def listen_sub(self):
        for i in self.ps.listen():
            if i['type'] == 'message':
                print("Task get", i['data'])

if __name__ == '__main__':
    print('listen task channel')
    Task().listen_sub()
