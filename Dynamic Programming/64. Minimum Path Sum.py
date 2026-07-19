"""
64. Minimum Path Sum
Difficulty: Medium
Topics: Array, Dynamic Programming, Matrix

Problem Statement
-----------------
Given a m x n grid filled with non-negative numbers, find a path from top left to
bottom right, which minimizes the sum of all numbers along its path.

Note: You can only move either down or right at any point in time.

Example 1:
    Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
    Output: 7
    Explanation: Because the path 1 -> 3 -> 1 -> 1 -> 1 minimizes the sum.

Example 2:
    Input: grid = [[1,2,3],[4,5,6]]
    Output: 12
    Explanation: The path 1 -> 2 -> 3 -> 6 sums to 12.

Constraints:
    - m == grid.length
    - n == grid[i].length
    - 1 <= m, n <= 200
    - 0 <= grid[i][j] <= 200


Approach: Dynamic Programming (in-place / rolling row)
------------------------------------------------------
Let dp[i][j] be the minimum sum of a path from the top-left cell (0, 0) to cell
(i, j). Because we may only move right or down, the only ways to arrive at (i, j)
are from the cell above (i-1, j) or the cell to the left (i, j-1). Therefore:

    dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])

with these boundary rules:
    - dp[0][0] = grid[0][0]
    - first row: dp[0][j] = dp[0][j-1] + grid[0][j]  (can only come from the left)
    - first column: dp[i][0] = dp[i-1][0] + grid[i][0] (can only come from above)

The answer is dp[m-1][n-1].

Why it works: any optimal path to (i, j) must pass through exactly one of its two
predecessors, and the prefix of an optimal path is itself optimal for that
predecessor (optimal substructure). Taking the cheaper predecessor is therefore
correct.

We optimize space by keeping just one row: when we process row i left to right,
row[j] first holds dp[i-1][j] (the value from above) and, after the update, holds
dp[i][j]. row[j-1] already holds dp[i][j-1] (the value from the left).

Complexity Analysis
-------------------
- Time:  O(m * n) -- each cell is visited once.
- Space: O(n) for the rolling row (the alternative below uses O(1) extra space by
  mutating the grid in place).
"""

from typing import List


def min_path_sum(grid: List[List[int]]) -> int:
    """Rolling-row DP. O(m*n) time, O(n) space. Does not mutate the input."""
    if not grid or not grid[0]:
        return 0

    n = len(grid[0])
    row = [0] * n

    # Initialize with the first grid row (prefix sums).
    row[0] = grid[0][0]
    for j in range(1, n):
        row[j] = row[j - 1] + grid[0][j]

    for i in range(1, len(grid)):
        row[0] += grid[i][0]  # first column: only from above
        for j in range(1, n):
            row[j] = grid[i][j] + min(row[j], row[j - 1])

    return row[-1]


# ----------------------------------------------------------------------------
# Alternative approach: in-place DP, O(1) extra space (mutates the grid).
# ----------------------------------------------------------------------------
def min_path_sum_in_place(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j - 1]
            elif j == 0:
                grid[i][j] += grid[i - 1][j]
            else:
                grid[i][j] += min(grid[i - 1][j], grid[i][j - 1])

    return grid[m - 1][n - 1]


if __name__ == "__main__":
    # Example 1
    assert min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7

    # Example 2
    assert min_path_sum([[1, 2, 3], [4, 5, 6]]) == 12

    # Single cell
    assert min_path_sum([[5]]) == 5

    # Single row: must sum the whole row
    assert min_path_sum([[1, 2, 3, 4]]) == 10

    # Single column: must sum the whole column
    assert min_path_sum([[1], [2], [3], [4]]) == 10

    # Grid with zeros
    assert min_path_sum([[0, 0, 0], [0, 0, 0]]) == 0

    # A case where going down first is better than right first
    assert min_path_sum([[1, 9, 9], [1, 9, 9], [1, 1, 1]]) == 5

    # The in-place variant must agree on a copy of each grid.
    cases = [
        [[1, 3, 1], [1, 5, 1], [4, 2, 1]],
        [[1, 2, 3], [4, 5, 6]],
        [[5]],
        [[1, 2, 3, 4]],
        [[1], [2], [3], [4]],
        [[1, 9, 9], [1, 9, 9], [1, 1, 1]],
    ]
    for g in cases:
        expected = min_path_sum([r[:] for r in g])
        assert min_path_sum_in_place([r[:] for r in g]) == expected

    print("All tests passed for 64. Minimum Path Sum")
