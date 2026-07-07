"""
34. Find First and Last Position of Element in Sorted Array
Difficulty: Medium
Topics: Array, Binary Search

Problem Statement:
Given an array of integers `nums` sorted in non-decreasing order, find the
starting and ending position of a given `target` value.

If `target` is not found in the array, return [-1, -1].

You must write an algorithm with O(log n) runtime complexity.

Examples:
    Input: nums = [5,7,7,8,8,10], target = 8
    Output: [3,4]

    Input: nums = [5,7,7,8,8,10], target = 6
    Output: [-1,-1]

    Input: nums = [], target = 0
    Output: [-1,-1]

Constraints:
    0 <= nums.length <= 10^5
    -10^9 <= nums[i] <= 10^9
    nums is a non-decreasing array.
    -10^9 <= target <= 10^9

Approach (Binary Search for Boundaries):
A plain binary search only finds *some* occurrence of the target, not
necessarily the first or last one. Instead we run two separate binary
searches:
  1. A "leftmost" search that keeps narrowing the search space toward the
     left whenever nums[mid] >= target, so it converges on the first index
     where target could appear.
  2. A "rightmost" search that keeps narrowing toward the right whenever
     nums[mid] <= target, so it converges on the first index *after* the
     last occurrence of target (an upper bound).

Both searches are O(log n) and run independently, giving O(log n) overall
(two passes of binary search is still O(log n) since constants are dropped).
After finding the lower bound, we verify the value at that index actually
equals target (handles the "not found" case); the upper bound minus one
then gives the last occurrence.

Complexity:
    Time:  O(log n) — two binary searches, each O(log n)
    Space: O(1) — only pointer variables used

Alternative Approach:
Use Python's bisect module (bisect_left / bisect_right), which implements
exactly this lower/upper bound binary search under the hood. This is
essentially the same algorithm, just using the standard library.
"""

from bisect import bisect_left, bisect_right
from typing import List


def search_range(nums: List[int], target: int) -> List[int]:
    def lower_bound(x: int) -> int:
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        return lo

    left = lower_bound(target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]

    right = lower_bound(target + 1) - 1
    return [left, right]


def search_range_bisect(nums: List[int], target: int) -> List[int]:
    """Alternative approach using the bisect standard library module."""
    left = bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect_right(nums, target) - 1
    return [left, right]


if __name__ == "__main__":
    for fn in (search_range, search_range_bisect):
        assert fn([5, 7, 7, 8, 8, 10], 8) == [3, 4]
        assert fn([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
        assert fn([], 0) == [-1, -1]
        assert fn([1], 1) == [0, 0]
        assert fn([1], 0) == [-1, -1]
        assert fn([2, 2], 2) == [0, 1]
        assert fn([1, 2, 3, 4, 5], 1) == [0, 0]
        assert fn([1, 2, 3, 4, 5], 5) == [4, 4]
        assert fn([1, 1, 1, 1, 1], 1) == [0, 4]

    print("All test cases passed!")
