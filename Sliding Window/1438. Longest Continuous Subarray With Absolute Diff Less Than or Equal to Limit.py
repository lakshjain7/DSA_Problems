"""
1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
Difficulty: Medium
Topics: Array, Queue, Sliding Window, Heap, Monotonic Queue

Problem:
    Given an array of integers nums and an integer limit, return the size of the
    longest non-empty subarray such that the absolute difference between any two
    elements of this subarray is less than or equal to limit.

Examples:
    Input: nums = [8,2,4,7], limit = 4      Output: 2
    Input: nums = [10,1,2,4,7,2], limit = 5 Output: 4
    Input: nums = [4,2,2,2,4,4,2,2], limit = 0 Output: 3

Constraints:
    1 <= nums.length <= 10^5
    1 <= nums[i] <= 10^9
    0 <= limit <= 10^9

Approach:
    Any two elements differ by at most (max - min) of the window, so a window is
    valid iff max - min <= limit. Use a variable-size sliding window and keep the
    window max and min in O(1) amortized using two monotonic deques (decreasing
    for max, increasing for min). Expand right; while invalid, shrink left and pop
    deque fronts whose index left the window. Validity is monotone (shrinking a
    window never breaks it), so two pointers are correct.

Complexity:
    Time: O(n) - each index enters and leaves each deque once.
    Space: O(n) worst case for the deques.
"""
from collections import deque
from typing import List
import heapq


def longestSubarray(nums: List[int], limit: int) -> int:
    maxq, minq = deque(), deque()  # store indices
    left = best = 0
    for right, x in enumerate(nums):
        while maxq and nums[maxq[-1]] <= x:
            maxq.pop()
        maxq.append(right)
        while minq and nums[minq[-1]] >= x:
            minq.pop()
        minq.append(right)
        while nums[maxq[0]] - nums[minq[0]] > limit:
            left += 1
            if maxq[0] < left:
                maxq.popleft()
            if minq[0] < left:
                minq.popleft()
        best = max(best, right - left + 1)
    return best


def longestSubarrayHeaps(nums: List[int], limit: int) -> int:
    """Alternative: two heaps with lazy deletion. O(n log n) time, O(n) space."""
    maxh, minh = [], []
    left = best = 0
    for right, x in enumerate(nums):
        heapq.heappush(maxh, (-x, right))
        heapq.heappush(minh, (x, right))
        while -maxh[0][0] - minh[0][0] > limit:
            left = min(maxh[0][1], minh[0][1]) + 1
            while maxh[0][1] < left:
                heapq.heappop(maxh)
            while minh[0][1] < left:
                heapq.heappop(minh)
        best = max(best, right - left + 1)
    return best


def _brute(nums, limit):
    best = 0
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i, len(nums)):
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            if hi - lo > limit:
                break
            best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    import random
    for f in (longestSubarray, longestSubarrayHeaps):
        assert f([8, 2, 4, 7], 4) == 2
        assert f([10, 1, 2, 4, 7, 2], 5) == 4
        assert f([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3
        assert f([1], 0) == 1
        assert f([5, 5, 5], 0) == 3
        assert f([1, 100], 1000) == 2
        assert f([1, 100], 5) == 1
    random.seed(1)
    for _ in range(300):
        a = [random.randint(1, 20) for _ in range(random.randint(1, 15))]
        l = random.randint(0, 10)
        e = _brute(a, l)
        assert longestSubarray(a, l) == e and longestSubarrayHeaps(a, l) == e
    print("All tests passed.")
