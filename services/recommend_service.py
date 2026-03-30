#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推荐服务模块
"""


class RecommendService:
    """推荐服务类"""
    
    @staticmethod
    def _sort_and_limit(items, method, n):
        """
        排序并限制返回数量（内部辅助方法）
        
        Args:
            items: 数据列表
            method: 排序方法
            n: 返回数量
        
        Returns:
            排序后的列表
        """
        if method == 'rating':
            items.sort(key=lambda x: x['rating'], reverse=True)
        else:
            items.sort(key=lambda x: x['popularity'], reverse=True)
        return items[:n]
    
    @staticmethod
    def get_spots(method='hot', n=6):
        """
        获取景点推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            景点列表
        """
        spots = [
            {"id": 1, "name": "故宫", "rating": 4.2, "popularity": 98, "category": "文化景点", "location": "北京市东城区"},
            {"id": 2, "name": "长城", "rating": 4.7, "popularity": 95, "category": "自然景点", "location": "北京市怀柔区"},
            {"id": 3, "name": "颐和园", "rating": 4.6, "popularity": 90, "category": "文化景点", "location": "北京市海淀区"},
            {"id": 4, "name": "天坛", "rating": 4.8, "popularity": 85, "category": "文化景点", "location": "北京市东城区"},
            {"id": 5, "name": "天安门", "rating": 4.5, "popularity": 99, "category": "文化景点", "location": "北京市东城区"},
            {"id": 6, "name": "圆明园", "rating": 4.4, "popularity": 80, "category": "文化景点", "location": "北京市海淀区"}
        ]
        return RecommendService._sort_and_limit(spots, method, n)
    
    @staticmethod
    def get_food(method='hot', n=6):
        """
        获取美食推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            美食列表
        """
        food = [
            {"id": 1, "name": "北京烤鸭", "rating": 4.8, "popularity": 95, "category": "烤鸭", "location": "北京市东城区"},
            {"id": 2, "name": "炸酱面", "rating": 4.5, "popularity": 85, "category": "面食", "location": "北京市西城区"},
            {"id": 3, "name": "豆汁", "rating": 4.0, "popularity": 70, "category": "传统小吃", "location": "北京市东城区"},
            {"id": 4, "name": "炒肝", "rating": 4.3, "popularity": 75, "category": "传统小吃", "location": "北京市东城区"},
            {"id": 5, "name": "卤煮火烧", "rating": 4.4, "popularity": 80, "category": "传统小吃", "location": "北京市西城区"},
            {"id": 6, "name": "涮羊肉", "rating": 4.6, "popularity": 88, "category": "火锅", "location": "北京市朝阳区"}
        ]
        return RecommendService._sort_and_limit(food, method, n)
    
    @staticmethod
    def get_universities(method='hot', n=6):
        """
        获取名校推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            名校列表
        """
        universities = [
            {"id": 1, "name": "北京大学", "rating": 4.9, "popularity": 98, "category": "高等学府", "location": "北京市海淀区"},
            {"id": 2, "name": "清华大学", "rating": 4.9, "popularity": 97, "category": "高等学府", "location": "北京市海淀区"},
            {"id": 3, "name": "复旦大学", "rating": 4.8, "popularity": 95, "category": "高等学府", "location": "上海市杨浦区"},
            {"id": 4, "name": "上海交通大学", "rating": 4.8, "popularity": 94, "category": "高等学府", "location": "上海市闵行区"},
            {"id": 5, "name": "浙江大学", "rating": 4.7, "popularity": 93, "category": "高等学府", "location": "浙江省杭州市"},
            {"id": 6, "name": "南京大学", "rating": 4.7, "popularity": 92, "category": "高等学府", "location": "江苏省南京市"}
        ]
        return RecommendService._sort_and_limit(universities, method, n)


recommend_service = RecommendService()
