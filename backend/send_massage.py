
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

if __name__ == "__main__":
    send_message(17620338333, str(datetime.datetime.now()))
    print(str(datetime.datetime.now()))