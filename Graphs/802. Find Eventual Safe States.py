"""
802. Find Eventual Safe States
Difficulty: Medium
Topics: Graph, Depth-First Search, Breadth-First Search, Topological Sort

Problem
-------
There is a directed graph of `n` nodes with each node labeled from 0 to n - 1.
The graph is represented by a 0-indexed 2D integer array `graph` where
`graph[i]` is an integer array of nodes adjacent to node i, meaning there is
an edge from node i to each node in `graph[i]`.

A node is a terminal node if there are no outgoing edges. A node is a safe node
if every possible path starting from that node leads to a terminal node (or
another safe node).

Return an array containing all the safe nodes of the graph. The answer should
be sorted in ascending order.

Example 1:
    Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
    Output: [2,4,5,6]
    Explanation: Nodes 5 and 6 are terminal nodes as there are no outgoing
    edges from either of them. Every path starting at nodes 2, 4, 5, and 6
    all lead to either node 5 or 6.

Example 2:
    Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
    Output: [4]
    Explanation: Only node 4 is a terminal node, and every path starting at
    node 4 leads to node 4.

Constraints:
    n == graph.length
    1 <= n <= 10^4
    0 <= graph[i].length <= n
    0 <= graph[i][j] <= n - 1
    graph[i] is sorted in a strictly increasing order.
    The graph may contain self-loops.
    The number of edges in the graph will be in the range [1, 4 * 10^4].

Approach (Kahn's topological sort on the reversed graph)
--------------------------------------------------------
A node is unsafe exactly when some path from it reaches a cycle. Terminal nodes
(out-degree 0) are safe. A node becomes safe once *all* of its outgoing
neighbours are known to be safe.

So reverse every edge and track each node's original out-degree. Start a queue
with all terminal nodes. Pop a safe node v; for every predecessor u (an edge
u -> v in the original graph), decrement outdeg[u]. When outdeg[u] hits 0, all
of u's successors are safe, so u is safe too -- push it.

Nodes on or leading into a cycle never get their out-degree to 0 (the cycle
edges are never "removed"), so exactly the safe nodes are discovered.

Complexity
----------
Time:  O(V + E) -- each node and edge is processed once.
Space: O(V + E) for the reversed adjacency list.

Alternative (DFS three-colour cycle detection)
----------------------------------------------
colour 0 = unvisited, 1 = on current DFS stack (visiting), 2 = safe.
DFS from each node; if we reach a node coloured 1 we've found a cycle, so the
whole current path is unsafe (we leave it coloured 1 permanently). If all
children return safe, colour the node 2. Also O(V + E). Implemented
iteratively below to avoid Python recursion limits on n = 10^4.
"""

from collections import deque
from typing import List


class Solution:
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        reverse: List[List[int]] = [[] for _ in range(n)]
        outdeg = [0] * n
        for u, nbrs in enumerate(graph):
            outdeg[u] = len(nbrs)
            for v in nbrs:
                reverse[v].append(u)

        queue = deque(i for i in range(n) if outdeg[i] == 0)
        safe = [False] * n
        while queue:
            v = queue.popleft()
            safe[v] = True
            for u in reverse[v]:
                outdeg[u] -= 1
                if outdeg[u] == 0:
                    queue.append(u)
        return [i for i in range(n) if safe[i]]

    def eventualSafeNodesDFS(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        color = [0] * n  # 0 unvisited, 1 visiting/unsafe, 2 safe
        for start in range(n):
            if color[start]:
                continue
            color[start] = 1
            stack = [(start, 0)]
            while stack:
                node, idx = stack[-1]
                nbrs = graph[node]
                if idx < len(nbrs):
                    stack[-1] = (node, idx + 1)
                    nxt = nbrs[idx]
                    if color[nxt] == 0:
                        color[nxt] = 1
                        stack.append((nxt, 0))
                    elif color[nxt] == 1:
                        # cycle (or reaches unsafe node): abort; path stays colour 1
                        stack.clear()
                else:
                    color[node] = 2
                    stack.pop()
        return [i for i in range(n) if color[i] == 2]


if __name__ == "__main__":
    sol = Solution()
    cases = [
        ([[1, 2], [2, 3], [5], [0], [5], [], []], [2, 4, 5, 6]),
        ([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []], [4]),
        ([[]], [0]),                       # single terminal node
        ([[0]], []),                       # single self-loop
        ([[1], [2], [0]], []),             # pure cycle
        ([[1], [2], []], [0, 1, 2]),       # simple chain
        ([[1, 2], [], [2]], [1]),          # node 0 reaches self-loop at 2
        ([[], [0, 2], [3], [2]], [0]),
    ]
    for g, exp in cases:
        assert sol.eventualSafeNodes(g) == exp, g
        assert sol.eventualSafeNodesDFS(g) == exp, g

    # randomised cross-check of both approaches
    import random

    random.seed(802)
    for _ in range(300):
        n = random.randint(1, 9)
        g = [sorted(random.sample(range(n), random.randint(0, min(3, n)))) for _ in range(n)]
        assert sol.eventualSafeNodes(g) == sol.eventualSafeNodesDFS(g), g

    # large chain: no recursion issues
    big = [[i + 1] for i in range(9999)] + [[]]
    assert sol.eventualSafeNodesDFS(big) == list(range(10000))
    print("All tests passed for 802. Find Eventual Safe States")
