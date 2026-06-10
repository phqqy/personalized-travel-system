#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
地图相关API路由模块
"""

from flask import Blueprint, jsonify, request
from config.settings import config
from services.indoor_service import IndoorService

map_bp = Blueprint('map', __name__)
indoor_service = IndoorService()


@map_bp.route('/api/map/amap/config', methods=['GET'])
def api_get_amap_config():
    """获取高德地图API配置"""
    try:
        return jsonify({
            'success': True,
            'api_key': config.AMAP_API_KEY,
            'security_code': config.AMAP_SECURITY_CODE
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@map_bp.route('/api/map/indoor/buildings', methods=['GET'])
def api_get_indoor_buildings():
    """获取所有室内建筑列表"""
    try:
        buildings = indoor_service.get_buildings()
        return jsonify({
            'success': True,
            'buildings': buildings
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@map_bp.route('/api/map/indoor/building/<building_id>', methods=['GET'])
def api_get_indoor_building(building_id):
    """获取指定建筑详情"""
    try:
        building = indoor_service.get_building(building_id)
        if building:
            return jsonify({
                'success': True,
                'building': building
            })
        else:
            return jsonify({'success': False, 'error': '建筑不存在'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@map_bp.route('/api/map/indoor/floor/<building_id>/<int:floor>', methods=['GET'])
def api_get_indoor_floor(building_id, floor):
    """获取指定楼层节点"""
    try:
        nodes = indoor_service.get_floor_nodes(building_id, floor)
        return jsonify({
            'success': True,
            'nodes': nodes,
            'floor': floor
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@map_bp.route('/api/map/indoor/path', methods=['POST'])
def api_get_indoor_path():
    """获取室内导航路径"""
    try:
        data = request.get_json()
        building_id = data.get('building_id')
        start_node_id = data.get('start_node_id')
        end_node_id = data.get('end_node_id')
        
        result = indoor_service.find_path(building_id, start_node_id, end_node_id)
        
        if result:
            return jsonify({
                'success': True,
                'path': result['path'],
                'total_distance': result['total_distance'],
                'steps': result['steps']
            })
        else:
            return jsonify({'success': False, 'error': '无法找到路径'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@map_bp.route('/api/map/indoor/search', methods=['GET'])
def api_search_indoor_nodes():
    """搜索室内节点"""
    try:
        building_id = request.args.get('building_id')
        keyword = request.args.get('keyword', '')
        
        results = indoor_service.search_nodes(building_id, keyword)
        return jsonify({
            'success': True,
            'nodes': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
