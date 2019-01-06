#!  /usr/bin/env python
# ecoding=utf-8

import redis


rds = redis.StrictRedis(host='39.108.122.83', port='6379', decode_responses=True)
template_urls_set = 'myspider:template_urls'

# 新建一条键名为"123456"的数据, 包含属性attr_1
rds.hset(template_urls_set,'attr_1','data')
# 更改键名为"123456"的数据, 更改属性attr_1的值
rds.hset(template_urls_set, "attr_1", 200)

# 长度
len=rds.hlen(template_urls_set)
print('len:'+str(len))

# 获取值
attr_1 = rds.hget(template_urls_set, "attr_1")
print(attr_1)

# key是否存在
res=rds.hexists(template_urls_set, 'attr_1')
print(str(res))

# 删除属性(可以批量删除)
rds.hdel(template_urls_set, "attr_1")
len=rds.hlen(template_urls_set)
print('len:'+str(len))



