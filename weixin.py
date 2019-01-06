#微信朋友分析
import itchat
# 用户多开
newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=True, statusStorageDir='newInstance.pkl')
@newInstance.msg_register(itchat.content.TEXT)
def reply(msg):
    return msg.text
newInstance.run()

friends = itchat.get_friends(update=True)[0:]

#初始化计数器
male = female = other = 0
#friends[0]是自己的信息,所以要从friends[1]开始
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
    	other += 1

#计算朋友总数
total = len(friends[1:])
#打印出自己的好友性别比例
print("男性好友: %.2f%%"%(float(male)/total*100) + "\n" +
      "女性好友: %.2f%%"%(float(female)/total*100)+"\n"+
      "不明性别好友: %.2f%%"%(float(other)/total*100))

#定义一个函数.用来爬取各个变量
def get_var(var):
    variable =[]
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable
#调用函数得到各个变量,并把数据存储到csv文件中,保存到当前位置
NickName = get_var("NickName")
Sex = get_var('Sex')
Province = get_var('Province')
City = get_var('City')
Signature = get_var('Signature')

from pandas import DataFrame
data = {'NickName':NickName,'Sex':Sex,'Province':Province,'City':City,
	'Signature':Signature}
frame = DataFrame(data)
frame.to_csv('data.csv',index=True)