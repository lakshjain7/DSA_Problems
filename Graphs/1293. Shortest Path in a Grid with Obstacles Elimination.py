"""
1293. Shortest Path in a Grid with Obstacles Elimination
Difficulty: Hard
Topics: Array, Breadth-First Search, Matrix

Problem:
You are given an m x n integer matrix grid where each cell is either 0 (empty)
or 1 (obstacle). You can move up, down, left, or right from and to an empty
cell in one step.

Return the minimum number of steps to walk from the upper left corner (0, 0) to
the lower right corner (m - 1, n - 1) given that you can eliminate at most k
obstacles. If it is not possible to find such walk return -1.

Example 1:
  Input: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1
  Output: 6
  Explanation: Without elimination the shortest path is 10 steps. Eliminating
  the obstacle at (3,2) gives (0,0)->(0,1)->(0,2)->(1,2)->(2,2)->(3,2)->(4,2),
  which is 6 steps.

Example 2:
  Input: grid = [[0,1,1],[1,1,1],[1,0,0]], k = 1
  Output: -1
  Explanation: We need to eliminate at least two obstacles to find such a walk.

Constraints:
  - m == grid.length, n == grid[i].length
  - 1 <= m, n <= 40
  - 1 <= k <= m * n
  - grid[i][j] is either 0 or 1.
  - grid[0][0] == grid[m - 1][n - 1] == 0

Approach (BFS over augmented state (row, col, remaining_k)):
  Plain BFS on cells fails because reaching a cell with more eliminations left
  is strictly better than reaching it with fewer, even if later. So the state
  is (r, c, rem). All edges have weight 1, hence BFS gives shortest steps.
  Pruning:
    1) If k >= m + n - 2, a Manhattan path is always possible: return m+n-2
       (we can blast through every obstacle on any monotone path).
    2) best[r][c] = max remaining eliminations with which (r, c) has been
       reached. A new arrival with rem <= best[r][c] is dominated (it is no
       earlier — BFS order — and has no more budget), so skip it. This
       collapses the state space to at most m*n*(k+1) but usually far less.

Complexity:
  Time:  O(m * n * k) in the worst case (each (cell, rem) enqueued once).
  Space: O(m * n * k) for the queue in the worst case; O(m*n) for best[].

Alternative approach (A* with Manhattan heuristic):
  Use a priority queue keyed by steps + manhattan_distance_to_target, still on
  (r, c, rem) states. The heuristic is admissible (never overestimates), so
  the first time the target is popped it is optimal; it typically explores
  far fewer states on large open grids.
"""
from collections import deque
import heapq
from typing import List


def shortest_path(grid: List[List[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if k >= m + n - 2:
        return m + n - 2

    best = [[-1] * n for _ in range(m)]
    best[0][0] = k
    q = deque([(0, 0, k)])
    steps = 0
    while q:
        for _ in range(len(q)):
            r, c, rem = q.popleft()
            if r == m - 1 and c == n - 1:
                return steps
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nrem = rem - grid[nr][nc]
                    if nrem > best[nr][nc]:
                        best[nr][nc] = nrem
                        q.append((nr, nc, nrem))
        steps += 1
    return -1


def shortest_path_astar(grid: List[List[int]], k: int) -> int:
    """Alternative: A* search on (r, c, rem) with Manhattan heuristic."""
    m, n = len(grid), len(grid[0])
    tr, tc = m - 1, n - 1
    if k >= m + n - 2:
        return m + n - 2

    def h(r: int, c: int) -> int:
        return (tr - r) + (tc - c)

    heap = [(h(0, 0), 0, 0, 0, k)]  # (f, g, r, c, rem)
    seen = {(0, 0, k)}
    while heap:
        f, g, r, c, rem = heapq.heappop(heap)
        # Shortcut: with enough budget left, walk straight to the target.
        if h(r, c) <= rem:
            return g + h(r, c)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n:
                nrem = rem - grid[nr][nc]
                if nrem >= 0 and (nr, nc, nrem) not in seen:
                    seen.add((nr, nc, nrem))
                    heapq.heappush(heap, (g + 1 + h(nr, nc), g + 1, nr, nc, nrem))
    return -1


if __name__ == "__main__":
    for f in (shortest_path, shortest_path_astar):
        assert f([[0, 0, 0], [1, 1, 0], [0, 0, 0], [0, 1, 1], [0, 0, 0]], 1) == 6
        assert f([[0, 1, 1], [1, 1, 1], [1, 0, 0]], 1) == -1
        # Single cell
        assert f([[0]], 1) == 0
        # Large k shortcut
        assert f([[0, 1, 1], [1, 1, 1], [1, 1, 0]], 4) == 4
        # Must detour because k is too small to go straight
        g = [[0, 1, 0, 0, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 1, 0]]
        assert f(g, 0 + 1) == 6
        # Zero-elimination behaviour via k=1 where an obstacle-free path exists
        assert f([[0, 0], [0, 0]], 1) == 2
        # Wall needing exactly two breaks
        w = [[0, 1, 1, 0],
             [1, 1, 1, 1],
             [1, 1, 1, 0]]
        assert f(w, 2) == -1
        assert f(w, 3) == 5

    # Randomized cross-check between BFS and A*
    import random
    random.seed(42)
    for _ in range(300):
        m, n = random.randint(1, 6), random.randint(1, 6)
        g = [[1 if random.random() < 0.4 else 0 for _ in range(n)] for _ in range(m)]
        g[0][0] = g[m - 1][n - 1] = 0
        k = random.randint(1, 4)
        assert shortest_path(g, k) == shortest_path_astar(g, k), (g, k)
    print("All tests passed for 1293. Shortest Path in a Grid with Obstacles Elimination")
