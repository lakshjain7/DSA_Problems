"""
1129. Shortest Path with Alternating Colors
Difficulty: Medium
Topics: Breadth-First Search, Graph

Problem:
You are given an integer n, the number of nodes in a directed graph labeled 0..n-1.
Each edge is red or blue. The graph may contain self-edges and parallel edges.
You are given two arrays redEdges and blueEdges where redEdges[i] = [a, b] is a red
directed edge a -> b, and blueEdges[j] = [u, v] is a blue directed edge u -> v.

Return an array answer of length n, where answer[x] is the length of the shortest path
from node 0 to node x such that the edge colors alternate along the path, or -1 if no
such path exists.

Example 1:
    Input: n = 3, redEdges = [[0,1],[1,2]], blueEdges = []
    Output: [0,1,-1]
Example 2:
    Input: n = 3, redEdges = [[0,1]], blueEdges = [[2,1]]
    Output: [0,1,-1]

Constraints:
    1 <= n <= 100
    0 <= redEdges.length, blueEdges.length <= 400
    0 <= a, b, u, v < n

Approach:
BFS over states (node, colour of the last edge used). From (u, c) we may only take an
edge of the opposite colour. Start with (0, red) and (0, blue) both at distance 0 (the
first edge may be either colour). BFS explores states in non-decreasing distance, so the
first time any state (x, c) is reached is its shortest alternating distance. The answer
for x is the minimum over both colours.

Complexity:
    Time:  O(n + E)  (2n states, each edge used from one state)
    Space: O(n + E)
"""
from collections import deque
from typing import List


def shortestAlternatingPaths(n: int, redEdges: List[List[int]], blueEdges: List[List[int]]) -> List[int]:
    adj = [[[] for _ in range(n)] for _ in range(2)]  # 0 = red, 1 = blue
    for a, b in redEdges:
        adj[0][a].append(b)
    for a, b in blueEdges:
        adj[1][a].append(b)

    INF = float("inf")
    dist = [[INF, INF] for _ in range(n)]
    dist[0][0] = dist[0][1] = 0
    q = deque([(0, 0), (0, 1)])
    while q:
        u, c = q.popleft()
        nc = 1 - c
        for v in adj[nc][u]:
            if dist[v][nc] == INF:
                dist[v][nc] = dist[u][c] + 1
                q.append((v, nc))
    return [-1 if min(d) == INF else min(d) for d in dist]


# Alternative: BFS with a visited set and level-by-level processing.
def shortestAlternatingPaths_levels(n: int, redEdges: List[List[int]], blueEdges: List[List[int]]) -> List[int]:
    adj = {0: {}, 1: {}}
    for a, b in redEdges:
        adj[0].setdefault(a, []).append(b)
    for a, b in blueEdges:
        adj[1].setdefault(a, []).append(b)
    ans = [-1] * n
    seen = {(0, 0), (0, 1)}
    level = [(0, 0), (0, 1)]
    d = 0
    while level:
        nxt = []
        for u, c in level:
            if ans[u] == -1:
                ans[u] = d
            for v in adj[1 - c].get(u, []):
                if (v, 1 - c) not in seen:
                    seen.add((v, 1 - c))
                    nxt.append((v, 1 - c))
        level = nxt
        d += 1
    return ans


if __name__ == "__main__":
    for f in (shortestAlternatingPaths, shortestAlternatingPaths_levels):
        assert f(3, [[0, 1], [1, 2]], []) == [0, 1, -1]
        assert f(3, [[0, 1]], [[2, 1]]) == [0, 1, -1]
        assert f(1, [], []) == [0]
        assert f(3, [[0, 1], [0, 2]], [[1, 0]]) == [0, 1, 1]
        assert f(5, [[0, 1], [1, 2], [2, 3], [3, 4]], [[1, 2], [2, 3], [3, 1]]) == [0, 1, 2, 3, 7]
        assert f(2, [[0, 0]], []) == [0, -1]
        assert f(3, [[0, 1]], [[1, 2]]) == [0, 1, 2]
    print("All tests passed")
