"""
221. Maximal Square
Difficulty: Medium
Topics: Array, Dynamic Programming, Matrix

Problem:
Given an m x n binary matrix filled with '0's and '1's, find the largest
square containing only '1's and return its area.

Example 1:
    Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],
                     ["1","1","1","1","1"],["1","0","0","1","0"]]
    Output: 4
Example 2:
    Input: matrix = [["0","1"],["1","0"]]
    Output: 1
Example 3:
    Input: matrix = [["0"]]
    Output: 0

Constraints:
    m == matrix.length, n == matrix[i].length
    1 <= m, n <= 300
    matrix[i][j] is '0' or '1'

Approach (DP):
    Let dp[i][j] be the side of the largest all-1 square whose bottom-right
    corner is (i, j). If matrix[i][j] == '1' then
        dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]).
    The square can only extend as far as the weakest of the three neighbours
    (up, left, diagonal), since all three sub-squares must be full of 1s.
    Otherwise dp[i][j] = 0. Answer is (max dp)^2.
    We only need the previous row, so space is O(n).

Complexity:
    Time: O(m * n)    Space: O(n)  (full table version: O(m * n))
"""
from typing import List


def maximalSquare(matrix: List[List[str]]) -> int:
    n = len(matrix[0])
    prev = [0] * (n + 1)
    best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if row[j - 1] == "1":
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
                best = max(best, cur[j])
        prev = cur
    return best * best


def maximalSquareTable(matrix: List[List[str]]) -> int:
    """Alternative: full 2D DP table."""
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    best = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i - 1][j - 1] == "1":
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                best = max(best, dp[i][j])
    return best * best


if __name__ == "__main__":
    tests = [
        ([["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]], 4),
        ([["0","1"],["1","0"]], 1),
        ([["0"]], 0),
        ([["1"]], 1),
        ([["1","1"],["1","1"]], 4),
        ([["1","1","1"],["1","1","1"],["1","1","1"]], 9),
        ([["1","1","1","1"]], 1),
        ([["1"],["1"],["1"]], 1),
        ([["0","0"],["0","0"]], 0),
    ]
    for mat, exp in tests:
        assert maximalSquare(mat) == exp, (mat, exp)
        assert maximalSquareTable(mat) == exp, (mat, exp)
    print("All tests passed.")
