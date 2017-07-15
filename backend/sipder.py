#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM


import json
import time

import requests
from core.view import app

def get_data():
    data_list = []
    lottery_dict = app.config.get("LOTTERY_DICR")
    for url, name in lottery_dict.items():
        data_dict = requests.get(url).json()
        data_dict['name'] = name
        print(data_dict)
        data_list.append(data_dict)

    return data_list




