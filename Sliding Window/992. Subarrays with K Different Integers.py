"""
992. Subarrays with K Different Integers
Difficulty: Hard
Topics: Array, Hash Table, Sliding Window, Counting

Problem Statement
-----------------
Given an integer array `nums` and an integer `k`, return the number of good
subarrays of `nums`.

A good array is an array where the number of DIFFERENT integers in that array is
exactly `k`.

    For example, [1, 2, 3, 1, 2] has 3 different integers: 1, 2, and 3.

A subarray is a contiguous part of an array.

Examples
--------
Example 1:
    Input:  nums = [1, 2, 1, 2, 3], k = 2
    Output: 7
    Explanation: Subarrays with exactly 2 different integers:
        [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2].

Example 2:
    Input:  nums = [1, 2, 1, 3, 4], k = 3
    Output: 3
    Explanation: [1,2,1,3], [2,1,3], [1,3,4].

Constraints
-----------
    1 <= nums.length <= 2 * 10^4
    1 <= nums[i], k <= nums.length

Approach (Sliding Window, "atMost" trick)
-----------------------------------------
Counting subarrays with EXACTLY k distinct integers directly is awkward, because
a single window's validity is not monotonic as we extend it. The standard trick
converts the problem into two monotonic ones:

    exactly(k) = atMost(k) - atMost(k - 1)

`atMost(k)` counts subarrays containing at most k distinct integers. This IS
solvable with a classic variable-size sliding window: expand `right`, and while
the window holds more than k distinct values, shrink from `left`. For each
`right`, every subarray ending at `right` and starting anywhere in
[left, right] is valid, contributing (right - left + 1) to the total.

Subtracting atMost(k - 1) removes the subarrays with at most k - 1 distinct
values, leaving precisely those with exactly k.

Why it works: the set of subarrays with at most k-1 distinct integers is a subset
of those with at most k distinct integers. Their difference is exactly the
subarrays whose distinct count is k. atMost is correct because the "at most"
constraint is monotone: if a window is valid, every subarray inside it is too,
so summing window widths counts each qualifying subarray once by its right end.

Complexity
----------
Time:  O(n) - each of the two atMost passes moves left and right pointers at most
       n times, so O(n) total; overall O(n).
Space: O(k) for the hash map of counts within the window (O(n) worst case).

Alternative Approach (Two windows, single pass)
-----------------------------------------------
Slide two windows simultaneously over the same right end using two independent
count maps: one keeping at most k distinct (left bound l1) and one keeping at
most k - 1 distinct (left bound l2). Since l2 >= l1, the number of subarrays
ending at `right` with EXACTLY k distinct integers is (l2 - l1). Summing over all
right ends gives the answer in a single pass, folding the atMost subtraction into
one loop.
"""

from typing import List
from collections import defaultdict


def subarraysWithKDistinct(nums: List[int], k: int) -> int:
    """Sliding window using exactly(k) = atMost(k) - atMost(k - 1)."""

    def at_most(m: int) -> int:
        if m < 0:
            return 0
        count = defaultdict(int)
        left = 0
        distinct = 0
        total = 0
        for right, val in enumerate(nums):
            if count[val] == 0:
                distinct += 1
            count[val] += 1
            while distinct > m:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    distinct -= 1
                left += 1
            total += right - left + 1
        return total

    return at_most(k) - at_most(k - 1)


def subarraysWithKDistinct_twowindows(nums: List[int], k: int) -> int:
    """Single-pass alternative sliding two windows with separate count maps."""
    c1 = defaultdict(int)  # window with at most k distinct
    c2 = defaultdict(int)  # window with at most k - 1 distinct
    l1 = l2 = 0
    d1 = d2 = 0
    res = 0
    for right, val in enumerate(nums):
        if c1[val] == 0:
            d1 += 1
        c1[val] += 1
        while d1 > k:
            c1[nums[l1]] -= 1
            if c1[nums[l1]] == 0:
                d1 -= 1
            l1 += 1

        if c2[val] == 0:
            d2 += 1
        c2[val] += 1
        while d2 > k - 1:
            c2[nums[l2]] -= 1
            if c2[nums[l2]] == 0:
                d2 -= 1
            l2 += 1

        # Subarrays ending at `right` with exactly k distinct = l2 - l1.
        res += l2 - l1
    return res


def _brute(nums: List[int], k: int) -> int:
    """O(n^2) reference for validation."""
    n = len(nums)
    total = 0
    for i in range(n):
        seen = set()
        for j in range(i, n):
            seen.add(nums[j])
            if len(seen) == k:
                total += 1
            elif len(seen) > k:
                break
    return total


if __name__ == "__main__":
    # Provided examples
    assert subarraysWithKDistinct([1, 2, 1, 2, 3], 2) == 7
    assert subarraysWithKDistinct([1, 2, 1, 3, 4], 3) == 3

    # k = 1 -> count runs of equal elements
    assert subarraysWithKDistinct([1, 1, 1], 1) == 6   # 3+2+1
    assert subarraysWithKDistinct([1, 2, 3], 1) == 3

    # k larger than distinct count -> 0
    assert subarraysWithKDistinct([1, 2], 3) == 0

    # Single element
    assert subarraysWithKDistinct([5], 1) == 1
    assert subarraysWithKDistinct([5], 2) == 0

    # Whole array is the only good subarray
    assert subarraysWithKDistinct([1, 2, 3, 4], 4) == 1

    # Cross-check both solutions against brute force on varied inputs
    import random
    random.seed(7)
    for _ in range(300):
        n = random.randint(1, 12)
        arr = [random.randint(1, 4) for _ in range(n)]
        kk = random.randint(1, 4)
        expected = _brute(arr, kk)
        assert subarraysWithKDistinct(arr, kk) == expected, (arr, kk)
        assert subarraysWithKDistinct_twowindows(arr, kk) == expected, (arr, kk)

    print("All tests passed for 992. Subarrays with K Different Integers")
