"""
162. Find Peak Element
Difficulty: Medium
Topics: Array, Binary Search

Problem Statement
-----------------
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array `nums`, find a peak element, and return its
index. If the array contains multiple peaks, return the index to any of the
peaks.

You may imagine that `nums[-1] = nums[n] = -infinity`. In other words, an element
is always considered to be strictly greater than a neighbor that is outside the
array.

You must write an algorithm that runs in O(log n) time.

Examples
--------
Example 1:
    Input:  nums = [1, 2, 3, 1]
    Output: 2
    Explanation: 3 is a peak element and your function should return index 2.

Example 2:
    Input:  nums = [1, 2, 1, 3, 5, 6, 4]
    Output: 5 (or 1)
    Explanation: Your function can return either index 1 (peak 2) or index 5
                 (peak 6).

Constraints
-----------
  - 1 <= nums.length <= 1000
  - -2^31 <= nums[i] <= 2^31 - 1
  - nums[i] != nums[i + 1] for all valid i.

Approach
--------
The O(log n) requirement rules out a linear scan and points to binary search —
even though the array is not sorted. The key insight is that we can binary search
on the *slope*.

At any middle index `mid`, compare nums[mid] with nums[mid + 1]:

  - If nums[mid] < nums[mid + 1], we are on an ascending slope. A peak must exist
    somewhere to the right, because the sequence rises here and is bounded above
    by nums[n] = -infinity at the far edge, so it must eventually come back down
    (or stay rising to the last element, which is itself a peak). Move left = mid + 1.

  - If nums[mid] > nums[mid + 1], we are on a descending slope. By symmetric
    reasoning a peak exists at mid or to its left. Move right = mid.

Because adjacent elements are never equal, one of the two branches always applies.
The search space halves each step and converges to an index where the "go right"
condition fails and the "go left" condition holds — precisely a peak. We never
read out of bounds because we only compare mid with mid + 1 while left < right,
guaranteeing mid + 1 <= right is valid.

Complexity
----------
Time:  O(log n) — the interval [left, right] halves each iteration.
Space: O(1).
"""

from typing import List


def findPeakElement(nums: List[int]) -> int:
    """Return the index of any peak element in O(log n) time."""
    left, right = 0, len(nums) - 1

    while left < right:
        mid = (left + right) // 2
        if nums[mid] < nums[mid + 1]:
            # Ascending slope: a peak lies strictly to the right.
            left = mid + 1
        else:
            # Descending slope (or plateau impossible): peak at mid or left of it.
            right = mid

    return left


def findPeakElement_linear(nums: List[int]) -> int:
    """
    Alternative O(n) reference implementation used only for cross-checking.
    The first index where the value stops increasing is a peak.
    """
    n = len(nums)
    for i in range(n):
        left_ok = i == 0 or nums[i - 1] < nums[i]
        right_ok = i == n - 1 or nums[i] > nums[i + 1]
        if left_ok and right_ok:
            return i
    return -1  # Unreachable given the constraints.


def _is_peak(nums: List[int], idx: int) -> bool:
    """Helper: verify that idx is a valid peak (uses -inf boundaries)."""
    n = len(nums)
    left = float("-inf") if idx == 0 else nums[idx - 1]
    right = float("-inf") if idx == n - 1 else nums[idx + 1]
    return nums[idx] > left and nums[idx] > right


if __name__ == "__main__":
    # Example cases (any valid peak index is acceptable, so validate structurally).
    assert findPeakElement([1, 2, 3, 1]) == 2
    idx = findPeakElement([1, 2, 1, 3, 5, 6, 4])
    assert idx in (1, 5)

    # Edge: single element is always a peak.
    assert findPeakElement([42]) == 0

    # Edge: two elements, ascending -> last is the peak.
    assert findPeakElement([1, 2]) == 1

    # Edge: two elements, descending -> first is the peak.
    assert findPeakElement([2, 1]) == 0

    # Edge: strictly increasing -> last element is the peak.
    assert findPeakElement([1, 2, 3, 4, 5]) == 4

    # Edge: strictly decreasing -> first element is the peak.
    assert findPeakElement([5, 4, 3, 2, 1]) == 0

    # Randomised structural check: result must be a genuine peak and match a
    # known-correct linear scan's validity.
    import random

    random.seed(7)
    for _ in range(2000):
        n = random.randint(1, 30)
        arr: List[int] = []
        prev = None
        for _ in range(n):
            # Ensure no two adjacent values are equal (per constraints).
            val = random.randint(-10, 10)
            while prev is not None and val == prev:
                val = random.randint(-10, 10)
            arr.append(val)
            prev = val
        peak = findPeakElement(arr)
        assert _is_peak(arr, peak), (arr, peak)
        assert _is_peak(arr, findPeakElement_linear(arr)), arr

    print("All tests passed for 162. Find Peak Element")
