"""
847. Shortest Path Visiting All Nodes
Difficulty: Hard
Topics: Dynamic Programming, Bit Manipulation, Breadth-First Search, Graph, Bitmask

You have an undirected, connected graph of n nodes labeled from 0 to n - 1.
You are given an array graph where graph[i] is a list of all the nodes
connected with node i by an edge.
Return the length of the shortest path that visits every node. You may start
and stop at any node, you may revisit nodes multiple times, and you may reuse
edges.

Example 1:
    Input: graph = [[1,2,3],[0],[0],[0]]   Output: 4
    Explanation: One possible path is [1,0,2,0,3]
Example 2:
    Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]   Output: 4
    Explanation: One possible path is [0,1,4,2,3]

Constraints:
    n == graph.length
    1 <= n <= 12
    0 <= graph[i].length < n
    graph[i] does not contain i.
    If graph[a] contains b, then graph[b] contains a.
    The input graph is always connected.

Approach (multi-source BFS over (node, visited-mask) states):
    A state is (node, mask) where mask records the visited nodes. Start from
    every (i, 1<<i) at distance 0 simultaneously. BFS moves along edges,
    OR-ing in the neighbour's bit. The first time any state has mask == full,
    the BFS distance is the answer, since all edges cost 1.

Complexity:
    Time:  O(n^2 * 2^n)  (n*2^n states, each with up to n edges)
    Space: O(n * 2^n)

Alternative: Floyd-Warshall all-pairs distances + TSP-style bitmask DP
(dp[mask][last]), O(n^2 * 2^n) as well.
"""
from collections import deque
from typing import List


class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        n = len(graph)
        if n == 1:
            return 0
        full = (1 << n) - 1
        q = deque((i, 1 << i, 0) for i in range(n))
        seen = {(i, 1 << i) for i in range(n)}
        while q:
            node, mask, d = q.popleft()
            for nb in graph[node]:
                nm = mask | (1 << nb)
                if nm == full:
                    return d + 1
                if (nb, nm) not in seen:
                    seen.add((nb, nm))
                    q.append((nb, nm, d + 1))
        return -1

    def shortestPathLengthDP(self, graph: List[List[int]]) -> int:
        n = len(graph)
        INF = float("inf")
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
            for j in graph[i]:
                dist[i][j] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        dp = [[INF] * n for _ in range(1 << n)]
        for i in range(n):
            dp[1 << i][i] = 0
        for mask in range(1 << n):
            for last in range(n):
                if dp[mask][last] == INF:
                    continue
                for nxt in range(n):
                    if not mask & (1 << nxt):
                        nm = mask | (1 << nxt)
                        c = dp[mask][last] + dist[last][nxt]
                        if c < dp[nm][nxt]:
                            dp[nm][nxt] = c
        return min(dp[(1 << n) - 1])


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([[1, 2, 3], [0], [0], [0]], 4),
        ([[1], [0, 2, 4], [1, 3, 4], [2], [1, 2]], 4),
        ([[]], 0),
        ([[1], [0]], 1),
        ([[1], [0, 2], [1]], 2),
        ([[1, 2], [0, 2], [0, 1]], 2),
    ]
    for g, exp in cases:
        assert sol.shortestPathLength(g) == exp, (g, exp)
        assert sol.shortestPathLengthDP(g) == exp, (g, exp)
    print("All tests passed.")
