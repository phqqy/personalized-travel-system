#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推荐服务路由模块
"""

from flask import Blueprint, request, jsonify
from services.recommend_service import recommend_service

recommend_bp = Blueprint('recommend', __name__, url_prefix='/api/recommend')


@recommend_bp.route('/spots')
def recommend_spots():
    """获取景点推荐"""
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    spots = recommend_service.get_spots(method, n)
    return jsonify(spots)


@recommend_bp.route('/food')
def recommend_food():
    """获取美食推荐"""
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    food = recommend_service.get_food(method, n)
    return jsonify(food)


@recommend_bp.route('/universities')
def recommend_universities():
    """获取名校推荐"""
    method = request.args.get('method', 'hot')
    n = int(request.args.get('n', 6))
    universities = recommend_service.get_universities(method, n)
    return jsonify(universities)
