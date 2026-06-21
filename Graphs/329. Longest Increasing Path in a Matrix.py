"""
Problem #329: Longest Increasing Path in a Matrix
Difficulty: Hard
Topics: DFS, Dynamic Programming, Memoization, Graph

Problem Statement:
    Given an m x n integers matrix, return the length of the longest increasing path in the matrix.
    From each cell, you can either move in four directions: left, right, up, or down.
    You may NOT move diagonally or move outside the boundary.
    You may NOT move to a cell with an equal or smaller value (strictly increasing only).

Examples:
    Example 1:
        Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]
        Output: 4
        Explanation: The longest increasing path is [1, 2, 6, 9].

    Example 2:
        Input: matrix = [[3,4,5],[3,2,6],[2,2,1]]
        Output: 4
        Explanation: The longest increasing path is [3, 4, 5, 6].

    Example 3:
        Input: matrix = [[1]]
        Output: 1

Constraints:
    - m == matrix.length
    - n == matrix[i].length
    - 1 <= m, n <= 200
    - 0 <= matrix[i][j] <= 2^31 - 1

Approach (DFS + Memoization):
    For each cell (r, c), the longest increasing path starting there is:
        1 + max(dfs(neighbor)) for all valid neighbors with greater value.

    Key insight: because paths are strictly increasing, the DFS graph is a DAG (no cycles).
    This means memoization is safe -- we never revisit a cell in the same DFS path, and
    cached results are always correct.

    Algorithm:
        1. For each unvisited cell, run DFS.
        2. Cache the result in memo[r][c].
        3. Track the global maximum.

    Why no visited set needed: strict increase guarantees we can't loop back (value must always
    grow), so we never revisit a cell during DFS descent.

Complexity:
    Time:  O(m * n) -- each cell computed exactly once due to memoization
    Space: O(m * n) -- memo table + recursion stack (at most m*n deep in a chain)

Alternative Approach (Topological Sort / BFS with indegree):
    Build a DAG where edge u->v exists if v is a valid next cell from u (v > u, adjacent).
    Process cells in topological order (Kahn's algorithm). Track the "level" of each cell.
    The max level is the answer. Avoids recursion stack. O(m*n) time and space.
"""

from typing import List
from functools import lru_cache


def longestIncreasingPath(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    memo = {}

    def dfs(r: int, c: int) -> int:
        if (r, c) in memo:
            return memo[(r, c)]

        best = 1
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))

        memo[(r, c)] = best
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))


def longestIncreasingPath_topo(matrix: List[List[int]]) -> int:
    """Topological sort (Kahn's BFS) approach -- no recursion."""
    from collections import deque

    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # indegree[r][c] = number of neighbors that are smaller (i.e., must be processed before (r,c))
    indegree = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] < matrix[r][c]:
                    indegree[r][c] += 1

    # Start with cells that have no smaller neighbors (local minima)
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if indegree[r][c] == 0:
                queue.append((r, c))

    length = 0
    while queue:
        length += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    indegree[nr][nc] -= 1
                    if indegree[nr][nc] == 0:
                        queue.append((nr, nc))

    return length


if __name__ == "__main__":
    def check(matrix, expected):
        r1 = longestIncreasingPath(matrix)
        r2 = longestIncreasingPath_topo(matrix)
        assert r1 == expected, f"DFS: got {r1}, expected {expected} for {matrix}"
        assert r2 == expected, f"Topo: got {r2}, expected {expected} for {matrix}"

    check([[9, 9, 4], [6, 6, 8], [2, 1, 1]], 4)
    check([[3, 4, 5], [3, 2, 6], [2, 2, 1]], 4)
    check([[1]], 1)

    # Single row increasing
    check([[1, 2, 3, 4, 5]], 5)

    # Single row decreasing
    check([[5, 4, 3, 2, 1]], 5)

    # All same values -- each cell is length 1
    check([[1, 1], [1, 1]], 1)

    # 2x2 increasing spiral
    check([[1, 2], [4, 3]], 4)  # 1 -> 2 -> 3 -> 4

    # Large plateau with one peak
    check([[1, 2, 3], [6, 5, 4], [7, 8, 9]], 9)

    # Connected increasing path through whole matrix
    check([[1, 100], [2, 3]], 4)  # 1->2->3->100

    print("All tests passed!")
