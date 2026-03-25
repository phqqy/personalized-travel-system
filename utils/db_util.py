#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库操作工具模块
"""

import sqlite3
import os


def get_db_connection(db_path):
    """
    获取数据库连接
    
    Args:
        db_path: 数据库文件路径
    
    Returns:
        数据库连接对象
    """
    # 确保数据库目录存在
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
    
    return conn


def init_database(db_path):
    """
    初始化数据库
    
    Args:
        db_path: 数据库文件路径
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建日记表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS diaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       热度 INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # 创建评分表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        diary_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        rating INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (diary_id) REFERENCES diaries (id),
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE (diary_id, user_id)
    )
    ''')
    
    # 创建评论表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        diary_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (diary_id) REFERENCES diaries (id),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()


def execute_query(db_path, query, params=()):
    """
    执行数据库查询
    
    Args:
        db_path: 数据库文件路径
        query: SQL查询语句
        params: 查询参数
    
    Returns:
        查询结果
    """
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()
    finally:
        conn.close()
