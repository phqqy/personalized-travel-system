#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
路线规划服务模块
"""

from algorithms.path import dijkstra, multi_point_path, indoor_navigation
from utils.map_builder import build_graph
from utils.data_loader import load_graph, save_graph
import os


class PathService:
    """路线规划服务"""
    
    def __init__(self, data_dir):
        """
        初始化路径服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.graph = None
        self.indoor_graph = None
        self.load_graphs()
    
    def load_graphs(self):
        """加载图结构"""
        # 加载景区路网
        graph_file = f"{self.data_dir}/graph/scenic_graph.gpickle"
        if os.path.exists(graph_file):
            self.graph = load_graph(graph_file)
        else:
            # 如果图文件不存在，从道路数据构建
            roads_file = f"{self.data_dir}/raw/roads.csv"
            if os.path.exists(roads_file):
                self.graph = build_graph(roads_file)
                save_graph(self.graph, graph_file)
    
    def plan_route(self, start, end, strategy='shortest', transport='walk'):
        """
        规划路线
        
        Args:
            start: 起点
            end: 终点
            strategy: 规划策略（shortest, fastest, least_congestion）
            transport: 交通工具（walk, bike, car）
        
        Returns:
            (路径列表, 总权重)
        """
        if not self.graph:
            return None, float('inf')
        
        # 根据策略选择权重函数
        def weight_func(u, v, data):
            if strategy == 'shortest':
                return data.get('distance', 1.0)
            elif strategy == 'fastest':
                return data.get('time', 1.0)
            elif strategy == 'least_congestion':
                return data.get('congestion', 1.0) * data.get('distance', 1.0)
            else:
                return data.get('weight', 1.0)
        
        return dijkstra(self.graph, start, end, weight_func)
    
    def plan_multi_point_route(self, points, strategy='shortest', transport='walk'):
        """
        多点路径规划
        
        Args:
            points: 要访问的点列表
            strategy: 规划策略
            transport: 交通工具
        
        Returns:
            (路径列表, 总权重)
        """
        if not self.graph:
            return None, float('inf')
        
        # 根据策略选择权重函数
        def weight_func(u, v, data):
            if strategy == 'shortest':
                return data.get('distance', 1.0)
            elif strategy == 'fastest':
                return data.get('time', 1.0)
            elif strategy == 'least_congestion':
                return data.get('congestion', 1.0) * data.get('distance', 1.0)
            else:
                return data.get('weight', 1.0)
        
        return multi_point_path(self.graph, points, weight_func)
    
    def plan_indoor_route(self, start, end, start_floor, end_floor):
        """
        室内导航
        
        Args:
            start: 起点
            end: 终点
            start_floor: 起点楼层
            end_floor: 终点楼层
        
        Returns:
            (路径列表, 总权重)
        """
        # 加载室内图
        if not self.indoor_graph:
            # 这里简化处理，实际应该从文件加载
            from utils.map_builder import build_indoor_graph
            self.indoor_graph = build_indoor_graph(5, 20, 30)
        
        return indoor_navigation(self.indoor_graph, start, end, start_floor, end_floor)
