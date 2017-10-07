#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import sys
import itchat


def get_msg():
    while True:
        msg = itchat.get_msg()[0]

        if len(msg) != 0:
            msg = msg[0]
            if msg.get('ToUserName', None) == 'filehelper':
                return msg.get('Content', '')


# 给好友发送祝福语
def send_greeting(friend_greeting_list, exist_name_flag):
    for friend_greeting in friend_greeting_list:
        user_name = friend_greeting['UserName']

        greeting_content = friend_greeting['GreetingContent']

        if len(greeting_content):
            if exist_name_flag:
                greeting_name = friend_greeting['GreetingName']
                greeting_content.replace('#name#', greeting_name)
            itchat.send_msg(greeting_content, toUserName=user_name)


# 生成提示信息
def create_prompt(index, distance, friend_greeting_list, exist_name_flag):
    prompt = ''
    for index_inner, friend_greeting in enumerate(friend_greeting_list[index * distance:(index + 1) * distance]):
        if exist_name_flag:
            remark_name = friend_greeting['RemarkName']
            nick_name = friend_greeting['NickName']
            greeting_name = friend_greeting['GreetingName']
            greeting_content = friend_greeting['GreetingContent']

            if len(greeting_content):
                prompt += '{}: {}  -->  {}\n'.format(index * distance + index_inner + 1, nick_name if not remark_name else remark_name, greeting_name)
            else:
                prompt += '{}: {}  -->  {}(已经取消发送祝福语)\n'.format(index * distance + index_inner + 1, nick_name if not remark_name else remark_name, greeting_name)

        else:
            remark_name = friend_greeting['RemarkName']
            nick_name = friend_greeting['NickName']
            greeting_content = friend_greeting['GreetingContent']

            if len(greeting_content):
                prompt += '{}: {}\n'.format(index * distance + index_inner + 1, nick_name if not remark_name else remark_name)
            else:
                prompt += '{}: {}(已经取消发送祝福语)\n'.format(index * distance + index_inner + 1, nick_name if not remark_name else remark_name)

    return prompt


def customize_broadcast_greetings():
    itchat.send_msg('欢迎使用由Wuli榜榜研发的个性化群发小工具', toUserName='filehelper')
    itchat.send_msg('请参照以下格式编写祝福语\n'
                    '参照格式：\n'
                    '   #name#，中秋节快乐！\n'
                    '\n'
                    '效果——\n'
                    '备注为"小小明"的用户:\n'
                    '   小明，中秋快乐！\n'
                    '\n'
                    '备注为"小明"的用户:\n'
                    '   小明，中秋快乐！\n'
                    '\n'
                    '没有备注，昵称为"Wuli榜榜"的用户:\n'
                    '   Wuli榜榜，中秋快乐!\n',
                    toUserName='filehelper')

    itchat.send_msg('请撰写专属于你的祝福语', toUserName='filehelper')

    # 是否要继续获取祝福语
    get_common_greeting_flag = True
    # 群发祝福语
    common_greeting = ''

    while True:
        # 获取祝福语
        if get_common_greeting_flag:
            common_greeting = get_msg()
            itchat.send_msg(common_greeting, toUserName='filehelper')

        itchat.send_msg('请确认你的祝福语\n'
                        '发送"确认"进入下一步\n'
                        '发送"修改"继续编辑', toUserName='filehelper')

        make_sure_text = get_msg()
        if make_sure_text == '确认':
            break
        elif make_sure_text == '修改':
            itchat.send_msg('请重新输入你的祝福语', toUserName='filehelper')
            get_common_greeting_flag = True
        else:
            get_common_greeting_flag = False

    friend_greeting_list = []
    exist_name_flag = True if '#name#' in common_greeting else False

    # 每次显示好友的数目
    friend_distance = 20

    friends = itchat.get_friends()[1:]
    for index in range(len(friends)//friend_distance):
        itchat.send_msg('请输入对应编号，单独修改该编号好友的名字或者祝福语', toUserName='filehelper')

        for index_inner, friend in enumerate(friends[index * friend_distance:(index + 1) * friend_distance]):
            friend_dict = {}
            user_name = friend['UserName']
            remark_name = friend.get('RemarkName', None)
            nick_name = friend.get('NickName', None)

            if exist_name_flag:
                if remark_name:
                    greeting_name = remark_name[1:] if len(remark_name) == 3 else remark_name
                else:
                    greeting_name = nick_name

                # friend_msg += '{}: {}  -->  {}\n'.format(index * 10 + index_inner + 1, nick_name if not remark_name else remark_name, greeting_name)
                friend_dict['UserName'] = user_name
                friend_dict['RemarkName'] = remark_name
                friend_dict['NickName'] = nick_name
                friend_dict['GreetingName'] = greeting_name
                friend_dict['GreetingContent'] = common_greeting
                friend_greeting_list.append(friend_dict)

            else:
                # friend_msg += '{}: {}\n'.format(index * 10 + index_inner + 1, nick_name if not remark_name else remark_name)
                friend_dict['UserName'] = user_name
                friend_dict['RemarkName'] = remark_name
                friend_dict['NickName'] = nick_name
                friend_dict['GreetingContent'] = common_greeting
                friend_greeting_list.append(friend_dict)

        prompt = create_prompt(index, friend_distance, friend_greeting_list, exist_name_flag)
        itchat.send_msg(prompt, toUserName='filehelper')

        while True:
            itchat.send_msg('输入对应编号修改相应好友祝福语消息， 输入"0"通过当前好友祝福语消息', toUserName='filehelper')

            try:
                number = int(get_msg())
            except Exception:
                itchat.send_msg('请输入正确的数字编号！', toUserName='filehelper')
                continue

            if number == 0:
                break

            elif index * friend_distance < number <= (index + 1) * friend_distance:
                if exist_name_flag:
                    itchat.send_msg('修改祝福语中的名字请发送"名字"\n'
                                    '修改祝福语请发送"祝福语"\n'
                                    '取消发送该好友请发送"取消",\n'
                                    '查看该好友祝福语请发送"查看"', toUserName='filehelper')
                    while True:
                        make_sure_text = get_msg()
                        if make_sure_text == '名字':
                            itchat.send_msg('请输入好友{}在祝福语中的名字'.format(friend_greeting_list[number-1]['RemarkName'] or friend_greeting_list[number-1]['NickName']), toUserName='filehelper')
                            greeting_name = get_msg()
                            friend_greeting_list[number-1]['GreetingName'] = greeting_name
                            friend_greeting_list[number-1]['GreetingContent'] = common_greeting.format(name=greeting_name)
                            break
                        elif make_sure_text == '祝福语':
                            itchat.send_msg('请为好友{}撰写专属于他的祝福语'.format(friend_greeting_list[number - 1]['RemarkName'] or friend_greeting_list[number - 1]['NickName']), toUserName='filehelper')
                            special_greeting = get_msg()
                            friend_greeting_list[number-1]['GreetingContent'] = special_greeting
                            break
                        elif make_sure_text == '取消':
                            friend_greeting_list[number - 1]['GreetingContent'] = ''
                            itchat.send_msg('取消成功!', toUserName='filehelper')
                            break
                        elif make_sure_text == '查看':
                            greeting_name = friend_greeting_list[number - 1]['GreetingName']
                            greeting_content = friend_greeting_list[number - 1]['GreetingContent'].replace('#name#', greeting_name)
                            if len(greeting_content):
                                itchat.send_msg(greeting_content, toUserName='filehelper')
                            else:
                                itchat.send_msg('该好友已被取消发送祝福语！', toUserName='filehelper')
                            break
                        else:
                            itchat.send_msg('请正确输入"名字"或者"祝福语"或者"取消"或者"查看"', toUserName='filehelper')

                    prompt = create_prompt(index, friend_distance, friend_greeting_list, exist_name_flag)
                    itchat.send_msg(prompt, toUserName='filehelper')

                else:
                    itchat.send_msg('修改祝福语请发送"祝福语"\n'
                                    '取消发送该好友请发送"取消"\n'
                                    '查看该好友祝福语请发送"查看"', toUserName='filehelper')
                    while True:
                        make_sure_text = get_msg()
                        if make_sure_text == '祝福语':
                            itchat.send_msg('请为好友{}撰写专属于他的祝福语'.format(friend_greeting_list[number - 1]['RemarkName'] or friend_greeting_list[number - 1]['NickName']), toUserName='filehelper')
                            special_greeting = get_msg()
                            friend_greeting_list[number - 1]['GreetingContent'] = special_greeting
                            break
                        elif make_sure_text == '取消':
                            friend_greeting_list[number - 1]['GreetingContent'] = ''
                            itchat.send_msg('取消成功!', toUserName='filehelper')
                            break
                        elif make_sure_text == '查看':
                            greeting_content = friend_greeting_list[number - 1]['GreetingContent']
                            if len(greeting_content):
                                itchat.send_msg(greeting_content, toUserName='filehelper')
                            else:
                                itchat.send_msg('该好友已被取消发送祝福语！', toUserName='filehelper')
                            break
                        else:
                            itchat.send_msg('请正确输入"名字"或者"祝福语"或者"取消"', toUserName='filehelper')

                    prompt = create_prompt(index, friend_distance, friend_greeting_list, exist_name_flag)
                    itchat.send_msg(prompt, toUserName='filehelper')

            else:
                itchat.send_msg('请输入正确的数字编号！', toUserName='filehelper')

    send_greeting(friend_greeting_list, exist_name_flag)


if __name__ == '__main__':
    itchat.auto_login(picDir='broadcasterQR.png', statusStorageDir='broadcaster.pkl')
    customize_broadcast_greetings()
    itchat.logout()
