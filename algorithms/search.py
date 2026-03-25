#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
查找算法模块
"""


def exact_search(items, query, key_func=lambda x: x):
    """
    精确查找
    
    Args:
        items: 待查找的列表
        query: 查询字符串
        key_func: 从列表元素中提取用于比较的键的函数
    
    Returns:
        匹配的元素列表
    """
    return [item for item in items if key_func(item) == query]


def fuzzy_search(items, query, key_func=lambda x: x, threshold=0.6):
    """
    模糊查找
    
    Args:
        items: 待查找的列表
        query: 查询字符串
        key_func: 从列表元素中提取用于比较的键的函数
        threshold: 相似度阈值
    
    Returns:
        匹配的元素列表，按相似度排序
    """
    def levenshtein_distance(s1, s2):
        """计算编辑距离"""
        if len(s1) < len(s2):
            return levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def similarity(s1, s2):
        """计算字符串相似度"""
        distance = levenshtein_distance(s1, s2)
        max_len = max(len(s1), len(s2))
        return 1 - (distance / max_len)
    
    results = []
    for item in items:
        key = str(key_func(item))
        sim = similarity(key, query)
        if sim >= threshold:
            results.append((item, sim))
    
    # 按相似度排序
    results.sort(key=lambda x: x[1], reverse=True)
    return [item for item, _ in results]


def prefix_search(items, query, key_func=lambda x: x):
    """
    前缀匹配查找
    
    Args:
        items: 待查找的列表
        query: 查询字符串
        key_func: 从列表元素中提取用于比较的键的函数
    
    Returns:
        匹配的元素列表
    """
    return [item for item in items if str(key_func(item)).startswith(query)]


def suffix_search(items, query, key_func=lambda x: x):
    """
    后缀匹配查找
    
    Args:
        items: 待查找的列表
        query: 查询字符串
        key_func: 从列表元素中提取用于比较的键的函数
    
    Returns:
        匹配的元素列表
    """
    return [item for item in items if str(key_func(item)).endswith(query)]
