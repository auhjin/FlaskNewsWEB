# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:manager.py
@time:2021/06/16
"""

from flask import session

from info import creat_app

app = creat_app("develop")


if __name__ == "__main__":
    app.run()