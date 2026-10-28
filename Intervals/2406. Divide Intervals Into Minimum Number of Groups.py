"""
2406. Divide Intervals Into Minimum Number of Groups
Difficulty: Medium
Topics: Array, Two Pointers, Greedy, Sorting, Heap (Priority Queue), Prefix Sum

Problem:
You are given a 2D integer array intervals where intervals[i] = [left_i, right_i]
represents the inclusive interval [left_i, right_i]. You have to divide the
intervals into one or more groups such that each interval is in exactly one
group, and no two intervals that are in the same group intersect each other.
Return the minimum number of groups you need to make. Two intervals intersect
if there is at least one common number between them.

Example 1:
    Input: intervals = [[5,10],[6,8],[1,5],[2,3],[1,10]]
    Output: 3
Example 2:
    Input: intervals = [[1,3],[5,6],[8,10],[11,13]]
    Output: 1

Constraints:
    1 <= intervals.length <= 10^5
    intervals[i].length == 2
    1 <= left_i <= right_i <= 10^6

Approach (min-heap of group end times):
    Sort by start. Keep a min-heap of the end of each existing group. For an
    interval starting at s, if the earliest-ending group ends before s
    (end < s, since intervals are inclusive) we reuse it; otherwise open a new
    group. The heap size at the end is the answer, which equals the maximum
    number of simultaneously overlapping intervals.

Complexity:
    Time:  O(n log n)
    Space: O(n)

Alternative (sweep line / difference array): +1 at left, -1 at right+1; the
maximum running sum is the answer. O(n + M) with M = max coordinate.
"""
from typing import List
import heapq


class Solution:
    def minGroups(self, intervals: List[List[int]]) -> int:
        heap: List[int] = []
        for s, e in sorted(intervals):
            if heap and heap[0] < s:
                heapq.heapreplace(heap, e)
            else:
                heapq.heappush(heap, e)
        return len(heap)

    def minGroupsSweep(self, intervals: List[List[int]]) -> int:
        events = []
        for s, e in intervals:
            events.append((s, 1))
            events.append((e + 1, -1))
        events.sort()  # -1 sorts before +1 at same coordinate
        cur = best = 0
        for _, d in events:
            cur += d
            best = max(best, cur)
        return best


if __name__ == "__main__":
    import random
    s = Solution()
    for f in (s.minGroups, s.minGroupsSweep):
        assert f([[5, 10], [6, 8], [1, 5], [2, 3], [1, 10]]) == 3
        assert f([[1, 3], [5, 6], [8, 10], [11, 13]]) == 1
        assert f([[1, 1]]) == 1
        assert f([[1, 5], [5, 8]]) == 2  # inclusive touching intersects
        assert f([[1, 2], [3, 4]]) == 1
        assert f([[1, 10]] * 5) == 5
    def brute(iv):
        pts = set(range(1, 31))
        return max(sum(1 for a, b in iv if a <= p <= b) for p in pts)
    random.seed(2)
    for _ in range(300):
        iv = []
        for _ in range(random.randint(1, 10)):
            a = random.randint(1, 25); b = random.randint(a, 30)
            iv.append([a, b])
        assert s.minGroups(iv) == s.minGroupsSweep(iv) == brute(iv)
    print("All tests passed")
