#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM

import datetime
import time

import requests

from .models import *
from .config import *

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

def updata():
    for data in get_data():
        if data['error']:
            name = data.get('name')
            expect = data.get('data')[0].get('expect')
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
                filter_by(name=name, expect=expect, opentimestamp=opentimestamp).first()
            if old_lotterys_info:
                continue
            else:
                session.add(lotterys_info)
                session.commit()

def spider():
    while True:
        updata()
        time.sleep(600)

if __name__ == '__main__':
    spider()