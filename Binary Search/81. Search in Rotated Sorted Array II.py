"""
81. Search in Rotated Sorted Array II
Difficulty: Medium
Topics: Array, Binary Search

Problem:
There is an integer array nums sorted in non-decreasing order (not
necessarily distinct values). Before being passed to your function, nums is
rotated at an unknown pivot index. Given the rotated array nums and an
integer target, return true if target is in nums, or false otherwise.
Decrease the overall operation steps as much as possible.

Example 1:
    Input: nums = [2,5,6,0,0,1,2], target = 0
    Output: true
Example 2:
    Input: nums = [2,5,6,0,0,1,2], target = 3
    Output: false

Constraints:
    1 <= nums.length <= 5000
    -10^4 <= nums[i], target <= 10^4
    nums is guaranteed to be rotated at some pivot.

Approach:
Modified binary search. At each step at least one half [lo..mid] or
[mid..hi] is sorted. With duplicates, if nums[lo] == nums[mid] == nums[hi]
we cannot tell which half is sorted, so shrink both ends by one. Otherwise,
determine the sorted half and check whether target lies inside it.

Complexity:
    Time:  O(log n) average, O(n) worst case (all duplicates)
    Space: O(1)
"""
from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> bool:
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return True
            if nums[lo] == nums[mid] == nums[hi]:
                lo += 1
                hi -= 1
            elif nums[lo] <= nums[mid]:  # left half sorted
                if nums[lo] <= target < nums[mid]:
                    hi = mid - 1
                else:
                    lo = mid + 1
            else:  # right half sorted
                if nums[mid] < target <= nums[hi]:
                    lo = mid + 1
                else:
                    hi = mid - 1
        return False

    # Alternative: simple linear scan, O(n) always.
    def searchLinear(self, nums: List[int], target: int) -> bool:
        return target in nums


if __name__ == "__main__":
    import random
    s = Solution()
    assert s.search([2, 5, 6, 0, 0, 1, 2], 0) is True
    assert s.search([2, 5, 6, 0, 0, 1, 2], 3) is False
    assert s.search([1], 1) is True
    assert s.search([1], 0) is False
    assert s.search([1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 13) is True
    assert s.search([1, 0, 1, 1, 1], 0) is True
    assert s.search([3, 1], 1) is True
    assert s.search([1, 1, 1], 2) is False
    # randomized cross-check against linear scan
    random.seed(1)
    for _ in range(2000):
        n = random.randint(1, 12)
        arr = sorted(random.randint(0, 5) for _ in range(n))
        k = random.randint(0, n - 1)
        arr = arr[k:] + arr[:k]
        t = random.randint(-1, 6)
        assert s.search(arr, t) == s.searchLinear(arr, t), (arr, t)
    print("All tests passed.")
