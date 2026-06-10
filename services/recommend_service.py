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
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
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
                
                # 检查图片文件是否存在，不存在则使用默认图片
                image_path = item.get('image', '')
                if image_path:
                    # 将 /static/images/... 转换为实际文件路径
                    # 静态文件实际在 web_app/static/ 下
                    relative_path = os.path.join('web_app', image_path.lstrip('/'))
                    full_path = os.path.join(base_dir, relative_path)
                    if not os.path.exists(full_path):
                        # 根据图片路径判断使用哪个默认图片
                        if '/food/' in image_path:
                            item['image'] = '/static/images/food/default.jpg'
                        else:
                            item['image'] = '/static/images/spots/picture.jpg'
                else:
                    item['image'] = '/static/images/spots/picture.jpg'
                
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
            # 按评分排序，评分相同则按热度排序
            items.sort(key=lambda x: (x.get('rating', 0), x.get('popularity', 0)), reverse=True)
        else:
            # 按热度排序，热度相同则按评分排序
            items.sort(key=lambda x: (x.get('popularity', 0), x.get('rating', 0)), reverse=True)
        return items[:n]

    def get_spots(self, method='hot', n=6, preferences=None):
        """
        获取景点推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
            preferences: 用户偏好字典，含spot_types等
        
        Returns:
            景点列表，每项含: id, name, rating, popularity, category, location, image, rating_count
        """
        spots = self.get_spots_data()
        
        # 根据用户偏好过滤景点
        if preferences and preferences.get('spot_types'):
            preferred_types = preferences['spot_types']
            filtered_spots = []
            for spot in spots:
                # 分割类别字符串，注意CSV中是用逗号分隔的
                spot_categories = [cat.strip() for cat in spot.get('category', '').split(',')]
                # 检查景点的分类是否包含用户偏好的类型
                for category in spot_categories:
                    if category in preferred_types:
                        filtered_spots.append(spot)
                        break
            # 如果过滤结果不为空，使用过滤后的结果
            if filtered_spots:
                spots = filtered_spots
        
        return RecommendService._sort_and_limit(spots[:], method, n)
    
    def search_spots(self, query):
        """
        搜索景点
        
        Args:
            query: 搜索关键词
        
        Returns:
            匹配的景点列表
        """
        spots = self.get_spots_data()
        
        # 简单的模糊搜索
        results = []
        for spot in spots:
            if query in spot['name'] or query in spot['category']:
                results.append(spot)
        
        return results
    
    def search_universities(self, query):
        """
        搜索名校
        
        Args:
            query: 搜索关键词
        
        Returns:
            匹配的名校列表
        """
        universities = self.get_universities_data()
        
        # 简单的模糊搜索
        results = []
        for uni in universities:
            if query in uni['name'] or query in uni['category']:
                results.append(uni)
        
        return results
    
    def search_food(self, query):
        """
        搜索美食
        
        Args:
            query: 搜索关键词
        
        Returns:
            匹配的美食列表
        """
        food = self.get_food_data()
        
        # 简单的模糊搜索
        results = []
        for item in food:
            if query in item['name'] or query in item['category']:
                results.append(item)
        
        return results

    def get_food(self, method='hot', n=6, preferences=None):
        """
        获取美食推荐
        
        Args:
            method: 推荐方法 ('hot' 或 'rating')
            n: 返回数量
            preferences: 用户偏好字典，含cuisines等
        
        Returns:
            美食列表，每项含: id, name, rating, popularity, category, location, image, rating_count
        """
        food = self.get_food_data()
        
        # 根据用户偏好过滤美食
        if preferences and preferences.get('cuisines'):
            preferred_cuisines = preferences['cuisines']
            filtered_food = []
            for food_item in food:
                food_category = food_item.get('category', '').strip()
                if food_category in preferred_cuisines:
                    filtered_food.append(food_item)
            food = filtered_food or food  # 如果过滤后为空，返回全部美食
        
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
