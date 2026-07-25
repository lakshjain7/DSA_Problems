"""
785. Is Graph Bipartite?
Difficulty: Medium
Topics: Graph, BFS, DFS, Union Find, Graph Coloring

Problem Statement
-----------------
There is an undirected graph with `n` nodes, where each node is numbered
between 0 and n - 1. You are given a 2D array `graph`, where graph[u] is an
array of nodes that node u is adjacent to. More formally, for each v in
graph[u], there is an undirected edge between node u and node v. The graph has
the following properties:

- There are no self-edges (graph[u] does not contain u).
- There are no parallel edges (graph[u] does not contain duplicate values).
- If v is in graph[u], then u is in graph[v] (the graph is undirected).
- The graph may not be connected, meaning there may be two nodes u and v such
  that there is no path between them.

A graph is bipartite if the nodes can be partitioned into two independent sets
A and B such that every edge in the graph connects a node in set A and a node
in set B.

Return true if and only if it is bipartite.

Examples
--------
Example 1:
    Input:  graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
    Output: false
    Explanation: There is no way to partition the nodes into two independent
    sets such that every edge connects a node in one and a node in the other.

Example 2:
    Input:  graph = [[1,3],[0,2],[1,3],[0,2]]
    Output: true
    Explanation: We can partition the nodes into two sets: {0, 2} and {1, 3}.

Constraints
-----------
- graph.length == n
- 1 <= n <= 100
- 0 <= graph[u].length < n
- 0 <= graph[u][i] <= n - 1
- graph[u] does not contain u.
- All the values of graph[u] are unique.
- If graph[u] contains v, then graph[v] contains u.

Approach (2-Coloring via BFS)
-----------------------------
A graph is bipartite if and only if it contains no odd-length cycle. This is
equivalent to being able to 2-color the graph so that no edge connects two
nodes of the same color.

We keep a `color` array (0 = uncolored, 1 and -1 = the two colors). For every
uncolored node we start a BFS, color it 1, and try to color each neighbor with
the opposite color of the current node. If we ever find a neighbor already
colored with the SAME color as the current node, an odd cycle exists and the
graph is not bipartite.

We iterate over every node as a start point because the graph may be
disconnected.

Why it works
------------
2-coloring succeeds exactly when the graph is bipartite. BFS assigns levels;
in a bipartite graph, adjacent nodes always sit on levels of opposite parity.
A conflict (same color on both ends of an edge) is a direct witness of an
odd cycle, which is impossible in a bipartite graph.

Complexity
----------
Time:  O(V + E) - each node and edge is visited once.
Space: O(V) for the color array and BFS queue.
"""

from collections import deque
from typing import List


def is_bipartite(graph: List[List[int]]) -> bool:
    """Return True if the undirected graph is bipartite (BFS 2-coloring)."""
    n = len(graph)
    color = [0] * n  # 0 = uncolored, 1 / -1 = the two colors

    for start in range(n):
        if color[start] != 0:
            continue
        color[start] = 1
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nei in graph[node]:
                if color[nei] == 0:
                    color[nei] = -color[node]
                    queue.append(nei)
                elif color[nei] == color[node]:
                    return False
    return True


def is_bipartite_dfs(graph: List[List[int]]) -> bool:
    """Alternative recursive DFS 2-coloring. Same O(V + E) complexity."""
    n = len(graph)
    color = [0] * n

    def dfs(node: int, c: int) -> bool:
        color[node] = c
        for nei in graph[node]:
            if color[nei] == c:
                return False
            if color[nei] == 0 and not dfs(nei, -c):
                return False
        return True

    for i in range(n):
        if color[i] == 0 and not dfs(i, 1):
            return False
    return True


if __name__ == "__main__":
    # Example 1 - not bipartite (contains an odd cycle)
    assert is_bipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False
    # Example 2 - bipartite
    assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True

    # Single node, no edges -> trivially bipartite
    assert is_bipartite([[]]) is True
    # Two nodes with one edge -> bipartite
    assert is_bipartite([[1], [0]]) is True

    # Triangle (odd cycle) -> not bipartite
    assert is_bipartite([[1, 2], [0, 2], [0, 1]]) is False
    # Even cycle of length 4 -> bipartite
    assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True

    # Disconnected graph: one bipartite component + isolated node
    assert is_bipartite([[1], [0], []]) is True
    # Disconnected graph where one component has an odd cycle
    assert is_bipartite([[1], [0], [3, 4], [2, 4], [2, 3]]) is False

    # Cross-check both implementations on a batch of cases
    cases = [
        [[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],
        [[1, 3], [0, 2], [1, 3], [0, 2]],
        [[]],
        [[1], [0]],
        [[1, 2], [0, 2], [0, 1]],
        [[1], [0], [3, 4], [2, 4], [2, 3]],
    ]
    for g in cases:
        assert is_bipartite(g) == is_bipartite_dfs(g)

    print("All tests passed for 785. Is Graph Bipartite?")
