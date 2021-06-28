# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/16
"""
from flask import session, current_app, render_template

from info.models import User
from info.modules.index import index_blue


@index_blue.route("/",methods = ["GET","POST"])
def hello_world():

    # session['name'] = "auhjin"
    # print(session.get("name"))
    # current_app.logger.debug("调试信息")
    # current_app.logger.info("详细信息")
    # current_app.logger.warning("警告信息")
    # current_app.logger.error("错误信息")

    #获取用户的登录信息
    user_id = session.get("user_id")
    #通过user_id取出用户对象
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    #拼接用户数据渲染页面
    # user_dict = {
    #     "nickname":user.nickname
    #     "mobile":user.mobile
    #     "...":user. ....
    # }

    data ={
        #如果user有值，返回左边，否则右边
        "user_info":user.to_dict()  if user else ""
    }
    # print('用户信息：%s'% user.nick_name)

    return render_template("news/index.html", data=data)

@index_blue.route("/favicon.icon")
def get_web_logo():
    return current_app.send_static_file("news/news.png")