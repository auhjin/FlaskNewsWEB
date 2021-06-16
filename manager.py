# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:manager.py
@time:2021/06/16
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config(object):
    DEBUG = True

    SQLAlCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/phm"
    SQOAOCHEMY_TRACK_MODIFICATIONS = False

app.config.from_object(Config)

db = SQLAlchemy(app)

def hellp_world():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)