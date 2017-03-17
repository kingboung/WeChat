#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import itchat
from itchat.content import *

@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    itchat.send('%s:%s'%(msg['Type'],msg['Text']),msg['FromUserName'])

@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])# attachment 附件
def download_reply(msg):
    msg['Text'](msg['FileName'])  #下载附件
    return '@%s@%s'%({'Picture':'img','Video':'vid'}.get(msg['Type'],'fil'),msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    # 该操作会自动将新好友的信息录入，不需要重载通讯录
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!',msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT,isGroupChat=True)
def text_reply(msg):
    if 'isAt' in msg:
        itchat.send(u'@%s\u2005I received:%s'%(msg['ActualNickName'],msg['Content']),msg['FromUserName'])
    return

itchat.auto_login(hotReload=True,enableCmdQR=True)
itchat.run()