"""
2392. Build a Matrix With Conditions
Difficulty: Hard
Topics: Array, Graph, Topological Sort, Matrix

Problem:
You are given a positive integer k. You are also given:
  - a 2D integer array rowConditions of size n where rowConditions[i] = [above_i, below_i], and
  - a 2D integer array colConditions of size m where colConditions[i] = [left_i, right_i].
The two arrays contain integers from 1 to k.

You have to build a k x k matrix that contains each of the numbers from 1 to k
exactly once. The remaining cells should have the value 0.

The matrix should also satisfy the following conditions:
  - The number above_i should appear in a row that is strictly above the row at
    which the number below_i appears for all i from 0 to n - 1.
  - The number left_i should appear in a column that is strictly left of the column
    at which the number right_i appears for all i from 0 to m - 1.

Return any matrix that satisfies the conditions. If no answer exists, return an
empty matrix.

Example 1:
    Input: k = 3, rowConditions = [[1,2],[3,2]], colConditions = [[2,1],[3,2]]
    Output: [[3,0,0],[0,0,1],[0,2,0]]

Example 2:
    Input: k = 3, rowConditions = [[1,2],[2,3],[3,1],[2,3]], colConditions = [[2,1]]
    Output: []
    Explanation: rows require 1 < 2 < 3 < 1 — a cycle, so no answer.

Constraints:
    2 <= k <= 400
    1 <= rowConditions.length, colConditions.length <= 10^4
    rowConditions[i].length == colConditions[i].length == 2
    1 <= above_i, below_i, left_i, right_i <= k
    above_i != below_i
    left_i != right_i

Approach (Two independent topological sorts):
    Row placement and column placement are independent constraints. Each set of
    conditions is a directed graph on nodes 1..k (edge a -> b means a must come
    before b). A valid ordering exists iff the graph is a DAG; Kahn's algorithm
    (BFS on in-degree 0 nodes) gives an ordering or detects a cycle (fewer than k
    nodes emitted). Take row_order and col_order, then place number x at
    (row_pos[x], col_pos[x]). Every number gets a unique row and unique column, so
    each number appears exactly once and all conditions hold.

Complexity:
    Time:  O(k^2 + n + m)  (k^2 to build the output matrix)
    Space: O(k^2 + n + m)

Alternative (DFS topological sort with 3-color cycle detection):
    Run DFS post-order on each graph, marking nodes white/gray/black; a gray
    neighbor means a back edge (cycle). Reverse post-order is the topological order.
"""

from collections import deque
from typing import List, Optional


class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def kahn(edges: List[List[int]]) -> List[int]:
            adj = [[] for _ in range(k + 1)]
            indeg = [0] * (k + 1)
            for a, b in edges:
                adj[a].append(b)
                indeg[b] += 1
            q = deque(i for i in range(1, k + 1) if indeg[i] == 0)
            order = []
            while q:
                u = q.popleft()
                order.append(u)
                for v in adj[u]:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        q.append(v)
            return order if len(order) == k else []

        rows, cols = kahn(rowConditions), kahn(colConditions)
        if not rows or not cols:
            return []
        col_pos = {x: i for i, x in enumerate(cols)}
        mat = [[0] * k for _ in range(k)]
        for r, x in enumerate(rows):
            mat[r][col_pos[x]] = x
        return mat

    def buildMatrixDFS(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topo(edges: List[List[int]]) -> Optional[List[int]]:
            adj = [[] for _ in range(k + 1)]
            for a, b in edges:
                adj[a].append(b)
            color = [0] * (k + 1)  # 0 white, 1 gray, 2 black
            post: List[int] = []
            for start in range(1, k + 1):
                if color[start]:
                    continue
                stack = [(start, 0)]
                color[start] = 1
                while stack:
                    u, idx = stack[-1]
                    if idx < len(adj[u]):
                        stack[-1] = (u, idx + 1)
                        v = adj[u][idx]
                        if color[v] == 1:
                            return None
                        if color[v] == 0:
                            color[v] = 1
                            stack.append((v, 0))
                    else:
                        color[u] = 2
                        post.append(u)
                        stack.pop()
            return post[::-1]

        rows, cols = topo(rowConditions), topo(colConditions)
        if rows is None or cols is None:
            return []
        col_pos = {x: i for i, x in enumerate(cols)}
        mat = [[0] * k for _ in range(k)]
        for r, x in enumerate(rows):
            mat[r][col_pos[x]] = x
        return mat


def is_valid(mat: List[List[int]], k: int, rc: List[List[int]], cc: List[List[int]]) -> bool:
    if len(mat) != k or any(len(r) != k for r in mat):
        return False
    pos = {}
    for i in range(k):
        for j in range(k):
            if mat[i][j]:
                if mat[i][j] in pos:
                    return False
                pos[mat[i][j]] = (i, j)
    if set(pos) != set(range(1, k + 1)):
        return False
    return all(pos[a][0] < pos[b][0] for a, b in rc) and all(pos[a][1] < pos[b][1] for a, b in cc)


if __name__ == "__main__":
    sol = Solution()
    for fn in (sol.buildMatrix, sol.buildMatrixDFS):
        rc, cc = [[1, 2], [3, 2]], [[2, 1], [3, 2]]
        assert is_valid(fn(3, rc, cc), 3, rc, cc)
        assert fn(3, [[1, 2], [2, 3], [3, 1], [2, 3]], [[2, 1]]) == []
        # cycle only in columns
        assert fn(2, [[1, 2]], [[1, 2], [2, 1]]) == []
        # duplicate edges, chain
        rc, cc = [[1, 2], [1, 2], [2, 3], [3, 4]], [[4, 3], [3, 2], [2, 1]]
        m = fn(4, rc, cc)
        assert is_valid(m, 4, rc, cc)
        assert m == [[0, 0, 0, 1], [0, 0, 2, 0], [0, 3, 0, 0], [4, 0, 0, 0]]
        # nodes with no constraints still placed
        rc, cc = [[5, 1]], [[2, 3]]
        assert is_valid(fn(5, rc, cc), 5, rc, cc)

    import random
    for _ in range(300):
        k = random.randint(2, 7)
        def rand_edges():
            return [[a, b] for a, b in (random.sample(range(1, k + 1), 2) for _ in range(random.randint(1, 8)))]
        rc, cc = rand_edges(), rand_edges()
        r1, r2 = sol.buildMatrix(k, rc, cc), sol.buildMatrixDFS(k, rc, cc)
        assert (r1 == []) == (r2 == [])
        if r1:
            assert is_valid(r1, k, rc, cc) and is_valid(r2, k, rc, cc)
    print("All tests passed!")
