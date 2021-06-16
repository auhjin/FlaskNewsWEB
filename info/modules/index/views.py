# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/16
"""
from flask import session

from info.modules.index import index_blue


@index_blue.route("/")
def hello_world():

    session['name'] = "auhjin"
    print(session.get("name"))

    return "hello world!"