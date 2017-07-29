import json

from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User, LotterysInfo
from .forms import LoginForm, RegistrationForm, AlarmInfoForm
from .. import db


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


@auth.route('/auth/<username>', methods=['GET', 'POST'])
@login_required
def user_index(username):
    error=''
    user = db.session.query(User).filter_by(username=username).first()
    alarm_info = json.loads(user.alarm_info)
    form = AlarmInfoForm()
    if form.validate_on_submit():
        new_info = {
            'lottery_name': form.lottery_name.data,
            'same_num': form.same_num.data,
            'is_order': form.is_order.data
        }
        if new_info in alarm_info:
            error = "重复添加无效！"
        else:
            alarm_info.append(new_info)

    return render_template('auth/user_index.html',
                           username=username,
                           alarm_info=alarm_info,
                           form=form,
                           error=error)


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
