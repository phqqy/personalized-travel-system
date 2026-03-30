#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据存储工具模块
"""

import pickle
import os


class DataStorage:
    """数据存储类，用于处理pickle文件的读写"""
    
    @staticmethod
    def load_data(file_path, default_value=None):
        """
        从pickle文件加载数据
        
        Args:
            file_path: 文件路径
            default_value: 默认值（如果文件不存在或加载失败）
        
        Returns:
            加载的数据或默认值
        """
        try:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return default_value if default_value is not None else {}
    
    @staticmethod
    def save_data(file_path, data):
        """
        保存数据到pickle文件
        
        Args:
            file_path: 文件路径
            data: 要保存的数据
        """
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception:
            return False
