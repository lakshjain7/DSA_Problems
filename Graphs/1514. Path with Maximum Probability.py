"""
Problem 1514: Path with Maximum Probability
Difficulty: Medium
Topics: Graph, Heap (Priority Queue), Shortest Path

You are given an undirected weighted graph of n nodes (0-indexed), represented
by an edge list where edges[i] = [a, b] is an undirected edge connecting nodes
a and b with a probability of success of traversing that edge succProb[i].
Given two nodes start and end, find the path with the maximum probability of
success to go from start to end and return its success probability.
If there is no path from start to end, return 0. Answers within 1e-5 of the
correct answer are accepted.

Example 1:
    Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2],
           start = 0, end = 2
    Output: 0.25

Example 2:
    Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3],
           start = 0, end = 2
    Output: 0.3

Example 3:
    Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
    Output: 0.0

Constraints:
    2 <= n <= 10^4
    0 <= start, end < n, start != end
    0 <= a, b < n, a != b
    0 <= succProb.length == edges.length <= 2*10^4
    0 <= succProb[i] <= 1
    There is at most one edge between every two nodes.

Approach (Dijkstra with max-heap):
    Probabilities lie in [0,1], so multiplying along a path never increases it
    - the analogue of non-negative weights. Greedily expanding the node with
    the highest known probability is therefore correct. Use a max-heap (negate
    values in heapq) and relax: prob[v] = max(prob[v], prob[u] * p).

Complexity:
    Time: O((V + E) log V)   Space: O(V + E)

Alternative (Bellman-Ford): relax all edges up to n-1 rounds, stopping early
when no update occurs. Time O(V*E) worst case, Space O(V).
"""
import heapq
from typing import List


def max_probability(n: int, edges: List[List[int]], succ_prob: List[float],
                    start: int, end: int) -> float:
    graph = [[] for _ in range(n)]
    for (a, b), p in zip(edges, succ_prob):
        graph[a].append((b, p))
        graph[b].append((a, p))

    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]
    while heap:
        neg, u = heapq.heappop(heap)
        prob = -neg
        if u == end:
            return prob
        if prob < best[u]:
            continue
        for v, p in graph[u]:
            cand = prob * p
            if cand > best[v]:
                best[v] = cand
                heapq.heappush(heap, (-cand, v))
    return 0.0


def max_probability_bellman_ford(n: int, edges: List[List[int]],
                                 succ_prob: List[float], start: int,
                                 end: int) -> float:
    best = [0.0] * n
    best[start] = 1.0
    for _ in range(n - 1):
        changed = False
        for (a, b), p in zip(edges, succ_prob):
            if best[a] * p > best[b]:
                best[b] = best[a] * p
                changed = True
            if best[b] * p > best[a]:
                best[a] = best[b] * p
                changed = True
        if not changed:
            break
    return best[end]


if __name__ == "__main__":
    for fn in (max_probability, max_probability_bellman_ford):
        e = [[0, 1], [1, 2], [0, 2]]
        assert abs(fn(3, e, [0.5, 0.5, 0.2], 0, 2) - 0.25) < 1e-5
        assert abs(fn(3, e, [0.5, 0.5, 0.3], 0, 2) - 0.3) < 1e-5
        assert fn(3, [[0, 1]], [0.5], 0, 2) == 0.0
        assert fn(2, [], [], 0, 1) == 0.0
        assert abs(fn(2, [[0, 1]], [1.0], 0, 1) - 1.0) < 1e-9
        assert fn(2, [[0, 1]], [0.0], 0, 1) == 0.0
        # chain beats nothing; longer path with higher probs beats direct edge
        e = [[0, 1], [1, 2], [2, 3], [0, 3]]
        assert abs(fn(4, e, [0.9, 0.9, 0.9, 0.5], 0, 3) - 0.729) < 1e-5
    print("All tests passed")
