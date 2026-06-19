import heapq
from typing import List


class Solution:
    """
    Compute the minimum total cost to connect all given 2D points with edges whose weights
    are the Manhattan (L1) distances between points.
    This method implements Prim's algorithm using an explicit adjacency list of all pairwise
    Manhattan distances and a min-heap (priority queue) to incrementally grow a minimum
    spanning tree (MST). It returns the sum of edge costs in the MST, which is the minimum
    cost to connect all points.
    Parameters
    ----------
    points : List[List[int]]
        A list of 2-element lists or tuples representing integer 2D coordinates [x, y]
        for each point.
    Returns
    -------
    int
        The minimum total cost (sum of Manhattan distances) required to connect all points.
    Notes
    -----
    - The Manhattan distance between two points (x1, y1) and (x2, y2) is
      |x1 - x2| + |y1 - y2|.
    - The implementation first builds a full undirected weighted graph (adjacency list)
      containing all pairwise distances, then runs Prim's algorithm using a min-heap.
    - Time complexity: O(N^2 log N) in the worst case, since there are O(N^2) edges and
      heap operations cost O(log N).
    - Space complexity: O(N^2) due to storing all pairwise distances in the adjacency list.
    Example
    -------
    Given points = [[0,0], [2,2], [3,10], [5,2], [7,0]], the function returns 20,
    the minimum total Manhattan distance to connect all points.
    """
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        adj = {i: [] for i in range(N)}
        for i in range(N):
            x1, y1 = points[i]
            for j in range(i + 1, N):
                x2, y2 = points[j]
                dist = abs(x1 - x2) + abs(y1 - y2)
                adj[i].append([dist, j])
                adj[j].append([dist, i])

        res = 0
        visit = set()
        minH = [[0, 0]]
        while len(visit) < N:
            cost, i = heapq.heappop(minH)
            if i in visit:
                continue
            res += cost
            visit.add(i)
            for neiCost, nei in adj[i]:
                if nei not in visit:
                    heapq.heappush(minH, [neiCost, nei])
        return res