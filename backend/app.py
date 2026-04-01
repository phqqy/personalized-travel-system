#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
个性化旅游系统 - 后端主应用
"""

from flask import Flask
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import config
from services.user_service import user_service
from backend.routes.main import main_bp
from backend.routes.auth import auth_bp
from backend.routes.diary import diary_bp
from backend.routes.recommend import recommend_bp
from backend.routes.rating import rating_bp


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__, 
                static_folder=os.path.join(config.WEB_APP_DIR, 'static'),
                static_url_path='/static',
                template_folder=os.path.join(config.WEB_APP_DIR, 'templates'))
    
    app.secret_key = config.SECRET_KEY
    app.debug = config.DEBUG
    
    register_blueprints(app)
    
    return app


def register_blueprints(app):
    """注册所有蓝图"""
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(rating_bp)


def init_data():
    """初始化数据"""
    user_service.create_test_account()


app = create_app()


def main():
    """启动应用"""
    init_data()
    app.run(host=config.HOST, port=config.PORT)


if __name__ == '__main__':
    main()
