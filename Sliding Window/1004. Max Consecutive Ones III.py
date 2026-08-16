"""
1004. Max Consecutive Ones III
Difficulty: Medium
Topics: Array, Binary Array, Sliding Window, Prefix Sum

Problem Statement
-----------------
Given a binary array nums and an integer k, return the maximum number of
consecutive 1's in the array if you can flip at most k 0's.

Examples
--------
Example 1:
    Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
    Output: 6
    Explanation: [1,1,1,0,0,1,1,1,1,1,1]
    Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Example 2:
    Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
    Output: 10
    Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
    Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.

Constraints
-----------
- 1 <= nums.length <= 10^5
- nums[i] is either 0 or 1.
- 0 <= k <= nums.length

Approach
--------
This asks for the longest subarray containing at most k zeros (each zero we
"keep" costs one flip). That is a classic variable-size sliding window.

Maintain a window [left, right]. Extend right one step at a time; if the new
element is 0, increment a zero counter. Whenever the window holds more than k
zeros, shrink from the left until the count is back to at most k, decrementing
the counter each time a 0 leaves the window. The window is always valid after
this adjustment, so its length right - left + 1 is a candidate answer; track
the maximum.

Why it works
------------
The window invariant is "at most k zeros inside." Growing the window can only
add zeros, and we only shrink exactly enough to restore the invariant, so we
never miss a longer valid window: for every right endpoint we keep the
smallest possible left, which maximises the length ending at that right.

Complexity
----------
Time:  O(n) - left and right each advance at most n times.
Space: O(1) - only a few counters.

Alternative Approach
--------------------
A "non-shrinking window" trick keeps the window size monotonically
non-decreasing: when a new zero pushes the zero-count over k, advance left by
exactly one (never shrinking below the best size found so far). The answer is
simply the final window size. It avoids the inner while loop and is a neat
O(n) one-pass variant, shown below as max_consecutive_ones_grow.
"""
from typing import List


def longest_ones(nums: List[int], k: int) -> int:
    """Shrinking sliding window: longest subarray with <= k zeros."""
    left = 0
    zeros = 0
    best = 0
    for right, val in enumerate(nums):
        if val == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def max_consecutive_ones_grow(nums: List[int], k: int) -> int:
    """Non-shrinking window variant; window size never decreases."""
    left = 0
    zeros = 0
    for right, val in enumerate(nums):
        if val == 0:
            zeros += 1
        if zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
    return len(nums) - left


if __name__ == "__main__":
    for fn in (longest_ones, max_consecutive_ones_grow):
        assert fn([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
        assert fn([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0,
                   1, 1, 1, 1], 3) == 10
        # k = 0: no flips, longest run of existing ones
        assert fn([1, 1, 0, 1, 1, 1], 0) == 3
        # All ones
        assert fn([1, 1, 1, 1], 2) == 4
        # All zeros, can flip all
        assert fn([0, 0, 0], 3) == 3
        # All zeros, flip some
        assert fn([0, 0, 0, 0], 2) == 2
        # Single element cases
        assert fn([0], 0) == 0
        assert fn([1], 0) == 1
        assert fn([0], 1) == 1
        # k larger than number of zeros -> whole array
        assert fn([1, 0, 1, 0, 1], 10) == 5

    print("All tests passed.")
