#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据加载工具模块
"""

import csv
import os
import pickle
import yaml


def load_csv(file_path):
    """
    加载CSV文件
    
    Args:
        file_path: CSV文件路径
    
    Returns:
        数据列表
    """
    data = []
    if not os.path.exists(file_path):
        return data
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    return data


def load_graph(file_path):
    """
    加载图结构
    
    Args:
        file_path: 图文件路径
    
    Returns:
        图对象
    """
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'rb') as f:
        graph = pickle.load(f)
    
    return graph


def save_graph(graph, file_path):
    """
    保存图结构
    
    Args:
        graph: 图对象
        file_path: 保存路径
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(graph, f)


def load_config(config_file):
    """
    加载配置文件
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        配置字典
    """
    if not os.path.exists(config_file):
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config
