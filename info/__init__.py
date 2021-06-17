# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:__init__.py
@time:2021/06/16
"""
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import envs, Config

redis_store = None

db = SQLAlchemy()





def creat_app(config_name):
    #调用日志方法，记录程序运行信息
    log_file(Config.LEVEL_NAME)

    app = Flask(__name__)

    config = envs.get(config_name)
    app.config.from_object(config)

    #创建数据库对象
    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT,decode_responses=True)

    Session(app)

    CSRFProtect(app)

    from info.modules.index import index_blue
    app.register_blueprint(index_blue)

    return app

def log_file(level_name):
    #设置日志的记录等级
    logging.basicConfig(level=level_name)
    #创建日志记录器，指明日志的保存路径，每个日志文件的最大大小，保存日志的文件个数\
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024*1024*100,backupCount=10)
    #创建日志文件的格式，日志等级，输入日志信息的文件名，行数，日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    #为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    #为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)