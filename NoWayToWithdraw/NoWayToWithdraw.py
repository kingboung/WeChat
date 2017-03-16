#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os,re,shutil,time,itchat
from itchat.content import *

# {msg_id:{msg_from,msg_to,msg_time,msg_time_touser,msg_type,msg_content,msg_url"}
msg_dict={}

# 清除超时信息（在有新消息动态时被调用）
def ClearTimeOutMsg():
    if len(msg_dict)>0:
        for msg_id in msg_dict:
            if time.time()-msg_dict[msg_id]['msg_time']>130.0:
                item=msg_dict.pop(msg_id)
                if item['msg_type']=='Picture' or item['msg_type']=='Recording'\
                        or item['msg_type']=='Video' or item['msg_type']=='Attachment':
                    print('Delete:',item['msg_content'])
                    os.remove(item['msg_content'])

@itchat.msg_register([TEXT,PICTURE,MAP,CARD,SHARING,RECORDING,ATTACHMENT,VIDEO,FRIENDS])
def Revocation(msg):
    mytime=time.localtime()
    msg_time_touser=mytime.tm_year.__str__()+'/'+mytime.tm_mon.__str__()+'/'+mytime.tm_mday.__str__()\
                    +' '+mytime.tm_hour.__str__()+':'+mytime.tm_min.__str__()+':'+mytime.tm_sec.__str__()
    msg_id=msg['MsgId']
    msg_time=msg['CreateTime']
    msg_from=itchat.search_friends(userName=msg['FromUserName'])['NickName']
    msg_type=msg['Type']
    msg_content=None
    msg_url=None
    if msg['Type']=='Text':
        msg_content=msg['Text']
    elif msg['Type']=='Picture':
        msg_content=msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type']=='Card':
        msg_content=msg['RecommendInfo']['NickName']+r'的名片'
    elif msg['Type']=='Map':
        x,y,location=re.search("<location x=\"(,*?)\" y=\"(.*?)\".*label=\"(.*?)\".*>",msg['OriContent']).group(1,2,3)
        if location is None:
            msg_content=r"纬度->"+x.__str__()+" 经度->"+y.__str__()
        else:
            msg_content=r""+location
    elif msg['Type']=='Sharing':
        msg_content=msg['Text']
        msg_url=msg['Url']
    elif msg['Type']=='Recording':
        msg_content=msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type']=='Attachment':
        msg_content=r""+msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type']=='Video':
        msg_content=r""+msg['FileName']
        msg['Text'](msg['FileName'])
    elif msg['Type']=='Friends':
        msg_content=msg['Text']

    msg_dict.update({msg_id:{'msg_from':msg_from,'msg_time':msg_time,'msg_time_touser':msg_time_touser,'msg_type':msg_type,'msg_content':msg_content,'msg_url':msg_url}})
    ClearTimeOutMsg()

@itchat.msg_register([NOTE])
def SaveMsg(msg):
    if not os.path.exists(".\\Revocation\\"):
        os.mkdir(".\\Revocation\\")

    if re.search(r"\<replacemsg\>",msg['Content'])!=None:
        old_msg_id=re.search(r"\<msgid\>(.*?)\<\/msgid\>",msg['Content']).group(1)
        old_msg=msg_dict[old_msg_id]
        msg_send=r"你的好友："+old_msg['msg_from']+r" 在 ["+old_msg['msg_time_touser']+\
                 r"],撤回了一条 ["+old_msg['msg_type']+" ] 消息，内容如下："+old_msg['msg_content']
        if old_msg['msg_type']=='Sharing':
            msg_send+=r",链接："+old_msg['msg_url']
        elif old_msg['msg_type']=='Picture' or old_msg['msg_type']=='Recording' or old_msg['msg_type']=='Video' or old_msg['msg_type']=='Attachment':
            msg_send+=r",存储在当前目录tmp文件夹中"
            shutil.move(old_msg['msg_content'],r".\\Recovation\\")
        itchat.send(msg_send,toUserName='filehelper')

        msg_dict.pop(old_msg_id)
        ClearTimeOutMsg()

if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()