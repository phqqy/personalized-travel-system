#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记 ORM 模型（MySQL 预留）

当前状态：骨架文件，尚未启用
迁移完成后，diary_service.py 将从 dict 操作切换为 ORM 查询
ID 自增由 MySQL AUTO_INCREMENT 接管，不再需要 _next_ids 字典

依赖安装：
    pip install flask-sqlalchemy pymysql
"""

# from db import db
# from datetime import datetime
#
# class Diary(db.Model):
#     __tablename__ = 'diaries'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     title = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'title': self.title,
#             'content': self.content,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'updated_at': self.updated_at.isoformat() if self.updated_at else None,
#         }
