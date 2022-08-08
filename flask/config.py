import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'winter'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:174402865@localhost:3306' \
                              '/winter?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
