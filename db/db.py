#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库初始化模块（MySQL 预留）

当前状态：骨架文件，尚未启用
迁移完成后，backend/app.py 将调用 init_db(app) 初始化 SQLAlchemy

使用方式（迁移完成后取消注释）：
    from db import db, init_db
    在 app.py 的 create_app() 中：
        init_db(app)

依赖安装：
    pip install flask-sqlalchemy pymysql

MySQL 建表参考 DDL（详见 整体架构.md §4.2）：
    CREATE DATABASE travel_system DEFAULT CHARSET utf8mb4;
    CREATE TABLE users (...);
    CREATE TABLE diaries(...);
"""

# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
#
# def init_db(app):
#     db.init_app(app)
#
#     with app.app_context():
#         db.create_all()
#         print("MySQL 数据库连接成功，表已就绪")
