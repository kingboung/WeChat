#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
import itchat
from itchat.content import *


@itchat.msg_register([TEXT], isFriendChat=True)
def save_msg(msg):
    from_user_name = msg.get('FromUserName', None)
    to_user_name = msg.get('ToUserName', None)
    msg_content = msg.get('Content', None)
    if itchat.search_friends(userName=to_user_name).get('NickName', None) == 'Wuli榜榜' and msg_content == '群发助手':
        itchat.send_msg('请扫描以下二维码接入群发助手服务，请务必打开微信用手机扫！不支持长按图片识别。', toUserName=from_user_name)
        os.popen('/usr/local/bin/python3 broadcaster.py {}'.format(from_user_name))
        while True:
            time.sleep(1)
            if os.path.exists('broadcasterQR.png'):
                itchat.send_image('broadcasterQR.png', toUserName=from_user_name)
                break


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    itchat.run()
