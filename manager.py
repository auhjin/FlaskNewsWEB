# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:manager.py
@time:2021/06/16
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

app = Flask(__name__)

class Config(object):
    DEBUG = True

    #配置MySQL信息
    SQLAlCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/phm"
    SQOAlCHEMY_TRACK_MODIFICATIONS = False

    #配置Redis信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

app.config.from_object(Config)

#创建数据库对象
db = SQLAlchemy(app)
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,decode_responses=True)

def hellp_world():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)