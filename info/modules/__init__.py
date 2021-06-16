# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:__init__.py.py
@time:2021/06/16
"""
from flask import Blueprint

index_blue = Blueprint("index", __name__)

from info.modules.index import views