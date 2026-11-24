"""
2104. Sum of Subarray Ranges
Difficulty: Medium
Topics: Array, Stack, Monotonic Stack

Problem:
You are given an integer array nums. The range of a subarray of nums is the
difference between the largest and smallest element in the subarray.
Return the sum of all subarray ranges of nums.
A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
    Input: nums = [1,2,3]
    Output: 4
    Explanation: [1]:0, [2]:0, [3]:0, [1,2]:1, [2,3]:1, [1,2,3]:2 -> 4

Example 2:
    Input: nums = [1,3,3]
    Output: 4

Example 3:
    Input: nums = [4,-2,-3,4,1]
    Output: 59

Constraints:
    1 <= nums.length <= 1000
    -10^9 <= nums[i] <= 10^9

Follow-up: Could you find a solution with O(n) time complexity?

Approach (Monotonic Stack - contribution technique):
    sum(max - min) over all subarrays = sum(max over subarrays) - sum(min over subarrays).
    For each index i, count how many subarrays have nums[i] as their maximum:
        left  = number of choices for the left boundary (distance to previous
                element that is strictly greater)
        right = number of choices for the right boundary (distance to next
                element that is greater-or-equal)
    nums[i] contributes nums[i] * left * right to the sum of maxima. The
    asymmetric strict / non-strict comparison guarantees each subarray with
    duplicate maxima is attributed to exactly one index. The same is done for
    minima with the comparisons flipped.
    A single pass of a monotonic stack computes both boundaries: when an
    element is popped, the element that pops it is its right boundary and the
    element beneath it in the stack is its left boundary.

Complexity:
    Time:  O(n) - each index is pushed and popped once per pass (two passes).
    Space: O(n) - the stack.

Alternative (Brute force expansion):
    Fix the left endpoint, extend right while tracking running min and max.
    Time O(n^2), Space O(1). Fine for n <= 1000.
"""
from typing import List, Callable


def _sum_of_extremes(nums: List[int], pop_cond: Callable[[int, int], bool]) -> int:
    """Sum of the extreme (max or min, decided by pop_cond) over all subarrays."""
    n = len(nums)
    total = 0
    stack: List[int] = []
    # Sentinel pass to i == n flushes the stack.
    for i in range(n + 1):
        while stack and (i == n or pop_cond(nums[stack[-1]], nums[i])):
            mid = stack.pop()
            left = mid - (stack[-1] if stack else -1)
            right = i - mid
            total += nums[mid] * left * right
        stack.append(i)
    return total


def subArrayRanges(nums: List[int]) -> int:
    # For max: pop while top <= current (current becomes the right boundary).
    sum_max = _sum_of_extremes(nums, lambda top, cur: top <= cur)
    # For min: pop while top >= current.
    sum_min = _sum_of_extremes(nums, lambda top, cur: top >= cur)
    return sum_max - sum_min


def subArrayRanges_brute(nums: List[int]) -> int:
    total = 0
    n = len(nums)
    for i in range(n):
        lo = hi = nums[i]
        for j in range(i, n):
            lo = min(lo, nums[j])
            hi = max(hi, nums[j])
            total += hi - lo
    return total


if __name__ == "__main__":
    import random

    assert subArrayRanges([1, 2, 3]) == 4
    assert subArrayRanges([1, 3, 3]) == 4
    assert subArrayRanges([4, -2, -3, 4, 1]) == 59
    assert subArrayRanges([5]) == 0
    assert subArrayRanges([7, 7, 7, 7]) == 0
    assert subArrayRanges([10**9, -10**9]) == 2 * 10**9

    for f in (subArrayRanges, subArrayRanges_brute):
        assert f([1, 2, 3]) == 4
        assert f([4, -2, -3, 4, 1]) == 59

    for _ in range(300):
        arr = [random.randint(-5, 5) for _ in range(random.randint(1, 30))]
        assert subArrayRanges(arr) == subArrayRanges_brute(arr), arr

    print("All tests passed!")
