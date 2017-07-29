from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    alarm_info = db.Column(db.Text, default='{}')
    alarms = db.relationship("Alarm", backref='alarm', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

class LotterysInfo(db.Model):
    __tablename__ = 'lotterys_infos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    expect = db.Column(db.String(64))
    opencode = db.Column(db.Text)
    opentime = db.Column(db.DateTime)
    opentimestamp = db.Column(db.Integer)

    def __repr__(self):
        return '<Lottery {}-{}>'.format(self.name, self.expect)

class Alarm(db.Model):
    __tablename__ = 'alarms'
    id = db.Column(db.Integer, primary_key=True)
    alarm_info = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    create_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Lottery {}-{}>'.format(self.alarm_info, self.user)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
