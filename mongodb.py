#_*_ecoding:utf8_*_
import pymongo

conn=pymongo.MongoClient()
mydb=conn["mydb"]
users=mydb["t_user"]

user1={"userName":"cc1","sex":"男","password":"111","email":"dcc666@163.com"}
# user2={"userName":"cc2","sex":"男","password":"122","email":"dcc667@163.com"}
# user3={"userName":"cc3","sex":"男","password":"123","email":"dcc668@163.com"}

users.insert(user1)
print("insert finish")