"""
210. Course Schedule II
Difficulty: Medium
Topics: Graph, Topological Sort, BFS, DFS, Depth-First Search

Problem Statement
-----------------
There are a total of numCourses courses you have to take, labeled from 0 to
numCourses - 1. You are given an array prerequisites where
prerequisites[i] = [a_i, b_i] indicates that you must take course b_i first if
you want to take course a_i.

    For example, the pair [0, 1] indicates that to take course 0 you have to
    first take course 1.

Return the ordering of courses you should take to finish all courses. If there
are many valid answers, return any of them. If it is impossible to finish all
courses, return an empty array.

Examples
--------
Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: [0,1]
    Explanation: There are a total of 2 courses to take. To take course 1 you
    should have finished course 0. So the correct course order is [0, 1].

Example 2:
    Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
    Output: [0,2,1,3]
    Explanation: There are a total of 4 courses to take. To take course 3 you
    should have finished both courses 1 and 2. Both courses 1 and 2 should be
    taken after you finished course 0. So one correct ordering is [0,1,2,3].
    Another correct ordering is [0,2,1,3].

Example 3:
    Input: numCourses = 1, prerequisites = []
    Output: [0]

Constraints
-----------
    * 1 <= numCourses <= 2000
    * 0 <= prerequisites.length <= numCourses * (numCourses - 1)
    * prerequisites[i].length == 2
    * 0 <= a_i, b_i < numCourses
    * a_i != b_i
    * All the pairs [a_i, b_i] are distinct.

Approach 1: Kahn's Algorithm (BFS Topological Sort)
---------------------------------------------------
The problem asks for a topological ordering of a directed graph, which exists
if and only if the graph is a DAG (has no cycle).

Build the graph where an edge b -> a means "b must come before a", and track the
in-degree (number of unmet prerequisites) of every node. Repeatedly take any
node with in-degree 0 (all prerequisites satisfied), append it to the ordering,
and decrement the in-degree of its neighbors, pushing any that drop to 0.

If we manage to output all numCourses nodes, that sequence is a valid ordering.
If the queue empties before we output everything, the remaining nodes lie on a
cycle, so no valid ordering exists and we return [].

Why it works: a node is emitted only after every prerequisite has been emitted,
so the produced sequence respects all edges. A cycle can never reach in-degree 0
(each node on it always has at least one unprocessed predecessor), so cycles are
detected by the shortfall in the output count.

Complexity
----------
Time:  O(V + E) - every node and edge is processed exactly once.
Space: O(V + E) - adjacency list plus the in-degree array and queue.

Approach 2: DFS with Cycle Detection
------------------------------------
Run DFS from each node using three states (unvisited, visiting, visited). If DFS
reaches a node currently in the "visiting" state, a back edge (cycle) exists ->
return []. Otherwise append a node to the order after all its descendants are
processed (post-order), then reverse the accumulated list to obtain a valid
topological order. Same O(V + E) time and space.
"""

from collections import deque
from typing import List


def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """Kahn's algorithm (BFS). Returns a valid order or [] if impossible."""
    adj: List[List[int]] = [[] for _ in range(num_courses)]
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        indegree[course] += 1

    queue = deque(c for c in range(num_courses) if indegree[c] == 0)
    order: List[int] = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in adj[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == num_courses else []


def find_order_dfs(num_courses: int, prerequisites: List[List[int]]) -> List[int]:
    """DFS post-order with cycle detection. Returns a valid order or []."""
    adj: List[List[int]] = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        adj[prereq].append(course)

    UNVISITED, VISITING, VISITED = 0, 1, 2
    state = [UNVISITED] * num_courses
    order: List[int] = []

    def dfs(node: int) -> bool:
        state[node] = VISITING
        for nxt in adj[node]:
            if state[nxt] == VISITING:
                return False           # back edge -> cycle
            if state[nxt] == UNVISITED and not dfs(nxt):
                return False
        state[node] = VISITED
        order.append(node)
        return True

    for c in range(num_courses):
        if state[c] == UNVISITED and not dfs(c):
            return []

    return order[::-1]


def _is_valid_order(num_courses: int, prerequisites: List[List[int]],
                    order: List[int]) -> bool:
    """Verify order is a permutation respecting every prerequisite edge."""
    if sorted(order) != list(range(num_courses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    return all(position[prereq] < position[course]
               for course, prereq in prerequisites)


if __name__ == "__main__":
    # Example 1
    assert find_order(2, [[1, 0]]) == [0, 1]

    # Example 2 - multiple valid answers, verify validity instead of equality
    order2 = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert _is_valid_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]], order2)

    # Example 3 - single course, no prerequisites
    assert find_order(1, []) == [0]

    # Cycle -> impossible
    assert find_order(2, [[1, 0], [0, 1]]) == []

    # No prerequisites at all -> any permutation of all nodes is valid
    order_free = find_order(3, [])
    assert sorted(order_free) == [0, 1, 2]

    # Larger DAG, validate ordering
    prereqs = [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]
    order_big = find_order(5, prereqs)
    assert _is_valid_order(5, prereqs, order_big)

    # Self-consistency between BFS and DFS approaches on validity
    for n, pr in [
        (2, [[1, 0]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
        (1, []),
        (5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]]),
        (3, []),
    ]:
        assert _is_valid_order(n, pr, find_order(n, pr))
        assert _is_valid_order(n, pr, find_order_dfs(n, pr))

    # Both detect the same cycle
    assert find_order(3, [[0, 1], [1, 2], [2, 0]]) == []
    assert find_order_dfs(3, [[0, 1], [1, 2], [2, 0]]) == []

    print("All test cases passed for 210. Course Schedule II")
