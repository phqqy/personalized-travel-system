#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
评分服务路由模块
"""

from flask import Blueprint, request, session, jsonify
from services.rating_service import rating_service
from backend.decorators import login_required

rating_bp = Blueprint('rating', __name__, url_prefix='/api/rating')


@rating_bp.route('/add', methods=['POST'])
@login_required
def add_rating():
    """添加评分"""
    username = session['user_id']
    data = request.json
    
    target_type = data.get('target_type')
    target_id = data.get('target_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not target_type or not target_id or not rating:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    success = rating_service.add_rating(username, target_type, target_id, rating, comment)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Invalid rating (must be 1-5)'}), 400


@rating_bp.route('/<target_type>/<target_id>')
def get_ratings(target_type, target_id):
    """获取某个目标的所有评分"""
    ratings = rating_service.get_ratings(target_type, target_id)
    avg_rating = rating_service.get_average_rating(target_type, target_id)
    return jsonify({
        'ratings': ratings,
        'average_rating': avg_rating,
        'rating_count': len(ratings)
    })


@rating_bp.route('/<target_type>/<target_id>/average')
def get_average_rating(target_type, target_id):
    """获取某个目标的平均评分"""
    avg_rating = rating_service.get_average_rating(target_type, target_id)
    return jsonify({'average_rating': avg_rating})


@rating_bp.route('/my/<target_type>/<target_id>')
@login_required
def get_my_rating(target_type, target_id):
    """获取当前用户的评分"""
    username = session['user_id']
    rating = rating_service.get_user_rating(username, target_type, target_id)
    if rating:
        return jsonify(rating)
    return jsonify({'rating': None})


@rating_bp.route('/<target_type>/<target_id>', methods=['DELETE'])
@login_required
def delete_rating(target_type, target_id):
    """删除评分"""
    username = session['user_id']
    success = rating_service.delete_rating(username, target_type, target_id)
    return jsonify({'success': success})


@rating_bp.route('/top/<target_type>')
def get_top_rated(target_type):
    """获取评分最高的目标"""
    n = int(request.args.get('n', 10))
    top_rated = rating_service.get_top_rated(target_type, n)
    return jsonify(top_rated)
