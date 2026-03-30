#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
场所查询服务模块
"""


class QueryService:
    """场所查询服务类"""
    
    @staticmethod
    def get_places(keyword='', category='all', location=''):
        """
        查询场所
        
        Args:
            keyword: 关键词
            category: 分类 ('all', '景点', '餐厅', '酒店', '购物', '交通')
            location: 位置
        
        Returns:
            场所列表
        """
        places = [
            {"name": "故宫", "category": "景点", "location": "北京市东城区", "rating": 4.8, "description": "中国明清两代的皇家宫殿"},
            {"name": "长城", "category": "景点", "location": "北京市怀柔区", "rating": 4.7, "description": "中国古代伟大的防御工程"},
            {"name": "颐和园", "category": "景点", "location": "北京市海淀区", "rating": 4.6, "description": "中国古典园林"},
            {"name": "全聚德烤鸭店", "category": "餐厅", "location": "北京市东城区", "rating": 4.5, "description": "著名的北京烤鸭店"},
            {"name": "北京饭店", "category": "酒店", "location": "北京市东城区", "rating": 4.6, "description": "豪华五星级酒店"},
            {"name": "王府井步行街", "category": "购物", "location": "北京市东城区", "rating": 4.4, "description": "著名的商业街"},
            {"name": "北京站", "category": "交通", "location": "北京市东城区", "rating": 4.3, "description": "重要的铁路枢纽"},
            {"name": "北京南站", "category": "交通", "location": "北京市丰台区", "rating": 4.4, "description": "现代化高铁站"}
        ]
        
        filtered_places = []
        for place in places:
            if keyword and keyword not in place['name']:
                continue
            if category != 'all' and place['category'] != category:
                continue
            if location and location not in place['location']:
                continue
            filtered_places.append(place)
        
        return filtered_places


query_service = QueryService()
