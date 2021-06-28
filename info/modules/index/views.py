# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/16
"""
from flask import session, current_app, render_template, jsonify

from info.models import User, News
from info.modules.index import index_blue
from info.utils.response_code import RET


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
    #查询热门新闻，根据点击量，查询前十条
    try:
        news = News.query.order_by(News.clicks.desc()).limit(10)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="获取新闻列表失败")
    #将新闻对象转成字典列表
    news_list=[]
    for item in news:
        news_list.append(item.to_dict())
    #拼接用户数据渲染页面
    # user_dict = {
    #     "nickname":user.nickname
    #     "mobile":user.mobile
    #     "...":user. ....
    # }
    data ={
        #如果user有值，返回左边，否则右边
        "user_info":user.to_dict()  if user else "",
        "news_list":news_list
    }
    # print('用户信息：%s'% user.nick_name)

    return render_template("news/index.html", data=data)

@index_blue.route("/favicon.icon")
def get_web_logo():
    return current_app.send_static_file("news/news.png")