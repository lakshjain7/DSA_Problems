"""
Problem #62 — Unique Paths
Difficulty : Medium
Topics     : Dynamic Programming, Math, Combinatorics

─────────────────────────────────────────────────────
Problem Statement
─────────────────────────────────────────────────────
There is a robot on an m x n grid. The robot is initially located at the
top-left corner (i.e., grid[0][0]). The robot tries to move to the
bottom-right corner (i.e., grid[m-1][n-1]). The robot can only move either
down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths
that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal
to 2 * 10^9.

─────────────────────────────────────────────────────
Examples
─────────────────────────────────────────────────────
Example 1:
    Input : m = 3, n = 7
    Output: 28

Example 2:
    Input : m = 3, n = 2
    Output: 3
    Explanation: From the top-left corner, there are a total of 3 ways to
    reach the bottom-right corner:
      1. Right -> Down -> Down
      2. Down -> Down -> Right
      3. Down -> Right -> Down

─────────────────────────────────────────────────────
Constraints
─────────────────────────────────────────────────────
  • 1 <= m, n <= 100
─────────────────────────────────────────────────────

Approach 1 — 2-D Dynamic Programming
──────────────────────────────────────
Build a dp table where dp[r][c] = number of unique paths to reach cell (r, c).

Base cases:
  • First row  (r == 0): only one way to reach any cell — always move right.
    dp[0][c] = 1 for all c.
  • First column (c == 0): only one way — always move down.
    dp[r][0] = 1 for all r.

Recurrence:
  dp[r][c] = dp[r-1][c] + dp[r][c-1]
  (robot arrives either from above or from the left)

Answer: dp[m-1][n-1]

Complexity
──────────
  Time : O(m * n)  — fill every cell once
  Space: O(m * n)  — full dp table

Approach 2 — Space-optimised 1-D DP
──────────────────────────────────────
We only ever look at the current row and the row above, so we can compress
dp to a single 1-D array of length n and update it in-place left-to-right.

  prev[c] always holds the value from the row above (what we'd call dp[r-1][c])
  After updating in-place, row[c] = row[c] + row[c-1]

Complexity
──────────
  Time : O(m * n)
  Space: O(n)       — single row array

Approach 3 — Combinatorics (O(min(m,n)) time, O(1) space)
──────────────────────────────────────────────────────────
The robot must make exactly (m-1) down-moves and (n-1) right-moves in some
order — total (m+n-2) moves. The answer is therefore C(m+n-2, m-1):

  C(m+n-2, m-1) = (m+n-2)! / ((m-1)! * (n-1)!)

Use Python's math.comb for exact integer arithmetic.
"""

from typing import List
import math


# ──────────────────────────────────────────────────────────────
# Approach 1 – 2-D DP  (most readable / interview-friendly)
# ──────────────────────────────────────────────────────────────
def uniquePaths(m: int, n: int) -> int:
    dp: List[List[int]] = [[1] * n for _ in range(m)]

    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp[m - 1][n - 1]


# ──────────────────────────────────────────────────────────────
# Approach 2 – 1-D DP  (O(n) space)
# ──────────────────────────────────────────────────────────────
def uniquePathsSpaceOpt(m: int, n: int) -> int:
    row = [1] * n          # represents the current row; first row is all 1s

    for _ in range(1, m):  # process rows 1 … m-1
        for c in range(1, n):
            row[c] += row[c - 1]

    return row[n - 1]


# ──────────────────────────────────────────────────────────────
# Approach 3 – Combinatorics  (O(1) space)
# ──────────────────────────────────────────────────────────────
def uniquePathsComb(m: int, n: int) -> int:
    return math.comb(m + n - 2, m - 1)


# ──────────────────────────────────────────────────────────────
# Tests
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for fn in (uniquePaths, uniquePathsSpaceOpt, uniquePathsComb):
        # Basic examples
        assert fn(3, 7) == 28,  f"{fn.__name__}: expected 28"
        assert fn(3, 2) == 3,   f"{fn.__name__}: expected 3"

        # Edge cases
        assert fn(1, 1) == 1,   f"{fn.__name__}: 1x1 grid"
        assert fn(1, 10) == 1,  f"{fn.__name__}: single-row grid"
        assert fn(10, 1) == 1,  f"{fn.__name__}: single-col grid"

        # Larger grid
        assert fn(7, 3) == 28,  f"{fn.__name__}: symmetric to (3,7)"
        assert fn(10, 10) == 48620, f"{fn.__name__}: 10x10 grid"

    print("All tests passed ✓")
