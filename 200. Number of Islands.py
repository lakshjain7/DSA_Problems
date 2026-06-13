"""
Problem 200: Number of Islands
Difficulty: Medium
Topics: Array, Depth-First Search, Breadth-First Search, Union Find, Matrix

Problem Statement:
Given an m x n 2D binary grid where '1' represents land and '0' represents water,
return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands
horizontally or vertically. You may assume all four edges of the grid are surrounded
by water.

Examples:
    Example 1:
        Input: grid = [
          ["1","1","1","1","0"],
          ["1","1","0","1","0"],
          ["1","1","0","0","0"],
          ["0","0","0","0","0"]
        ]
        Output: 1

    Example 2:
        Input: grid = [
          ["1","1","0","0","0"],
          ["1","1","0","0","0"],
          ["0","0","1","0","0"],
          ["0","0","0","1","1"]
        ]
        Output: 3

Constraints:
    - m == grid.length
    - n == grid[i].length
    - 1 <= m, n <= 300
    - grid[i][j] is '0' or '1'

Approach (DFS):
    For each unvisited '1' cell, launch a DFS that marks all connected land cells
    as visited (by setting them to '0'). Each DFS call corresponds to one island.
    The count of DFS calls equals the number of islands.

    Why this works: DFS from any cell will flood-fill the entire connected component
    of land, so the next unvisited '1' must belong to a different island.

Complexity:
    Time:  O(m * n) -- each cell is visited at most once
    Space: O(m * n) -- recursion stack in the worst case (entire grid is land)
"""

from typing import List
from collections import deque


def numIslands(grid: List[List[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # Mark visited by sinking the land
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)

    return count


# Alternative Approach: BFS (iterative, avoids recursion stack overflow for large grids)
def numIslands_bfs(grid: List[List[str]]) -> int:
    """
    BFS variant -- useful when recursion depth is a concern (Python default limit ~1000).
    For a 300x300 grid filled with land, DFS could hit stack limits; BFS uses a queue.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def bfs(r: int, c: int) -> None:
        queue = deque([(r, c)])
        grid[r][c] = "0"
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                bfs(r, c)

    return count


if __name__ == "__main__":
    # Single large island
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert numIslands([row[:] for row in grid1]) == 1

    # Three separate islands
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert numIslands([row[:] for row in grid2]) == 3

    # All water
    grid3 = [["0", "0", "0"], ["0", "0", "0"]]
    assert numIslands([row[:] for row in grid3]) == 0

    # All land
    grid4 = [["1", "1"], ["1", "1"]]
    assert numIslands([row[:] for row in grid4]) == 1

    # Single cell land
    assert numIslands([["1"]]) == 1

    # Single cell water
    assert numIslands([["0"]]) == 0

    # Diagonal -- not connected (only horizontal/vertical)
    grid5 = [["1", "0"], ["0", "1"]]
    assert numIslands([row[:] for row in grid5]) == 2

    # BFS versions
    assert numIslands_bfs([row[:] for row in grid1]) == 1
    assert numIslands_bfs([row[:] for row in grid2]) == 3

    print("All tests passed!")
