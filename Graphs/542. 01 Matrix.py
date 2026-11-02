"""
542. 01 Matrix
Difficulty: Medium
Topics: Array, Dynamic Programming, Breadth-First Search, Matrix

Problem:
Given an m x n binary matrix mat, return the distance of the nearest 0 for each
cell. The distance between two cells sharing a common edge is 1.

Example 1:
  Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
  Output: [[0,0,0],[0,1,0],[0,0,0]]
Example 2:
  Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
  Output: [[0,0,0],[0,1,0],[1,2,1]]

Constraints:
  m == mat.length, n == mat[i].length
  1 <= m, n <= 10^4, 1 <= m * n <= 10^4
  mat[i][j] is either 0 or 1.
  There is at least one 0 in mat.

Approach (multi-source BFS):
Start BFS from every 0 simultaneously (distance 0). BFS expands in layers, so
the first time a cell is reached it is by the closest 0. Cells with 1 start as
unvisited (-1) and are assigned dist[parent] + 1 when discovered.

Complexity:
  Time:  O(m * n)  - each cell enqueued once
  Space: O(m * n)

Alternative (two-pass DP): nearest 0 is reached from top/left or bottom/right.
Pass 1 (top-left to bottom-right) takes min(up, left) + 1; pass 2 (reverse)
takes min(down, right) + 1. Also O(m * n) time, O(1) extra space.
"""
from collections import deque
from typing import List


def updateMatrix(mat: List[List[int]]) -> List[List[int]]:
    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    q = deque()
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                dist[i][j] = 0
                q.append((i, j))
    while q:
        i, j = q.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            x, y = i + di, j + dj
            if 0 <= x < m and 0 <= y < n and dist[x][y] == -1:
                dist[x][y] = dist[i][j] + 1
                q.append((x, y))
    return dist


def updateMatrixDP(mat: List[List[int]]) -> List[List[int]]:
    m, n = len(mat), len(mat[0])
    INF = m + n + 1
    d = [[0 if mat[i][j] == 0 else INF for j in range(n)] for i in range(m)]
    for i in range(m):
        for j in range(n):
            if i > 0:
                d[i][j] = min(d[i][j], d[i - 1][j] + 1)
            if j > 0:
                d[i][j] = min(d[i][j], d[i][j - 1] + 1)
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if i < m - 1:
                d[i][j] = min(d[i][j], d[i + 1][j] + 1)
            if j < n - 1:
                d[i][j] = min(d[i][j], d[i][j + 1] + 1)
    return d


if __name__ == "__main__":
    import random
    for f in (updateMatrix, updateMatrixDP):
        assert f([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
        assert f([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == [[0, 0, 0], [0, 1, 0], [1, 2, 1]]
        assert f([[0]]) == [[0]]
        assert f([[0, 1, 1, 1]]) == [[0, 1, 2, 3]]
        assert f([[1], [1], [0]]) == [[2], [1], [0]]
        assert f([[1, 1], [1, 0]]) == [[2, 1], [1, 0]]
    for _ in range(200):
        m, n = random.randint(1, 6), random.randint(1, 6)
        g = [[random.randint(0, 1) for _ in range(n)] for _ in range(m)]
        g[random.randrange(m)][random.randrange(n)] = 0
        zeros = [(i, j) for i in range(m) for j in range(n) if g[i][j] == 0]
        exp = [[min(abs(i - a) + abs(j - b) for a, b in zeros) for j in range(n)] for i in range(m)]
        assert updateMatrix(g) == exp and updateMatrixDP(g) == exp, g
    print("All tests passed.")
