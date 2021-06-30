# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/30
"""
from flask import current_app, jsonify, render_template, abort

from . import  news_blue
from ...models import News


# 新闻详情请求接口
# 请求路径： /news/<int:news_id>
# 请求方式： get
# 请求参数： news_id
# 返回数据： detail.html页面 data字典数据
from ...utils.response_code import RET


@news_blue.route("/<int:news_id>")
def news_detail(news_id):
    # 1、根据新闻编号，查询新闻对象
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="获取新闻信息失败")
    if not news:
        abort(404)
    # 2、携带数据，渲染界面
    data = {
        "news_info":news.to_dict() if news else ""
    }
    return render_template("news/detail.html", data=data)