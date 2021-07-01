# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/16
"""
from flask import session, current_app, render_template, jsonify, request, g

from info.models import User, News, Category
from info.modules.index import index_blue
from info.utils.commons import user_login_data
from info.utils.response_code import RET

# 新闻列表首页展示：
# 请求方式：get
# 请求参数：page, per_page, category_id
# 返回值：data数据
@index_blue.route("/newslist")
def newslist():
#   操作步骤
#   1 获取参数
    category_id = request.args.get("cid","1")
    page = request.args.get("page","1")
    per_page = request.args.get("per_page","10")
#   2.参数类型转换
    try:
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        page = 1
        per_page = 10
#   3.分页查询
    try:
        filters = ""
        if category_id != "1":
            filters = (News.category_id == category_id)
        paginate = News.query.paginate(page, per_page, False)
        # paginate = News.query.filter().order_by(News.create_time.desc()).paginate(page, per_page, False)

        # if category_id == "1":
        #     paginate = News.query.filter().order_by(News.create_time.desc()).paginate(page, per_page, False)
        # else:
        #     paginate = News.query.filter(News.category_id == category_id).order_by(News.create_time.desc()).paginate(page,per_page,False)

        # filters = []
        # if category_id != "1":
        #     filters.append(News.category_id == category_id)
        # paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg = "获取新闻列表失败l")
#   4.获取分页对象中的属性，总页数，当前页，当前页的对象列表
    totalPage = paginate.pages
    currentPage = paginate.page
    items = paginate.items
#   5.将对象列表转化为字典列表
    newsList = []
    for news in items:
        newsList.append(news.to_dict())
#   6.返回数据，返回响应
    return jsonify(errno=RET.OK, errmsg="获取新闻列表成功", totalPage=totalPage, currentPage=currentPage, newsList=newsList)

@index_blue.route("/",methods = ["GET","POST"])
@user_login_data
def hello_world():

    # session['name'] = "auhjin"
    # print(session.get("name"))
    # current_app.logger.debug("调试信息")
    # current_app.logger.info("详细信息")
    # current_app.logger.warning("警告信息")
    # current_app.logger.error("错误信息")

    # #获取用户的登录信息
    # user_id = session.get("user_id")
    # #通过user_id取出用户对象
    # user = None
    # if user_id:
    #     try:
    #         user = User.query.get(user_id)
    #     except Exception as e:
    #         current_app.logger.error(e)
    #查询热门新闻，根据点击量，查询前十条
    try:
        # news = News.query.order_by(News.clicks.desc()).limit(10).all()
        news = News.query.order_by(News.clicks).limit(10).all()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="获取新闻列表失败r")
    #将新闻对象转成字典列表
    news_list=[]
    for item in news:
        news_list.append(item.to_dict())
    #查询所有的分类数据
    try:
        category = Category.query.all()
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="获取分类列表失败")
    #将分类对象列表转为字典列表
    category_list = []
    for item in category:
        category_list.append(item.to_dict())
    #拼接用户数据渲染页面
    # user_dict = {
    #     "nickname":user.nickname
    #     "mobile":user.mobile
    #     "...":user. ....
    # }
    data ={
        #如果user有值，返回左边，否则右边
        "user_info":g.user.to_dict()  if g.user else "",
        "news_list":news_list,
        "category_list":category_list
    }
    # print('用户信息：%s'% user.nick_name)

    return render_template("news/index.html", data=data)

@index_blue.route("/favicon.icon")
def get_web_logo():
    return current_app.send_static_file("news/news.png")