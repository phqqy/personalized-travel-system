#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
系统配置模块
"""

import os


class Config:
    """系统配置类"""
    
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Web应用目录
    WEB_APP_DIR = os.path.join(BASE_DIR, 'web_app')
    
    # 数据目录
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    DB_DIR = os.path.join(DATA_DIR, 'db')
    RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
    
    # Flask配置
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # 数据文件路径
    USER_DATA_FILE = os.path.join(DB_DIR, 'user_data.pkl')
    DIARY_DATA_FILE = os.path.join(DB_DIR, 'diary_data.pkl')
    RATING_DATA_FILE = os.path.join(DB_DIR, 'ratings.pkl')
    
    # 静态文件配置
    STATIC_FOLDER = 'static'
    STATIC_URL_PATH = '/static'
    TEMPLATE_FOLDER = 'templates'


config = Config()
