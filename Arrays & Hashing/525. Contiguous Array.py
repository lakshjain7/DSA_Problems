"""
525. Contiguous Array
Difficulty: Medium
Topics: Array, Hash Table, Prefix Sum

Problem:
Given a binary array nums, return the maximum length of a contiguous subarray
with an equal number of 0 and 1.

Example 1:
    Input: nums = [0,1]
    Output: 2
Example 2:
    Input: nums = [0,1,0]
    Output: 2
Example 3:
    Input: nums = [0,1,1,1,1,1,0,0,0]
    Output: 6

Constraints:
    1 <= nums.length <= 10^5
    nums[i] is either 0 or 1.

Approach:
Treat 0 as -1 and 1 as +1. A subarray has equal 0s and 1s iff its sum is 0,
i.e. two prefix sums are equal. Store the first index at which each prefix
sum appears; when the same prefix sum reappears at index i, the subarray
between has sum 0 and length i - first[prefix].

Complexity: Time O(n), Space O(n).
"""
from typing import List


def findMaxLength(nums: List[int]) -> int:
    first = {0: -1}
    prefix = best = 0
    for i, x in enumerate(nums):
        prefix += 1 if x else -1
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best


def findMaxLengthArray(nums: List[int]) -> int:
    """Alternative: array of size 2n+1 instead of a dict (offset by n)."""
    n = len(nums)
    first = [None] * (2 * n + 1)
    first[n] = -1
    prefix, best = n, 0
    for i, x in enumerate(nums):
        prefix += 1 if x else -1
        if first[prefix] is None:
            first[prefix] = i
        else:
            best = max(best, i - first[prefix])
    return best


def _brute(nums):
    best = 0
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += 1 if nums[j] else -1
            if s == 0:
                best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    import random
    for f in (findMaxLength, findMaxLengthArray):
        assert f([0, 1]) == 2
        assert f([0, 1, 0]) == 2
        assert f([0, 1, 1, 1, 1, 1, 0, 0, 0]) == 6
        assert f([0]) == 0
        assert f([1, 1, 1]) == 0
        assert f([0, 0, 1, 1]) == 4
        for _ in range(300):
            a = [random.randint(0, 1) for _ in range(random.randint(1, 14))]
            assert f(a) == _brute(a), a
    print("All tests passed")
