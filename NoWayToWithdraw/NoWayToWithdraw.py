#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import time
import itchat
from itchat.content import *
from threading import Thread

# {msg_id : {msg_from, msg_time, msg_type, msg_content, msg_url}
messages = []


# 清除超时信息（在有新消息动态时被调用）
def clear_timeout_msg():
    # 如果有积压消息
    if len(messages) > 0:
        for message in messages:
            msg_id = list(message.keys())[0]
            msg_time = message[msg_id]['msg_time']
            msg_type = message[msg_id]['msg_type']
            msg_content = message[msg_id]['msg_content']

            current_time = time.time()

            if current_time - msg_time > 120.0:
                messages.remove(message)
                # 删除文件
                if msg_type == 'Picture' or msg_type == 'Recording' or msg_type == 'Video' or msg_type == 'Attachment':
                    print('Delete:', msg_content)
                    os.remove(msg_content)


@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS], isGroupChat=True)
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS], isFriendChat=True)
def save_msg(msg):
    msg_time = msg['CreateTime']
    msg_id = msg['MsgId']

    actual_user_name = msg.get('ActualUserName', None)
    if actual_user_name:
        msg_from = itchat.search_friends(userName=actual_user_name)['NickName']
    else:
        msg_from = msg['User'].get('NickName', None)

    msg_type = msg['Type']
    msg_content = None
    msg_url = None

    if msg['Type'] == 'Text':
        msg_content = msg['Text']

    elif msg['Type'] == 'Picture':
        msg_content = msg['FileName']
        # 下载文件
        msg['Text'](msg['FileName'])

    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r'的名片'

    elif msg['Type'] == 'Map':
        x, y, location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*>", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location

    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_url = msg['Url']

    elif msg['Type'] == 'Recording':
        msg_content = msg['FileName']
        msg['Text'](msg['FileName'])

    elif msg['Type'] == 'Attachment':
        msg_content = r"" + msg['FileName']
        msg['Text'](msg['FileName'])

    elif msg['Type'] == 'Video':
        msg_content = r"" + msg['FileName']
        msg['Text'](msg['FileName'])

    elif msg['Type'] == 'Friends':
        msg_content = msg['Text']

    message = {
        msg_id: {
            'msg_from': msg_from,
            'msg_time': msg_time,
            'msg_type': msg_type,
            'msg_content': msg_content,
            'msg_url': msg_url
        }
    }
    messages.append(message)

    # 如果积压了100条，那么清理过时信息
    if len(messages) >= 100:
        clear_timeout_msg()


@itchat.msg_register([NOTE], isGroupChat=True)
@itchat.msg_register([NOTE], isFriendChat=True)
def get_withdraw_msg(msg):
    if re.search(r"\<replacemsg\>", msg['Content']) != None:
        try:
            old_msg_id = re.search(r"\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
            old_msg = None

            for message in messages:
                if old_msg_id == list(message.keys())[0]:
                    old_msg = message[old_msg_id]
                    break

            msg_url = old_msg['msg_url']
            msg_time = old_msg['msg_time']
            msg_from = old_msg['msg_from']
            msg_type = old_msg['msg_type']
            msg_content = old_msg['msg_content']

            group_or_friend_name = msg['User'].get('NickName', None)
            if group_or_friend_name == msg_from:
                itchat.send(r"你的好友{}在[{}]撤回了一条消息".format(msg_from, time.ctime(msg_time)), toUserName='filehelper')
            else:
                itchat.send(r"你的好友{}在[{}]于群聊#{}#中撤回了一条消息".format(msg_from, time.ctime(msg_time), group_or_friend_name), toUserName='filehelper')

            if msg_type == 'Sharing':
                itchat.send("链接：{}".format(msg_url), toUserName='filehelper')

            elif msg_type == 'Picture':
                itchat.send_image(msg_content, toUserName='filehelper')

            elif msg_type == 'Video':
                itchat.send_video(msg_content, toUserName='filehelper')

            elif msg_type == 'Attachment':
                itchat.send_file(msg_content, toUserName='filehelper')

            elif msg_type == 'Recording':
                itchat.send_file(msg_content, toUserName='filehelper')

            else:
                itchat.send(old_msg['msg_content'], toUserName='filehelper')

        except Exception as ex:
            print('Can not find the withdraw message.Error message: {}'.format(ex))



if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
