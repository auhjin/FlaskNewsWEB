# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:__init__.py.py
@time:2021/06/16
"""
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import envs
from info.modules import index_blue

redis_store = None

def creat_app(config_name):
    app = Flask(__name__)

    config = envs.get(config_name)
    app.config.from_object(config)

    #创建数据库对象
    db = SQLAlchemy(app)
    redis_store = StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT,decode_responses=True)

    Session(app)

    CSRFProtect(app)

    app.register_blueprint(index_blue)

    return app
