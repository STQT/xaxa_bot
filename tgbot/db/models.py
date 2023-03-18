import datetime

from sqlalchemy import Column, VARCHAR, INTEGER, DateTime, BigInteger, sql

from tgbot.db.database import db


class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger(), unique=True)
    lang = Column(VARCHAR(2))
    name = Column(VARCHAR(200))
    date = Column(DateTime, default=datetime.datetime.utcnow())


class City(db.Model):
    __tablename__ = 'citys'
    query: sql.Select

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    name_uz = Column(VARCHAR(200))
    name_ru = Column(VARCHAR(200))
    name_en = Column(VARCHAR(200))
    date = Column(DateTime, default=datetime.datetime.utcnow())