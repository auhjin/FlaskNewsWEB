# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/30
"""
from flask import current_app, jsonify, render_template, abort, session, g, request

from . import  news_blue
from ...models import News, User

# 新闻详情请求接口
# 请求路径： /news/<int:news_id>
# 请求方式： get
# 请求参数： news_id
# 返回数据： detail.html页面 data字典数据
from ...utils.commons import user_login_data
from ...utils.response_code import RET

#收藏操作API
#请求方式：post
#请求参数：news_id,action,g.user
#返回参数：errno，errmsg
news_blue.route("/news_collect")
def news_collect():
    #判断用户是否登录
    if not g.user:
        return jsonify(errno=RET.NODATA, errmsg="用户未登录")
    #获取用户参数、动作参数、新闻id
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    #参数校验
    if not all([news_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")
    #操作类型
    if not action in ["collect", "cancel_collect"]:
        return jsonify(errno=RET.DATAERR, errmsg="操作类型有误")
    #根据新闻id取出新闻对象，判断是否存在
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="新闻获取失败")
    if not news:
        return jsonify(errno=RET.NODATA, errmsg="新闻不存在")
    #根据操作参数，进行收藏或取消操作
    if action == "collect":
        if not news in g.user.collection_news:
            g.user.collection_news.append(news)
    else:
        if news in g.user.collection_news:
            g.user.collection_news.remove(news)
    #返回响应
    return jsonify(errno=RET.OK, errmsg="操作成功")

@news_blue.route("/<int:news_id>")
@user_login_data
def news_detail(news_id):
    # # 从session中取出user_id
    # user_id = session.get("user_id")
    # # 通过user_id取出用户对象
    # user = None
    # if user_id:
    #     try:
    #         from info.models import User
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
    # 1、根据新闻编号，查询新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻信息失败")
    if not news:
        abort(404)
    #获取热门新闻排行数据
    try:
        click_news = News.query.order_by(News.clicks).limit(6).all()
        # click_news = News.query.order_by(News.clicks.desc()).limit(6).all()
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news_item in click_news:
        click_news_list.append(news_item.to_dict())
    is_collected = False
    if g.user:
        if news in g.user.collection_news:
            is_collected = True

    # 2、携带数据，渲染界面
    data = {
        "news_info":news.to_dict() if news else "",
        "user_info":g.user.to_dict() if g.user else "",
        "news_list":click_news_list,
        "is_collected":is_collected
    }

    return render_template("news/detail.html", data=data)