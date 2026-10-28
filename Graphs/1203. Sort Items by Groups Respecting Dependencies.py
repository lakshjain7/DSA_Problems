"""
1203. Sort Items by Groups Respecting Dependencies
Difficulty: Hard
Topics: Depth-First Search, Breadth-First Search, Graph, Topological Sort

Problem:
There are n items each belonging to zero or one of m groups where group[i] is
the group that the i-th item belongs to and it's equal to -1 if the i-th item
belongs to no group. Return a sorted list of the items such that:
  * The items that belong to the same group are next to each other in the
    sorted list.
  * There are some relations between these items where beforeItems[i] is a list
    containing all the items that should come before the i-th item in the
    sorted array (to the left of the i-th item).
Return any solution if there is more than one solution and return an empty list
if there is no solution.

Example 1:
    Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
           beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]
    Output: a valid ordering, e.g. [6,3,4,1,5,2,0,7]
Example 2:
    Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1],
           beforeItems = [[],[6],[5],[6],[3],[],[4],[]]
    Output: []

Constraints:
    1 <= m <= n <= 3 * 10^4
    group.length == beforeItems.length == n
    -1 <= group[i] <= m - 1
    0 <= beforeItems[i].length <= n - 1
    0 <= beforeItems[i][j] <= n - 1, i != beforeItems[i][j]
    beforeItems[i] does not contain duplicates.

Approach (two-level topological sort):
    Give every group-less item its own fresh group id so every item has one.
    Build (1) an item graph with edges before -> item and (2) a group graph with
    an edge group[before] -> group[item] when they differ. Topologically sort the
    groups (Kahn). Topologically sort the items. If either has a cycle, return [].
    Then bucket the sorted items by group (preserving item order) and emit the
    buckets in group order. Items of one group are contiguous, group order
    respects cross-group dependencies, and the item order respects within-group
    dependencies.

Complexity:
    Time:  O(n + m + E) where E = total beforeItems entries
    Space: O(n + m + E)
"""
from typing import List
from collections import deque, defaultdict


class Solution:
    def sortItems(self, n: int, m: int, group: List[int],
                  beforeItems: List[List[int]]) -> List[int]:
        group = group[:]
        for i in range(n):
            if group[i] == -1:
                group[i] = m
                m += 1

        item_adj = [[] for _ in range(n)]
        item_in = [0] * n
        group_adj = [[] for _ in range(m)]
        group_in = [0] * m

        for i in range(n):
            for b in beforeItems[i]:
                item_adj[b].append(i)
                item_in[i] += 1
                if group[b] != group[i]:
                    group_adj[group[b]].append(group[i])
                    group_in[group[i]] += 1

        def topo(adj, indeg, size):
            q = deque(v for v in range(size) if indeg[v] == 0)
            order = []
            while q:
                v = q.popleft()
                order.append(v)
                for w in adj[v]:
                    indeg[w] -= 1
                    if indeg[w] == 0:
                        q.append(w)
            return order if len(order) == size else []

        item_order = topo(item_adj, item_in, n)
        group_order = topo(group_adj, group_in, m)
        if not item_order or not group_order:
            return []

        buckets = defaultdict(list)
        for it in item_order:
            buckets[group[it]].append(it)
        res: List[int] = []
        for g in group_order:
            res.extend(buckets[g])
        return res


def _valid(n, group, before, res):
    if sorted(res) != list(range(n)):
        return False
    pos = {v: i for i, v in enumerate(res)}
    for i in range(n):
        for b in before[i]:
            if pos[b] > pos[i]:
                return False
    # same-group items contiguous
    seen_done = set()
    prev = None
    for v in res:
        g = group[v]
        if g == -1:
            prev = None
            continue
        if g != prev and g in seen_done:
            return False
        if prev is not None and g != prev:
            seen_done.add(prev)
        prev = g
    return True


if __name__ == "__main__":
    s = Solution()
    g = [-1, -1, 1, 0, 0, 1, 0, -1]
    b1 = [[], [6], [5], [6], [3, 6], [], [], []]
    r = s.sortItems(8, 2, g, b1)
    assert _valid(8, g, b1, r), r
    b2 = [[], [6], [5], [6], [3], [], [4], []]
    assert s.sortItems(8, 2, g, b2) == []
    # no dependencies
    r = s.sortItems(5, 1, [-1] * 5, [[] for _ in range(5)])
    assert sorted(r) == [0, 1, 2, 3, 4]
    # cross-group cycle: 0(g0)->1(g1)->2(g0)
    assert s.sortItems(3, 2, [0, 1, 0], [[], [0], [1]]) == []
    # chain across groups
    gg = [0, 1, 0, 1]
    bb = [[], [0], [], [2]]
    r = s.sortItems(4, 2, gg, bb)
    assert _valid(4, gg, bb, r), r
    # single item
    assert s.sortItems(1, 1, [0], [[]]) == [0]
    print("All tests passed")
