"""
Problem #33 — Search in Rotated Sorted Array
Difficulty: Medium
Topics: Binary Search, Array

Given rotated sorted array with distinct values and a target, return index or -1.
Must run in O(log n).

Approach: Modified Binary Search — determine which half is sorted,
then decide which half to search based on target's range.
"""

from typing import List


def search(nums: List[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2

        if nums[mid] == target:
            return mid

        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1


if __name__ == "__main__":
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search([1], 0) == -1
    assert search([4, 5, 6, 7, 0, 1, 2], 4) == 0
    assert search([4, 5, 6, 7, 0, 1, 2], 2) == 6
    assert search([1, 2, 3, 4, 5], 3) == 2
    assert search([3, 1], 1) == 1
    assert search([3, 1], 3) == 0
    assert search([3, 1], 2) == -1
    assert search([6, 7, 1, 2, 3, 4, 5], 1) == 2
    assert search([6, 7, 1, 2, 3, 4, 5], 6) == 0
    print("All assertions passed!")
