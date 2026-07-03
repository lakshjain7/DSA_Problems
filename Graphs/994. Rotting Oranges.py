"""
994. Rotting Oranges
Difficulty: Medium
Topics: Graphs, BFS, Matrix, Multi-source BFS

Problem Statement:
You are given an m x n grid where each cell can have one of three values:
    0 representing an empty cell,
    1 representing a fresh orange, or
    2 representing a rotten orange.

Every minute, any fresh orange that is 4-directionally adjacent to a rotten
orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a
fresh orange. If this is impossible, return -1.

Examples:
    Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
    Output: 4

    Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
    Output: -1
    Explanation: The orange in the bottom left corner (row 2, column 0) is
    never rotten, because rotting only happens 4-directionally.

    Input: grid = [[0,2]]
    Output: 0
    Explanation: Since there are no fresh oranges at minute 0, the answer is
    just 0.

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 10
    grid[i][j] is 0, 1, or 2.

Approach (Multi-source BFS):
Treat every initially rotten orange as a BFS source and push them all into a
queue simultaneously (multi-source BFS). Process the queue level by level:
each level represents one minute passing. For every rotten orange popped,
look at its 4 neighbors; any fresh orange found gets rotted, decremented
from the fresh-orange counter, and pushed into the queue for the next
level. The number of levels processed until the queue empties is the
number of minutes elapsed. If fresh oranges remain after BFS completes,
it's impossible, so return -1. Doing BFS from all rotten oranges at once
(rather than one at a time) guarantees each fresh orange is rotted at the
minute corresponding to the shortest distance to any rotten orange, which
is exactly what "elapsed minutes" means here.

Complexity Analysis:
    Time:  O(m * n) - every cell is enqueued and processed at most once.
    Space: O(m * n) - queue can hold up to all cells in the worst case.

Alternative Approach:
Repeatedly scan the whole grid, rot any fresh orange adjacent to a rotten
one, and stop when a full pass produces no changes. This simulation
approach is O((m*n)^2) in the worst case since each pass is O(m*n) and we
may need O(m*n) passes, making multi-source BFS strictly better.
"""

from collections import deque
from typing import List


def oranges_rotting(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    minutes_elapsed = 0

    while queue:
        r, c, minute = queue.popleft()
        minutes_elapsed = max(minutes_elapsed, minute)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, minute + 1))

    return minutes_elapsed if fresh == 0 else -1


def oranges_rotting_simulation(grid: List[List[int]]) -> int:
    """Alternative brute-force simulation approach for comparison."""
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    minutes = 0

    def has_fresh():
        return any(grid[r][c] == 1 for r in range(rows) for c in range(cols))

    while has_fresh():
        to_rot = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 2:
                    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            to_rot.append((nr, nc))
        if not to_rot:
            return -1
        for nr, nc in to_rot:
            grid[nr][nc] = 2
        minutes += 1

    return minutes


if __name__ == "__main__":
    assert oranges_rotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting([[0, 2]]) == 0
    assert oranges_rotting([[0]]) == 0
    assert oranges_rotting([[1]]) == -1
    assert oranges_rotting([[2]]) == 0
    assert oranges_rotting([[2, 2], [1, 1]]) == 1

    assert oranges_rotting_simulation([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
    assert oranges_rotting_simulation([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
    assert oranges_rotting_simulation([[0, 2]]) == 0

    print("All tests passed for 994. Rotting Oranges")
