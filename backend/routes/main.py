#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主页和页面路由模块
"""

from flask import Blueprint, render_template
from backend.decorators import login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首页"""
    return render_template('index.html')


@main_bp.route('/recommend')
@login_required
def recommend():
    """推荐页面"""
    return render_template('recommend.html')


@main_bp.route('/diary')
@login_required
def diary():
    """日记管理页面"""
    return render_template('diary.html')


@main_bp.route('/map')
@login_required
def map_page():
    """地图展示页面"""
    return render_template('map.html')


@main_bp.route('/spots')
def spots_page():
    """景点大全页面"""
    return render_template('spots.html')


@main_bp.route('/universities')
def universities_page():
    """名校游览页面"""
    return render_template('universities.html')


@main_bp.route('/food')
def food_page():
    """特色美食页面"""
    return render_template('food.html')
