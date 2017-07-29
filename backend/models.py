

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True)
    phone = Column(String(64))
    username = Column(String(64), unique=True, index=True)
    role_id = Column(Integer)
    password_hash = Column(String(128))
    alarm_info = Column(Text, default='{}')

    def __repr__(self):
        return '<User %r>' % self.username

class Alarm(Base):
    __tablename__ = 'alarms'
    id = Column(Integer, primary_key=True)
    alarm_info = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    create_time = Column(DateTime)

    def __repr__(self):
        return '<Lottery {}-{}>'.format(self.alarm_info, self.user)

class LotterysInfo(Base):
    __tablename__ = 'lotterys_infos'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    expect = Column(String(64))
    opencode = Column(Text)
    opentime = Column(DateTime)
    opentimestamp = Column(Integer)

    def __repr__(self):
        return '<Lottery {}-{}>'.format(self.name, self.expect)