# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/17
"""
import json
import random
import re
from flask import request, current_app, make_response, jsonify, session
from info import redis_store, constants, db
from info.constants import IMAGE_CODE_REDIS_EXPIRES
# from info.libs.yuntongxun.sms import CCP
from info.models import User
from info.modules.passport import passport_blue
from info.utils.captcha.captcha import captcha
from info.utils.response_code import RET

#API
#请求路径： ”/passport/logout“
#请求方式：POST
#请求参数：无
#返回值： errno，errmsg
@passport_blue.route("/logout",methods=["POST"])
def logout():
    #1、清楚session信息
    session.pop("user_id",None)
    #2、返回相应
    return jsonify(errno=RET.OK, errmsg="退出成功")

@passport_blue.route("/login", methods=["POST"])
def login():
    #1.获取参数
    dict_data = request.get_json()
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")
    #2.校验参数，空值校验
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    #3.通过手机号参数，查询数据库中的用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="获取用户失败")
    #4.判断用户对象是否存在
    if not user:
        return jsonify(errno=RET.NODATA,errmsg="用户不存在")
    #5.校验密码是否正确
    if not user.check_password(password):

        return jsonify(errno=RET.PWDERR,errmsg="密码错误")
    #6.将用户信息保存在Session中
    session["user_id"] = user.id
    print(user.id)
    #7.返回响应
    return jsonify(errno=RET.OK, errmsg="用户登录成功")

@passport_blue.route("/register", methods=["POST"])
def register():
    # 1、获取参数
    # json_data = request.data
    # dict_data = json.loads(json_data)
    dict_data = request.json
    # dict_data = request.get_json()
    mobile = dict_data.get("mobile")
    sms_code = dict_data.get("sms_code")
    password = dict_data.get("password")
    # 2、校验参数，空值检验
    if not all([mobile,sms_code,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数获取不全!!!!")
    # 3手机号作为key取出redis中的验证码，进行校验
    try:
        redis_sms_code = redis_store.get("sms_code:%s"%mobile)
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="读取redis数据库失败")
    # 4判断验证码是否过期
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA,errmsg="短信验证码已经过期")
    # 5判断验证码是否正确
    if sms_code !=redis_sms_code:
        return jsonify(errno=RET.DATAERR,errmsg="短信验证码填写错误")
    # 6删除redis中验证码数据
    try:
        redis_store.delete(redis_sms_code)
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="删除redis中短信数据失败")
    # 7创建用户对象
    user = User()
    # 8设置用户对象属性
    user.nick_name = mobile
    user.password = password
    user.mobile = mobile
    user.signature = "该用户很懒，什么都没写！"
    # 9保存用户信息到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify(errno=RET.DBERR,errmsg="用户注册失败")
    # 10返回响应
    return jsonify(errno=RET.OK,errmsg="注册成功")

@passport_blue.route("/image_code")
def get_image_code():
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")
    name, text, image_data = captcha.generate_captcha()
    # print("name:%s，text:%s,image_data:%s"%(name,text,image_data))
    try:
        redis_store.set("image_code:%s"%cur_id, text, IMAGE_CODE_REDIS_EXPIRES)
        if pre_id:
            redis_store.delete("image_code:%s"%pre_id)
    except Exception as e:
        current_app.logger.error(e)
        return "图片验证码加载失败！"

    response = make_response(image_data)
    response.headers["Content-Type"] = "image/png"
    return response

@passport_blue.route("/sms_code",methods=['POST'])
def sms_code():
    #1、获取参数
    json_data = request.data
    dict_data = json.loads(json_data)
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")
    #2、校验参数，图片验证码
    #校验参数存在空值
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")
    #校验手机格式
    if not re.match("1[3-9]\d{9}",mobile):
        return jsonify(errno=RET.DATAERR, errmsg="手机号填写错误")

    #从redis中取出验证码
    try:
        redis_image_code = redis_store.get("image_code:%s"%image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="操作redis数据库失败")
    #判断验证码是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg="图片验证码已经过期")
    #进行验证码的比较
    if image_code.upper() != redis_image_code.upper():
        return jsonify(errno=RET.DATAERR, errmsg="验证码填写错误")
    try:
        redis_store.delete("image_code:%s"%image_code_id)
    except Exception as e:
        current_app.lpgger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="删除redis数据失败")

    #发送短信，调用封装好的CPP
    sms_code = "%06d"%random.randint(0,999999)
    print(sms_code)
    # ccp = CCP()
    # result = ccp.send_template_sms(mobile, [sms_code, 5], 1)
    # #5、返回发送状态
    # if result == -1:
    #     return jsonify(error=RET.DATAERR,errmsg="短信发送失败")
    #将sms_code保存到redis中
    try:
        redis_store.set("sms_code:%s"%mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        return jsonify(errno=RET.DBERR, errmsg="手机验证码存储进redis失败")
    print("短信发送成功")
    return jsonify(errno=RET.OK, essmsg="短信发送成功")