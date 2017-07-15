#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM


# api http://kj.1680api.com/Open/CurrentOpenOne?code=10016
# response {"s":0,"m":"","c":"10016","c_t":628416,"c_d":"2017/07/12 22:22:26","c_r":"4,2,10,5,1,7,9,6,3,8","n_t":628417,"n_d":"2017/07/12 22:26:56","l_c":160,"no":179,"o_g":100,"o_info":"每5分钟","os":0,"osm":"暂停开奖","o_m":[6,"小","双","虎","虎","龙","虎","虎"]}

# 备用接口
# http://www.opencai.net/apifree/


import requests


response = requests.get('http://f.apiplus.net/dlt.json')


print(response.json()['data'])