import json

from flask import render_template
from . import main
from backend.sipder import get_data


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/updata')
def updata():

    data = get_data()

    return json.dumps(data)