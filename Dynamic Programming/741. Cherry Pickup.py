"""
741. Cherry Pickup
Difficulty: Hard
Topics: Array, Dynamic Programming, Matrix

Problem:
You are given an n x n grid representing a field of cherries, each cell is
one of three possible integers.
    0 means the cell is empty, so you can pass through,
    1 means the cell contains a cherry that you can pick up and pass through,
    -1 means the cell contains a thorn that blocks your way.
Return the maximum number of cherries you can collect by following the rules:
    Starting at (0, 0) and reaching (n-1, n-1) by moving right or down
    through valid path cells (cells with value 0 or 1).
    After reaching (n-1, n-1), returning to (0, 0) by moving left or up
    through valid path cells.
    When passing through a path cell containing a cherry, you pick it up and
    the cell becomes an empty cell 0.
    If there is no valid path between (0, 0) and (n-1, n-1), then no cherries
    can be collected.

Example 1:
    Input: grid = [[0,1,-1],[1,0,-1],[1,1,1]]
    Output: 5

Example 2:
    Input: grid = [[1,1,-1],[1,-1,1],[-1,1,1]]
    Output: 0

Constraints:
    n == grid.length == grid[i].length
    1 <= n <= 50
    grid[i][j] is -1, 0, or 1.
    grid[0][0] != -1 and grid[n-1][n-1] != -1

Approach (two walkers simultaneously):
    The return trip reversed is another path from (0,0) to (n-1,n-1). So we
    send two walkers down together. After k steps walker 1 is at (r1, k-r1)
    and walker 2 at (r2, k-r2). State: dp[k][r1][r2] = max cherries collected.
    Walkers only share a cell when r1 == r2 (same diagonal), and then the
    cherry is counted once. Transitions: each walker came from up or left ->
    4 predecessors. Answer max(0, dp[2n-2][n-1][n-1]).

Complexity: O(n^3) time, O(n^2) space (rolling over k).

Alternative: top-down memoized recursion over (r1, c1, r2) with the same
    recurrence (c2 = r1 + c1 - r2).
"""
from functools import lru_cache
from typing import List

NEG = float("-inf")


def cherryPickup(grid: List[List[int]]) -> int:
    n = len(grid)
    dp = [[NEG] * n for _ in range(n)]
    dp[0][0] = grid[0][0]
    for k in range(1, 2 * n - 1):
        nd = [[NEG] * n for _ in range(n)]
        for r1 in range(max(0, k - n + 1), min(n - 1, k) + 1):
            c1 = k - r1
            if grid[r1][c1] == -1:
                continue
            for r2 in range(r1, min(n - 1, k) + 1):
                c2 = k - r2
                if c2 >= n or grid[r2][c2] == -1:
                    continue
                best = dp[r1][r2]  # both came from left
                if r1 > 0:
                    best = max(best, dp[r1 - 1][r2])
                if r2 > 0:
                    best = max(best, dp[r1][r2 - 1])
                if r1 > 0 and r2 > 0:
                    best = max(best, dp[r1 - 1][r2 - 1])
                if best == NEG:
                    continue
                gain = grid[r1][c1]
                if r1 != r2:
                    gain += grid[r2][c2]
                nd[r1][r2] = best + gain
        dp = nd
    return max(0, dp[n - 1][n - 1]) if dp[n - 1][n - 1] != NEG else 0


def cherryPickupMemo(grid: List[List[int]]) -> int:
    n = len(grid)

    @lru_cache(maxsize=None)
    def go(r1: int, c1: int, r2: int) -> float:
        c2 = r1 + c1 - r2
        if min(r1, c1, r2, c2) < 0 or grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return NEG
        if r1 == c1 == n - 1:
            return grid[r1][c1]
        if r1 >= n or c1 >= n or r2 >= n or c2 >= n:
            return NEG
        gain = grid[r1][c1] + (grid[r2][c2] if (r1, c1) != (r2, c2) else 0)
        best = max(
            go(r1 + 1, c1, r2 + 1) if r1 + 1 < n and r2 + 1 < n else NEG,
            go(r1 + 1, c1, r2) if r1 + 1 < n and c2 + 1 < n else NEG,
            go(r1, c1 + 1, r2 + 1) if c1 + 1 < n and r2 + 1 < n else NEG,
            go(r1, c1 + 1, r2) if c1 + 1 < n and c2 + 1 < n else NEG,
        )
        return NEG if best == NEG else gain + best

    res = go(0, 0, 0)
    return 0 if res == NEG else int(res)


if __name__ == "__main__":
    g1 = [[0, 1, -1], [1, 0, -1], [1, 1, 1]]
    g2 = [[1, 1, -1], [1, -1, 1], [-1, 1, 1]]
    for f in (cherryPickup, cherryPickupMemo):
        assert f(g1) == 5
        assert f(g2) == 0
        assert f([[1]]) == 1
        assert f([[0]]) == 0
        assert f([[1, 1], [1, 1]]) == 4
        assert f([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 8
        assert f([[1, -1], [-1, 1]]) == 0
        assert f([[1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 1],
                  [1, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 1]]) == 15
    import random
    for _ in range(100):
        n = random.randint(1, 6)
        g = [[random.choice([0, 1, 1, -1, 0]) for _ in range(n)] for _ in range(n)]
        g[0][0] = 0 if g[0][0] == -1 else g[0][0]
        g[n - 1][n - 1] = 0 if g[n - 1][n - 1] == -1 else g[n - 1][n - 1]
        assert cherryPickup(g) == cherryPickupMemo(g)
    print("All tests passed")
