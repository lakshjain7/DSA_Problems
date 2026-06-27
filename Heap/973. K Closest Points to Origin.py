"""
Problem 973: K Closest Points to Origin
Difficulty: Medium
Topics: Heap, Sorting, Divide and Conquer

Problem Statement:
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane
and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance:
    sqrt((x1 - x2)^2 + (y1 - y2)^2).

You may return the answer in any order. The answer is guaranteed to be unique
(except for the order that it is in).

Examples:
    Input: points = [[1,3],[-2,2]], k = 1
    Output: [[-2,2]]
    Explanation: The distance of (1,3) from origin is sqrt(10).
                 The distance of (-2,2) from origin is sqrt(8).
                 Since sqrt(8) < sqrt(10), (-2,2) is closer.

    Input: points = [[3,3],[5,-1],[-2,4]], k = 2
    Output: [[3,3],[-2,4]]

Constraints:
    - 1 <= k <= points.length <= 10^4
    - -10^4 <= xi, yi <= 10^4

Approach (Max-Heap of size k):
    Maintain a max-heap of size k. For each point, push (distance, point).
    If heap exceeds size k, pop the farthest point. Remaining k points are the answer.
    We compare squared distances (avoid sqrt) and negate for Python's min-heap.

    Time:  O(n log k)  — n pushes, each O(log k)
    Space: O(k)        — heap size

Alternative (Sort): O(n log n) — simpler but slower.
Alternative (Quickselect): O(n) average, O(n^2) worst.
"""

import heapq
from typing import List


class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap (negate distance to use Python's min-heap as max-heap)
        max_heap: list = []

        for x, y in points:
            dist_sq = x * x + y * y
            heapq.heappush(max_heap, (-dist_sq, x, y))
            if len(max_heap) > k:
                heapq.heappop(max_heap)

        return [[x, y] for _, x, y in max_heap]


class SolutionSort:
    """Simple sort approach — O(n log n)."""
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        points.sort(key=lambda p: p[0] ** 2 + p[1] ** 2)
        return points[:k]


class SolutionHeapq:
    """Using heapq.nsmallest — concise, O(n log k)."""
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        return heapq.nsmallest(k, points, key=lambda p: p[0] ** 2 + p[1] ** 2)


if __name__ == "__main__":
    def sets_equal(a, b):
        return sorted(map(tuple, a)) == sorted(map(tuple, b))

    sol = Solution()
    sol_sort = SolutionSort()
    sol_nsmall = SolutionHeapq()

    # Test 1
    pts = [[1,3],[-2,2]]
    assert sets_equal(sol.kClosest(pts, 1), [[-2,2]])
    assert sets_equal(sol_sort.kClosest([p[:] for p in pts], 1), [[-2,2]])
    assert sets_equal(sol_nsmall.kClosest(pts, 1), [[-2,2]])

    # Test 2
    pts = [[3,3],[5,-1],[-2,4]]
    result = sol.kClosest(pts, 2)
    assert sets_equal(result, [[3,3],[-2,4]])
    assert sets_equal(sol_sort.kClosest([p[:] for p in pts], 2), [[3,3],[-2,4]])

    # Test 3: k == len(points) — return all
    pts = [[1,1],[2,2]]
    assert sets_equal(sol.kClosest(pts, 2), [[1,1],[2,2]])

    # Test 4: origin included
    pts = [[0,0],[1,0],[0,1],[2,2]]
    assert sets_equal(sol.kClosest(pts, 2), [[0,0],[1,0]])
    assert sets_equal(sol_nsmall.kClosest(pts, 2), [[0,0],[1,0]])

    # Test 5: negative coordinates
    pts = [[-5,4],[3,-3],[1,1]]
    # distances sq: 41, 18, 2 => sorted: [1,1], [3,-3], [-5,4]
    assert sets_equal(sol.kClosest(pts, 1), [[1,1]])
    assert sets_equal(sol.kClosest(pts, 2), [[1,1],[3,-3]])

    print("All tests passed!")
