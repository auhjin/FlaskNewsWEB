# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:__init__.py.py
@time:2021/06/17
"""
from flask import Blueprint

passport_blue = Blueprint("passport",__name__,url_prefix="/passport")

from . import views
