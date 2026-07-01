"""
154. Find Minimum in Rotated Sorted Array II
Difficulty: Hard
Topics: Array, Binary Search

Problem Statement:
Suppose an array of length n sorted in ascending order is rotated between
1 and n times. For example, the array nums = [0,1,4,4,5,6,7] might become:
    [4,5,6,7,0,1,4]  if it was rotated 4 times.
    [0,1,4,4,5,6,7]  if it was rotated 7 times.
Notice that rotating an array [a[0], a[1], ..., a[n-1]] 1 time results in
the array [a[n-1], a[0], a[1], ..., a[n-2]].

Given the sorted rotated array `nums` that may contain duplicates, return
the minimum element of this array.

You must decrease the overall operation steps as much as possible.

Examples:
    Input: nums = [1,3,5]
    Output: 1

    Input: nums = [2,2,2,0,1]
    Output: 0

Constraints:
    n == nums.length
    1 <= n <= 5000
    -5000 <= nums[i] <= 5000
    nums is sorted and rotated between 1 and n times.

Approach (Binary search with duplicate tie-breaking):
This is the follow-up to "Find Minimum in Rotated Sorted Array" (#153)
where duplicates are allowed, which breaks the simple invariant used
there. We still binary search with `left`/`right` pointers and compare
nums[mid] to nums[right]:
  - If nums[mid] > nums[right]: the minimum must be strictly to the right
    of mid (mid itself cannot be the minimum, and the rotation point lies
    in (mid, right]), so set left = mid + 1.
  - If nums[mid] < nums[right]: the minimum is at mid or to its left
    (nums[right] cannot be the minimum since something smaller exists at
    or before mid), so set right = mid.
  - If nums[mid] == nums[right]: we cannot determine which half holds the
    minimum (e.g. [3,1,3,3,3] vs [3,3,3,1,3] look identical from the
    comparison of mid/right alone), so we can only safely shrink the
    search space by discarding the duplicate at `right` -- right -= 1.
    This is always safe because nums[mid] == nums[right] guarantees that
    nums[right] has at least one other equal (or smaller) representative
    still in range at index mid, so we never lose the true minimum.
The loop terminates when left == right, at which point nums[left] is the
minimum.

Complexity Analysis:
    Time:  O(log n) average case. O(n) worst case when the array is full
    of duplicates (e.g. [3,3,3,...,3,1,3,3,...,3]), since the
    nums[mid] == nums[right] branch can degrade to a linear scan. This
    worst case is unavoidable in general -- it is proven that no
    comparison-based algorithm can guarantee better than O(n) when
    duplicates are allowed, because e.g. [1,1,1,1,1] and [1,1,0,1,1]
    cannot always be distinguished without inspecting up to O(n) elements.
    Space: O(1) -- only pointers are used (iterative implementation).

Alternative Approach (Linear scan):
Simply scan the array once and track the minimum seen so far. This is
O(n) time, O(1) space -- asymptotically no worse than the binary search's
worst case, but it forgoes the average-case O(log n) speedup that binary
search provides on inputs with few duplicates. It's included both as a
brute-force baseline and as a way to cross-check correctness against the
binary search solution in the tests below.
"""

from typing import List


def find_min(nums: List[int]) -> int:
    """Return the minimum element of a rotated sorted array with duplicates.

    Binary search with O(log n) average / O(n) worst case (duplicates).
    """
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            # nums[mid] == nums[right]: can't tell which side has the min,
            # but it's safe to drop the duplicate at `right`.
            right -= 1

    return nums[left]


def find_min_linear(nums: List[int]) -> int:
    """Alternative brute-force O(n) linear scan."""
    return min(nums)


if __name__ == "__main__":
    for solve in (find_min, find_min_linear):
        # Example 1: no actual rotation effect visible (rotated n times)
        assert solve([1, 3, 5]) == 1
        # Example 2: duplicates around the rotation point
        assert solve([2, 2, 2, 0, 1]) == 0
        # Single element
        assert solve([1]) == 1
        # Two elements, rotated
        assert solve([2, 1]) == 1
        # Two elements, not rotated (or rotated n times)
        assert solve([1, 2]) == 1
        # All identical elements
        assert solve([3, 3, 3, 3, 3]) == 3
        # Minimum at the very start (fully "rotated back")
        assert solve([0, 1, 2, 4, 4, 4]) == 0
        # Minimum somewhere in the middle with duplicates on both sides
        assert solve([4, 4, 4, 0, 4, 4, 4]) == 0
        # Classic tricky duplicate case
        assert solve([3, 1, 3, 3, 3]) == 1
        assert solve([3, 3, 3, 1, 3]) == 1
        # Larger rotated array
        assert solve([4, 5, 6, 7, 0, 1, 4]) == 0

    print("All tests passed.")
