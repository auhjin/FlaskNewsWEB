# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/16
"""
from flask import session, current_app, render_template

from info.modules.index import index_blue


@index_blue.route("/")
def hello_world():

    session['name'] = "auhjin"
    print(session.get("name"))

    # current_app.logger.debug("调试信息")
    # current_app.logger.info("详细信息")
    # current_app.logger.warning("警告信息")
    # current_app.logger.error("错误信息")

    return render_template("news/index.html")

@index_blue.route("/favicon.icon")
def get_web_logo():
    return current_app.send_static_file("news/news.png")