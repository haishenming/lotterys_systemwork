#! /usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = HSM

import json

from flask import Flask, render_template
app = Flask(__name__)

from backend.sipder import get_data

print("__name__",__name__)


@app.route('/index')
def index():
    datas = get_data()
    print(datas)
    return render_template('index.html', datas=datas)
