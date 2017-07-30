#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM

import datetime
import time
import json

import requests

from backend.models import *
from backend.config import *

engine = create_engine('mysql+pymysql://root:Haishen@127.0.0.1:3306/lotterydb?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()

def request_data(url, name):
    while True:
        try:
            data_dict = requests.get(url).json()
            data_dict['name'] = name
            data_dict['error'] = ''
            print(data_dict)
        except Exception as e:
            # 有错就返回错误
            print(e, '稍后重试')
            time.sleep(1)
            continue
        return data_dict


def get_data():
    global DATA_LIST
    lottery_dict = LOTTERY_DICR
    for url, name in lottery_dict.items():
        yield request_data(url, name)

def get_info():
    user_infos = []
    users = session.query(User).all()
    for user in users:
        info = {
            'username': user.username,
            'phone': user.phone,
            'alarm_info': json.loads(user.alarm_info)
        }
        user_infos.append(info)
    return user_infos

def check_info_same(lottery_name, opencode, order=False):
    '''
    检查并返回相同的彩票信息
    '''
    ret = []
    lottery_infos = session.query(LotterysInfo).filter_by(name=lottery_name)
    for info in lottery_infos:
        if order:
            if info.opencode == opencode:
                ret.append(info)
        else:
            ''.split()
            if sorted(info.opencode.split(',')) == sorted(opencode.split(",")):
                ret.append(info)

    return {"name": lottery_name, "number": len(ret), 'order':order, 'data': ret}


def check(lottery_info_now, info):
    '''
    检查是否需要发送短信并返回号码和短信内容
    '''
    SMS = info['username'] + ' 你好，您所订阅的信息有新的动向。\n\n'
    info = {'username': 'haishyen',
            'phone': '17723503316',
            'alarm_info': [{'id': '3b929f83f15f4b66753952f2e17b1f05',
                            'lottery_name': '河南中原风采22选5',
                            'same_num': 2,
                            'is_order': True,
                            'is_start': True},
                           {'id': '3b929f83f15f4b66753952f2e17b1f05',
                            'lottery_name': '埃及二分彩',
                            'same_num': 2,
                            'is_order': True,
                            'is_start': True}
                           ]}
    messages = SMS
    for new_lottery in lottery_info_now:
        for alarm in info['alarm_info']:
            if new_lottery.name == alarm['lottery_name']:
                same_info = check_info_same(new_lottery.name, new_lottery.opencode, order=alarm['is_order'])
                if same_info['number'] >= alarm['same_num']:
                    message = \
                        "彩票名称：{}，\n相同期数：{}，\n是否检查顺序：{}，\n具体期数：{}。\n\n".\
                            format(same_info['name'], same_info['number'],same_info['order'],same_info['data'])
                    messages += message
    return (messages, info['phone'])

    # for same_info in same_infos:
    #
    #     SMS =





def send_SMS(new_info):
    '''
    根据返回信息发送短信
    '''
    SMS = ''
    user_infos = get_info()
    for user in user_infos:
        messages, phone = check(new_info, user)


def updata():
    new_info = []
    for data in get_data():
        if not data['error']:
            # name = data.get('name')
            # expect = data.get('data')[0].get('expect')
            # opencode = data.get('data')[0].get('opencode')
            # opentime = data.get('data')[0].get('opentime')
            # opentime = datetime.datetime.strptime(opentime, '%Y-%m-%d %X')
            # opentimestamp = data.get('data')[0].get('opentimestamp')

            name = '河南中原风采22选5'
            expect = 20172015
            opencode = data.get('data')[0].get('opencode')
            opentime = data.get('data')[0].get('opentime')
            opentime = datetime.datetime.strptime(opentime, '%Y-%m-%d %X')
            opentimestamp = data.get('data')[0].get('opentimestamp')

            lotterys_info = LotterysInfo(
                name=name,
                expect=expect,
                opencode=opencode,
                opentime=opentime,
                opentimestamp=opentimestamp
            )
            old_lotterys_info = session.query(LotterysInfo).\
                filter_by(name=name, expect=expect).first()
            if old_lotterys_info:
                continue
            else:
                session.add(lotterys_info)
                session.commit()
                new_info.append(lotterys_info)
    send_SMS(new_info)

def spider():
    updata()

if __name__ == '__main__':
    spider()