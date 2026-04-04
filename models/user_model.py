#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户 ORM 模型（MySQL 预留）

当前状态：骨架文件，尚未启用
迁移完成后，user_service.py 将从 dict 操作切换为 ORM 查询

依赖安装：
    pip install flask-sqlalchemy pymysql
"""

# from db import db
#
# class User(db.Model):
#     __tablename__ = 'users'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password_hash = db.Column(db.String(64), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     diaries = db.relationship('Diary', backref='user', lazy='dynamic', cascade='all, delete-orphan')
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'email': self.email,
#             'password_hash': self.password_hash,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None,
#         }
