"""
Problem #239 — Sliding Window Maximum
Difficulty: Hard
Topics: Array, Sliding Window, Monotonic Deque, Heap

Given nums and k, return the maximum of each sliding window of size k.

Example: nums = [1,3,-1,-3,5,3,6,7], k=3 -> [3,3,5,5,6,7]

Approach: Monotonic Deque (Decreasing) — O(n) time, O(k) space
Maintain deque of indices with decreasing values. Front = current max.
Alternative: Max Heap — O(n log k)
"""

from collections import deque
from typing import List
import heapq


def maxSlidingWindow(nums: List[int], k: int) -> List[int]:
    result: List[int] = []
    dq: deque = deque()

    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] <= num:
            dq.pop()

        dq.append(i)

        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


def maxSlidingWindow_heap(nums: List[int], k: int) -> List[int]:
    result: List[int] = []
    heap: List[tuple] = []

    for i, num in enumerate(nums):
        heapq.heappush(heap, (-num, i))

        while heap[0][1] <= i - k:
            heapq.heappop(heap)

        if i >= k - 1:
            result.append(-heap[0][0])

    return result


if __name__ == "__main__":
    assert maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert maxSlidingWindow([1], 1) == [1]
    assert maxSlidingWindow([1, 3, -1, -3, 5], 5) == [5]
    assert maxSlidingWindow([4, 4, 4, 4], 2) == [4, 4, 4]
    assert maxSlidingWindow([5, 4, 3, 2, 1], 3) == [5, 4, 3]
    assert maxSlidingWindow([1, 2, 3, 4, 5], 3) == [3, 4, 5]
    assert maxSlidingWindow([7, 2, 4], 1) == [7, 2, 4]
    assert maxSlidingWindow([-4, -2, -5, -1, -3], 2) == [-2, -2, -1, -1]
    cases = [([1, 3, -1, -3, 5, 3, 6, 7], 3), ([1], 1), ([5, 4, 3, 2, 1], 3)]
    for nums, k in cases:
        assert maxSlidingWindow(nums, k) == maxSlidingWindow_heap(nums, k)
    print("All tests passed!")
