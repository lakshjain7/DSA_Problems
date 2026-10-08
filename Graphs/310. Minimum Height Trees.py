"""
Problem: 310. Minimum Height Trees
Difficulty: Medium
Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort

A tree is an undirected graph in which any two vertices are connected by
exactly one path. Given a tree of n nodes labelled from 0 to n - 1, and an
array of n - 1 edges where edges[i] = [ai, bi] is an undirected edge, you can
choose any node as the root. The height of a rooted tree is the number of
edges on the longest downward path between the root and a leaf. Among all
possible rooted trees, those with minimum height are called minimum height
trees (MHTs). Return a list of all MHTs' root labels in any order.

Example 1:
    Input: n = 4, edges = [[1,0],[1,2],[1,3]]
    Output: [1]

Example 2:
    Input: n = 6, edges = [[3,0],[3,1],[3,2],[3,4],[5,4]]
    Output: [3,4]

Constraints:
    1 <= n <= 2 * 10^4
    edges.length == n - 1
    0 <= ai, bi < n, ai != bi, all pairs distinct, input is a tree.
"""
from collections import deque
from typing import List

# Approach (peel leaves, topological-sort style):
#   The MHT roots are the centre(s) of the tree - at most two nodes. Repeatedly
#   remove all current leaves (degree 1) layer by layer; when 2 or fewer nodes
#   remain, they are the centres. Removing leaves never changes the centre.
#
# Complexity: Time O(n), Space O(n).


class Solution:
    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))
        adj = [set() for _ in range(n)]
        for a, b in edges:
            adj[a].add(b)
            adj[b].add(a)
        leaves = deque(i for i in range(n) if len(adj[i]) == 1)
        remaining = n
        while remaining > 2:
            for _ in range(len(leaves)):
                leaf = leaves.popleft()
                remaining -= 1
                nb = adj[leaf].pop()
                adj[nb].discard(leaf)
                if len(adj[nb]) == 1:
                    leaves.append(nb)
        return list(leaves)

    # Alternative: find the diameter path with two BFS runs; the middle
    # node(s) of that path are the answer. O(n) time and space.
    def findMinHeightTreesDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))
        adj = [[] for _ in range(n)]
        for a, b in edges:
            adj[a].append(b)
            adj[b].append(a)

        def bfs(src):
            par = [-1] * n
            dist = [-1] * n
            dist[src] = 0
            q = deque([src])
            last = src
            while q:
                u = q.popleft()
                last = u
                for v in adj[u]:
                    if dist[v] < 0:
                        dist[v] = dist[u] + 1
                        par[v] = u
                        q.append(v)
            return last, par

        a, _ = bfs(0)
        b, par = bfs(a)
        path = []
        while b != -1:
            path.append(b)
            b = par[b]
        m = len(path)
        return [path[m // 2]] if m % 2 else [path[m // 2 - 1], path[m // 2]]


if __name__ == "__main__":
    s = Solution()
    for f in (s.findMinHeightTrees, s.findMinHeightTreesDiameter):
        assert sorted(f(4, [[1, 0], [1, 2], [1, 3]])) == [1]
        assert sorted(f(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])) == [3, 4]
        assert sorted(f(1, [])) == [0]
        assert sorted(f(2, [[0, 1]])) == [0, 1]
        assert sorted(f(3, [[0, 1], [1, 2]])) == [1]
        assert sorted(f(5, [[0, 1], [1, 2], [2, 3], [3, 4]])) == [2]
        assert sorted(f(4, [[0, 1], [1, 2], [2, 3]])) == [1, 2]
    print("All tests passed.")
