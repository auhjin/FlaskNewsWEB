# -*- coding: UTF-8 -*-
"""
@author: auhjin
@file:manager.py
@time:2021/06/16
"""
from flask_script import Manager
from info import creat_app, db
from flask_migrate import Migrate, MigrateCommand

app = creat_app("develop")

manager = Manager(app)

Migrate(app, db)

manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()