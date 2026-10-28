"""
120. Triangle
Difficulty: Medium
Topics: Array, Dynamic Programming

Problem:
Given a triangle array, return the minimum path sum from top to bottom.
For each step, you may move to an adjacent number of the row below. More
formally, if you are on index i on the current row, you may move to either
index i or index i + 1 on the next row.

Example 1:
    Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
    Output: 11   (2 + 3 + 5 + 1)
Example 2:
    Input: triangle = [[-10]]
    Output: -10

Constraints:
    1 <= triangle.length <= 200
    triangle[0].length == 1
    triangle[i].length == triangle[i - 1].length + 1
    -10^4 <= triangle[i][j] <= 10^4

Approach (bottom-up DP, 1D array):
    Let dp[j] = min path sum from cell (i, j) down to the bottom. Start with
    the last row. For each row above, dp[j] = triangle[i][j] + min(dp[j], dp[j+1]).
    Working bottom-up means every cell has a well-defined answer and the top
    cell holds the final result. We reuse one array, so no extra 2D table.

Complexity:
    Time:  O(n^2) where n = number of rows (total cells)
    Space: O(n)
"""
from typing import List
from functools import lru_cache


class Solution:
    def minimumTotal(self, triangle: List[List[int]]) -> int:
        dp = triangle[-1][:]
        for i in range(len(triangle) - 2, -1, -1):
            for j in range(i + 1):
                dp[j] = triangle[i][j] + min(dp[j], dp[j + 1])
        return dp[0]

    # Alternative: top-down memoized recursion, O(n^2) time and space.
    def minimumTotalMemo(self, triangle: List[List[int]]) -> int:
        n = len(triangle)

        @lru_cache(maxsize=None)
        def go(i: int, j: int) -> int:
            if i == n - 1:
                return triangle[i][j]
            return triangle[i][j] + min(go(i + 1, j), go(i + 1, j + 1))

        return go(0, 0)


if __name__ == "__main__":
    import random
    s = Solution()
    for f in (s.minimumTotal, s.minimumTotalMemo):
        assert f([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]) == 11
        assert f([[-10]]) == -10
        assert f([[1], [2, 3]]) == 3
        assert f([[-1], [2, 3], [1, -1, -3]]) == -1
        assert f([[0], [0, 0], [0, 0, 0]]) == 0
    # brute-force cross-check
    def brute(t, i=0, j=0):
        if i == len(t) - 1:
            return t[i][j]
        return t[i][j] + min(brute(t, i + 1, j), brute(t, i + 1, j + 1))
    random.seed(1)
    for _ in range(200):
        n = random.randint(1, 8)
        t = [[random.randint(-20, 20) for _ in range(r + 1)] for r in range(n)]
        assert s.minimumTotal(t) == s.minimumTotalMemo(t) == brute(t)
    print("All tests passed")
