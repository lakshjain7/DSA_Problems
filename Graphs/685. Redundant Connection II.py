"""
685. Redundant Connection II
Difficulty: Hard
Topics: Depth-First Search, Breadth-First Search, Union Find, Graph

Problem:
In this problem, a rooted tree is a directed graph such that there is exactly
one node (the root) for which all other nodes are descendants of this node,
plus every node has exactly one parent, except for the root node which has no
parents. The given input is a directed graph that started as a rooted tree
with n nodes (with distinct values from 1 to n), with one additional directed
edge added. The added edge has two different vertices chosen from 1 to n, and
was not an edge that already existed. The graph is given as a 2D array edges
where edges[i] = [ui, vi] represents a directed edge from ui to vi (ui is a
parent of child vi). Return an edge that can be removed so that the resulting
graph is a rooted tree of n nodes. If there are multiple answers, return the
answer that occurs last in the given 2D-array.

Example 1:
    Input: edges = [[1,2],[1,3],[2,3]]
    Output: [2,3]
Example 2:
    Input: edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
    Output: [4,1]

Constraints:
    n == edges.length
    3 <= n <= 1000
    edges[i].length == 2
    1 <= ui, vi <= n
    ui != vi

Approach:
The extra edge causes one of three situations:
  A) A node has two parents (no cycle needed to be considered yet).
  B) A cycle exists, with every node having <= 1 parent.
  C) Both: a node with two parents AND a cycle.
Step 1: find a node with two parents; record the two candidate edges
        cand1 (earlier) and cand2 (later).
Step 2: run union-find over all edges, skipping cand2 (if exists).
  - If no node has two parents: the first edge closing a cycle is the answer.
  - If a node has two parents and skipping cand2 still yields a cycle, then
    cand1 is the culprit (it lies on the cycle).
  - If skipping cand2 yields no cycle, cand2 is the answer.

Complexity:
    Time:  O(n * alpha(n))
    Space: O(n)
"""
from typing import List


class Solution:
    def findRedundantDirectedConnection(self, edges: List[List[int]]) -> List[int]:
        n = len(edges)
        parent_of = [0] * (n + 1)
        cand1 = cand2 = None
        for u, v in edges:
            if parent_of[v]:
                cand1 = [parent_of[v], v]
                cand2 = [u, v]
            else:
                parent_of[v] = u

        uf = list(range(n + 1))

        def find(x: int) -> int:
            while uf[x] != x:
                uf[x] = uf[uf[x]]
                x = uf[x]
            return x

        for u, v in edges:
            if cand2 and [u, v] == cand2:
                continue
            ru, rv = find(u), find(v)
            if ru == rv:
                # cycle found
                return cand1 if cand1 else [u, v]
            uf[rv] = ru  # u is parent, so v's root hangs under u's root
        return cand2


if __name__ == "__main__":
    s = Solution()
    f = s.findRedundantDirectedConnection
    assert f([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert f([[1, 2], [2, 3], [3, 4], [4, 1], [1, 5]]) == [4, 1]
    # two parents, no cycle: remove the later one
    assert f([[2, 1], [3, 1], [4, 2], [1, 4]]) == [2, 1]
    # pure cycle, all nodes one parent
    assert f([[1, 2], [2, 3], [3, 1]]) == [3, 1]
    # two parents where the cycle is created by earlier edge
    assert f([[1, 2], [2, 3], [3, 1], [4, 1]]) == [3, 1]
    assert f([[4, 2], [1, 5], [5, 2], [5, 3], [2, 4]]) == [4, 2]
    assert f([[2, 1], [3, 1], [4, 2], [1, 4]]) == [2, 1]
    print("All tests passed.")
