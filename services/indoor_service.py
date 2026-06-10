#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
室内导航服务模块
"""

import json
import os
from collections import defaultdict
from config.settings import config


class IndoorService:
    """室内导航服务类"""
    
    def __init__(self):
        self.data = {}
        self.load_data()
    
    def load_data(self):
        """加载室内地图数据"""
        indoor_file = os.path.join(config.DATA_DIR, 'indoor.json')
        if os.path.exists(indoor_file):
            with open(indoor_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
    
    def get_buildings(self):
        """获取所有建筑列表"""
        buildings = []
        for building in self.data.get('buildings', []):
            buildings.append({
                'id': building['id'],
                'name': building['name'],
                'floors': [{'floor': f['floor'], 'name': f['name']} for f in building['floors']]
            })
        return buildings
    
    def get_building(self, building_id):
        """获取指定建筑详情"""
        for building in self.data.get('buildings', []):
            if building['id'] == building_id:
                return building
        return None
    
    def get_floor_nodes(self, building_id, floor):
        """获取指定楼层的节点"""
        building = self.get_building(building_id)
        if not building:
            return []
        
        for f in building.get('floors', []):
            if f['floor'] == floor:
                return f.get('nodes', [])
        return []
    
    def find_path(self, building_id, start_node_id, end_node_id):
        """
        寻找室内路径
        使用Dijkstra算法
        """
        building = self.get_building(building_id)
        if not building:
            return None
        
        # 构建图
        graph = defaultdict(list)
        all_nodes = {}
        
        # 添加各楼层节点和边
        for floor in building.get('floors', []):
            for node in floor.get('nodes', []):
                all_nodes[node['id']] = {**node, 'floor': floor['floor']}
            
            for edge in floor.get('edges', []):
                distance = edge['distance']
                graph[edge['from']].append((edge['to'], distance))
                graph[edge['to']].append((edge['from'], distance))
        
        # 添加楼层间连接
        for conn in building.get('connections', []):
            # 电梯/楼梯连接，距离设为固定值
            graph[conn['from']].append((conn['to'], 10))
            graph[conn['to']].append((conn['from'], 10))
        
        # Dijkstra算法
        import heapq
        
        distances = {node_id: float('inf') for node_id in all_nodes}
        distances[start_node_id] = 0
        previous = {node_id: None for node_id in all_nodes}
        
        heap = [(0, start_node_id)]
        
        while heap:
            current_dist, current_node = heapq.heappop(heap)
            
            if current_node == end_node_id:
                break
            
            if current_dist > distances[current_node]:
                continue
            
            for neighbor, weight in graph.get(current_node, []):
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(heap, (distance, neighbor))
        
        # 重构路径
        if distances[end_node_id] == float('inf'):
            return None
        
        path = []
        current = end_node_id
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        # 获取路径详细信息
        path_details = []
        for node_id in path:
            if node_id in all_nodes:
                path_details.append(all_nodes[node_id])
        
        return {
            'path': path_details,
            'total_distance': distances[end_node_id],
            'steps': len(path_details) - 1
        }
    
    def search_nodes(self, building_id, keyword):
        """搜索节点"""
        building = self.get_building(building_id)
        if not building:
            return []
        
        results = []
        for floor in building.get('floors', []):
            for node in floor.get('nodes', []):
                if keyword.lower() in node['name'].lower():
                    results.append({
                        'id': node['id'],
                        'name': node['name'],
                        'floor': floor['floor'],
                        'floor_name': floor['name'],
                        'type': node['type'],
                        'x': node['x'],
                        'y': node['y']
                    })
        return results
