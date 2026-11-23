"""
261. Graph Valid Tree
Difficulty: Medium
Topics: Graph, Union-Find, Depth-First Search, Breadth-First Search

Problem:
You have a graph of n nodes labeled from 0 to n - 1. You are given an integer n
and a list of edges where edges[i] = [a_i, b_i] indicates that there is an
undirected edge between nodes a_i and b_i in the graph.

Return true if the edges of the given graph make up a valid tree, and false
otherwise.

Example 1:
    Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
    Output: true

Example 2:
    Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
    Output: false   (cycle 1-2-3-1)

Constraints:
    1 <= n <= 2000
    0 <= edges.length <= 5000
    edges[i].length == 2
    0 <= a_i, b_i < n
    a_i != b_i
    There are no self-loops or repeated edges.

Approach (Union-Find):
A graph on n nodes is a tree iff it is connected AND acyclic. Equivalently,
it has exactly n - 1 edges AND contains no cycle (n - 1 acyclic edges on n
nodes necessarily connect everything).
  1. If len(edges) != n - 1, it cannot be a tree -> False.
  2. Union the endpoints of every edge. If an edge joins two nodes that are
     already in the same component, it closes a cycle -> False.
  3. Otherwise every edge merged two components; n - 1 merges of n singletons
     leaves exactly one component -> True.
Path compression + union by size keep each operation near O(1).

Complexity:
    Time:  O(n + E * α(n)) ≈ O(n + E)
    Space: O(n) for parent/size arrays

Alternative (DFS/BFS):
Check the edge count, build an adjacency list, traverse from node 0, and verify
every node was reached. Same O(n + E) time, O(n + E) space.
"""
from collections import deque
from typing import List


def valid_tree(n: int, edges: List[List[int]]) -> bool:
    if len(edges) != n - 1:
        return False

    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False  # cycle
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
    return True


def valid_tree_bfs(n: int, edges: List[List[int]]) -> bool:
    if len(edges) != n - 1:
        return False
    adj: List[List[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen) == n


if __name__ == "__main__":
    cases = [
        (5, [[0, 1], [0, 2], [0, 3], [1, 4]], True),
        (5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], False),
        (1, [], True),                       # single node
        (2, [], False),                      # disconnected, too few edges
        (4, [[0, 1], [2, 3], [0, 2]], True),
        (4, [[0, 1], [1, 2], [2, 0]], False),  # n-1 edges but cycle + isolated node
        (3, [[0, 1], [1, 2]], True),         # path
        (6, [[0, 1], [0, 2], [0, 3], [0, 4], [0, 5]], True),  # star
    ]
    for n, edges, expected in cases:
        assert valid_tree(n, edges) == expected, (n, edges)
        assert valid_tree_bfs(n, edges) == expected, (n, edges)
    print("All tests passed for 261. Graph Valid Tree")
