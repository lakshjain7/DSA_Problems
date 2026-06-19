"""
Problem 4: Median of Two Sorted Arrays
Difficulty: Hard
Topics: Array, Binary Search, Divide and Conquer

Given two sorted arrays nums1 and nums2, return the median. O(log(m+n)) required.

Approach: Binary Search on the smaller array.
Find partition i in nums1 and j = half_len - i in nums2 such that
nums1[i-1] <= nums2[j] and nums2[j-1] <= nums1[i].
"""

from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2
        j = half_len - i

        nums1_left  = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i]     if i < m else float('inf')
        nums2_left  = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j]     if j < n else float('inf')

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if (m + n) % 2 == 1:
                return float(max(nums1_left, nums2_left))
            else:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
        elif nums1_left > nums2_right:
            hi = i - 1
        else:
            lo = i + 1

    raise ValueError("Input arrays are not sorted")


if __name__ == "__main__":
    assert findMedianSortedArrays([1, 3], [2]) == 2.0
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5
    assert findMedianSortedArrays([], [1]) == 1.0
    assert findMedianSortedArrays([2], []) == 2.0
    assert findMedianSortedArrays([1, 3, 5], [2, 4, 6]) == 3.5
    assert findMedianSortedArrays([1, 1], [1, 1]) == 1.0
    assert findMedianSortedArrays([-5, -3, -1], [-4, -2, 0]) == -2.5
    assert findMedianSortedArrays([1], [2]) == 1.5
    print("All tests passed!")
