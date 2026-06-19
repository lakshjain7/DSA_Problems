"""
Problem Number: 153
Title: Find Minimum in Rotated Sorted Array
Difficulty: Medium
Topics: Array, Binary Search

Given sorted rotated array with unique elements, return the minimum in O(log n).

Approach: Modified Binary Search
Compare mid vs right: if nums[mid] > nums[right], min is in right half.
Otherwise min is at mid or left half.
"""

from typing import List


def findMin(nums: List[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid

    return nums[left]


if __name__ == "__main__":
    assert findMin([3, 4, 5, 1, 2]) == 1
    assert findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert findMin([11, 13, 15, 17]) == 11
    assert findMin([1]) == 1
    assert findMin([2, 1]) == 1
    assert findMin([1, 2]) == 1
    assert findMin([2, 3, 4, 5, 1]) == 1
    assert findMin([1, 2, 3, 4, 5]) == 1
    assert findMin([5, 6, 7, 1, 2, 3, 4]) == 1
    assert findMin([0, 1, 2, -4, -3, -2, -1]) == -4
    print("All tests passed!")
