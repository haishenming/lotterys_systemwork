#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM

import datetime
import time
import json
from send_massage import send_message, phone_up

import logging

# 配置日志文件和日志级别
ch = logging.StreamHandler()
ch2 = logging.FileHandler('logging.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('root')

# Set default log level
logger.setLevel(logging.INFO)
ch2.setLevel(logging.INFO)

ch.setFormatter(formatter)
ch2.setFormatter(formatter)

# add ch to logger
# The final log level is the higher one between the default and the one in handler
logger.addHandler(ch)
logger.addHandler(ch2)

import requests

from models import *
from config import *

engine = create_engine('mysql+pymysql://root:haishenming123@127.0.0.1:3306/lotterydb?charset=utf8mb4')
Session = sessionmaker(bind=engine)
session = Session()

def request_data(url, name):
    while True:
        try:
            data_dict = requests.get(url).json()
            data_dict['name'] = name
            data_dict['error'] = ''
            logger.info(data_dict['name'] + '-' + data_dict['error'])
            print(data_dict['name'], data_dict['error'])
        except Exception as e:
            # 有错就返回错误
            logger.warn(e)
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
    is_five = False
    lottery_infos = session.query(LotterysInfo).filter_by(name=lottery_name)
    for info in lottery_infos:
        if order:
            if info.opencode == opencode:
                ret.append(info)
        else:
            ''.split()
            if sorted(info.opencode.split(',')) == sorted(opencode.split(",")):
                ret.append(info)  # 返回具体开奖号
        if len(ret) > 5:
            ret = ret[-5:]
            is_five = True

    return {"name": lottery_name, "number": len(ret), 'order':order, 'data': ret, 'is_five':is_five, 'num': len(ret)}


def check(lottery_info_now, info):
    '''
    检查是否需要发送短信并返回号码和短信内容
    '''
    SMS = info['username'] + ' 你好，您所订阅的信息有新的动向。\n\n'
    messages = SMS
    print("用户用户配置中有新获取的彩票信息。。。。。。")
    print("检查是否有符合要求的信息。。。。。。")
    for new_lottery in lottery_info_now:
        for alarm in info['alarm_info']:
            if new_lottery.name == alarm['lottery_name']:
                print("正在检查{}".format(alarm['lottery_name']))
                same_info = check_info_same(new_lottery.name, new_lottery.opencode, order=alarm['is_order'])
                one_pice = same_info['data'][0]

                if same_info['number'] >= alarm['same_num']:
                    inner_mess = ''
                    if same_info['is_five']:
                        inner_mess = "\n由于次数过多无法显示，以下数据仅显示最近五次历史相同"
                    message = \
                        "彩票名称：{}，\n相同期数：{}，\n是否检查顺序：{}，\n历史相同期数{}，{}\n具体期数：{}，\n历史开奖号：{}。\n\n".\
                            format(same_info['name'], same_info['number'],same_info['order'],\
                                   len(same_info['num']), inner_mess, same_info['data'],same_info['data'][0].opencode)
                    messages += message
    print("检查完毕")
    return (messages, info['phone'])

def send_SMS(new_info):
    '''
    根据返回信息发送短信
    '''
    SMS = ''
    user_infos = get_info()
    for user in user_infos:
        print('检查用户{}的配置'.format(user['username']))
        messages, phone = check(new_info, user)
        if '彩票名称' in messages and '具体期数' in messages:
            logger.info("检查完毕，正在发送短信\n---{}---, {}".format(messages, phone))
            print("检查完毕，正在发送短信\n---{}---, {}".format(messages, phone))
            for i in range(5):
                ret1 = send_message(phone, messages)
                if ret1.get('error', 1) == 0:
                    logger.info('短信发送成功')
                    break
                else:
                    logger.warn('短信发送失败，重新发送！')
                    continue
            logger.warn('重发次数超过5次，此次发送失败，请检查接口！')
            for i in range(5):
                ret1 = phone_up(phone)
                if ret1.get('error', 1) == 0:
                    logger.info('电话拨打成功')
                    break
                else:
                    logger.warn('电话拨打失败，重拨！')
                    continue
            logger.warn('重拨次数超过5次，此次发送失败，请检查接口！')
        else:
            logger.info("没有要发送的信息！")
            print("没有要发送的信息！")


def updata():
    new_info = []
    for data in get_data():
        if not data['error']:
            name = data.get('name')
            expect = data.get('data')[0].get('expect')
            opencode = data.get('data')[0].get('opencode')
            opentime = data.get('data')[0].get('opentime')
            opentime = datetime.datetime.strptime(opentime, '%Y-%m-%d %X')
            opentimestamp = data.get('data')[0].get('opentimestamp')

            # 测试数据
            # name = '河南中原风采22选5'
            # expect = 20172015
            # opencode = data.get('data')[0].get('opencode')
            # opentime = data.get('data')[0].get('opentime')
            # opentime = datetime.datetime.strptime(opentime, '%Y-%m-%d %X')
            # opentimestamp = data.get('data')[0].get('opentimestamp')

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
    print("准备发送短信。。。。。。")
    send_SMS(new_info)

def spider():
    while True:
        updata()
        time.sleep(60)

if __name__ == '__main__':
    spider()