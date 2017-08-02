import os
basedir = os.path.abspath(os.path.dirname(__file__))
import json

MYSQLDB = 'mysql+pymysql://root:Haishen@127.0.0.1:3306/lotterydb'
SQLITE = 'sqlite:///{}'.format(os.path.join(basedir, 'db.sqlite'))
print(os.path.join(basedir, 'data.sqlite'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')


    # from tools.get_lottery_dict import get_lottery_dict

    DEBUG = True

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    print(BASE_DIR)


    # 主URL
    MASTER_URL = 'http://f.apiplus.net/'
    # 次URL
    SLAVE_URL = None

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = MYSQLDB


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = MYSQLDB


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = MYSQLDB


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
