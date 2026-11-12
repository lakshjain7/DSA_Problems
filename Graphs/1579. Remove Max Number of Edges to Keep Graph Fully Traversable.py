"""
1579. Remove Max Number of Edges to Keep Graph Fully Traversable
Difficulty: Hard
Topics: Union Find, Graph

Problem:
Alice and Bob have an undirected graph of n nodes and three types of edges:
  - Type 1: Can be traversed by Alice only.
  - Type 2: Can be traversed by Bob only.
  - Type 3: Can be traversed by both Alice and Bob.

Given an array `edges` where edges[i] = [type_i, u_i, v_i] represents a
bidirectional edge of type type_i between nodes u_i and v_i, find the maximum
number of edges you can remove so that after removing the edges, the graph can
still be fully traversed by both Alice and Bob. The graph is fully traversed by
Alice and Bob if starting from any node, they can reach all other nodes.

Return the maximum number of edges you can remove, or return -1 if Alice and
Bob cannot fully traverse the graph.

Example 1:
    Input: n = 4, edges = [[3,1,2],[3,2,3],[1,2,4],[1,1,3],[2,3,4],[2,1,2]]
    Output: 2
    Explanation: Removing [1,1,3] and [2,1,2] keeps the graph fully
    traversable for both. Removing any more breaks it.

Example 2:
    Input: n = 4, edges = [[3,1,2],[3,2,3],[1,1,4],[2,1,4]]
    Output: 0
    Explanation: Every edge is needed.

Example 3:
    Input: n = 4, edges = [[3,2,3],[1,1,2],[2,3,4]]
    Output: -1
    Explanation: Alice can't reach node 4 and Bob can't reach node 1.

Constraints:
    1 <= n <= 10^5
    1 <= edges.length <= min(10^5, 3 * n * (n - 1) / 2)
    edges[i].length == 3
    1 <= type_i <= 3
    1 <= u_i < v_i <= n
    All tuples (type_i, u_i, v_i) are distinct.

Approach (Greedy Kruskal-style with two Union-Find structures):
    We want to KEEP as few edges as possible such that both Alice's graph
    (types 1+3) and Bob's graph (types 2+3) are spanning-connected.
    A type-3 edge serves both people at once, so it is always at least as
    useful as a type-1 or type-2 edge. Therefore:
      1. Process all type-3 edges first, unioning in BOTH DSUs. Keep the edge
         if it merges components (it merges in both or neither, since both
         DSUs are identical at this stage).
      2. Process type-1 edges in Alice's DSU, type-2 edges in Bob's DSU,
         keeping each only if it merges two components.
      3. If either DSU has more than one component, return -1.
      4. Answer = total edges - kept edges.

    Why it works: by a matroid/exchange argument (same as Kruskal's MST with
    weights: type-3 cheaper than single-use edges), using a shared edge
    whenever it connects new components never increases the number of edges
    needed. Each DSU ends as a spanning forest with exactly n-1 edges, and
    the shared edges are counted once — the maximal possible sharing.

Complexity:
    Time:  O((n + E) * α(n)) with path compression + union by size.
    Space: O(n) for the two DSUs.

Alternative (Brute force, for validation only):
    A naive approach tries removing each edge and re-checks connectivity
    with BFS — O(E * (n + E)), far too slow, but useful to validate the greedy
    on small inputs (used as a brute-force oracle in the tests below via
    exhaustive subset search on tiny graphs).
"""
from itertools import combinations
from typing import List


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.components = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True


class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        alice, bob = DSU(n), DSU(n)
        kept = 0

        for t, u, v in edges:
            if t == 3:
                merged_a = alice.union(u, v)
                merged_b = bob.union(u, v)
                if merged_a or merged_b:
                    kept += 1

        for t, u, v in edges:
            if t == 1 and alice.union(u, v):
                kept += 1
            elif t == 2 and bob.union(u, v):
                kept += 1

        if alice.components != 1 or bob.components != 1:
            return -1
        return len(edges) - kept


def _brute_force(n: int, edges: List[List[int]]) -> int:
    """Try keeping subsets in increasing size; return max removable or -1."""
    def connected(subset, allowed) -> bool:
        d = DSU(n)
        for t, u, v in subset:
            if t in allowed:
                d.union(u, v)
        return d.components == 1

    m = len(edges)
    for keep in range(0, m + 1):
        for subset in combinations(edges, keep):
            if connected(subset, (1, 3)) and connected(subset, (2, 3)):
                return m - keep
    return -1


if __name__ == "__main__":
    import random

    s = Solution()
    cases = [
        (4, [[3, 1, 2], [3, 2, 3], [1, 2, 4], [1, 1, 3], [2, 3, 4], [2, 1, 2]], 2),
        (4, [[3, 1, 2], [3, 2, 3], [1, 1, 4], [2, 1, 4]], 0),
        (4, [[3, 2, 3], [1, 1, 2], [2, 3, 4]], -1),
        (2, [[1, 1, 2], [2, 1, 2], [3, 1, 2]], 2),      # one shared edge suffices
        (2, [[1, 1, 2]], -1),                           # Bob can't traverse
        (3, [[1, 1, 2], [2, 1, 2], [1, 2, 3], [2, 2, 3]], 0),
    ]
    for n, edges, expected in cases:
        assert s.maxNumEdgesToRemove(n, edges) == expected, (n, edges)

    rng = random.Random(1579)
    for _ in range(200):
        n = rng.randint(1, 4)
        all_edges = [[t, u, v] for t in (1, 2, 3)
                     for u in range(1, n + 1) for v in range(u + 1, n + 1)]
        if not all_edges:
            continue
        k = rng.randint(1, min(7, len(all_edges)))
        edges = rng.sample(all_edges, k)
        assert s.maxNumEdgesToRemove(n, edges) == _brute_force(n, edges), (n, edges)

    print("All tests passed for 1579. Remove Max Number of Edges to Keep Graph Fully Traversable")
