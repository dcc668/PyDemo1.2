import itchat
import _thread as thread
from itchat.content import *
import os
import time

def get_name_in_group(chatroom,msg):
    """利用 id 返回备注或者昵称"""
    user = itchat.search_friends(name=msg['ActualNickName'])
    if user!=[] and user[0]['RemarkName'] != '':
        return user[0]['RemarkName']
    elif user!=[]:
        return user[0]['NickName']
    else:
        memberList = chatroom['MemberList']
        for user in memberList:
            if user['UserName'] == msg['ActualUserName']:
                return user['NickName']
                break
        # return ""

def write_sub(room_id, from_user_name, content, msgtime):
    ###存储历史chatroom###
    input = open('room_history.txt', 'a', encoding='utf-8')
    content = content.replace('\n', ' ')
    if msgtime==None or msgtime=="":
        msgtime=str(time.time())
    input.write(room_id + '##$##' + from_user_name + '##$##' + content + '##$##' + msgtime + '\n')
    input.close()

def update_function():
    """
    微信动态注册消息
    """
    @itchat.msg_register(TEXT, isGroupChat=True)
    def group_reply(msg):
        from_userid = msg['ActualUserName']
        room_id = msg['FromUserName']
        content = msg['Content']
        isat = msg['IsAt']
        msgtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if from_userid != account1_id:
            chatroom=itchat.search_chatrooms(userName=room_id);
            room_name = chatroom['NickName']
            from_user_name = get_name_in_group(chatroom,msg)
            print('群 %s: %s --> %s' % (room_name, from_user_name, content))
            write_sub(room_name, from_user_name, content, msgtime)
        else:
            room_id = msg['ToUserName']
            room_name = itchat.search_chatrooms(userName=room_id)['NickName']
            from_user_name = '我自己'
            write_sub(room_name, from_user_name, content, msgtime)

if __name__ == '__main__':
    # itchat
    itchat.auto_login(hotReload=True)
    itchat.dump_login_status()
    thread.start_new_thread(itchat.run, ())

    # 用户设置
    account1_id = itchat.search_friends()['UserName']
    if not os.path.exists(os.getcwd() + '/room_history.txt'):
        with open('room_history.txt','w') as f:
            pass;

    while 1:
        update_function()
        time.sleep(1)