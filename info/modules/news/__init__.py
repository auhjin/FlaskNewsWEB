# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:__init__.py.py
@time:2021/06/30
"""
from flask import  Blueprint

# 创建蓝图对象
news_blue = Blueprint("news", __name__, url_prefix="/news")

# 使用蓝图对象，装饰视图函数
from . import views