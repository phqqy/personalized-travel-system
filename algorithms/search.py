#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索算法 & 字符串匹配模块
包含: 二分搜索、KMP、Rabin-Karp
"""

from typing import List, Optional


# ==================== 二分搜索 ====================

def binary_search(arr: List[int], target: int) -> int:
    """
    二分搜索 — 返回目标下标，未找到返回 -1
    O(log n)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(arr: List[int], target: int) -> int:
    """第一个 >= target 的位置"""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr: List[int], target: int) -> int:
    """第一个 > target 的位置"""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def equal_range(arr: List[int], target: int) -> tuple:
    """返回 target 的 [起始, 结束) 区间"""
    return lower_bound(arr, target), upper_bound(arr, target)


def interpolation_search(arr: List[int], target: int) -> int:
    """
    插值搜索 — 均匀分布数据 O(log log n)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[lo] == arr[hi]:
            return lo if arr[lo] == target else -1
        pos = lo + (hi - lo) * (target - arr[lo]) // (arr[hi] - arr[lo])
        pos = max(lo, min(hi, pos))
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


# ==================== KMP 字符串匹配 ====================

def kmp_search(text: str, pattern: str) -> List[int]:
    """
    KMP 字符串匹配 — O(n + m)
    返回所有匹配的起始位置
    """
    if not pattern:
        return list(range(len(text)))

    n, m = len(text), len(pattern)
    lps = _compute_lps(pattern)
    result = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            result.append(i - m + 1)
            j = lps[j - 1]
    return result


def _compute_lps(pattern: str) -> List[int]:
    """计算最长相同前后缀 (LPS) 数组"""
    m = len(pattern)
    lps = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        lps[i] = j
    return lps


# ==================== Rabin-Karp ====================

def rabin_karp(text: str, pattern: str, base: int = 256, mod: int = 10 ** 9 + 7) -> List[int]:
    """
    Rabin-Karp 字符串匹配 — O(n + m) 平均
    返回所有匹配的起始位置
    """
    if not pattern:
        return list(range(len(text)))

    n, m = len(text), len(pattern)
    if m > n:
        return []

    # 计算 pattern 的 hash
    p_hash = 0
    t_hash = 0
    highest_pow = 1

    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
        if i < m - 1:
            highest_pow = (highest_pow * base) % mod

    result = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i:i + m] == pattern:
            result.append(i)
        if i < n - m:
            t_hash = (t_hash - ord(text[i]) * highest_pow) % mod
            t_hash = (t_hash * base + ord(text[i + m])) % mod
    return result


# ==================== 测试 ====================

if __name__ == '__main__':
    arr = [1, 3, 5, 5, 5, 7, 9, 11]
    print("二分搜索 5:", binary_search(arr, 5))
    print("lower_bound 5:", lower_bound(arr, 5))
    print("upper_bound 5:", upper_bound(arr, 5))
    print("equal_range 5:", equal_range(arr, 5))

    text = "ABABCABABABABCABAB"
    pattern = "ABABC"
    print(f"KMP '{pattern}' in text:", kmp_search(text, pattern))
    print(f"Rabin-Karp '{pattern}' in text:", rabin_karp(text, pattern))
