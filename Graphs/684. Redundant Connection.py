"""
684. Redundant Connection
Difficulty: Medium
Topics: Union-Find (Disjoint Set Union), Graph, DFS/BFS

Problem
-------
In this problem, a tree is an undirected graph that is connected and has no
cycles.

You are given a graph that started as a tree with `n` nodes labeled from 1 to n,
with one additional edge added. The added edge has two different vertices chosen
from 1 to n, and was not an edge that already existed. The graph is represented
as an array `edges` of length n where edges[i] = [a_i, b_i] indicates that there
is an edge between nodes a_i and b_i in the graph.

Return an edge that can be removed so that the resulting graph is a tree of n
nodes. If there are multiple answers, return the answer that occurs last in the
input.

Examples
--------
Example 1:
    Input:  edges = [[1, 2], [1, 3], [2, 3]]
    Output: [2, 3]

Example 2:
    Input:  edges = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    Output: [1, 4]

Constraints
-----------
    n == edges.length
    3 <= n <= 1000
    edges[i].length == 2
    1 <= a_i < b_i <= edges.length
    a_i != b_i
    There are no repeated edges.
    The given graph is connected.

Approach 1 — Union-Find (recommended)
-------------------------------------
The graph is a tree plus exactly one extra edge, so it contains exactly one
cycle. Process edges in the given order and maintain a disjoint-set structure.
For each edge (u, v):
    - If u and v are already in the same component, adding this edge would close
      a cycle -> this is the redundant edge. Because we scan left-to-right, the
      first such edge we hit is the last one (in input order) that completes the
      cycle, which is exactly what the problem asks for.
    - Otherwise union the two components.

We use union by rank/size and path compression for near-constant amortized
operations (inverse-Ackermann).

Why "first cycle-closing edge in scan order" == "last valid answer":
Since there is exactly one extra edge, there is exactly one cycle. Every edge on
that cycle is a valid removable edge. Union-Find only reports the single edge
whose two endpoints were connected before it was added — that is the last edge
of the cycle encountered while scanning, i.e. the answer occurring last in the
input among the cycle edges.

Complexity
----------
    Time:  O(n * alpha(n))  ~ O(n)   (alpha = inverse Ackermann)
    Space: O(n)             parent and rank arrays

Approach 2 — DFS cycle check per edge
-------------------------------------
Build the graph incrementally. Before adding edge (u, v), run DFS/BFS to test
whether v is already reachable from u using existing edges. If it is, (u, v) is
redundant. This is O(n^2) in the worst case but requires no DSU bookkeeping.
"""

from typing import List


class _DSU:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Return True if merged, False if a and b were already connected."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """Return the last input edge that closes a cycle (Union-Find)."""
    n = len(edges)
    dsu = _DSU(n + 1)  # nodes are 1-indexed
    for u, v in edges:
        if not dsu.union(u, v):
            return [u, v]
    return []  # problem guarantees an answer exists


def find_redundant_connection_dfs(edges: List[List[int]]) -> List[int]:
    """Alternative: incremental build with a DFS reachability check per edge."""
    graph = {i: [] for i in range(1, len(edges) + 1)}

    def connected(src: int, dst: int) -> bool:
        seen = set()
        stack = [src]
        while stack:
            node = stack.pop()
            if node == dst:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(graph[node])
        return False

    for u, v in edges:
        if connected(u, v):  # already reachable -> this edge is redundant
            return [u, v]
        graph[u].append(v)
        graph[v].append(u)
    return []


if __name__ == "__main__":
    # Example 1
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection_dfs([[1, 2], [1, 3], [2, 3]]) == [2, 3]

    # Example 2
    assert find_redundant_connection(
        [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    ) == [1, 4]
    assert find_redundant_connection_dfs(
        [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
    ) == [1, 4]

    # Self-contained triangle appended to a path; last cycle edge is the answer
    assert find_redundant_connection([[1, 2], [2, 3], [1, 3]]) == [1, 3]

    # Redundant edge is the very last edge
    assert find_redundant_connection(
        [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]
    ) == [1, 5]

    # Larger star-with-extra example
    assert find_redundant_connection(
        [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]
    ) == [1, 3]
    assert find_redundant_connection_dfs(
        [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]
    ) == [1, 3]

    print("All tests passed for 684. Redundant Connection")
