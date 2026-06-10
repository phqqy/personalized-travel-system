#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据结构模块
包含: 二叉搜索树、线段树、树状数组、LRU缓存、Trie
"""

from typing import List, Optional, Any, Tuple, Dict


# ==================== 二叉搜索树 ====================

class TreeNode:
    """二叉树节点"""
    __slots__ = ('val', 'left', 'right')

    def __init__(self, val: Any):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None


class BST:
    """二叉搜索树（支持插入、搜索、删除、遍历）"""

    def __init__(self):
        self.root: Optional[TreeNode] = None
        self._size = 0

    def insert(self, val: Any) -> None:
        self.root = self._insert(self.root, val)

    def _insert(self, node: Optional[TreeNode], val: Any) -> TreeNode:
        if node is None:
            self._size += 1
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val: Any) -> bool:
        return self._search(self.root, val)

    def _search(self, node: Optional[TreeNode], val: Any) -> bool:
        if node is None:
            return False
        if val == node.val:
            return True
        return self._search(node.left if val < node.val else node.right, val)

    def delete(self, val: Any) -> None:
        self.root = self._delete(self.root, val)

    def _delete(self, node: Optional[TreeNode], val: Any) -> Optional[TreeNode]:
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            self._size -= 1
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # 找后继
            succ = node.right
            while succ.left:
                succ = succ.left
            node.val = succ.val
            node.right = self._delete(node.right, succ.val)
            self._size += 1  # 纠正计数
        return node

    def inorder(self) -> List[Any]:
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)

    def preorder(self) -> List[Any]:
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node:
            result.append(node.val)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def postorder(self) -> List[Any]:
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.val)

    def __len__(self):
        return self._size


# ==================== 线段树 ====================

class SegmentTree:
    """
    线段树 — 区间查询、单点更新
    O(log n) 查询，O(log n) 更新

    Example:
        >>> st = SegmentTree([1, 3, 5, 7, 9, 11])
        >>> st.query(1, 3)  # arr[1:4] 的和
        15
        >>> st.update(1, 10)  # arr[1] = 10
        >>> st.query(1, 3)
        22
    """

    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        self._build(data, 0, 0, self.n - 1)

    def _build(self, data, node, left, right):
        if left == right:
            self.tree[node] = data[left]
            return
        mid = (left + right) // 2
        self._build(data, node * 2 + 1, left, mid)
        self._build(data, node * 2 + 2, mid + 1, right)
        self.tree[node] = self.tree[node * 2 + 1] + self.tree[node * 2 + 2]

    def query(self, ql: int, qr: int) -> int:
        """查询区间 [ql, qr] 的和"""
        return self._query(0, 0, self.n - 1, ql, qr)

    def _query(self, node, left, right, ql, qr):
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return self.tree[node]
        mid = (left + right) // 2
        return self._query(node * 2 + 1, left, mid, ql, qr) + \
               self._query(node * 2 + 2, mid + 1, right, ql, qr)

    def update(self, idx: int, val: int) -> None:
        """更新下标 idx 的值为 val"""
        self._update(0, 0, self.n - 1, idx, val)

    def _update(self, node, left, right, idx, val):
        if left == right:
            self.tree[node] = val
            return
        mid = (left + right) // 2
        if idx <= mid:
            self._update(node * 2 + 1, left, mid, idx, val)
        else:
            self._update(node * 2 + 2, mid + 1, right, idx, val)
        self.tree[node] = self.tree[node * 2 + 1] + self.tree[node * 2 + 2]


# ==================== 树状数组 (Fenwick Tree) ====================

class FenwickTree:
    """
    树状数组 — 前缀和查询、点更新
    O(log n) 查询和更新，空间 O(n)

    Example:
        >>> ft = FenwickTree(5)
        >>> ft.add(0, 3); ft.add(2, 5)
        >>> ft.prefix_sum(3)
        8
    """

    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx: int, delta: int) -> None:
        i = idx + 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, idx: int) -> int:
        """前缀和 [0, idx]"""
        s = 0
        i = idx + 1
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l: int, r: int) -> int:
        """区间和 [l, r]"""
        return self.prefix_sum(r) - (self.prefix_sum(l - 1) if l > 0 else 0)


# ==================== LRU 缓存 ====================

class LRUCache:
    """
    LRU 缓存 — 哈希表 + 双向链表
    O(1) get / put

    Example:
        >>> cache = LRUCache(2)
        >>> cache.put(1, 'A'); cache.put(2, 'B')
        >>> cache.get(1)
        'A'
        >>> cache.put(3, 'C')  # 淘汰 key=2
        >>> cache.get(2)
        -1
    """

    class _Node:
        __slots__ = ('key', 'val', 'prev', 'next')

        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, LRUCache._Node] = {}
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> Any:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key: int, val: Any) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = self._Node(key, val)
        self._add_to_head(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# ==================== Trie 前缀树 ====================

class Trie:
    """
    前缀树 — 字符串集合存储和前缀查询

    Example:
        >>> t = Trie()
        >>> t.insert('hello')
        >>> t.search('hello')
        True
        >>> t.starts_with('hel')
        True
    """

    def __init__(self):
        self.root = {}
        self._end = '*'

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node[self._end] = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and self._end in node

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def delete(self, word: str) -> None:
        self._delete(self.root, word, 0)

    def _delete(self, node, word, depth):
        if depth == len(word):
            if self._end in node:
                del node[self._end]
            return len(node) == 0
        ch = word[depth]
        if ch not in node:
            return False
        if self._delete(node[ch], word, depth + 1):
            del node[ch]
            return len(node) == 0
        return False


# ==================== 测试 ====================

if __name__ == '__main__':
    # BST
    bst = BST()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(v)
    print("BST inorder:", bst.inorder())
    print("BST size:", len(bst))

    # Segment Tree
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    print("SegmentTree query [1,3]:", st.query(1, 3))
    st.update(1, 10)
    print("After update, query [1,3]:", st.query(1, 3))

    # Fenwick Tree
    ft = FenwickTree(5)
    for i, v in enumerate([1, 2, 3, 4, 5]):
        ft.add(i, v)
    print("Fenwick prefix_sum 3:", ft.prefix_sum(3))
    print("Fenwick range_sum [1,3]:", ft.range_sum(1, 3))

    # LRU
    lru = LRUCache(2)
    lru.put(1, 'A')
    lru.put(2, 'B')
    print("LRU get 1:", lru.get(1))
    lru.put(3, 'C')
    print("LRU get 2:", lru.get(2))

    # Trie
    t = Trie()
    for w in ['hello', 'world', 'hi']:
        t.insert(w)
    print("Trie search 'hello':", t.search('hello'))
    print("Trie starts_with 'he':", t.starts_with('he'))
