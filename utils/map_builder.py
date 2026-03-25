#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
道路图构建工具模块
"""

import networkx as nx
from utils.data_loader import load_csv


def build_graph(roads_file):
    """
    从道路数据构建图结构
    
    Args:
        roads_file: 道路数据CSV文件路径
    
    Returns:
        NetworkX图对象
    """
    # 创建有向图
    graph = nx.DiGraph()
    
    # 加载道路数据
    roads = load_csv(roads_file)
    
    # 添加边
    for road in roads:
        try:
            start = road['start']
            end = road['end']
            distance = float(road.get('distance', 1.0))
            speed = float(road.get('speed', 5.0))
            congestion = float(road.get('congestion', 1.0))
            
            # 计算权重（时间）
            time_weight = distance / (speed / congestion)
            
            # 添加边，同时添加距离和时间作为属性
            graph.add_edge(start, end, 
                         distance=distance, 
                         speed=speed, 
                         congestion=congestion, 
                         time=time_weight, 
                         weight=time_weight)  # 默认权重为时间
            
            # 添加反向边（双向道路）
            graph.add_edge(end, start, 
                         distance=distance, 
                         speed=speed, 
                         congestion=congestion, 
                         time=time_weight, 
                         weight=time_weight)
        except KeyError:
            # 跳过缺少必要字段的道路
            pass
    
    return graph


def build_indoor_graph(floors, nodes_per_floor, edges_per_floor):
    """
    构建室内导航图
    
    Args:
        floors: 楼层数
        nodes_per_floor: 每层节点数
        edges_per_floor: 每层边数
    
    Returns:
        NetworkX图对象
    """
    graph = nx.DiGraph()
    
    # 添加楼层内节点和边
    for floor in range(1, floors + 1):
        for node in range(1, nodes_per_floor + 1):
            node_id = f"node{node}_floor{floor}"
            graph.add_node(node_id, floor=floor)
        
        # 添加楼层内边
        for i in range(edges_per_floor):
            start = f"node{i % nodes_per_floor + 1}_floor{floor}"
            end = f"node{(i + 1) % nodes_per_floor + 1}_floor{floor}"
            graph.add_edge(start, end, weight=1.0)
            graph.add_edge(end, start, weight=1.0)
    
    # 添加楼层间连接（电梯/楼梯）
    for node in range(1, nodes_per_floor + 1):
        for floor in range(1, floors):
            start = f"node{node}_floor{floor}"
            end = f"node{node}_floor{floor + 1}"
            graph.add_edge(start, end, weight=2.0)  # 楼层转换权重稍高
            graph.add_edge(end, start, weight=2.0)
    
    return graph
