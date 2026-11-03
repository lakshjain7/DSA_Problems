"""
918. Maximum Sum Circular Subarray
Difficulty: Medium
Topics: Array, Divide and Conquer, Dynamic Programming, Queue, Monotonic Queue

Problem:
Given a circular integer array nums of length n, return the maximum possible
sum of a non-empty subarray of nums. A circular array means the end connects
to the beginning. A subarray may include each element at most once.

Example 1:
    Input: nums = [1,-2,3,-2]
    Output: 3
Example 2:
    Input: nums = [5,-3,5]
    Output: 10      (5 + 5 wrapping around)
Example 3:
    Input: nums = [-3,-2,-3]
    Output: -2

Constraints:
    n == nums.length
    1 <= n <= 3 * 10^4
    -3 * 10^4 <= nums[i] <= 3 * 10^4

Approach (Kadane twice):
    A best subarray is either non-wrapping (plain Kadane max) or wrapping. A
    wrapping subarray = total - (a contiguous middle block), so the best wrapping
    sum = total - minimum subarray sum (Kadane for min). Answer is
    max(maxKadane, total - minKadane). Edge case: if every element is negative,
    maxKadane < 0 and total - minKadane would be 0 (empty subarray), which is
    illegal, so return maxKadane.

Complexity:
    Time:  O(n)
    Space: O(1)

Alternative (prefix sums + monotonic deque):
    Double the array, prefix sums P; for each j find min P[i] for
    j - n < i < j with a sliding-window deque. O(n) time, O(n) space.
"""
from collections import deque
from typing import List


def max_subarray_sum_circular(nums: List[int]) -> int:
    total = 0
    cur_max = cur_min = 0
    best_max = nums[0]
    best_min = nums[0]
    for x in nums:
        total += x
        cur_max = max(cur_max + x, x)
        best_max = max(best_max, cur_max)
        cur_min = min(cur_min + x, x)
        best_min = min(best_min, cur_min)
    if best_max < 0:
        return best_max
    return max(best_max, total - best_min)


def max_subarray_sum_circular_deque(nums: List[int]) -> int:
    n = len(nums)
    prefix = [0] * (2 * n + 1)
    for i in range(2 * n):
        prefix[i + 1] = prefix[i] + nums[i % n]
    best = float("-inf")
    dq: deque = deque()  # indices with increasing prefix values
    for j in range(1, 2 * n + 1):
        while dq and prefix[dq[-1]] >= prefix[j - 1]:
            dq.pop()
        dq.append(j - 1)
        while dq[0] < j - n:
            dq.popleft()
        best = max(best, prefix[j] - prefix[dq[0]])
    return int(best)


if __name__ == "__main__":
    import random

    def brute(a: List[int]) -> int:
        n = len(a)
        return max(
            sum(a[(s + k) % n] for k in range(l))
            for s in range(n)
            for l in range(1, n + 1)
        )

    for fn in (max_subarray_sum_circular, max_subarray_sum_circular_deque):
        assert fn([1, -2, 3, -2]) == 3
        assert fn([5, -3, 5]) == 10
        assert fn([-3, -2, -3]) == -2
        assert fn([7]) == 7
        assert fn([-5]) == -5
        assert fn([3, -1, 2, -1]) == 4
        assert fn([3, -2, 2, -3]) == 3
        assert fn([0, 0, 0]) == 0
        random.seed(1)
        for _ in range(300):
            a = [random.randint(-10, 10) for _ in range(random.randint(1, 8))]
            assert fn(a) == brute(a), a
    print("All tests passed")
