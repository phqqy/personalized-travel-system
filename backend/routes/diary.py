#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记路由模块
"""

from flask import Blueprint, request, session, jsonify
from services.diary_service import diary_service
from backend.decorators import login_required

diary_bp = Blueprint('diary', __name__, url_prefix='/api')


@diary_bp.route('/diary', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def diary_operations():
    """日记CRUD操作"""
    username = session['user_id']
    
    if request.method == 'GET':
        diaries = diary_service.get_user_diaries(username)
        return jsonify(diaries)
    
    elif request.method == 'POST':
        data = request.json
        diary_id = diary_service.create_diary(
            username,
            data.get('title', ''),
            data.get('content', ''),
            data.get('date')
        )
        return jsonify({'id': diary_id})
    
    elif request.method == 'PUT':
        data = request.json
        diary_id = int(data.get('id', 0))
        success = diary_service.update_diary(
            username,
            diary_id,
            data.get('title'),
            data.get('content')
        )
        if success:
            return jsonify({'success': True})
        return jsonify({'error': 'Diary not found'}), 404
    
    elif request.method == 'DELETE':
        diary_id = int(request.args.get('id', 0))
        success = diary_service.delete_diary(username, diary_id)
        return jsonify({'success': success})


@diary_bp.route('/diary/export')
@login_required
def export_diary():
    """导出日记"""
    username = session['user_id']
    export_data = diary_service.export_diaries(username)
    return jsonify(export_data)


@diary_bp.route('/diary/import', methods=['POST'])
@login_required
def import_diary():
    """导入日记"""
    username = session['user_id']
    data = request.json
    
    if 'diaries' in data:
        count = diary_service.import_diaries(username, data['diaries'])
        return jsonify({'success': True, 'imported': count})
    
    return jsonify({'error': 'Invalid data'}), 400
