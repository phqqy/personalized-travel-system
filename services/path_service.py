#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
路线规划服务模块
"""


class PathService:
    """路线规划服务类"""
    
    @staticmethod
    def plan_path(start, end, strategy='shortest'):
        """
        规划路线
        
        Args:
            start: 起点
            end: 终点
            strategy: 策略 ('shortest', 'fastest', 'least_crowded')
        
        Returns:
            路线规划结果
        """
        path = [start, "中间点1", "中间点2", end]
        distance = 10000
        time = 30
        transport = "公共交通"
        
        if strategy == 'fastest':
            time = 20
            transport = "出租车"
        elif strategy == 'least_crowded':
            distance = 12000
            time = 40
            transport = "共享单车"
        
        return {
            "path": path,
            "distance": distance,
            "time": time,
            "transport": transport
        }


path_service = PathService()
