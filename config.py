# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:config.py
@time:2021/06/16
"""
import logging
from datetime import timedelta

from redis import StrictRedis


class Config(object):
    DEBUG = True

    SECRET_KEY = "auhjin_ai8@163.com"

    #配置MySQL信息
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/phm"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #配置Redis信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    #Session配置信息
    SESSION_TYPE = "redis"
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(seconds = 20)

    LEVEL_NAME = logging.DEBUG

class DevelopConfig(Config):
    DEBUG = True
    #
    # dbinfo = {
    #     "ENGINE":"mysql",
    #     "DRIVER":"pymysql",
    #     "USER":"root",
    #     "PASSWORD":"root",
    #     "HOST":"localhost",
    #     "PORT":3306,
    #     "NAME":"phm"
    # }
    #
    # SQLALCHEMY_TRACK_MODIFICATIONS = get_db_url(dbinfo)


class TestingConfig(Config):

    pass

class StagingConfig(Config):

    pass


class ProductConfig(Config):

    pass

envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}