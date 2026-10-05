"""
695. Max Area of Island
Difficulty: Medium
Topics: Array, Depth-First Search, Breadth-First Search, Union Find, Matrix

Problem:
You are given an m x n binary matrix grid. An island is a group of 1's
(representing land) connected 4-directionally (horizontal or vertical). You may
assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.

Example 1:
    Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],
                   [0,0,0,0,0,0,0,1,1,1,0,0,0],
                   [0,1,1,0,1,0,0,0,0,0,0,0,0],
                   [0,1,0,0,1,1,0,0,1,0,1,0,0],
                   [0,1,0,0,1,1,0,0,1,1,1,0,0],
                   [0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,0,0,0,0,0,0,1,1,1,0,0,0],
                   [0,0,0,0,0,0,0,1,1,0,0,0,0]]
    Output: 6
    Explanation: The answer is not 11, because the island must be connected
    4-directionally.

Example 2:
    Input: grid = [[0,0,0,0,0,0,0,0]]
    Output: 0

Constraints:
    m == grid.length
    n == grid[i].length
    1 <= m, n <= 50
    grid[i][j] is either 0 or 1.

Approach (Iterative DFS flood fill):
    Scan every cell. When an unvisited land cell is found, it is the first cell
    of a new island, so flood-fill the whole island with an explicit stack,
    counting cells as they are popped. Each land cell is marked visited (set to
    0 in a copy of the grid) the moment it is pushed, so it is counted exactly
    once and never pushed twice. Track the maximum count over all islands.

    Why it works: 4-directional connectivity defines connected components of
    land cells; flood fill from any cell of a component reaches exactly that
    component, so its count is the island's area.

    An explicit stack avoids Python's recursion limit on a 50x50 all-land grid
    (2500 cells deep).

Complexity:
    Time:  O(m * n) - every cell is pushed/popped at most once.
    Space: O(m * n) - grid copy plus the stack in the worst case.

Alternative (Union-Find):
    Union each land cell with its land neighbours, tracking component sizes;
    the answer is the largest size. Same O(m*n * alpha) time, useful when
    cells are added online (see 305. Number of Islands II).
"""

from typing import List


def max_area_of_island(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    g = [row[:] for row in grid]  # don't mutate caller's input
    best = 0

    for r in range(rows):
        for c in range(cols):
            if g[r][c] != 1:
                continue
            g[r][c] = 0
            stack = [(r, c)]
            area = 0
            while stack:
                cr, cc = stack.pop()
                area += 1
                for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and g[nr][nc] == 1:
                        g[nr][nc] = 0
                        stack.append((nr, nc))
            best = max(best, area)
    return best


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def max_area_of_island_union_find(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    dsu = DSU(rows * cols)
    has_land = False
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            has_land = True
            idx = r * cols + c
            if r + 1 < rows and grid[r + 1][c] == 1:
                dsu.union(idx, idx + cols)
            if c + 1 < cols and grid[r][c + 1] == 1:
                dsu.union(idx, idx + 1)
    if not has_land:
        return 0
    return max(
        dsu.size[dsu.find(r * cols + c)]
        for r in range(rows)
        for c in range(cols)
        if grid[r][c] == 1
    )


if __name__ == "__main__":
    ex1 = [[0,0,1,0,0,0,0,1,0,0,0,0,0],
           [0,0,0,0,0,0,0,1,1,1,0,0,0],
           [0,1,1,0,1,0,0,0,0,0,0,0,0],
           [0,1,0,0,1,1,0,0,1,0,1,0,0],
           [0,1,0,0,1,1,0,0,1,1,1,0,0],
           [0,0,0,0,0,0,0,0,0,0,1,0,0],
           [0,0,0,0,0,0,0,1,1,1,0,0,0],
           [0,0,0,0,0,0,0,1,1,0,0,0,0]]
    cases = [
        (ex1, 6),
        ([[0,0,0,0,0,0,0,0]], 0),
        ([[1]], 1),
        ([[0]], 0),
        ([[1,1],[1,1]], 4),
        ([[1,0],[0,1]], 1),              # diagonal does not connect
        ([[1,1,0,0],[1,0,0,1],[0,0,1,1]], 3),
        ([[1] * 50 for _ in range(50)], 2500),  # deep: no recursion limit issue
    ]
    for grid, expected in cases:
        snapshot = [row[:] for row in grid]
        assert max_area_of_island(grid) == expected, (grid, expected)
        assert grid == snapshot, "input must not be mutated"
        assert max_area_of_island_union_find(grid) == expected, (grid, expected)
    print("All tests passed for 695. Max Area of Island")
