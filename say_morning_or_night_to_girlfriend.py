#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import itchat
from threading import Timer


def say_morning_or_night():
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min

    # 8：00～8：30发早安
    if hour == 8 and minute < 30:
        itchat.send('早安', toUserName='@68af34551d1a98c62d53fb899d83037650ad9a66c516551346d1f1f648e85767')

    # 23：00～23：30发晚安
    if hour == 23 and minute < 30:
        itchat.send('晚安', toUserName='@68af34551d1a98c62d53fb899d83037650ad9a66c516551346d1f1f648e85767')

    timer = Timer(60 * 30, say_morning_or_night)
    timer.start()


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    # 半个小时启动一次
    timer = Timer(60 * 30, say_morning_or_night)
    timer.start()
