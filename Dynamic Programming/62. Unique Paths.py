"""
Problem #62 — Unique Paths
Difficulty : Medium
Topics     : Dynamic Programming, Math, Combinatorics

Robot on m x n grid, can only move right or down. Count paths to bottom-right.
Three approaches: 2D DP, 1D DP, combinatorics C(m+n-2, m-1).
Complexity: O(m*n) time, O(n) space (1D DP).
"""

from typing import List
import math


def uniquePaths(m: int, n: int) -> int:
    dp: List[List[int]] = [[1] * n for _ in range(m)]
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]


def uniquePathsSpaceOpt(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[n - 1]


def uniquePathsComb(m: int, n: int) -> int:
    return math.comb(m + n - 2, m - 1)


if __name__ == "__main__":
    for fn in (uniquePaths, uniquePathsSpaceOpt, uniquePathsComb):
        assert fn(3, 7) == 28
        assert fn(3, 2) == 3
        assert fn(1, 1) == 1
        assert fn(1, 10) == 1
        assert fn(10, 1) == 1
        assert fn(7, 3) == 28
        assert fn(10, 10) == 48620
    print("All tests passed ✓")
