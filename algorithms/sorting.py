#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
排序算法模块
包含: 快速、归并、堆、插入、计数、桶排序
"""

from typing import List, Any, Callable, Optional


def quick_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    快速排序（原地，返回排序后列表）
    平均 O(n log n)，最坏 O(n²)
    """
    arr = arr[:]
    _quick_sort(arr, 0, len(arr) - 1, key or (lambda x: x))
    return arr


def _quick_sort(arr, lo, hi, key):
    if lo >= hi:
        return
    pivot = _partition(arr, lo, hi, key)
    _quick_sort(arr, lo, pivot - 1, key)
    _quick_sort(arr, pivot + 1, hi, key)


def _partition(arr, lo, hi, key):
    pivot_val = key(arr[hi])
    i = lo
    for j in range(lo, hi):
        if key(arr[j]) <= pivot_val:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def merge_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    归并排序（稳定）
    O(n log n) 时间，O(n) 空间
    """
    key = key or (lambda x: x)
    if len(arr) <= 1:
        return arr[:]

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    return _merge(left, right, key)


def _merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def heap_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    堆排序
    O(n log n) 时间，O(1) 额外空间
    """
    import heapq
    key = key or (lambda x: x)
    indexed = [(key(v), i, v) for i, v in enumerate(arr)]
    heapq.heapify(indexed)
    return [heapq.heappop(indexed)[2] for _ in range(len(indexed))]


def insertion_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """
    插入排序 — 小数据量或近乎有序时表现优异
    O(n²) 最坏，O(n) 最好
    """
    arr = arr[:]
    key = key or (lambda x: x)
    for i in range(1, len(arr)):
        cur = arr[i]
        cur_key = key(cur)
        j = i - 1
        while j >= 0 and key(arr[j]) > cur_key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = cur
    return arr


def selection_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """选择排序"""
    arr = arr[:]
    key = key or (lambda x: x)
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if key(arr[j]) < key(arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def bubble_sort(arr: List[Any], key: Optional[Callable] = None) -> List[Any]:
    """冒泡排序（带提前终止优化）"""
    arr = arr[:]
    key = key or (lambda x: x)
    for i in range(len(arr)):
        swapped = False
        for j in range(len(arr) - 1 - i):
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def counting_sort(arr: List[int], max_val: Optional[int] = None) -> List[int]:
    """
    计数排序 — 仅适用于非负整数
    O(n + k) 时间
    """
    if not arr:
        return []
    if max_val is None:
        max_val = max(arr)
    counts = [0] * (max_val + 1)
    for v in arr:
        counts[v] += 1
    result = []
    for v in range(max_val + 1):
        result.extend([v] * counts[v])
    return result


def bucket_sort(arr: List[float], bucket_count: int = 10) -> List[float]:
    """
    桶排序 — 适用于 [0, 1) 范围的浮点数
    O(n + k) 平均时间
    """
    if not arr:
        return []
    buckets = [[] for _ in range(bucket_count)]
    for v in arr:
        idx = min(int(v * bucket_count), bucket_count - 1)
        buckets[idx].append(v)
    result = []
    for b in buckets:
        result.extend(sorted(b))
    return result


def merge_sorted_lists(lists: List[List[int]]) -> List[int]:
    """
    合并 K 个有序列表（使用最小堆）
    O(N log K)
    """
    import heapq
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    result = []

    while heap:
        val, li, idx = heapq.heappop(heap)
        result.append(val)
        if idx + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][idx + 1], li, idx + 1))
    return result


# ==================== 测试 ====================

if __name__ == '__main__':
    import random
    data = [random.randint(1, 100) for _ in range(15)]
    print("原始:", data)
    print("快排:", quick_sort(data))
    print("归并:", merge_sort(data))
    print("堆排:", heap_sort(data))
    print("插入:", insertion_sort(data))
    print("计数:", counting_sort([3, 1, 4, 1, 5, 9, 2, 6], 9))

    floats = [random.random() for _ in range(10)]
    print("桶排:", bucket_sort(floats)[:5], "...")

    # 按对象属性排序
    items = [{'name': 'A', 'score': 85}, {'name': 'B', 'score': 92}, {'name': 'C', 'score': 78}]
    print("按score排序:", merge_sort(items, key=lambda x: x['score']))
