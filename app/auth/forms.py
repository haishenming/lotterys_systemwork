from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, LotterysInfo


class LoginForm(FlaskForm):
    '''
    登录表单
    '''
    email = StringField('Email', validators={Required(), Length(1, 64),
                                             Email()})
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    '''
    注册表单
    '''
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z0-9]*$', 0, '')
    ])
    phone = StringField("Phone", validators=[
        Required(), Regexp('^[0-9]*$', 0, '')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Password must match!')])
    password2 = PasswordField('Confirm passwoed', validators=[Required(), ])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user.')


class AlarmInfoForm(FlaskForm):
    '''
    警报配置表单
    '''
    lottery_name = StringField(
        '彩票名称', validators=[
            Required(),
        ]
    )
    same_num = IntegerField(
        '相同期数', validators=[
            Required(),
        ]
    )

    is_start = BooleanField(
        '提交后启用', validators=[
        ],
        default=True
    )

    is_order = BooleanField(
        '是否检查顺序', validators=[
        ],
        default=False
    )

    submit = SubmitField('提交')

    def validate_lottery_name(self, field):
        if LotterysInfo.query.filter_by(name=field.data).first():
            pass
        else:
            raise ValidationError('该彩票未收录，或彩票名称输入有误。')
