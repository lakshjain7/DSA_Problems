"""
174. Dungeon Game
Difficulty: Hard
Topics: Array, Dynamic Programming, Matrix

Problem Statement
-----------------
The demons had captured the princess and imprisoned her in the bottom-right
corner of a `dungeon`. The dungeon consists of `m x n` rooms laid out in a 2D
grid. Our valiant knight was initially positioned in the top-left room and must
fight his way through the dungeon to rescue the princess.

The knight has an initial health point represented by a positive integer. If at
any point his health point drops to 0 or below, he dies immediately.

Some of the rooms are guarded by demons (represented by negative integers), so
the knight loses health upon entering these rooms; other rooms are either empty
(0) or contain magic orbs that increase the knight's health (positive integers).

To reach the princess as fast as possible, the knight decides to move only
rightward or downward in each step.

Return the knight's minimum initial health so that he can rescue the princess.

Note that any room can contain threats or power-ups, even the first room the
knight enters and the bottom-right room where the princess is imprisoned.

Examples
--------
Example 1:
    Input:  dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]
    Output: 7
    Explanation: The initial health of the knight must be at least 7 if he
    follows the optimal path RIGHT-> RIGHT -> DOWN -> DOWN.

Example 2:
    Input:  dungeon = [[0]]
    Output: 1

Constraints
-----------
    m == dungeon.length
    n == dungeon[i].length
    1 <= m, n <= 200
    -1000 <= dungeon[i][j] <= 1000

Approach: Bottom-up DP from the princess back to the entrance
-------------------------------------------------------------
The tricky part is that a greedy forward pass fails: maximizing health at an
intermediate cell can leave the knight unable to survive a later drop. The
health he needs at a cell depends on what lies *ahead*, so we process the grid
from the bottom-right corner backwards.

Let `dp[i][j]` = the minimum health the knight must have upon *entering* room
(i, j) to be able to reach the princess. Health must stay >= 1 at all times.

    - From (i, j) the knight goes to (i+1, j) or (i, j+1); he picks whichever
      requires less entering health:
          need_next = min(dp[i+1][j], dp[i][j+1])
    - Before moving he is in room (i, j) whose value is dungeon[i][j]. After
      applying that value his health must be at least `need_next`, so on entry
      he needs:
          dp[i][j] = max(1, need_next - dungeon[i][j])
      The max(1, ...) enforces that health never drops to 0 or below.

Boundary conditions: the princess room needs `need_next = 1` (he must survive
with >= 1 health). We pad the grid with +infinity sentinels on the bottom and
right edges so the recurrence is uniform.

The answer is dp[0][0].

Complexity
----------
Time:  O(m * n)  -- each cell processed once.
Space: O(n)      -- rolling 1D row (a straightforward O(m*n) 2D table also works
                    and is shown as the alternative).
"""

from typing import List
from math import inf


def calculate_minimum_hp(dungeon: List[List[int]]) -> int:
    """Space-optimized O(n) DP: minimum entry health to rescue the princess."""
    m, n = len(dungeon), len(dungeon[0])
    # dp[j] = min health needed on entering the current row's cell j.
    dp = [inf] * (n + 1)
    dp[n - 1] = 1  # sentinel just past the princess so the corner needs 1

    for i in range(m - 1, -1, -1):
        new = [inf] * (n + 1)
        for j in range(n - 1, -1, -1):
            need_next = min(dp[j], new[j + 1])
            new[j] = max(1, need_next - dungeon[i][j])
        dp = new
    return dp[0]


def calculate_minimum_hp_2d(dungeon: List[List[int]]) -> int:
    """Alternative full 2D table version (used to cross-check the 1D one)."""
    m, n = len(dungeon), len(dungeon[0])
    dp = [[inf] * (n + 1) for _ in range(m + 1)]
    dp[m][n - 1] = 1
    dp[m - 1][n] = 1
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need_next = min(dp[i + 1][j], dp[i][j + 1])
            dp[i][j] = max(1, need_next - dungeon[i][j])
    return dp[0][0]


if __name__ == "__main__":
    # Provided examples
    assert calculate_minimum_hp([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]]) == 7
    assert calculate_minimum_hp([[0]]) == 1

    # Edge cases
    assert calculate_minimum_hp([[100]]) == 1          # power-up only room
    assert calculate_minimum_hp([[-3]]) == 4           # single damaging room
    assert calculate_minimum_hp([[1, -3, 3],
                                 [0, -2, 0],
                                 [-3, -3, -3]]) == 3
    assert calculate_minimum_hp([[0, 0, 0]]) == 1      # single row, harmless
    assert calculate_minimum_hp([[0], [0], [0]]) == 1  # single column, harmless
    assert calculate_minimum_hp([[-5]]) == 6           # need to survive -5

    # Cross-check the 1D and 2D formulations on random grids.
    import random
    for _ in range(500):
        m = random.randint(1, 8)
        n = random.randint(1, 8)
        grid = [[random.randint(-20, 20) for _ in range(n)] for _ in range(m)]
        assert calculate_minimum_hp(grid) == calculate_minimum_hp_2d(grid), grid

    print("All tests passed for 174. Dungeon Game")
