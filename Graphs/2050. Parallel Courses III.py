"""
2050. Parallel Courses III
Difficulty: Hard
Topics: Array, Dynamic Programming, Graph, Topological Sort

Problem:
You are given an integer n, the number of courses labeled 1..n, and a 2D
array relations where relations[j] = [prevCourse_j, nextCourse_j] means
prevCourse_j must be completed before nextCourse_j. You are also given a
0-indexed array time where time[i] is the number of months to complete course
i+1. Rules: a course can start as soon as all its prerequisites are done, and
any number of courses can be taken at the same time. Return the minimum number
of months needed to complete all courses.

Example 1:
    Input: n = 3, relations = [[1,3],[2,3]], time = [3,2,5]
    Output: 8
Example 2:
    Input: n = 5, relations = [[1,5],[2,5],[3,5],[3,4],[4,5]], time = [1,2,3,4,5]
    Output: 12

Constraints:
    1 <= n <= 5 * 10^4
    0 <= relations.length <= min(n*(n-1)/2, 5 * 10^4)
    relations[j].length == 2, 1 <= prev, next <= n, prev != next
    All pairs are unique; the graph is a DAG.
    time.length == n, 1 <= time[i] <= 10^4

Approach (Kahn's topological sort + longest path DP):
    The answer is the longest weighted path in the DAG. Let finish[c] be the
    earliest month course c can finish = time[c] + max(finish[p]) over its
    prerequisites. Process nodes in topological order; when popping u, relax
    each successor v: start[v] = max(start[v], finish[u]). When v's indegree hits
    0, finish[v] = start[v] + time[v]. Answer = max finish.

Complexity:
    Time:  O(n + E)
    Space: O(n + E)

Alternative (memoized DFS):
    finish(c) = time[c] + max(finish(p) for p in prereqs[c]) with caching; same
    complexity, but recursion depth can reach n, so it is run iteratively here
    by raising the recursion limit.
"""
import sys
from collections import deque
from typing import List


def minimum_time(n: int, relations: List[List[int]], time: List[int]) -> int:
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in relations:
        adj[a - 1].append(b - 1)
        indeg[b - 1] += 1
    start = [0] * n
    finish = [0] * n
    q = deque(i for i in range(n) if indeg[i] == 0)
    while q:
        u = q.popleft()
        finish[u] = start[u] + time[u]
        for v in adj[u]:
            start[v] = max(start[v], finish[u])
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return max(finish)


def minimum_time_dfs(n: int, relations: List[List[int]], time: List[int]) -> int:
    sys.setrecursionlimit(max(10000, 2 * n + 100))
    prereq = [[] for _ in range(n)]
    for a, b in relations:
        prereq[b - 1].append(a - 1)
    memo = [-1] * n

    def finish(c: int) -> int:
        if memo[c] != -1:
            return memo[c]
        memo[c] = time[c] + max((finish(p) for p in prereq[c]), default=0)
        return memo[c]

    return max(finish(c) for c in range(n))


if __name__ == "__main__":
    for fn in (minimum_time, minimum_time_dfs):
        assert fn(3, [[1, 3], [2, 3]], [3, 2, 5]) == 8
        assert fn(5, [[1, 5], [2, 5], [3, 5], [3, 4], [4, 5]], [1, 2, 3, 4, 5]) == 12
        assert fn(1, [], [7]) == 7
        assert fn(3, [], [1, 9, 4]) == 9
        assert fn(4, [[1, 2], [2, 3], [3, 4]], [1, 2, 3, 4]) == 10
        assert fn(4, [[1, 2], [1, 3], [2, 4], [3, 4]], [2, 5, 1, 3]) == 10
    n = 2000
    rel = [[i, i + 1] for i in range(1, n)]
    assert minimum_time(n, rel, [1] * n) == n
    assert minimum_time_dfs(n, rel, [1] * n) == n
    print("All tests passed")
