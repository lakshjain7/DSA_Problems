"""
1851. Minimum Interval to Include Each Query
Difficulty: Hard
Topics: Array, Binary Search, Sorting, Line Sweep, Heap (Priority Queue)

Problem:
You are given a 2D integer array intervals, where intervals[i] = [left_i, right_i]
describes the i-th interval starting at left_i and ending at right_i (inclusive).
The size of an interval is defined as the number of integers it contains, or
more formally right_i - left_i + 1.

You are also given an integer array queries. The answer to the j-th query is
the size of the smallest interval i such that left_i <= queries[j] <= right_i.
If no such interval exists, the answer is -1.

Return an array containing the answers to the queries.

Example 1:
    Input: intervals = [[1,4],[2,4],[3,6],[4,4]], queries = [2,3,4,5]
    Output: [3,3,1,4]
    Explanation:
      - Query = 2: [2,4] is the smallest interval containing 2 -> size 3.
      - Query = 3: [2,4] -> size 3.
      - Query = 4: [4,4] -> size 1.
      - Query = 5: [3,6] -> size 4.

Example 2:
    Input: intervals = [[2,3],[2,5],[1,8],[20,25]], queries = [2,19,5,22]
    Output: [2,-1,4,6]

Constraints:
    1 <= intervals.length <= 10^5
    1 <= queries.length <= 10^5
    intervals[i].length == 2
    1 <= left_i <= right_i <= 10^7
    1 <= queries[j] <= 10^7

Approach (Offline sweep + min-heap):
    Answer queries offline in increasing order of value.
      1. Sort intervals by left endpoint; sort query indices by query value.
      2. For each query q (ascending), push every interval with left <= q onto
         a min-heap keyed by (size, right).
      3. Pop from the heap while the top's right < q — that interval ended
         before q and, since later queries are even larger, it can never be
         useful again (lazy deletion).
      4. The heap top (if any) is the smallest interval covering q.
    Correctness: every interval in the heap has left <= q (pushed only then),
    and after step 3 the top has right >= q, so it covers q. Any covering
    interval of smaller size would also be in the heap and not yet popped,
    contradicting minimality of the top.

Complexity:
    Time:  O(n log n + m log m) — sorting plus each interval pushed/popped once.
    Space: O(n + m) for the heap and answer array.

Alternative (Sort by size + DSU "paint" over sorted queries):
    Sort intervals by size ascending. Sort distinct query values. For each
    interval, binary-search the first unanswered query >= left and assign it
    while <= right, using a union-find "next unanswered" pointer to skip
    already-answered queries. Each query is answered exactly once by the
    smallest interval that covers it. O((n + m) log m) time.
"""

import heapq
from bisect import bisect_left


def minInterval(intervals: list[list[int]], queries: list[int]) -> list[int]:
    intervals = sorted(intervals)
    order = sorted(range(len(queries)), key=lambda j: queries[j])
    ans = [-1] * len(queries)
    heap: list[tuple[int, int]] = []
    i = 0
    for j in order:
        q = queries[j]
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heapq.heappush(heap, (r - l + 1, r))
            i += 1
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        if heap:
            ans[j] = heap[0][0]
    return ans


def minIntervalDSU(intervals: list[list[int]], queries: list[int]) -> list[int]:
    vals = sorted(set(queries))
    k = len(vals)
    best = [-1] * k
    parent = list(range(k + 1))  # parent[x] -> next unanswered index >= x

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for l, r in sorted(intervals, key=lambda iv: iv[1] - iv[0]):
        size = r - l + 1
        idx = find(bisect_left(vals, l))
        while idx < k and vals[idx] <= r:
            best[idx] = size
            parent[idx] = idx + 1
            idx = find(idx + 1)

    pos = {v: t for t, v in enumerate(vals)}
    return [best[pos[q]] for q in queries]


def _brute(intervals: list[list[int]], queries: list[int]) -> list[int]:
    out = []
    for q in queries:
        sizes = [r - l + 1 for l, r in intervals if l <= q <= r]
        out.append(min(sizes) if sizes else -1)
    return out


if __name__ == "__main__":
    import random

    cases = [
        ([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5], [3, 3, 1, 4]),
        ([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22], [2, -1, 4, 6]),
        ([[1, 1]], [1], [1]),
        ([[1, 1]], [2], [-1]),
        ([[5, 10]], [1, 5, 10, 11], [-1, 6, 6, -1]),
        ([[1, 10], [2, 3], [2, 3]], [3, 3, 1], [2, 2, 10]),  # duplicate queries
        ([[1, 10000000]], [10000000], [10000000]),
    ]
    for iv, qs, exp in cases:
        assert minInterval([x[:] for x in iv], qs[:]) == exp, (iv, qs)
        assert minIntervalDSU([x[:] for x in iv], qs[:]) == exp, (iv, qs)

    rng = random.Random(1851)
    for _ in range(400):
        n = rng.randint(1, 15)
        iv = []
        for _ in range(n):
            a = rng.randint(1, 30)
            b = rng.randint(a, min(30, a + rng.randint(0, 12)))
            iv.append([a, b])
        qs = [rng.randint(1, 32) for _ in range(rng.randint(1, 15))]
        exp = _brute(iv, qs)
        assert minInterval(iv, qs) == exp, (iv, qs)
        assert minIntervalDSU(iv, qs) == exp, (iv, qs)

    print("All tests passed for 1851. Minimum Interval to Include Each Query")
