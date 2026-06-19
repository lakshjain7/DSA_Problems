"""
Problem 4: Median of Two Sorted Arrays
Difficulty: Hard
Topics: Array, Binary Search, Divide and Conquer

Problem Statement:
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the
median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Examples:
    Example 1:
        Input: nums1 = [1,3], nums2 = [2]
        Output: 2.00000
        Explanation: merged array = [1,2,3] and median is 2.

    Example 2:
        Input: nums1 = [1,2], nums2 = [3,4]
        Output: 2.50000
        Explanation: merged array = [1,2,3,4] and median is (2+3)/2 = 2.5.

Constraints:
    - nums1.length == m
    - nums2.length == n
    - 0 <= m <= 1000
    - 0 <= n <= 1000
    - 1 <= m + n <= 2000
    - -10^6 <= nums1[i], nums2[i] <= 10^6

Approach (Binary Search on the smaller array):
    We need to find a partition of both arrays such that:
    - The left half contains (m + n + 1) // 2 elements total.
    - Every element on the left is <= every element on the right.

    Binary search on the partition index `i` in nums1 (the smaller array, for
    O(log(min(m,n))) complexity). The corresponding partition in nums2 is:
        j = half_len - i

    At each step check:
        nums1[i-1] <= nums2[j]  AND  nums2[j-1] <= nums1[i]

    If not, adjust the binary search boundary. Use -inf/+inf as sentinels at edges.

    When the correct partition is found:
    - If total length is odd: median = max(left_max1, left_max2)
    - If total length is even: median = (max(left halves) + min(right halves)) / 2

    Key insight: we're not merging arrays -- we're binary-searching for where to
    "cut" both arrays so that all elements left of the cut are <= all elements right.

Complexity:
    Time:  O(log(min(m, n))) -- binary search on the smaller array
    Space: O(1)
"""

from typing import List


def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    # Ensure nums1 is the smaller array for O(log min(m,n))
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half_len = (m + n + 1) // 2

    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2   # partition in nums1
        j = half_len - i     # partition in nums2

        # Sentinels for boundary conditions
        nums1_left  = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i]     if i < m else float('inf')
        nums2_left  = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j]     if j < n else float('inf')

        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Found the correct partition
            if (m + n) % 2 == 1:
                return float(max(nums1_left, nums2_left))
            else:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
        elif nums1_left > nums2_right:
            # nums1's left side is too large, move partition left
            hi = i - 1
        else:
            # nums2's left side is too large, move partition right
            lo = i + 1

    raise ValueError("Input arrays are not sorted")


# Alternative Approach: Merge and find median -- O((m+n) log(m+n)) or O(m+n), simpler but doesn't meet constraint
def findMedianSortedArrays_naive(nums1: List[int], nums2: List[int]) -> float:
    """
    Merge both arrays and find median. O(m+n) time, O(m+n) space.
    Does NOT meet the O(log(m+n)) constraint but useful for verification.
    """
    merged = sorted(nums1 + nums2)
    total = len(merged)
    mid = total // 2
    if total % 2 == 0:
        return (merged[mid - 1] + merged[mid]) / 2.0
    return float(merged[mid])


if __name__ == "__main__":
    # Basic cases
    assert findMedianSortedArrays([1, 3], [2]) == 2.0
    assert findMedianSortedArrays([1, 2], [3, 4]) == 2.5

    # One empty array
    assert findMedianSortedArrays([], [1]) == 1.0
    assert findMedianSortedArrays([2], []) == 2.0
    assert findMedianSortedArrays([], [1, 2, 3, 4]) == 2.5

    # Arrays of different lengths
    assert findMedianSortedArrays([1, 3, 5], [2, 4, 6]) == 3.5
    assert findMedianSortedArrays([1, 2, 3], [4, 5, 6, 7, 8]) == 4.5

    # Identical elements
    assert findMedianSortedArrays([1, 1], [1, 1]) == 1.0

    # Negative numbers
    assert findMedianSortedArrays([-5, -3, -1], [-4, -2, 0]) == -2.5

    # One element each, even total
    assert findMedianSortedArrays([1], [2]) == 1.5

    # Large value spread
    assert findMedianSortedArrays([0, 0], [0, 0]) == 0.0
    assert findMedianSortedArrays([1, 2], [1, 2, 3]) == 2.0

    # Verify against naive solution
    import random
    random.seed(42)
    for _ in range(100):
        a = sorted(random.randint(-100, 100) for _ in range(random.randint(0, 10)))
        b = sorted(random.randint(-100, 100) for _ in range(random.randint(1, 10)))
        expected = findMedianSortedArrays_naive(a, b)
        result = findMedianSortedArrays(a, b)
        assert abs(result - expected) < 1e-9, f"Mismatch: {a}, {b} -> got {result}, expected {expected}"

    print("All tests passed!")
