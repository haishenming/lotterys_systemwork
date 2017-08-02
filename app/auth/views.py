import json
import hashlib
import os

from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User, LotterysInfo
from .forms import LoginForm, RegistrationForm, AlarmInfoForm
from .. import db
from config import basedir

with open(os.path.join(basedir, 'lottery_dict'), 'r') as f:
    lottery_dict = json.loads(f.read())
# lottery_dict = json.dump(os.path.join(basedir, 'lottery_dict'))
print(lottery_dict)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            username = user.username
            return redirect(request.args.get('next') or url_for('.user_index', username=username))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/<username>', methods=['GET', 'POST'])
@login_required
def user_index(username):
    error = ''
    lottery_name_list = []
    for url, name in lottery_dict.items():
        lottery_name_list.append(name)
    user = db.session.query(User).filter_by(username=username).first()
    alarm_info = json.loads(user.alarm_info)
    # if not isinstance(alarm_info, list):
    #     alarm_info = {}
    form = AlarmInfoForm()
    md5 = hashlib.md5()
    md5.update(json.dumps([form.lottery_name.data, form.same_num.data, str(form.is_order)]).encode(encoding='utf-8'))
    if form.validate_on_submit():
        new_info = {
            'id': md5.hexdigest(),
            'lottery_name': form.lottery_name.data,
            'same_num': form.same_num.data,
            'is_order': form.is_order.data,
            'is_start': form.is_start.data,
        }
        if new_info in alarm_info:
            error = "重复添加无效！"
        else:
            alarm_info.extend([new_info, ])
            user.alarm_info = json.dumps(alarm_info)
    print(alarm_info)
    return render_template('auth/user_index.html',
                           username=username,
                           alarm_info=alarm_info,
                           form=form,
                           error=error,
                           lottery_name_list = lottery_name_list)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    phone=form.phone.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/<username>/<data>/<type>')
@login_required
def updata_rule(username, data, type):
    error = ''
    form = AlarmInfoForm()
    info_id = data
    print(data)
    type = type
    user = db.session.query(User).filter_by(username=username).first()

    alarm_info = json.loads(user.alarm_info)
    for i, a in enumerate(alarm_info):
        if a['id'] == info_id:
            info_index = i
            old_info = a
    alarm_info.pop(info_index)

    type = type
    if type == 'forbidden':
        old_info.update({"is_start": False})
        new_info = old_info
        alarm_info.insert(info_index, new_info)
    elif type == 'start':
        old_info.update({"is_start": True})
        new_info = old_info
        alarm_info.insert(info_index, new_info)
    elif type == 'delete':
        pass
    else:
        error = "未知的操作类型"
    user.alarm_info = json.dumps(alarm_info)
    return redirect(url_for('.user_index', username=username))
