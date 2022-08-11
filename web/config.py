import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '数据库名'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://数据库用户名:密码@localhost:3306' \
                              '/数据库名?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
