"""
862. Shortest Subarray with Sum at Least K
Difficulty: Hard
Topics: Array, Binary Search, Queue, Sliding Window, Heap, Prefix Sum,
        Monotonic Queue

Problem:
Given an integer array nums and an integer k, return the length of the
shortest non-empty subarray of nums with a sum of at least k. If there is no
such subarray, return -1.
A subarray is a contiguous part of an array.

Example 1:
    Input: nums = [1], k = 1
    Output: 1
Example 2:
    Input: nums = [1,2], k = 4
    Output: -1
Example 3:
    Input: nums = [2,-1,2], k = 3
    Output: 3

Constraints:
    1 <= nums.length <= 10^5
    -10^5 <= nums[i] <= 10^5
    1 <= k <= 10^9

Approach (prefix sums + monotonic deque):
    Let P[i] be prefix sums. We want min (j - i) with P[j] - P[i] >= k, i < j.
    Because values can be negative, a plain two-pointer window fails. Keep a
    deque of indices with strictly increasing prefix sums:
      * While P[j] - P[deque[0]] >= k: record j - deque[0], pop front. Any later
        j' > j would give a longer length with that same start, so the front
        is never useful again.
      * While P[j] <= P[deque[-1]]: pop back. A later end that works with the
        popped index i would work at least as well with j (larger start index,
        smaller-or-equal prefix), so i is dominated.
      * Append j.

Complexity:
    Time:  O(n) - every index enters and leaves the deque at most once.
    Space: O(n) for the prefix sums and deque.
"""
from collections import deque
from typing import List
import heapq


class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)
        for i, x in enumerate(nums):
            P[i + 1] = P[i] + x
        best = n + 1
        dq: deque = deque()
        for j in range(n + 1):
            while dq and P[j] - P[dq[0]] >= k:
                best = min(best, j - dq.popleft())
            while dq and P[j] <= P[dq[-1]]:
                dq.pop()
            dq.append(j)
        return best if best <= n else -1

    # Alternative: min-heap of (prefix sum, index); pop while condition holds.
    def shortestSubarrayHeap(self, nums: List[int], k: int) -> int:
        best = len(nums) + 1
        heap = [(0, -1)]
        total = 0
        for j, x in enumerate(nums):
            total += x
            while heap and total - heap[0][0] >= k:
                _, i = heapq.heappop(heap)
                best = min(best, j - i)
            heapq.heappush(heap, (total, j))
        return best if best <= len(nums) else -1

    # Brute force O(n^2) for cross-checking.
    def shortestSubarrayBrute(self, nums: List[int], k: int) -> int:
        best = len(nums) + 1
        for i in range(len(nums)):
            t = 0
            for j in range(i, len(nums)):
                t += nums[j]
                if t >= k:
                    best = min(best, j - i + 1)
                    break
        return best if best <= len(nums) else -1


if __name__ == "__main__":
    import random
    s = Solution()
    cases = [
        ([1], 1, 1),
        ([1, 2], 4, -1),
        ([2, -1, 2], 3, 3),
        ([84, -37, 32, 40, 95], 167, 3),
        ([-1, -2, -3], 1, -1),
        ([5], 10, -1),
        ([1, 1, 1, 1], 4, 4),
        ([48, 99, 37, 4, -31], 140, 2),
        ([10, -5, 10], 10, 1),
    ]
    for nums, k, exp in cases:
        assert s.shortestSubarray(nums, k) == exp, (nums, k)
        assert s.shortestSubarrayHeap(nums, k) == exp, (nums, k)
        assert s.shortestSubarrayBrute(nums, k) == exp, (nums, k)
    random.seed(7)
    for _ in range(3000):
        a = [random.randint(-8, 8) for _ in range(random.randint(1, 10))]
        k = random.randint(1, 20)
        b = s.shortestSubarrayBrute(a, k)
        assert s.shortestSubarray(a, k) == b, (a, k)
        assert s.shortestSubarrayHeap(a, k) == b, (a, k)
    print("All tests passed")
