"""
778. Swim in Rising Water
Difficulty: Hard
Topics: Array, Binary Search, Depth-First Search, Breadth-First Search,
        Union Find, Heap (Priority Queue), Matrix

Problem:
You are given an n x n integer matrix grid where each value grid[i][j]
represents the elevation at that point (i, j).

The rain starts to fall. At time t, the depth of the water everywhere is t.
You can swim from a square to another 4-directionally adjacent square if and
only if the elevation of both squares individually are at most t. You can swim
infinite distances in zero time. Of course, you must stay within the boundaries
of the grid during your swim.

Return the least time until you can reach the bottom right square (n - 1, n - 1)
if you start at the top left square (0, 0).

Example 1:
    Input: grid = [[0,2],[1,3]]
    Output: 3
    Explanation: At time 0 you are at (0,0). You cannot go anywhere else
    because 4-directionally adjacent neighbours have higher elevation than t=0.
    You cannot reach (1,1) until time 3, when all cells are swimmable.

Example 2:
    Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],
                   [11,17,18,19,20],[10,9,8,7,6]]
    Output: 16
    Explanation: We need to wait until time 16 so that (0,0) and (4,4) are
    connected.

Constraints:
    n == grid.length
    n == grid[i].length
    1 <= n <= 50
    0 <= grid[i][j] < n^2
    Each value grid[i][j] is unique.

Approach (Modified Dijkstra / minimax path):
    The time needed along a path is the maximum elevation on that path, so we
    want the path from (0,0) to (n-1,n-1) minimising its maximum cell. This is
    a "bottleneck shortest path" and Dijkstra works with the cost function
    cost(path + cell) = max(cost(path), cell), which is monotone
    non-decreasing - the property Dijkstra needs.

    Push (grid[0][0], 0, 0) into a min-heap. Repeatedly pop the cell with the
    smallest bottleneck seen so far; the first time a cell is popped its value
    is final. When the target is popped, return its bottleneck.

Complexity:
    Time:  O(n^2 log n) - n^2 cells, each pushed once (marked on push).
    Space: O(n^2) for the heap and visited set.

Alternative (Binary search on time + BFS):
    The answer T lies in [max(grid[0][0], grid[-1][-1]), n^2 - 1]. For a
    candidate T, BFS over cells with elevation <= T and check if the target is
    reachable. Feasibility is monotone in T, so binary search finds the
    smallest feasible T. O(n^2 log n) time, O(n^2) space.

Alternative 2 (Union-Find by increasing elevation):
    Process cells in increasing elevation order, unioning with already-open
    neighbours; the first elevation at which (0,0) and (n-1,n-1) share a root
    is the answer.
"""

import heapq
from collections import deque
from typing import List


def swim_in_water(grid: List[List[int]]) -> int:
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    while heap:
        t, r, c = heapq.heappop(heap)
        if r == n - 1 and c == n - 1:
            return t
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
    return -1  # unreachable per constraints


def swim_in_water_binary_search(grid: List[List[int]]) -> int:
    n = len(grid)

    def can_reach(t: int) -> bool:
        if grid[0][0] > t:
            return False
        q = deque([(0, 0)])
        seen = {(0, 0)}
        while q:
            r, c = q.popleft()
            if r == n - 1 and c == n - 1:
                return True
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen
                        and grid[nr][nc] <= t):
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return False

    lo, hi = max(grid[0][0], grid[n - 1][n - 1]), n * n - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if can_reach(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def swim_in_water_union_find(grid: List[List[int]]) -> int:
    n = len(grid)
    parent = list(range(n * n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    pos = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            pos[grid[r][c]] = (r, c)

    for t in range(n * n):
        r, c = pos[t]
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] <= t:
                a, b = find(r * n + c), find(nr * n + nc)
                if a != b:
                    parent[a] = b
        if find(0) == find(n * n - 1):
            return t
    return -1


if __name__ == "__main__":
    import random

    cases = [
        ([[0, 2], [1, 3]], 3),
        ([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16],
          [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]], 16),
        ([[0]], 0),
        ([[3, 2], [0, 1]], 3),               # start cell is the bottleneck
        ([[0, 3], [2, 1]], 2),               # go down then right
        ([[0, 1, 2], [7, 8, 3], [6, 5, 4]], 4),
    ]
    solvers = (swim_in_water, swim_in_water_binary_search, swim_in_water_union_find)
    for grid, expected in cases:
        for f in solvers:
            assert f(grid) == expected, (f.__name__, grid, expected)

    random.seed(778)
    for _ in range(200):
        n = random.randint(1, 7)
        vals = list(range(n * n))
        random.shuffle(vals)
        g = [vals[i * n:(i + 1) * n] for i in range(n)]
        results = {f(g) for f in solvers}
        assert len(results) == 1, (g, results)

    big = list(range(2500))
    random.shuffle(big)
    gbig = [big[i * 50:(i + 1) * 50] for i in range(50)]
    assert len({f(gbig) for f in solvers}) == 1
    print("All tests passed for 778. Swim in Rising Water")
