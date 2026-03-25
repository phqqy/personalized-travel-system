#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
排序算法模块
"""


def top_n_sort(items, key_func, n=10, reverse=True):
    """
    TopN不完全排序
    
    Args:
        items: 待排序的列表
        key_func: 排序键函数
        n: 返回前n个元素
        reverse: 是否降序排列
    
    Returns:
        排序后的前n个元素列表
    """
    # 使用堆排序的思想，只维护一个大小为n的堆
    import heapq
    
    if len(items) <= n:
        return sorted(items, key=key_func, reverse=reverse)
    
    # 构建小顶堆（如果是降序）或大顶堆（如果是升序）
    if reverse:
        # 降序，使用小顶堆
        heap = [(key_func(item), i, item) for i, item in enumerate(items[:n])]
        heapq.heapify(heap)
        
        for i, item in enumerate(items[n:], n):
            key = key_func(item)
            if key > heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (key, i, item))
        
        return [item for _, _, item in sorted(heap, key=lambda x: x[0], reverse=True)]
    else:
        # 升序，使用大顶堆（通过取负值实现）
        heap = [(-key_func(item), i, item) for i, item in enumerate(items[:n])]
        heapq.heapify(heap)
        
        for i, item in enumerate(items[n:], n):
            key = key_func(item)
            if key < -heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (-key, i, item))
        
        return [item for _, _, item in sorted(heap, key=lambda x: -x[0])]


def dynamic_sort(items, key_funcs, weights=None):
    """
    动态排序
    
    Args:
        items: 待排序的列表
        key_funcs: 多个排序键函数的列表
        weights: 每个排序键的权重列表
    
    Returns:
        排序后的列表
    """
    if not key_funcs:
        return items
    
    if weights is None:
        weights = [1.0] * len(key_funcs)
    
    def composite_key(item):
        """组合键函数"""
        return sum(w * kf(item) for w, kf in zip(weights, key_funcs))
    
    return sorted(items, key=composite_key, reverse=True)
