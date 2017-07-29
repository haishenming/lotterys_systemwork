#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM


import json
import time

from gevent import monkey; monkey.patch_socket()
import gevent

import requests
from manage import app

DATA_LIST = []

def request_data(url, name):
    data_dict = requests.get(url).json()
    data_dict['name'] = name
    print(data_dict)
    global DATA_LIST
    DATA_LIST.append(data_dict)

def get_data():
    global DATA_LIST
    lottery_dict = app.config.get("LOTTERY_DICR")
    for url, name in lottery_dict.items():
        g = gevent.spawn(request_data, url, name)
        g.join()

    return DATA_LIST




