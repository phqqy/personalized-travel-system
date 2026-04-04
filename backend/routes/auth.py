#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户认证路由模块
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from services.user_service import user_service
from services.diary_service import diary_service
from backend.decorators import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """登录页面 - 兼容表单提交和API调用"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '')
            password = data.get('password', '')
        else:
            username = request.form['username']
            password = request.form['password']

        if user_service.verify_user(username, password):
            session['user_id'] = username
            user = user_service.get_user(username)
            session['user_name'] = user['name']
            if request.is_json:
                return jsonify({'success': True, 'message': '登录成功', 'redirect': '/'})
            return redirect(url_for('main.index'))
        else:
            error = '密码错误' if user_service.user_exists(username) else '用户不存在'
            if request.is_json:
                return jsonify({'success': False, 'error': error}), 400
            return render_template('auth.html', error=error)
    return render_template('auth.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """注册页面 - 兼容表单提交和API调用"""
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data.get('username', '')
            email = data.get('email', '')
            password = data.get('password', '')
            confirm_password = data.get('confirm_password', '')
        else:
            username = request.form['username']
            email = request.form.get('email', '')
            password = request.form['password']
            confirm_password = request.form['confirm_password']

        if user_service.user_exists(username):
            error = '用户名已存在'
            if request.is_json:
                return jsonify({'success': False, 'error': error}), 400
            return render_template('auth.html', error=error)

        if password != confirm_password:
            error = '两次密码不一致'
            if request.is_json:
                return jsonify({'success': False, 'error': error}), 400
            return render_template('auth.html', error=error)

        if user_service.create_user(username, email, password):
            diary_service.init_user_diaries(username)
            if request.is_json:
                return jsonify({'success': True, 'message': '注册成功，请登录'})
            return render_template('auth.html', success='注册成功，请登录')
    return render_template('auth.html')


@auth_bp.route('/logout')
def logout():
    """退出登录"""
    session.clear()
    return redirect(url_for('main.index'))


@auth_bp.route('/api/user/status')
def get_user_status():
    """获取用户登录状态API"""
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user_id': session['user_id'],
            'user_name': session.get('user_name', session['user_id'])
        })
    else:
        return jsonify({'logged_in': False})
