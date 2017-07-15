#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM


import os
import json

# from tools.get_lottery_dict import get_lottery_dict

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
print(BASE_DIR)
lottery_dict_path = os.path.join(BASE_DIR, 'lottery_dict')


LOTTERY_DICR = json.loads(open(lottery_dict_path).read())

# 主URL
MASTER_URL = 'http://f.apiplus.net/'
# 次URL
SLAVE_URL = None