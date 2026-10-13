"""
827. Making A Large Island
Difficulty: Hard
Topics: Array, Depth-First Search, Breadth-First Search, Union Find, Matrix

Problem:
You are given an n x n binary matrix grid. You are allowed to change at most
one 0 to be 1. Return the size of the largest island in grid after applying
this operation. An island is a 4-directionally connected group of 1s.

Example 1:
    Input: grid = [[1,0],[0,1]]   Output: 3
Example 2:
    Input: grid = [[1,1],[1,0]]   Output: 4
Example 3:
    Input: grid = [[1,1],[1,1]]   Output: 4

Constraints:
    n == grid.length == grid[i].length
    1 <= n <= 500
    grid[i][j] is either 0 or 1.

Approach (label islands, then try each 0):
    1. Flood-fill every island, give it an id (2, 3, ...) and record its size.
    2. For each 0 cell, collect the *distinct* ids among its 4 neighbours;
       flipping it merges those islands, giving 1 + sum of their sizes.
    3. Answer is the max over all zeros; if there are no zeros the whole grid
       is one island of size n*n.
    Using a set of neighbour ids prevents double-counting an island that
    touches the cell on several sides.

Complexity:
    Time: O(n^2)    Space: O(n^2)

Alternative: Union-Find with component sizes (same complexity), implemented
below as largestIslandDSU.
"""
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def largestIsland(grid: List[List[int]]) -> int:
    n = len(grid)
    g = [row[:] for row in grid]
    size = {}
    next_id = 2
    for r in range(n):
        for c in range(n):
            if g[r][c] == 1:
                stack = [(r, c)]
                g[r][c] = next_id
                cnt = 0
                while stack:
                    x, y = stack.pop()
                    cnt += 1
                    for dx, dy in DIRS:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n and g[nx][ny] == 1:
                            g[nx][ny] = next_id
                            stack.append((nx, ny))
                size[next_id] = cnt
                next_id += 1
    best = max(size.values(), default=0)
    for r in range(n):
        for c in range(n):
            if g[r][c] == 0:
                seen = set()
                for dx, dy in DIRS:
                    nx, ny = r + dx, c + dy
                    if 0 <= nx < n and 0 <= ny < n and g[nx][ny] > 1:
                        seen.add(g[nx][ny])
                best = max(best, 1 + sum(size[i] for i in seen))
    return best


def largestIslandDSU(grid: List[List[int]]) -> int:
    """Alternative: Union-Find."""
    n = len(grid)
    parent = list(range(n * n))
    sz = [1] * (n * n)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            if sz[ra] < sz[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            sz[ra] += sz[rb]

    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                if r + 1 < n and grid[r + 1][c]:
                    union(r * n + c, (r + 1) * n + c)
                if c + 1 < n and grid[r][c + 1]:
                    union(r * n + c, r * n + c + 1)
    best = max((sz[find(i)] for i in range(n * n) if grid[i // n][i % n]), default=0)
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                roots = set()
                for dx, dy in DIRS:
                    nx, ny = r + dx, c + dy
                    if 0 <= nx < n and 0 <= ny < n and grid[nx][ny]:
                        roots.add(find(nx * n + ny))
                best = max(best, 1 + sum(sz[x] for x in roots))
    return best


if __name__ == "__main__":
    tests = [
        ([[1, 0], [0, 1]], 3),
        ([[1, 1], [1, 0]], 4),
        ([[1, 1], [1, 1]], 4),
        ([[0]], 1),
        ([[1]], 1),
        ([[0, 0], [0, 0]], 1),
        ([[1, 0, 1], [0, 0, 0], [1, 0, 1]], 3),
        ([[1, 0, 1], [1, 0, 1], [1, 1, 1]], 8),
        ([[0, 1, 0], [1, 0, 1], [0, 1, 0]], 5),
    ]
    for g, exp in tests:
        assert largestIsland(g) == exp, (g, exp, largestIsland(g))
        assert largestIslandDSU(g) == exp, (g, exp, largestIslandDSU(g))
    print("All tests passed.")
