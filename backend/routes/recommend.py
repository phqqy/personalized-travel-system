#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推荐服务路由模块
"""

from flask import Blueprint, request, jsonify, session
from services.recommend_service import recommend_service
from services.user_service import user_service

recommend_bp = Blueprint('recommend', __name__, url_prefix='/api/recommend')


@recommend_bp.route('/spots')
def recommend_spots():
    """获取景点推荐"""
    method = request.args.get('method', 'hot')
    # 处理n参数的非法输入，限制范围在1-20
    try:
        n = int(request.args.get('n', 6))
        n = max(1, min(n, 20))
    except (ValueError, TypeError):
        n = 6
    
    # 获取用户偏好
    preferences = None
    if 'user_id' in session:
        username = session['user_id']
        preferences = user_service.get_preferences(username)
        print(f"[DEBUG] 用户: {username}, 偏好: {preferences}")
    
    spots = recommend_service.get_spots(method, n, preferences)
    print(f"[DEBUG] 返回景点数量: {len(spots)}, 偏好: {preferences}")
    return jsonify(spots)


@recommend_bp.route('/food')
def recommend_food():
    """获取美食推荐"""
    method = request.args.get('method', 'hot')
    # 处理n参数的非法输入，限制范围在1-20
    try:
        n = int(request.args.get('n', 6))
        n = max(1, min(n, 20))
    except (ValueError, TypeError):
        n = 6
    
    # 获取用户偏好
    preferences = None
    if 'user_id' in session:
        username = session['user_id']
        preferences = user_service.get_preferences(username)
    
    food = recommend_service.get_food(method, n, preferences)
    return jsonify(food)


@recommend_bp.route('/universities')
def recommend_universities():
    """获取名校推荐"""
    method = request.args.get('method', 'hot')
    # 处理n参数的非法输入，限制范围在1-20
    try:
        n = int(request.args.get('n', 6))
        n = max(1, min(n, 20))
    except (ValueError, TypeError):
        n = 6
    
    universities = recommend_service.get_universities(method, n)
    return jsonify(universities)


@recommend_bp.route('/search')
def search_spots():
    """搜索景点"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify([])
    
    spots = recommend_service.search_spots(query)
    return jsonify(spots)


@recommend_bp.route('/search/universities')
def search_universities():
    """搜索名校"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify([])
    
    universities = recommend_service.search_universities(query)
    return jsonify(universities)


@recommend_bp.route('/search/food')
def search_food():
    """搜索美食"""
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify([])
    
    food = recommend_service.search_food(query)
    return jsonify(food)
