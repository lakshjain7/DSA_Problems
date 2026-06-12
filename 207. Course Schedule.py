"""
Problem 207 - Course Schedule
Difficulty: Medium
Topics: Graphs, Topological Sort, DFS, BFS

Problem Statement:
There are a total of numCourses courses you have to take, labeled from 0 to
numCourses - 1. You are given an array prerequisites where
prerequisites[i] = [ai, bi] indicates that you must take course bi first if
you want to take course ai.

Return true if you can finish all courses. Otherwise, return false.

Example 1:
    Input: numCourses = 2, prerequisites = [[1,0]]
    Output: true
    Explanation: There are 2 courses to take. To take course 1 you should have
    finished course 0. So it is possible.

Example 2:
    Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
    Output: false
    Explanation: There are 2 courses to take. To take course 1 you should have
    finished course 0, and to take course 0 you should have finished course 1.
    This is impossible -- a cycle exists.

Constraints:
    1 <= numCourses <= 2000
    0 <= prerequisites.length <= 5000
    prerequisites[i].length == 2
    0 <= ai, bi < numCourses
    All the pairs prerequisites[i] are unique.

Approach (DFS with 3-state coloring):
    This reduces to cycle detection in a directed graph.
    Each course is a node; an edge (bi -> ai) means "bi must precede ai".
    A cycle means there's a circular dependency -> impossible.

    3-state DFS:
        0 = unvisited
        1 = currently in the DFS stack (being explored)
        2 = fully processed (no cycle found downstream)

    For each unvisited node, run DFS. If we reach a node marked 1 (still on
    the stack), we found a back edge -> cycle -> return False.
    Once all neighbors are processed, mark node as 2 (safe).

Complexity:
    Time:  O(V + E) where V = numCourses, E = len(prerequisites)
    Space: O(V + E) for adjacency list + O(V) recursion stack

Alternative Approach (Kahn's Algorithm / BFS Topological Sort):
    Compute in-degree for every node.
    Enqueue all nodes with in-degree 0 (no prerequisites).
    Process queue: decrement neighbors' in-degrees; enqueue those that reach 0.
    If all V nodes are processed, no cycle exists -> return True.
    Otherwise at least one node was never reachable -> cycle exists -> False.
"""
from typing import List
from collections import defaultdict, deque


def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    DFS with 3-state coloring for cycle detection.
    """
    graph: defaultdict = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    # 0 = unvisited | 1 = in current DFS path | 2 = fully processed
    state = [0] * numCourses

    def dfs(node: int) -> bool:
        """Returns True if no cycle is reachable from node."""
        if state[node] == 1:   # back edge -> cycle
            return False
        if state[node] == 2:   # already verified safe
            return True

        state[node] = 1        # mark as currently visiting
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        state[node] = 2        # mark as fully processed / safe
        return True

    return all(dfs(i) for i in range(numCourses) if state[i] == 0)


def canFinish_kahn(numCourses: int, prerequisites: List[List[int]]) -> bool:
    """
    Alternative: Kahn's Algorithm (BFS topological sort).
    A valid topological order exists iff no cycle exists.
    """
    graph: defaultdict = defaultdict(list)
    in_degree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with all courses that have no prerequisites
    queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
    processed = 0

    while queue:
        node = queue.popleft()
        processed += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If we processed every course, no cycle exists
    return processed == numCourses


if __name__ == "__main__":
    # --- DFS version ---
    assert canFinish(2, [[1, 0]]) == True
    assert canFinish(2, [[1, 0], [0, 1]]) == False   # direct cycle
    assert canFinish(1, []) == True                   # single course
    assert canFinish(4, [[1, 0], [2, 1], [3, 2]]) == True   # linear chain
    assert canFinish(3, [[0, 1], [0, 2], [1, 2]]) == True   # diamond, no cycle
    assert canFinish(3, [[0, 1], [1, 2], [2, 0]]) == False  # 3-node cycle
    assert canFinish(5, [[1, 4], [2, 4], [3, 1], [3, 2]]) == True
    assert canFinish(3, [[1, 0], [2, 0]]) == True    # two courses depend on same
    assert canFinish(2, []) == True                   # no prerequisites

    # --- Kahn's version (same expected results) ---
    assert canFinish_kahn(2, [[1, 0]]) == True
    assert canFinish_kahn(2, [[1, 0], [0, 1]]) == False
    assert canFinish_kahn(1, []) == True
    assert canFinish_kahn(3, [[0, 1], [1, 2], [2, 0]]) == False
    assert canFinish_kahn(4, [[1, 0], [2, 1], [3, 2]]) == True

    print("All tests passed!")
