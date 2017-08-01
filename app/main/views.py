import json
import datetime

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/<username>')
def user_index(username):
    return render_template('user_index.html', username=username)
