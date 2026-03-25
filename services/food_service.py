#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
美食推荐服务模块
"""

from algorithms.sort import top_n_sort
from algorithms.search import fuzzy_search
from utils.data_loader import load_csv


class FoodService:
    """美食推荐服务"""
    
    def __init__(self, data_dir):
        """
        初始化美食服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.food_data = []
        self.load_data()
    
    def load_data(self):
        """加载美食数据"""
        food_file = f"{self.data_dir}/raw/food.csv"
        self.food_data = load_csv(food_file)
    
    def recommend_by_rating(self, n=10):
        """
        基于评分推荐美食
        
        Args:
            n: 推荐数量
        
        Returns:
            推荐美食列表
        """
        def rating_key(food):
            try:
                return float(food.get('评分', 0))
            except (ValueError, TypeError):
                return 0
        
        return top_n_sort(self.food_data, rating_key, n)
    
    def recommend_by_hot(self, n=10):
        """
        基于热度推荐美食
        
        Args:
            n: 推荐数量
        
        Returns:
            推荐美食列表
        """
        def hot_key(food):
            try:
                return int(food.get('热度', 0))
            except (ValueError, TypeError):
                return 0
        
        return top_n_sort(self.food_data, hot_key, n)
    
    def search_food(self, query):
        """
        搜索美食
        
        Args:
            query: 查询字符串
        
        Returns:
            美食列表
        """
        return fuzzy_search(self.food_data, query, key_func=lambda x: x.get('名称'))
    
    def recommend_by_category(self, category, n=10):
        """
        按分类推荐美食
        
        Args:
            category: 分类
            n: 推荐数量
        
        Returns:
            推荐美食列表
        """
        # 过滤分类
        filtered = [f for f in self.food_data if f.get('分类') == category]
        
        # 按评分排序
        def rating_key(food):
            try:
                return float(food.get('评分', 0))
            except (ValueError, TypeError):
                return 0
        
        return top_n_sort(filtered, rating_key, n)
