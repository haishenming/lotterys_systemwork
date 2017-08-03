
# -*- coding: utf-8 -*-
import requests
import json
import datetime

def send_message(phone, message):
    resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
    auth=("api", "key-44b9b31582fdbb959202b6e20114bc17"),
    data={
	"mobile": str(phone),
	"message": message+"【海神名】"
    },timeout=3 , verify=False)
    result = resp.json()
    print(result)
    return result

def phone_up(phone):
    resp = requests.post("http://voice-api.luosimao.com/v1/verify.json",
    auth=("api", "key-3149f95d5dbc11a3a8eeee054beb0bbb"),
    data={
	"mobile": str(phone),
	"code": 1234
    },timeout=3 , verify=False)
    result = resp.json()
    print(result)
    return result

if __name__ == "__main__":
    phone_up(17620338333)
    print(str(datetime.datetime.now()))