"""
547. Number of Provinces
Difficulty: Medium
Topics: Depth-First Search, Breadth-First Search, Union Find, Graph

Problem:
There are n cities. Some are connected directly or indirectly. A province is
a group of directly or indirectly connected cities with no other outside
connections. Given an n x n matrix isConnected where isConnected[i][j] = 1 if
city i and city j are directly connected (else 0), return the number of
provinces.

Examples:
    Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]  Output: 2
    Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]  Output: 3

Constraints:
    1 <= n <= 200
    isConnected[i][i] == 1, isConnected[i][j] == isConnected[j][i]

Approach (Union-Find with path compression + union by size):
    Start with n components. For every pair (i, j) with an edge, union their
    sets; each successful union merges two components, so decrement the
    count. The final count is the number of provinces.

Complexity: Time O(n^2 * alpha(n)), Space O(n).
"""
from typing import List


def findCircleNum(isConnected: List[List[int]]) -> int:
    n = len(isConnected)
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    count = n
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j]:
                a, b = find(i), find(j)
                if a != b:
                    if size[a] < size[b]:
                        a, b = b, a
                    parent[b] = a
                    size[a] += size[b]
                    count -= 1
    return count


# Alternative: iterative DFS over the adjacency matrix. O(n^2) time, O(n) space.
def findCircleNumDFS(isConnected: List[List[int]]) -> int:
    n = len(isConnected)
    seen = [False] * n
    provinces = 0
    for s in range(n):
        if seen[s]:
            continue
        provinces += 1
        stack = [s]
        seen[s] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if isConnected[u][v] and not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return provinces


if __name__ == "__main__":
    for f in (findCircleNum, findCircleNumDFS):
        assert f([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2
        assert f([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3
        assert f([[1]]) == 1
        assert f([[1, 1], [1, 1]]) == 1
        # chain 0-1-2-3 is one province
        assert f([[1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 1], [0, 0, 1, 1]]) == 1
        # two pairs
        assert f([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]) == 2
    print("All tests passed")
