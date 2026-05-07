#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户偏好设置路由模块
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from services.user_service import user_service
from backend.decorators import login_required

preferences_bp = Blueprint('preferences', __name__)


@preferences_bp.route('/preferences', methods=['GET'])
@login_required
def preferences():
    """用户偏好设置页面"""
    return render_template('preferences.html')


@preferences_bp.route('/api/preferences', methods=['POST'])
@login_required
def save_preferences():
    """保存用户偏好API"""
    if not request.is_json:
        return jsonify({'success': False, 'error': '请求格式错误'}), 400
    
    data = request.get_json()
    username = session['user_id']
    
    preferences = {
        'spot_types': data.get('spot_types', []),
        'cuisines': data.get('cuisines', []),
        'restaurant_types': data.get('restaurant_types', [])
    }
    
    if user_service.set_preferences(username, preferences):
        session['preferences_set'] = True
        return jsonify({'success': True, 'message': '偏好设置成功'})
    else:
        return jsonify({'success': False, 'error': '保存失败'}), 500


@preferences_bp.route('/api/preferences', methods=['GET'])
@login_required
def get_preferences():
    """获取用户偏好API"""
    username = session['user_id']
    preferences = user_service.get_preferences(username)
    return jsonify({'success': True, 'preferences': preferences})