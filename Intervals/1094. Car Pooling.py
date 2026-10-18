"""
1094. Car Pooling
Difficulty: Medium
Topics: Array, Sorting, Heap, Prefix Sum, Simulation, Intervals

Problem:
    There is a car with capacity empty seats. The vehicle only drives east.
    Given trips where trips[i] = [numPassengers, from, to] (passengers picked up
    at `from` and dropped at `to`), return true if it is possible to pick up and
    drop off all passengers for all trips, otherwise false.

Examples:
    Input: trips = [[2,1,5],[3,3,7]], capacity = 4   Output: false
    Input: trips = [[2,1,5],[3,3,7]], capacity = 5   Output: true

Constraints:
    1 <= trips.length <= 1000
    trips[i].length == 3
    1 <= numPassengers <= 100
    0 <= from < to <= 1000
    1 <= capacity <= 10^5

Approach:
    Difference array: add +p at `from`, -p at `to` (passengers leave before new
    ones board at the same stop since the interval is half-open). A running
    prefix sum over positions gives the load at each point; if it ever exceeds
    capacity the answer is false.

Complexity:
    Time: O(n + M) where M = max stop (1001).
    Space: O(M).
"""
from typing import List
import heapq


def carPooling(trips: List[List[int]], capacity: int) -> bool:
    diff = [0] * 1002
    for p, s, e in trips:
        diff[s] += p
        diff[e] -= p
    load = 0
    for d in diff:
        load += d
        if load > capacity:
            return False
    return True


def carPoolingHeap(trips: List[List[int]], capacity: int) -> bool:
    """Alternative: sort by start, min-heap of (end, passengers) for drop-offs.
    Time O(n log n), space O(n)."""
    load = 0
    heap = []
    for p, s, e in sorted(trips, key=lambda t: t[1]):
        while heap and heap[0][0] <= s:
            load -= heapq.heappop(heap)[1]
        load += p
        if load > capacity:
            return False
        heapq.heappush(heap, (e, p))
    return True


if __name__ == "__main__":
    for f in (carPooling, carPoolingHeap):
        assert f([[2, 1, 5], [3, 3, 7]], 4) is False
        assert f([[2, 1, 5], [3, 3, 7]], 5) is True
        assert f([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11) is True
        assert f([[5, 0, 1]], 4) is False
        assert f([[5, 0, 1]], 5) is True
        assert f([[2, 1, 5], [3, 5, 7]], 3) is True  # drop-off before pickup at 5
    print("All tests passed.")
