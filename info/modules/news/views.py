# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/30
"""
from . import  news_blue

@news_blue.route("/news_detail")
def news_detail():

    return "展示新闻详细内容"