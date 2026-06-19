"""
Problem #417 — Pacific Atlantic Water Flow
Difficulty: Medium
Topics: Graph, BFS, DFS, Matrix

Return cells from which water can flow to both Pacific (top/left) and Atlantic (bottom/right).

Approach: Reverse multi-source BFS from each ocean's border, flood uphill.
Intersection of reachable sets = answer.

Complexity: O(m*n) time and space.
"""

from collections import deque
from typing import List


def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    if not heights or not heights[0]:
        return []

    m, n = len(heights), len(heights[0])
    DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def bfs(starts: List[tuple]) -> set:
        visited = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < m and 0 <= nc < n
                        and (nr, nc) not in visited
                        and heights[nr][nc] >= heights[r][c]):
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return visited

    pacific_starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
    atlantic_starts = [(m-1, c) for c in range(n)] + [(r, n-1) for r in range(m-1)]

    pacific = bfs(pacific_starts)
    atlantic = bfs(atlantic_starts)

    return [[r, c] for r, c in pacific & atlantic]


if __name__ == "__main__":
    def sr(res): return sorted(tuple(x) for x in res)
    heights1 = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    expected1 = sorted([(0,4),(1,3),(1,4),(2,2),(3,0),(3,1),(4,0)])
    assert sr(pacificAtlantic(heights1)) == expected1
    assert sr(pacificAtlantic([[1]])) == [(0, 0)]
    assert sr(pacificAtlantic([[1,2,3]])) == [(0,0),(0,1),(0,2)]
    print("All tests passed!")
