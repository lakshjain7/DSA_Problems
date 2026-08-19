"""
980. Unique Paths III
Difficulty: Hard
Topics: Array, Backtracking, Bit Manipulation, Matrix

Problem Statement
-----------------
You are given an m x n integer array grid where grid[i][j] could be:

    1  representing the starting square. There is exactly one starting square.
    2  representing the ending square. There is exactly one ending square.
    0  representing empty squares we can walk over.
   -1  representing obstacles that we cannot walk over.

Return the number of 4-directional walks from the starting square to the ending
square, that walk over every non-obstacle square exactly once.

Examples
--------
Example 1:
    Input:  grid = [[1,0,0,0],[0,0,0,0],[0,0,2,-1]]
    Output: 2
    Explanation: We have the following two paths:
        1. (0,0),(0,1),(0,2),(0,3),(1,3),(1,2),(1,1),(1,0),(2,0),(2,1),(2,2)
        2. (0,0),(1,0),(2,0),(2,1),(1,1),(0,1),(0,2),(1,2),(2,2)... etc.

Example 2:
    Input:  grid = [[1,0,0,0],[0,0,0,0],[0,0,0,2]]
    Output: 4

Example 3:
    Input:  grid = [[0,1],[2,0]]
    Output: 0
    Explanation: There is no way to walk over every empty square exactly once.
        Note that the starting and ending square can be anywhere in the grid.

Constraints
-----------
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 20
    1 <= m * n <= 20
    -1 <= grid[i][j] <= 2
    There is exactly one starting cell and one ending cell.

Approach
--------
Classic backtracking / DFS with a "visited every free cell" completion check.

First count the number of walkable squares we must cover: every cell that is not
an obstacle (values 0, 1, 2). Call this `need`. We must step onto exactly that
many cells, finishing on the target square 2.

Run a DFS from the start square. Mark the current cell visited (temporarily set
it to -1 so it acts as an obstacle for deeper recursion), then explore the four
neighbours. Two things terminate a branch:

    * Reaching the end square (value 2): it counts as a valid path only if we
      have already stepped on all `need` cells (tracked by a decreasing
      `remaining` counter). Otherwise this branch is a dead end.
    * Running out of neighbours before covering everything.

On the way back up we restore the cell (backtracking), so other branches see it
as free again. Summing the valid completions gives the answer.

Why it works: The problem is an exhaustive-search / Hamiltonian-path count on a
tiny grid (m * n <= 20), so brute-force enumeration with pruning is both correct
and fast enough. The visited-restore pattern guarantees each square is used at
most once per path, and the `remaining == 0` gate at the end square enforces the
"every non-obstacle square exactly once" requirement.

Complexity
----------
Time:  O(4^(m*n)) in the worst case (each step branches up to 4 ways), but the
       "visit each cell once" constraint and the m*n <= 20 bound keep it small.
Space: O(m*n) for the recursion stack (path depth is bounded by the cell count).
"""

from typing import List
from copy import deepcopy


def uniquePathsIII(grid: List[List[int]]) -> int:
    """Count 4-directional walks from start to end covering every free cell."""
    rows, cols = len(grid), len(grid[0])

    start_r = start_c = -1
    remaining = 0  # number of non-obstacle cells still to visit
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != -1:
                remaining += 1
            if grid[r][c] == 1:
                start_r, start_c = r, c

    total = 0

    def dfs(r: int, c: int, left: int) -> None:
        nonlocal total
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == -1:
            return

        if grid[r][c] == 2:
            # Valid only when this is the last cell (all others visited).
            if left == 1:
                total += 1
            return

        saved = grid[r][c]
        grid[r][c] = -1  # mark visited

        dfs(r + 1, c, left - 1)
        dfs(r - 1, c, left - 1)
        dfs(r, c + 1, left - 1)
        dfs(r, c - 1, left - 1)

        grid[r][c] = saved  # backtrack

    dfs(start_r, start_c, remaining)
    return total


if __name__ == "__main__":
    cases = [
        ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]], 2),
        ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]], 4),
        ([[0, 1], [2, 0]], 0),
        ([[1, 2]], 1),                     # adjacent start/end, no free cells
        ([[1, 0, 2]], 1),                  # single straight path
        ([[1, -1, 2]], 0),                 # blocked by obstacle
        ([[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, -1]], 2),  # start/end swapped
        ([[1, 0], [0, 2]], 0),             # start/end diagonal: no Hamiltonian path
        ([[1, 0], [2, 0]], 1),             # start/end share a column: one covering walk
    ]

    for grid, want in cases:
        got = uniquePathsIII(deepcopy(grid))
        assert got == want, f"uniquePathsIII({grid}) = {got}, expected {want}"

    # The function must not mutate the caller's grid (backtracking restores it).
    original = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]]
    snapshot = deepcopy(original)
    uniquePathsIII(original)
    assert original == snapshot, "grid was mutated"

    print("All tests passed for 980. Unique Paths III")
