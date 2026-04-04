#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
推荐服务模块

数据来源：data/raw/ 下的 CSV 文件（spots.csv / food.csv / universities.csv）
支持字段：name, rating, popularity, category, location, image, rating_count
"""

import csv
import os


class RecommendService:
    """推荐服务类"""

    def __init__(self):
        self._spots_cache = None
        self._food_cache = None
        self._universities_cache = None

    def _load_csv(self, filename, field_mapping, default_category='未知', default_location=''):
        """
        通用 CSV 加载方法，将中文列名映射为英文字段名
        
        Args:
            filename: CSV 文件相对路径（相对于 data/raw/）
            field_mapping: 列名映射字典 {csv列名: 目标字段名}
            default_category: 默认分类
            default_location: 默认地区
        
        Returns:
            数据列表
        """
        raw_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'raw', filename)
        
        if not os.path.exists(raw_path):
            return []
        
        items = []
        with open(raw_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                item = {'id': idx + 1}
                for csv_key, target_key in field_mapping.items():
                    value = row.get(csv_key, '').strip()
                    if target_key in ('rating', 'popularity', 'rating_count'):
                        try:
                            item[target_key] = float(value) if '.' in str(value) else int(value)
                        except (ValueError, TypeError):
                            item[target_key] = 0
                    else:
                        item[target_key] = value
                
                if not item.get('category'):
                    item['category'] = default_category
                if not item.get('location'):
                    item['location'] = default_location
                if not item.get('image'):
                    item['image'] = '/static/images/default.jpg'
                
                items.append(item)
        
        return items

    def get_spots_data(self):
        """获取景点原始数据（带缓存）"""
        if self._spots_cache is None:
            self._spots_cache = self._load_csv(
                'spots.csv',
                {
                    '名称': 'name',
                    '热度': 'popularity',
                    '评分': 'rating',
                    '评分人数': 'rating_count',
                    '标签': 'category',
                    '图片': 'image',
                },
                default_location='中国',
            )
        return self._spots_cache

    def get_food_data(self):
        """获取美食原始数据（带缓存）"""
        if self._food_cache is None:
            self._food_cache = self._load_csv(
                'food.csv',
                {
                    '名称': 'name',
                    '热度': 'popularity',
                    '评分': 'rating',
                    '评分人数': 'rating_count',
                    '分类': 'category',
                    '图片': 'image',
                },
                default_location='中国',
            )
        return self._food_cache

    def get_universities_data(self):
        """获取名校原始数据（带缓存）"""
        if self._universities_cache is None:
            self._universities_cache = self._load_csv(
                'universities.csv',
                {
                    '名称': 'name',
                    '热度': 'popularity',
                    '评分': 'rating',
                    '评分人数': 'rating_count',
                    '分类': 'category',
                    '地区': 'location',
                    '图片': 'image',
                },
                default_category='高等学府',
            )
        return self._universities_cache

    @staticmethod
    def _sort_and_limit(items, method, n):
        """
        排序并限制返回数量
        
        Args:
            items: 数据列表
            method: 排序方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            排序后的列表
        """
        if method == 'rating':
            items.sort(key=lambda x: x.get('rating', 0), reverse=True)
        else:
            items.sort(key=lambda x: x.get('popularity', 0), reverse=True)
        return items[:n]

    def get_spots(self, method='hot', n=6):
        """
        获取景点推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            景点列表，每项含: id, name, rating, popularity, category, location, image, rating_count
        """
        spots = self.get_spots_data()
        return RecommendService._sort_and_limit(spots[:], method, n)

    def get_food(self, method='hot', n=6):
        """
        获取美食推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            美食列表，每项含: id, name, rating, popularity, category, location, image, rating_count
        """
        food = self.get_food_data()
        return RecommendService._sort_and_limit(food[:], method, n)

    def get_universities(self, method='hot', n=6):
        """
        获取名校推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
        
        Returns:
            名校列表，每项含: id, name, rating, popularity, category, location, image, rating_count
        """
        universities = self.get_universities_data()
        return RecommendService._sort_and_limit(universities[:], method, n)


recommend_service = RecommendService()
