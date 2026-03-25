#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
场所查询服务模块
"""

from algorithms.search import fuzzy_search, exact_search
from utils.data_loader import load_csv


class QueryService:
    """场所查询服务"""
    
    def __init__(self, data_dir):
        """
        初始化查询服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.facilities_data = []
        self.spots_data = []
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        # 加载设施数据
        facilities_file = f"{self.data_dir}/raw/facilities.csv"
        self.facilities_data = load_csv(facilities_file)
        
        # 加载景点数据
        spots_file = f"{self.data_dir}/raw/spots.csv"
        self.spots_data = load_csv(spots_file)
    
    def query_nearby(self, location, radius=1000, categories=None):
        """
        查询附近设施
        
        Args:
            location: 位置（坐标或地点名称）
            radius: 搜索半径（米）
            categories: 分类过滤
        
        Returns:
            附近设施列表
        """
        # 这里简化处理，实际应该根据坐标计算距离
        # 目前返回所有设施，按距离排序（模拟）
        
        def distance_key(facility):
            try:
                # 模拟距离计算
                return float(facility.get('distance', 9999))
            except (ValueError, TypeError):
                return 9999
        
        # 过滤分类
        filtered = self.facilities_data
        if categories:
            filtered = [f for f in filtered if f.get('分类') in categories]
        
        # 按距离排序
        filtered.sort(key=distance_key)
        
        # 返回在半径内的设施
        return [f for f in filtered if distance_key(f) <= radius]
    
    def query_by_category(self, category):
        """
        按分类查询设施
        
        Args:
            category: 分类
        
        Returns:
            设施列表
        """
        return exact_search(self.facilities_data, category, key_func=lambda x: x.get('分类'))
    
    def search_spots(self, query):
        """
        搜索景点
        
        Args:
            query: 查询字符串
        
        Returns:
            景点列表
        """
        return fuzzy_search(self.spots_data, query, key_func=lambda x: x.get('名称'))
    
    def search_facilities(self, query):
        """
        搜索设施
        
        Args:
            query: 查询字符串
        
        Returns:
            设施列表
        """
        return fuzzy_search(self.facilities_data, query, key_func=lambda x: x.get('名称'))
