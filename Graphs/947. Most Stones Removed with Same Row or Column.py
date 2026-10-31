"""
947. Most Stones Removed with Same Row or Column
Difficulty: Medium
Topics: Union-Find, Graph, DFS

On a 2D plane, we place n stones at some integer coordinate points. Each
coordinate point may have at most one stone.

A stone can be removed if it shares either the same row or the same column as
another stone that has not been removed.

Given an array stones of length n where stones[i] = [xi, yi] represents the
location of the ith stone, return the largest possible number of stones that
can be removed.

Example 1:
    Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
    Output: 5
Example 2:
    Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
    Output: 3
Example 3:
    Input: stones = [[0,0]]
    Output: 0

Constraints:
    1 <= stones.length <= 1000
    0 <= xi, yi <= 10^4
    No two stones are at the same coordinate point.

Approach (Union-Find on rows/columns):
    Stones sharing a row or column form a connected component. In each
    component of size k, we can always remove k-1 stones (remove leaves of a
    spanning tree, keeping the last one), and never all k. So the answer is
    n - (number of components). Treat each row x and column y as nodes
    (column offset by 10001) and union x with y for every stone; the number of
    distinct roots among used nodes is the number of components.

Complexity:
    Time:  O(n * alpha(n))
    Space: O(n)

Alternative: DFS over stones, grouping by row/column adjacency lists.
"""
from typing import List
from collections import defaultdict


class Solution:
    def removeStones(self, stones: List[List[int]]) -> int:
        parent = {}

        def find(x: int) -> int:
            parent.setdefault(x, x)
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[ra] = rb

        for x, y in stones:
            union(x, y + 10001)
        components = len({find(x) for x in list(parent)})
        return len(stones) - components

    def removeStonesDFS(self, stones: List[List[int]]) -> int:
        rows, cols = defaultdict(list), defaultdict(list)
        for i, (x, y) in enumerate(stones):
            rows[x].append(i)
            cols[y].append(i)
        seen = [False] * len(stones)
        comps = 0
        for i in range(len(stones)):
            if seen[i]:
                continue
            comps += 1
            stack = [i]
            seen[i] = True
            while stack:
                j = stack.pop()
                x, y = stones[j]
                for k in rows[x] + cols[y]:
                    if not seen[k]:
                        seen[k] = True
                        stack.append(k)
        return len(stones) - comps


if __name__ == "__main__":
    s = Solution()
    for f in (s.removeStones, s.removeStonesDFS):
        assert f([[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]) == 5
        assert f([[0,0],[0,2],[1,1],[2,0],[2,2]]) == 3
        assert f([[0,0]]) == 0
        assert f([[0,0],[1,1]]) == 0
        assert f([[0,0],[0,1],[0,2]]) == 2
        assert f([[0,5],[10000,5]]) == 1
    print("All tests passed")
