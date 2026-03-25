#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
路径规划算法模块
"""

import heapq


def dijkstra(graph, start, end, weight_func=lambda u, v, data: data.get('weight', 1)):
    """
    Dijkstra最短路径算法
    
    Args:
        graph: 图结构（NetworkX格式）
        start: 起点节点
        end: 终点节点
        weight_func: 计算边权重的函数
    
    Returns:
        (路径列表, 总权重)
    """
    # 优先队列，存储 (距离, 节点, 路径)
    priority_queue = [(0, start, [start])]
    # 已访问节点的最短距离
    distances = {start: 0}
    
    while priority_queue:
        current_distance, current_node, current_path = heapq.heappop(priority_queue)
        
        # 如果到达终点
        if current_node == end:
            return current_path, current_distance
        
        # 如果当前距离大于已知最短距离，跳过
        if current_distance > distances.get(current_node, float('inf')):
            continue
        
        # 遍历相邻节点
        for neighbor, data in graph[current_node].items():
            weight = weight_func(current_node, neighbor, data)
            distance = current_distance + weight
            
            # 如果找到更短的路径
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                new_path = current_path + [neighbor]
                heapq.heappush(priority_queue, (distance, neighbor, new_path))
    
    # 没有找到路径
    return None, float('inf')


def multi_point_path(graph, points, weight_func=lambda u, v, data: data.get('weight', 1)):
    """
    多点路径规划（旅行商问题近似解）
    
    Args:
        graph: 图结构（NetworkX格式）
        points: 要访问的点列表
        weight_func: 计算边权重的函数
    
    Returns:
        (路径列表, 总权重)
    """
    if not points:
        return [], 0
    
    # 简单的最近邻算法
    path = [points[0]]
    remaining = set(points[1:])
    total_weight = 0
    
    while remaining:
        current = path[-1]
        nearest = None
        min_distance = float('inf')
        best_subpath = []
        
        for point in remaining:
            subpath, distance = dijkstra(graph, current, point, weight_func)
            if distance < min_distance:
                min_distance = distance
                nearest = point
                best_subpath = subpath[1:]  # 去掉重复的起点
        
        if nearest:
            path.extend(best_subpath)
            total_weight += min_distance
            remaining.remove(nearest)
    
    return path, total_weight


def indoor_navigation(graph, start, end, start_floor, end_floor, weight_func=lambda u, v, data: data.get('weight', 1)):
    """
    室内导航
    
    Args:
        graph: 图结构（NetworkX格式）
        start: 起点节点
        end: 终点节点
        start_floor: 起点楼层
        end_floor: 终点楼层
        weight_func: 计算边权重的函数
    
    Returns:
        (路径列表, 总权重)
    """
    # 室内导航需要考虑楼层转换
    # 这里简化处理，假设存在电梯或楼梯连接不同楼层
    
    # 构建包含楼层信息的节点
    start_node = f"{start}_floor{start_floor}"
    end_node = f"{end}_floor{end_floor}"
    
    # 调用Dijkstra算法
    return dijkstra(graph, start_node, end_node, weight_func)
