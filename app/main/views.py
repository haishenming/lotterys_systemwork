import json
import datetime

from flask import render_template
from . import main
from backend.spider import get_data
from ..models import LotterysInfo, Alarm
from .. import db
from backend.spider import updata


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
