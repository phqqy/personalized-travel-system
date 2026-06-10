#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图论算法模块
包含: 最短路径、最小生成树、拓扑排序、图遍历
"""

import heapq
from collections import deque
from typing import List, Dict, Tuple, Optional, Set


# ==================== 最短路径 ====================

def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int) -> Dict[int, int]:
    """
    Dijkstra 最短路径算法（非负权）

    Args:
        graph: 邻接表 {节点: [(邻居, 权重), ...]}
        start: 起点

    Returns:
        {节点: 最短距离}，不可达节点不包含

    Example:
        >>> g = {0: [(1,4),(2,2)], 1: [(3,3)], 2: [(1,1),(3,5)], 3: []}
        >>> dijkstra(g, 0)
        {0: 0, 1: 3, 2: 2, 3: 6}
    """
    dist = {start: 0}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


def dijkstra_path(graph: Dict[int, List[Tuple[int, int]]], start: int, end: int) -> Tuple[List[int], int]:
    """
    Dijkstra 最短路径（返回路径和距离）

    Returns:
        (路径节点列表, 总距离)，不可达返回 ([], -1)
    """
    dist = {start: 0}
    prev = {}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float('inf')):
            continue
        if u == end:
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float('inf')):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))

    if end not in dist:
        return [], -1

    path = []
    cur = end
    while cur != start:
        path.append(cur)
        cur = prev[cur]
    path.append(start)
    path.reverse()
    return path, dist[end]


def bellman_ford(edges: List[Tuple[int, int, int]], n: int, start: int) -> Dict[int, int]:
    """
    Bellman-Ford 最短路径（支持负权边，检测负环）

    Args:
        edges: [(u, v, w), ...] 边列表
        n: 节点数量
        start: 起点

    Returns:
        {节点: 最短距离}，有负环返回空dict
    """
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0

    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    # 检测负环
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return {}  # 存在负环

    return {k: v for k, v in dist.items() if v != float('inf')}


def floyd_warshall(n: int, edges: List[Tuple[int, int, int]]) -> List[List[float]]:
    """
    Floyd-Warshall 全源最短路径

    Args:
        n: 节点数量
        edges: [(u, v, w), ...]

    Returns:
        n×n 距离矩阵，不可达为 float('inf')
    """
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[k][j] == INF:
                    continue
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist


# ==================== 最小生成树 ====================

def prim(graph: Dict[int, List[Tuple[int, int]]], n: int) -> List[Tuple[int, int, int]]:
    """
    Prim 最小生成树算法

    Args:
        graph: 邻接表（无向图）
        n: 节点数量

    Returns:
        [(u, v, w), ...] MST 边列表
    """
    visited = [False] * n
    mst = []
    pq = [(0, 0, -1)]  # (weight, node, parent)

    while pq and len(mst) < n - 1:
        w, u, p = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        if p != -1:
            mst.append((p, u, w))
        for v, weight in graph.get(u, []):
            if not visited[v]:
                heapq.heappush(pq, (weight, v, u))
    return mst


class UnionFind:
    """并查集"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True


def kruskal(n: int, edges: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Kruskal 最小生成树算法

    Args:
        n: 节点数量
        edges: [(u, v, w), ...]

    Returns:
        [(u, v, w), ...] MST 边列表
    """
    edges = sorted(edges, key=lambda x: x[2])
    uf = UnionFind(n)
    mst = []

    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == n - 1:
                break
    return mst


# ==================== 拓扑排序 ====================

def topological_sort(graph: Dict[int, List[int]], n: int) -> List[int]:
    """
    拓扑排序（Kahn算法 / BFS）

    Args:
        graph: 邻接表 {节点: [后继节点, ...]}
        n: 节点数量

    Returns:
        拓扑序列，有环返回空列表
    """
    indegree = [0] * n
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1

    queue = deque([i for i in range(n) if indegree[i] == 0])
    result = []

    while queue:
        u = queue.popleft()
        result.append(u)
        for v in graph.get(u, []):
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)

    return result if len(result) == n else []


def topological_sort_dfs(graph: Dict[int, List[int]], n: int) -> List[int]:
    """
    拓扑排序（DFS 后序遍历）
    """
    visited = [0] * n  # 0=未访问, 1=访问中, 2=已完成
    result = []

    def dfs(u):
        visited[u] = 1
        for v in graph.get(u, []):
            if visited[v] == 1:
                return False  # 检测到环
            if visited[v] == 0 and not dfs(v):
                return False
        visited[u] = 2
        result.append(u)
        return True

    for i in range(n):
        if visited[i] == 0 and not dfs(i):
            return []

    result.reverse()
    return result


# ==================== 图遍历 ====================

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """广度优先遍历"""
    visited = set()
    queue = deque([start])
    visited.add(start)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            if v not in visited:
                visited.add(v)
                queue.append(v)
    return order


def dfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """深度优先遍历（迭代）"""
    visited = set()
    stack = [start]
    order = []

    while stack:
        u = stack.pop()
        if u not in visited:
            visited.add(u)
            order.append(u)
            for v in reversed(graph.get(u, [])):
                if v not in visited:
                    stack.append(v)
    return order


def connected_components(n: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """求无向图连通分量"""
    graph = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = []

    for i in range(n):
        if i not in visited:
            comp = bfs(graph, i)
            visited.update(comp)
            components.append(comp)
    return components


# ==================== 测试入口 ====================

if __name__ == '__main__':
    # Dijkstra 测试
    g = {0: [(1, 4), (2, 2)], 1: [(3, 3)], 2: [(1, 1), (3, 5)], 3: []}
    print("Dijkstra:", dijkstra(g, 0))
    print("Dijkstra path 0->3:", dijkstra_path(g, 0, 3))

    # Prim 测试
    ug = {0: [(1, 4), (2, 2)], 1: [(0, 4), (2, 1), (3, 3)], 2: [(0, 2), (1, 1), (3, 5)], 3: [(1, 3), (2, 5)]}
    print("Prim MST:", prim(ug, 4))
    print("Kruskal MST:", kruskal(4, [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 3), (2, 3, 5)]))

    # 拓扑排序
    dag = {0: [1, 2], 1: [3], 2: [3], 3: []}
    print("Topo Sort:", topological_sort(dag, 4))

    # BFS/DFS
    ug2 = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
    print("BFS:", bfs(ug2, 0))
    print("DFS:", dfs(ug2, 0))
    print("Connected components:", connected_components(4, [(0, 1), (2, 3)]))
