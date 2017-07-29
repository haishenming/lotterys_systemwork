#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM



import os
import json
from config import Config

from bs4 import BeautifulSoup
from config import basedir as BASE_DIR

MASTER_URL = Config.MASTER_URL

def open_html(filename):
    html = open(filename, 'r', encoding='utf-8').read()

    return html


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def get_lottery_dict():
    lottery_dict = {}
    html = open_html('lottery.html')
    soup = parse_html(html)

    lottery_tags = soup.find_all('button')

    for tag in lottery_tags:
        lottery_code = tag.attrs['val']
        lottery_name = tag.text
        lottery_dict[MASTER_URL + lottery_code + ".json"] = lottery_name.rstrip(' 3IPs')

    return lottery_dict


def write_lottery(lottery_dict):
    file_path = os.path.join(BASE_DIR, 'lottery_dict')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(lottery_dict))

def main():
    lottery_dict = get_lottery_dict()
    write_lottery(lottery_dict)



if __name__ == '__main__':
    main()