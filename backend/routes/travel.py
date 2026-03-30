#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
路线规划和查询服务路由模块
"""

from flask import Blueprint, request, jsonify
from services.path_service import path_service
from services.query_service import query_service

travel_bp = Blueprint('travel', __name__, url_prefix='/api')


@travel_bp.route('/path/plan', methods=['POST'])
def plan_path():
    """路线规划"""
    data = request.get_json()
    start = data.get('start')
    end = data.get('end')
    strategy = data.get('strategy', 'shortest')
    result = path_service.plan_path(start, end, strategy)
    return jsonify(result)


@travel_bp.route('/query/places', methods=['POST'])
def query_places():
    """场所查询"""
    data = request.get_json()
    keyword = data.get('keyword', '')
    category = data.get('category', 'all')
    location = data.get('location', '')
    places = query_service.get_places(keyword, category, location)
    return jsonify(places)
