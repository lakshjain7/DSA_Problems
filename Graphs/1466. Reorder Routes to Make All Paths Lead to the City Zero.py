"""
1466. Reorder Routes to Make All Paths Lead to the City Zero
Difficulty: Medium
Topics: Graphs, Depth-First Search, Breadth-First Search, Trees

Problem Statement
-----------------
There are n cities numbered from 0 to n - 1 and n - 1 roads such that there is
only one way to travel between two different cities (this network forms a tree).
Roads were originally designed to be traveled in a single direction.

You are given roads, where roads[i] = [a_i, b_i] represents a road from city a_i
to city b_i.

This year, there will be a big event in the capital (city 0), and many people
want to travel to this city.

Your task is to reorient some roads such that each city can visit city 0. Return
the minimum number of edges changed.

It is guaranteed that each city can reach city 0 after reorder.

Examples
--------
Example 1:
    Input: n = 6, connections = [[0,1],[1,3],[2,3],[4,0],[4,5]]
    Output: 3
    Explanation: Change the direction of edges shown in red so that each node can
    reach node 0 (capital).

Example 2:
    Input: n = 5, connections = [[1,0],[1,2],[3,2],[3,4]]
    Output: 2

Example 3:
    Input: n = 3, connections = [[1,0],[2,0]]
    Output: 0

Constraints
-----------
- 2 <= n <= 5 * 10^4
- connections.length == n - 1
- connections[i].length == 2
- 0 <= a_i, b_i <= n - 1
- a_i != b_i

Approach (DFS / BFS on an undirected view with direction flags)
---------------------------------------------------------------
The underlying graph is a tree (n nodes, n - 1 edges, connected). If we ignore
directions, there is a unique simple path between city 0 and every other city.
We want every city to be able to reach 0, which means along the unique path from
0 outward to each city, every edge must point *back toward* 0. Equivalently, when
we traverse the tree starting at 0 and moving away from it, any edge that points
in the same direction as our traversal (away from 0) must be reversed.

To detect direction while still being able to walk the whole tree, we build an
adjacency list containing both orientations: for a given road a -> b we store
(b, 1) in a's list (a real forward edge, cost 1 if traversed away from 0) and
(a, 0) in b's list (the reverse edge, cost 0). Starting a DFS/BFS from node 0,
whenever we move to an unvisited neighbor across an edge marked with cost 1, that
original edge points away from 0 and must be flipped, so we add 1 to the answer.

Why it works
------------
Because the graph is a tree, the DFS from 0 visits each edge exactly once in the
"away from 0" direction. An edge needs flipping if and only if its stored
original direction is away from 0, which is exactly the cost bit we recorded.
Summing these bits over all edges gives the minimum number of reversals.

Complexity
----------
Time:  O(n) - we build adjacency in O(n) and visit each of the n nodes and
       n - 1 edges a constant number of times.
Space: O(n) - adjacency list, visited set, and the DFS/BFS frontier.

Alternative Approach (iterative BFS)
------------------------------------
The same idea works with a queue instead of recursion, avoiding recursion-depth
limits on very deep (path-like) trees. Included below as `min_reorder_bfs`.
"""

from collections import defaultdict, deque
from typing import List


def min_reorder(n: int, connections: List[List[int]]) -> int:
    """Recursive DFS solution. O(n) time."""
    graph = defaultdict(list)
    for a, b in connections:
        graph[a].append((b, 1))  # original direction a->b : cost 1 if walked away from 0
        graph[b].append((a, 0))  # reverse direction : cost 0

    visited = set()

    def dfs(node: int) -> int:
        visited.add(node)
        changes = 0
        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                changes += cost + dfs(neighbor)
        return changes

    return dfs(0)


def min_reorder_bfs(n: int, connections: List[List[int]]) -> int:
    """Iterative BFS solution (safe for deep trees). O(n) time."""
    graph = defaultdict(list)
    for a, b in connections:
        graph[a].append((b, 1))
        graph[b].append((a, 0))

    visited = {0}
    queue = deque([0])
    changes = 0
    while queue:
        node = queue.popleft()
        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                changes += cost
                queue.append(neighbor)
    return changes


if __name__ == "__main__":
    # Example 1
    assert min_reorder(6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]) == 3
    assert min_reorder_bfs(6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]) == 3

    # Example 2
    assert min_reorder(5, [[1, 0], [1, 2], [3, 2], [3, 4]]) == 2
    assert min_reorder_bfs(5, [[1, 0], [1, 2], [3, 2], [3, 4]]) == 2

    # Example 3
    assert min_reorder(3, [[1, 0], [2, 0]]) == 0
    assert min_reorder_bfs(3, [[1, 0], [2, 0]]) == 0

    # Two cities, edge points away from 0 -> must flip
    assert min_reorder(2, [[0, 1]]) == 1
    # Two cities, edge already points to 0 -> no flip
    assert min_reorder(2, [[1, 0]]) == 0

    # Star centered at 0 with all edges pointing outward -> flip all
    star_out = [[0, 1], [0, 2], [0, 3], [0, 4]]
    assert min_reorder(5, star_out) == 4
    assert min_reorder_bfs(5, star_out) == 4

    # Star centered at 0 with all edges pointing inward -> zero flips
    star_in = [[1, 0], [2, 0], [3, 0], [4, 0]]
    assert min_reorder(5, star_in) == 0

    # Deep chain to exercise BFS path safety (all point away -> n-1 flips)
    chain = [[i, i + 1] for i in range(999)]
    assert min_reorder_bfs(1000, chain) == 999

    print("All tests passed for 1466. Reorder Routes to Make All Paths Lead to the City Zero")
