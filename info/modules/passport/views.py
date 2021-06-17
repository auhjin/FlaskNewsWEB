# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:views.py
@time:2021/06/17
"""
from flask import request, current_app, make_response

from info import redis_store
from info.constants import IMAGE_CODE_REDIS_EXPIRES
from info.modules.passport import passport_blue
from info.utils.captcha.captcha import captcha


@passport_blue.route("/image_code")
def get_image_code():
    cur_id = request.args.get("cur_id")
    pre_id = request.args.get("pre_id")
    name, text, image_data = captcha.generate_captcha()
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