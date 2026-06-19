"""
Problem 207 - Course Schedule
Difficulty: Medium
Topics: Graphs, Topological Sort, DFS, BFS

Return true if you can finish all courses given prerequisites.
Reduces to cycle detection in a directed graph.

Approach 1: DFS with 3-state coloring (0=unvisited, 1=in-stack, 2=done)
Approach 2: Kahn's BFS topological sort

Complexity: O(V + E) time, O(V + E) space
"""
from typing import List
from collections import defaultdict, deque


def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    graph: defaultdict = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    state = [0] * numCourses

    def dfs(node: int) -> bool:
        if state[node] == 1:
            return False
        if state[node] == 2:
            return True
        state[node] = 1
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
        state[node] = 2
        return True

    return all(dfs(i) for i in range(numCourses) if state[i] == 0)


def canFinish_kahn(numCourses: int, prerequisites: List[List[int]]) -> bool:
    graph: defaultdict = defaultdict(list)
    in_degree = [0] * numCourses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    queue = deque(i for i in range(numCourses) if in_degree[i] == 0)
    processed = 0
    while queue:
        node = queue.popleft()
        processed += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return processed == numCourses


if __name__ == "__main__":
    assert canFinish(2, [[1, 0]]) == True
    assert canFinish(2, [[1, 0], [0, 1]]) == False
    assert canFinish(3, [[0, 1], [1, 2], [2, 0]]) == False
    assert canFinish(4, [[1, 0], [2, 1], [3, 2]]) == True
    assert canFinish_kahn(2, [[1, 0]]) == True
    assert canFinish_kahn(2, [[1, 0], [0, 1]]) == False
    print("All tests passed!")
