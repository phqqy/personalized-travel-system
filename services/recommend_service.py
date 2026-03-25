#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
旅游推荐服务模块
"""

from algorithms.sort import top_n_sort, dynamic_sort
from utils.data_loader import load_csv


class RecommendService:
    """旅游推荐服务"""
    
    def __init__(self, data_dir):
        """
        初始化推荐服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = data_dir
        self.spots_data = []
        self.load_data()
    
    def load_data(self):
        """加载景点数据"""
        spots_file = f"{self.data_dir}/raw/spots.csv"
        self.spots_data = load_csv(spots_file)
    
    def recommend_by_hot(self, n=10):
        """
        基于热度推荐景点
        
        Args:
            n: 推荐数量
        
        Returns:
            推荐景点列表
        """
        def hot_key(spot):
            try:
                return int(spot.get('热度', 0))
            except (ValueError, TypeError):
                return 0
        
        return top_n_sort(self.spots_data, hot_key, n)
    
    def recommend_by_rating(self, n=10):
        """
        基于评分推荐景点
        
        Args:
            n: 推荐数量
        
        Returns:
            推荐景点列表
        """
        def rating_key(spot):
            try:
                return float(spot.get('评分', 0))
            except (ValueError, TypeError):
                return 0
        
        return top_n_sort(self.spots_data, rating_key, n)
    
    def recommend_by_interest(self, interests, n=10):
        """
        基于用户兴趣推荐景点
        
        Args:
            interests: 用户兴趣列表
            n: 推荐数量
        
        Returns:
            推荐景点列表
        """
        def interest_key(spot):
            score = 0
            spot_tags = spot.get('标签', '').split(',')
            for interest in interests:
                if interest in spot_tags:
                    score += 1
            return score
        
        return top_n_sort(self.spots_data, interest_key, n)
    
    def recommend_personalized(self, user_preferences, n=10):
        """
        个性化推荐
        
        Args:
            user_preferences: 用户偏好（包含热度、评分、兴趣权重）
            n: 推荐数量
        
        Returns:
            推荐景点列表
        """
        def hot_key(spot):
            try:
                return int(spot.get('热度', 0))
            except (ValueError, TypeError):
                return 0
        
        def rating_key(spot):
            try:
                return float(spot.get('评分', 0))
            except (ValueError, TypeError):
                return 0
        
        def interest_key(spot):
            score = 0
            spot_tags = spot.get('标签', '').split(',')
            for interest in user_preferences.get('interests', []):
                if interest in spot_tags:
                    score += 1
            return score
        
        # 组合排序键
        key_funcs = [hot_key, rating_key, interest_key]
        weights = [
            user_preferences.get('hot_weight', 0.3),
            user_preferences.get('rating_weight', 0.4),
            user_preferences.get('interest_weight', 0.3)
        ]
        
        sorted_spots = dynamic_sort(self.spots_data, key_funcs, weights)
        return sorted_spots[:n]
