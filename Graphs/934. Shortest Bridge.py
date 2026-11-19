"""
934. Shortest Bridge
Difficulty: Medium
Topics: Array, Depth-First Search, Breadth-First Search, Matrix

Problem:
You are given an n x n binary matrix grid where 1 represents land and 0 represents
water. An island is a 4-directionally connected group of 1's not connected to any
other 1's. There are exactly two islands in grid.

You may change 0's to 1's to connect the two islands to form one island.

Return the smallest number of 0's you must flip to connect the two islands.

Example 1:
    Input: grid = [[0,1],[1,0]]
    Output: 1

Example 2:
    Input: grid = [[0,1,0],[0,0,0],[0,0,1]]
    Output: 2

Example 3:
    Input: grid = [[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
    Output: 1

Constraints:
    n == grid.length == grid[i].length
    2 <= n <= 100
    grid[i][j] is either 0 or 1.
    There are exactly two islands in grid.

Approach (DFS to label one island, then multi-source BFS):
    1. Find any land cell and flood-fill its whole island (iterative DFS), marking
       its cells as 2 and collecting them all as BFS sources at distance 0.
    2. Run BFS outward from all of those cells simultaneously. Expanding one layer
       at a time means the first time we touch a cell of value 1 (the other island)
       we have used the minimum number of water cells; the current layer number is
       the answer. Multi-source BFS is correct because it is equivalent to adding a
       virtual super-source connected to every cell of island A with cost 0.

Complexity:
    Time:  O(n^2) - every cell is visited at most once by DFS and once by BFS.
    Space: O(n^2) for the stack/queue in the worst case.

Alternative:
    Collect the cells of both islands and take min(|r1-r2| + |c1-c2| - 1) over all
    pairs. Correct (Manhattan paths through water exist between the closest pair)
    but O(n^4) in the worst case; used below as a brute-force checker.
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def shortestBridge(self, grid: List[List[int]]) -> int:
        grid = [row[:] for row in grid]  # don't mutate caller's input
        n = len(grid)

        start = next((r, c) for r in range(n) for c in range(n) if grid[r][c] == 1)
        q = deque()
        stack = [start]
        grid[start[0]][start[1]] = 2
        while stack:
            r, c = stack.pop()
            q.append((r, c))
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    stack.append((nr, nc))

        steps = 0
        while q:
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < n and 0 <= nc < n):
                        continue
                    if grid[nr][nc] == 1:
                        return steps
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 2
                        q.append((nr, nc))
            steps += 1
        return -1  # unreachable under the constraints

    def shortestBridgePairs(self, grid: List[List[int]]) -> int:
        n = len(grid)
        seen = [[False] * n for _ in range(n)]
        islands = []
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1 and not seen[r][c]:
                    cells, stack = [], [(r, c)]
                    seen[r][c] = True
                    while stack:
                        x, y = stack.pop()
                        cells.append((x, y))
                        for dx, dy in DIRS:
                            a, b = x + dx, y + dy
                            if 0 <= a < n and 0 <= b < n and grid[a][b] == 1 and not seen[a][b]:
                                seen[a][b] = True
                                stack.append((a, b))
                    islands.append(cells)
        a, b = islands
        return min(abs(x1 - x2) + abs(y1 - y2) - 1 for x1, y1 in a for x2, y2 in b)


if __name__ == "__main__":
    s = Solution()
    cases = [
        ([[0, 1], [1, 0]], 1),
        ([[0, 1, 0], [0, 0, 0], [0, 0, 1]], 2),
        ([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]], 1),
        ([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]], 5),  # opposite corners
        ([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1]], 2),  # nearest pair is diagonal
        ([[1, 0, 1], [1, 0, 1], [1, 0, 1]], 1),                         # parallel walls
    ]
    for grid, exp in cases:
        original = [row[:] for row in grid]
        assert s.shortestBridge(grid) == exp, grid
        assert grid == original, "input was mutated"
        assert s.shortestBridgePairs(grid) == exp, grid

    # Randomised cross-check: two random single cells / small blobs.
    import random
    random.seed(1)
    for _ in range(200):
        n = random.randint(2, 8)
        cells = random.sample([(r, c) for r in range(n) for c in range(n)], 2)
        (r1, c1), (r2, c2) = cells
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            continue  # adjacent cells would form one island
        g = [[0] * n for _ in range(n)]
        g[r1][c1] = g[r2][c2] = 1
        assert s.shortestBridge(g) == s.shortestBridgePairs(g)

    big = [[0] * 100 for _ in range(100)]
    big[0][0] = big[99][99] = 1
    assert s.shortestBridge(big) == 197
    print("All tests passed!")
