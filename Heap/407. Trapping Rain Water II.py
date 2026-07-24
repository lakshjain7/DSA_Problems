"""
407. Trapping Rain Water II
Difficulty: Hard
Topics: Array, Breadth-First Search, Heap (Priority Queue), Matrix

Problem Statement
-----------------
Given an m x n integer matrix `heightMap` representing the height of each unit
cell in a 2D elevation map, return the volume of water it can trap after raining.

Examples
--------
Example 1:
    Input:  heightMap = [[1, 4, 3, 1, 3, 2],
                         [3, 2, 1, 3, 2, 4],
                         [2, 3, 3, 2, 3, 1]]
    Output: 4
    Explanation: After the rain, water is trapped in the interior low cells,
                 totalling 4 units.

Example 2:
    Input:  heightMap = [[3, 3, 3, 3, 3],
                         [3, 2, 2, 2, 3],
                         [3, 2, 1, 2, 3],
                         [3, 2, 2, 2, 3],
                         [3, 3, 3, 3, 3]]
    Output: 10

Constraints
-----------
  - m == heightMap.length
  - n == heightMap[i].length
  - 1 <= m, n <= 200
  - 0 <= heightMap[i][j] <= 2 * 10^4

Approach
--------
In the 1D version (LeetCode 42) water above a bar is bounded by the higher of the
tallest walls to its left and right. In 2D, water can escape in any of four
directions, so a cell's water level is determined by the lowest point on the
lowest path from that cell to the border. This is naturally solved by a
"shrinking boundary" flood fill driven by a min-heap.

Algorithm (Dijkstra-like BFS from the border inward):
  1. Push every border cell into a min-heap keyed by its height, and mark all
     border cells visited. Water can never be trapped on the border itself.
  2. Repeatedly pop the lowest cell on the current boundary. Let its height be
     `h`. This is the current water level of the frontier — the lowest wall
     surrounding the unexplored interior.
  3. For each unvisited neighbor:
        - If the neighbor is lower than `h`, water fills it up to level `h`;
          add (h - neighbor_height) to the total.
        - The neighbor's effective boundary height becomes max(h, neighbor_height)
          (it either holds water up to h, or is itself a taller new wall). Push
          that effective height into the heap and mark it visited.

Why it works: always processing the globally lowest boundary cell guarantees that
when we first reach an interior cell, we have approached it over the lowest
possible surrounding wall. Water it can hold equals that wall height minus its
own height. Because we expand from the outside in and never revisit a cell, each
cell's trapped water is counted exactly once and is correct. This is the standard
Dijkstra "process the minimum frontier" argument applied to elevation.

Complexity
----------
Let m x n = number of cells.
Time:  O(m * n * log(m * n)) — each cell is pushed/popped from the heap once.
Space: O(m * n) for the visited grid and the heap.
"""

import heapq
from typing import List


def trapRainWater(heightMap: List[List[int]]) -> int:
    if not heightMap or not heightMap[0]:
        return 0

    m, n = len(heightMap), len(heightMap[0])

    # Water needs an enclosed interior; grids thinner than 3 in either dimension
    # cannot trap anything.
    if m < 3 or n < 3:
        return 0

    visited = [[False] * n for _ in range(m)]
    heap: List[tuple] = []

    # Seed the heap with all border cells.
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                visited[i][j] = True
                heapq.heappush(heap, (heightMap[i][j], i, j))

    total = 0
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while heap:
        height, i, j = heapq.heappop(heap)
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not visited[ni][nj]:
                visited[ni][nj] = True
                # Water trapped here is bounded by the current frontier height.
                if heightMap[ni][nj] < height:
                    total += height - heightMap[ni][nj]
                # New boundary height for this cell.
                boundary = max(height, heightMap[ni][nj])
                heapq.heappush(heap, (boundary, ni, nj))

    return total


if __name__ == "__main__":
    # Example 1
    assert trapRainWater([
        [1, 4, 3, 1, 3, 2],
        [3, 2, 1, 3, 2, 4],
        [2, 3, 3, 2, 3, 1],
    ]) == 4

    # Example 2
    assert trapRainWater([
        [3, 3, 3, 3, 3],
        [3, 2, 2, 2, 3],
        [3, 2, 1, 2, 3],
        [3, 2, 2, 2, 3],
        [3, 3, 3, 3, 3],
    ]) == 10

    # Edge: too thin to trap water.
    assert trapRainWater([[1, 2, 3]]) == 0
    assert trapRainWater([[1], [2], [3]]) == 0
    assert trapRainWater([[5, 5], [5, 5]]) == 0

    # Edge: flat interior, no trapping.
    assert trapRainWater([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]) == 0

    # Single deep well: walls of height 5 around a single 0 cell -> 5 units.
    assert trapRainWater([
        [5, 5, 5],
        [5, 0, 5],
        [5, 5, 5],
    ]) == 5

    # A leak on the border means no water is held.
    assert trapRainWater([
        [5, 5, 5],
        [5, 0, 0],
        [5, 5, 5],
    ]) == 0

    # Two-cell basin bounded by height 4 walls; interior cells 1 and 2.
    assert trapRainWater([
        [4, 4, 4, 4],
        [4, 1, 2, 4],
        [4, 4, 4, 4],
    ]) == (4 - 1) + (4 - 2)

    print("All tests passed for 407. Trapping Rain Water II")
