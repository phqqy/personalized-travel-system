#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
装饰器模块
"""

from functools import wraps
from flask import session, redirect, url_for


def login_required(f):
    """登录状态检查装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
