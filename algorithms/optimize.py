#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动态规划 & 贪心算法模块
包含: 背包问题、LCS/LIS、编辑距离、硬币找零、区间调度
"""

from typing import List, Tuple


# ==================== 背包问题 ====================

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 背包 — 每件物品只能选一次
    O(n * capacity) 时间，O(capacity) 空间

    Returns:
        最大价值
    """
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_01_items(weights: List[int], values: List[int], capacity: int) \
        -> Tuple[int, List[int]]:
    """0/1 背包 — 返回最大价值和选中物品下标"""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if c >= w:
                dp[i][c] = max(dp[i][c], dp[i - 1][c - w] + v)

    # 回溯
    items = []
    c = capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            items.append(i - 1)
            c -= weights[i - 1]

    return dp[n][capacity], list(reversed(items))


def unbounded_knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    完全背包 — 每件物品可以选无限次
    """
    dp = [0] * (capacity + 1)
    for c in range(capacity + 1):
        for w, v in zip(weights, values):
            if c >= w:
                dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


# ==================== 序列 DP ====================

def lcs(a: str, b: str) -> str:
    """
    最长公共子序列 (Longest Common Subsequence)
    O(m * n)
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 回溯
    i, j = m, n
    result = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return ''.join(reversed(result))


def lis(nums: List[int]) -> List[int]:
    """
    最长递增子序列 (Longest Increasing Subsequence)
    O(n log n)

    Returns:
        最长递增子序列
    """
    import bisect
    tails = []           # tails[i] = 长度为 i+1 的 LIS 的最小末尾
    prev = [-1] * len(nums)
    indices = []

    for i, x in enumerate(nums):
        idx = bisect.bisect_left(tails, x, key=lambda j: nums[j])
        if idx == len(tails):
            tails.append(i)
        else:
            tails[idx] = i
        if idx > 0:
            prev[i] = tails[idx - 1]

    # 回溯
    result = []
    cur = tails[-1] if tails else -1
    while cur != -1:
        result.append(nums[cur])
        cur = prev[cur]
    return list(reversed(result))


def edit_distance(a: str, b: str) -> int:
    """
    编辑距离 (Levenshtein)
    O(m * n)
    """
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]


def coin_change(coins: List[int], amount: int) -> int:
    """
    硬币找零 — 最少硬币数
    返回 -1 表示无法凑出
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1


# ==================== 贪心 ====================

def interval_scheduling(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    区间调度 — 选择最多不重叠区间
    贪心：按结束时间排序

    Args:
        intervals: [(start, end), ...]

    Returns:
        最大不重叠区间列表
    """
    intervals = sorted(intervals, key=lambda x: x[1])
    result = []
    last_end = float('-inf')

    for s, e in intervals:
        if s >= last_end:
            result.append((s, e))
            last_end = e
    return result


def huffman_coding(freqs: List[Tuple[str, int]]) -> dict:
    """
    Huffman 编码
    """
    import heapq

    class _Node:
        __slots__ = ('freq', 'char', 'left', 'right')
        def __init__(self, freq, char, left=None, right=None):
            self.freq = freq
            self.char = char
            self.left = left
            self.right = right
        def __lt__(self, other):
            return self.freq < other.freq

    heap = [_Node(f, ch) for ch, f in freqs]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, _Node(left.freq + right.freq, left.char + right.char, left, right))

    codes = {}

    def traverse(node, code):
        if node.left is None and node.right is None:
            codes[node.char] = code if code else '0'
            return
        if node.left:
            traverse(node.left, code + '0')
        if node.right:
            traverse(node.right, code + '1')

    if heap:
        traverse(heap[0], '')
    return codes


# ==================== 测试 ====================

if __name__ == '__main__':
    # 0/1 背包
    max_val, items = knapsack_01_items([2, 3, 4, 5], [3, 4, 5, 6], 8)
    print(f"0/1 背包: 最大价值={max_val}, 物品={items}")

    # LCS
    print("LCS('abcde', 'ace'):", lcs('abcde', 'ace'))

    # LIS
    print("LIS:", lis([10, 9, 2, 5, 3, 7, 101, 18]))

    # 编辑距离
    print("编辑距离('horse', 'ros'):", edit_distance('horse', 'ros'))

    # 硬币找零
    print("硬币找零([1,2,5], 11):", coin_change([1, 2, 5], 11))

    # 区间调度
    intervals = [(1, 3), (2, 5), (4, 6), (6, 7), (5, 8)]
    print("区间调度:", interval_scheduling(intervals))

    # Huffman
    freqs = [('A', 5), ('B', 9), ('C', 12), ('D', 13), ('E', 16), ('F', 45)]
    print("Huffman 编码:", huffman_coding(freqs))
