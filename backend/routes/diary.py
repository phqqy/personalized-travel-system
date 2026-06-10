#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
日记路由模块
支持：全局共享、点赞、评论
"""

from flask import Blueprint, request, session, jsonify
from services.diary_service import diary_service
from backend.decorators import login_required

diary_bp = Blueprint('diary', __name__, url_prefix='/api')


# ==================== 日记 CRUD ====================

@diary_bp.route('/diary', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def diary_operations():
    """日记CRUD操作 —— GET 返回所有用户的日记（全局共享）"""
    username = session['user_id']

    if request.method == 'GET':
        # 返回所有用户的日记（全局共享）
        sort = request.args.get('sort', 'time')
        all_diaries = diary_service.get_all_diaries(sort=sort)
        return jsonify(all_diaries)

    elif request.method == 'POST':
        data = request.json
        diary_id, global_id = diary_service.create_diary(
            username,
            data.get('title', ''),
            data.get('content', ''),
            data.get('date')
        )
        return jsonify({'id': diary_id, 'global_id': global_id})

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


@diary_bp.route('/diary/<global_id>', methods=['GET'])
@login_required
def get_diary(global_id):
    """通过 global_id 获取单个日记"""
    diary, owner = diary_service.get_diary_by_global_id(global_id)
    if diary:
        gid = diary.get('global_id', '')
        diary_copy = dict(diary)
        diary_copy['like_count'] = len(diary_service.likes.get(gid, []))
        diary_copy['comment_count'] = len(diary_service.comments.get(gid, []))
        # 增加浏览量
        diary_service.increment_view(gid)
        return jsonify(diary_copy)
    return jsonify({'error': 'Diary not found'}), 404


# ==================== 点赞 ====================

@diary_bp.route('/diary/<global_id>/like', methods=['POST'])
@login_required
def toggle_like(global_id):
    """切换点赞状态"""
    username = session['user_id']
    liked, count = diary_service.toggle_like(username, global_id)

    if liked is None:
        return jsonify({'error': 'Diary not found'}), 404

    return jsonify({
        'success': True,
        'liked': liked,
        'like_count': count
    })


@diary_bp.route('/diary/likes/batch', methods=['POST'])
@login_required
def batch_like_status():
    """批量获取点赞状态"""
    username = session['user_id']
    data = request.json
    global_ids = data.get('global_ids', [])
    result = diary_service.get_likes_batch(username, global_ids)
    return jsonify({'likes': result})


# ==================== 评论 ====================

@diary_bp.route('/diary/<global_id>/comments', methods=['GET', 'POST'])
@login_required
def diary_comments(global_id):
    """获取或添加评论"""
    username = session['user_id']

    if request.method == 'GET':
        comments = diary_service.get_comments(global_id)
        return jsonify({'comments': comments})

    elif request.method == 'POST':
        data = request.json
        content = data.get('content', '').strip()
        if not content:
            return jsonify({'error': '评论内容不能为空'}), 400

        comment = diary_service.add_comment(username, global_id, content)
        if comment is None:
            return jsonify({'error': 'Diary not found'}), 404

        return jsonify({'success': True, 'comment': comment})


@diary_bp.route('/diary/<global_id>/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(global_id, comment_id):
    """删除评论（仅作者可删）"""
    username = session['user_id']
    success = diary_service.delete_comment(username, global_id, comment_id)
    if success:
        return jsonify({'success': True})
    return jsonify({'error': 'Comment not found or permission denied'}), 403


# ==================== 导出/导入 ====================

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
