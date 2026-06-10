#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个性化旅游系统 — 算法库

模块概览:
  algorithms.graph      — 图论 (Dijkstra, Prim, Kruskal, BFS/DFS, 拓扑排序)
  algorithms.sorting    — 排序 (快排, 归并, 堆排, 插入, 计数, 桶排)
  algorithms.structures — 数据结构 (BST, 线段树, 树状数组, LRU, Trie)
  algorithms.optimize   — 动态规划 & 贪心 (背包, LCS, LIS, 编辑距离, 区间调度)
  algorithms.search     — 搜索 & 字符串匹配 (二分, KMP, Rabin-Karp)
  algorithms.math       — 数学 (素数, GCD, 快速幂, 组合数, 矩阵)
"""

# ===== 图论 =====
from algorithms.graph import (
    dijkstra,
    dijkstra_path,
    bellman_ford,
    floyd_warshall,
    prim,
    kruskal,
    UnionFind,
    topological_sort,
    topological_sort_dfs,
    bfs,
    dfs,
    connected_components,
)

# ===== 排序 =====
from algorithms.sorting import (
    quick_sort,
    merge_sort,
    heap_sort,
    insertion_sort,
    selection_sort,
    bubble_sort,
    counting_sort,
    bucket_sort,
    merge_sorted_lists,
)

# ===== 数据结构 =====
from algorithms.structures import (
    BST,
    SegmentTree,
    FenwickTree,
    LRUCache,
    Trie,
)

# ===== 动态规划 & 贪心 =====
from algorithms.optimize import (
    knapsack_01,
    knapsack_01_items,
    unbounded_knapsack,
    lcs,
    lis,
    edit_distance,
    coin_change,
    interval_scheduling,
    huffman_coding,
)

# ===== 搜索 & 字符串 =====
from algorithms.search import (
    binary_search,
    lower_bound,
    upper_bound,
    equal_range,
    interpolation_search,
    kmp_search,
    rabin_karp,
)

# ===== 数学 =====
from algorithms.math import (
    gcd,
    lcm,
    extended_gcd,
    is_prime,
    sieve_of_eratosthenes,
    prime_factors,
    fast_pow,
    factorial,
    permutations,
    combinations,
    Combinatorics,
    matrix_multiply,
    matrix_pow,
    fibonacci,
    catalan,
)
