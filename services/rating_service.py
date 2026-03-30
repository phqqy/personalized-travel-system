#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
评分服务模块
"""

import os
from datetime import datetime
from config.settings import config
from utils.storage import DataStorage


class RatingService:
    """评分服务类"""
    
    def __init__(self):
        self.ratings = DataStorage.load_data(
            os.path.join(os.path.dirname(config.USER_DATA_FILE), 'ratings.pkl'),
            {}
        )
    
    def _save(self):
        """保存评分数据"""
        DataStorage.save_data(
            os.path.join(os.path.dirname(config.USER_DATA_FILE), 'ratings.pkl'),
            self.ratings
        )
    
    def add_rating(self, username, target_type, target_id, rating, comment=''):
        """
        添加评分
        
        Args:
            username: 用户名
            target_type: 评分目标类型 ('spot', 'food', 'diary', 'university')
            target_id: 目标ID
            rating: 评分 (1-5)
            comment: 评论（可选）
        
        Returns:
            是否成功
        """
        if rating < 1 or rating > 5:
            return False
        
        key = f"{target_type}_{target_id}"
        if key not in self.ratings:
            self.ratings[key] = []
        
        rating_data = {
            'username': username,
            'rating': rating,
            'comment': comment,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.ratings[key].append(rating_data)
        self._save()
        return True
    
    def get_ratings(self, target_type, target_id):
        """
        获取某个目标的所有评分
        
        Args:
            target_type: 评分目标类型
            target_id: 目标ID
        
        Returns:
            评分列表
        """
        key = f"{target_type}_{target_id}"
        return self.ratings.get(key, [])
    
    def get_average_rating(self, target_type, target_id):
        """
        获取某个目标的平均评分
        
        Args:
            target_type: 评分目标类型
            target_id: 目标ID
        
        Returns:
            平均评分
        """
        ratings = self.get_ratings(target_type, target_id)
        if not ratings:
            return 0.0
        return sum(r['rating'] for r in ratings) / len(ratings)
    
    def get_user_rating(self, username, target_type, target_id):
        """
        获取某个用户对某个目标的评分
        
        Args:
            username: 用户名
            target_type: 评分目标类型
            target_id: 目标ID
        
        Returns:
            评分数据或None
        """
        key = f"{target_type}_{target_id}"
        ratings = self.ratings.get(key, [])
        for r in ratings:
            if r['username'] == username:
                return r
        return None
    
    def delete_rating(self, username, target_type, target_id):
        """
        删除评分
        
        Args:
            username: 用户名
            target_type: 评分目标类型
            target_id: 目标ID
        
        Returns:
            是否成功
        """
        key = f"{target_type}_{target_id}"
        if key not in self.ratings:
            return False
        
        original_length = len(self.ratings[key])
        self.ratings[key] = [r for r in self.ratings[key] if r['username'] != username]
        
        if len(self.ratings[key]) != original_length:
            self._save()
            return True
        return False
    
    def get_top_rated(self, target_type, n=10):
        """
        获取评分最高的目标
        
        Args:
            target_type: 评分目标类型
            n: 返回数量
        
        Returns:
            按平均评分排序的目标列表
        """
        target_ratings = []
        for key, ratings in self.ratings.items():
            if key.startswith(f"{target_type}_"):
                target_id = key.split('_')[1]
                avg_rating = self.get_average_rating(target_type, target_id)
                target_ratings.append({
                    'target_id': target_id,
                    'average_rating': avg_rating,
                    'rating_count': len(ratings)
                })
        
        target_ratings.sort(key=lambda x: x['average_rating'], reverse=True)
        return target_ratings[:n]


rating_service = RatingService()
