#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学算法模块
包含: 素数、GCD/LCM、快速幂、组合数、矩阵运算
"""

from typing import List, Tuple


# ==================== GCD / LCM ====================

def gcd(a: int, b: int) -> int:
    """辗转相除法求最大公约数"""
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """最小公倍数"""
    return a // gcd(a, b) * b


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    扩展欧几里得算法
    返回 (g, x, y) 使得 a*x + b*y = g = gcd(a,b)
    """
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


# ==================== 素数 ====================

def is_prime(n: int) -> bool:
    """判断素数 — O(sqrt(n))"""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    埃拉托色尼筛法 — 返回 [0, n] 内所有素数
    O(n log log n)
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i, is_p in enumerate(sieve) if is_p]


def prime_factors(n: int) -> List[Tuple[int, int]]:
    """
    质因数分解
    返回 [(质因数, 指数), ...]
    """
    factors = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            cnt = 0
            while n % d == 0:
                n //= d
                cnt += 1
            factors.append((d, cnt))
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append((n, 1))
    return factors


# ==================== 快速幂 ====================

def fast_pow(base: int, exp: int, mod: int = None) -> int:
    """
    快速幂 — O(log exp)
    """
    result = 1
    while exp > 0:
        if exp & 1:
            result = result * base
            if mod:
                result %= mod
        base = base * base
        if mod:
            base %= mod
        exp >>= 1
    return result


# ==================== 组合数学 ====================

def factorial(n: int, mod: int = None) -> int:
    """阶乘 n!"""
    result = 1
    for i in range(2, n + 1):
        result = result * i
        if mod:
            result %= mod
    return result


def permutations(n: int, r: int) -> int:
    """排列数 P(n, r)"""
    result = 1
    for i in range(n - r + 1, n + 1):
        result *= i
    return result


def combinations(n: int, r: int) -> int:
    """组合数 C(n, r)"""
    if r < 0 or r > n:
        return 0
    if r > n - r:
        r = n - r
    result = 1
    for i in range(1, r + 1):
        result = result * (n - r + i) // i
    return result


class Combinatorics:
    """组合数预处理 — 支持 O(1) 查询 C(n, k) % mod"""

    def __init__(self, n_max: int, mod: int = 10 ** 9 + 7):
        self.mod = mod
        self.fact = [1] * (n_max + 1)
        self.inv_fact = [1] * (n_max + 1)

        for i in range(1, n_max + 1):
            self.fact[i] = self.fact[i - 1] * i % mod

        self.inv_fact[n_max] = pow(self.fact[n_max], mod - 2, mod)
        for i in range(n_max, 0, -1):
            self.inv_fact[i - 1] = self.inv_fact[i] * i % mod

    def C(self, n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.inv_fact[k] % self.mod * self.inv_fact[n - k] % self.mod


# ==================== 矩阵运算 ====================

def matrix_multiply(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """
    矩阵乘法
    O(n*m*p) — a 是 n×m, b 是 m×p
    """
    n, m, p = len(a), len(a[0]), len(b[0])
    result = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            if a[i][k]:
                for j in range(p):
                    result[i][j] += a[i][k] * b[k][j]
    return result


def matrix_pow(mat: List[List[int]], exp: int) -> List[List[int]]:
    """矩阵快速幂 — 方阵"""
    n = len(mat)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in mat]

    while exp > 0:
        if exp & 1:
            result = matrix_multiply(result, base)
        base = matrix_multiply(base, base)
        exp >>= 1
    return result


def fibonacci(n: int) -> int:
    """
    斐波那契数列第 n 项（矩阵快速幂法）
    O(log n)
    """
    if n <= 1:
        return n
    mat = [[1, 1], [1, 0]]
    result = matrix_pow(mat, n - 1)
    return result[0][0]


# ==================== 卡特兰数 ====================

def catalan(n: int) -> int:
    """第 n 个卡特兰数 C(2n, n) / (n+1)"""
    return combinations(2 * n, n) // (n + 1)


# ==================== 测试 ====================

if __name__ == '__main__':
    print("gcd(48, 18):", gcd(48, 18))
    print("lcm(12, 18):", lcm(12, 18))
    g, x, y = extended_gcd(48, 18)
    print(f"extended_gcd(48, 18): g={g}, x={x}, y={y} -> 48*{x}+18*{y}={48 * x + 18 * y}")

    print("素数 [0,50]:", sieve_of_eratosthenes(50))
    print("prime_factors(84):", prime_factors(84))

    print("2^10 =", fast_pow(2, 10))
    print("2^10 mod 1000 =", fast_pow(2, 10, 1000))

    print("C(10, 3):", combinations(10, 3))
    print("fibonacci(20):", fibonacci(20))

    # 组合数预处理
    comb = Combinatorics(100)
    print("C(100, 50) mod 1e9+7:", comb.C(100, 50))

    print("catalan(5):", catalan(5))
