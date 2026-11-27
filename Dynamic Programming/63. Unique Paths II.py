"""
63. Unique Paths II
Difficulty: Medium
Topics: Array, Dynamic Programming, Matrix

Problem:
You are given an m x n integer array `grid`. There is a robot initially located
at the top-left corner (grid[0][0]). The robot tries to move to the
bottom-right corner (grid[m-1][n-1]). The robot can only move either down or
right at any point in time.

An obstacle and space are marked as 1 and 0 respectively in grid. A path that
the robot takes cannot include any square that is an obstacle.

Return the number of possible unique paths that the robot can take to reach the
bottom-right corner. The answer will be less than or equal to 2 * 10^9.

Example 1:
    Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
    Output: 2
    Explanation: There is one obstacle in the middle of the 3x3 grid.
    Right -> Right -> Down -> Down, and Down -> Down -> Right -> Right.

Example 2:
    Input: obstacleGrid = [[0,1],[0,0]]
    Output: 1

Constraints:
    m == obstacleGrid.length
    n == obstacleGrid[i].length
    1 <= m, n <= 100
    obstacleGrid[i][j] is 0 or 1.

Approach (1-D rolling DP):
    Let dp[j] = number of ways to reach cell (i, j) in the current row.
    The only ways into (i, j) are from above (i-1, j) -- which is the old dp[j]
    -- and from the left (i, j-1) -- which is the already-updated dp[j-1].
    So for each cell:
        if obstacle:  dp[j] = 0
        else:         dp[j] = dp[j] + dp[j-1]   (for j > 0)
    Seed dp[0] = 1 if the start is open. An obstacle zeroes its cell, which
    automatically cuts off every path that would have passed through it.

Complexity:
    Time:  O(m * n) -- each cell visited once.
    Space: O(n)     -- one row of DP.

Alternative:
    Top-down memoised recursion paths(i, j) = paths(i-1, j) + paths(i, j-1),
    O(m*n) time and space (recursion + cache).
"""
from functools import lru_cache
from typing import List


class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        n = len(obstacleGrid[0])
        dp = [0] * n
        dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
        for row in obstacleGrid:
            for j in range(n):
                if row[j] == 1:
                    dp[j] = 0
                elif j > 0:
                    dp[j] += dp[j - 1]
        return dp[-1]

    def uniquePathsWithObstaclesMemo(self, obstacleGrid: List[List[int]]) -> int:
        @lru_cache(maxsize=None)
        def paths(i: int, j: int) -> int:
            if i < 0 or j < 0 or obstacleGrid[i][j] == 1:
                return 0
            if i == 0 and j == 0:
                return 1
            return paths(i - 1, j) + paths(i, j - 1)

        return paths(len(obstacleGrid) - 1, len(obstacleGrid[0]) - 1)


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[0, 0, 0], [0, 1, 0], [0, 0, 0]], 2),
        ([[0, 1], [0, 0]], 1),
        ([[0]], 1),
        ([[1]], 0),                      # start blocked
        ([[0, 0], [0, 1]], 0),           # end blocked
        ([[0, 0, 0, 0]], 1),             # single row
        ([[0], [1], [0]], 0),            # single column blocked
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 6),
        ([[0, 0], [1, 1], [0, 0]], 0),   # wall
    ]
    for grid, exp in cases:
        assert s.uniquePathsWithObstacles(grid) == exp, (grid, exp)
        assert s.uniquePathsWithObstaclesMemo(grid) == exp, (grid, exp)
    # Large open grid: C(198, 99) would overflow constraint, so use 17x17 -> C(32,16)
    big = [[0] * 17 for _ in range(17)]
    assert s.uniquePathsWithObstacles(big) == 601080390
    print("All tests passed!")
