"""
1027. Longest Arithmetic Subsequence
Difficulty: Medium
Topics: Array, Hash Table, Binary Search, Dynamic Programming

Problem:
Given an array nums of integers, return the length of the longest arithmetic
subsequence in nums. A sequence seq is arithmetic if seq[i+1] - seq[i] are all
the same value (for 0 <= i < seq.length - 1). A subsequence keeps relative order
but may skip elements.

Example 1:
    Input: nums = [3,6,9,12]        Output: 4
Example 2:
    Input: nums = [9,4,7,2,10]      Output: 3   ([4,7,10])
Example 3:
    Input: nums = [20,1,15,3,10,5,8]  Output: 4  ([20,15,10,5])

Constraints:
- 2 <= nums.length <= 1000
- 0 <= nums[i] <= 500

Approach (DP keyed by difference):
dp[j][d] = length of the longest arithmetic subsequence ending at index j with
common difference d. For each pair i < j, d = nums[j] - nums[i], then
dp[j][d] = dp[i].get(d, 1) + 1. Every pair extends the best chain ending at i
with the same difference, or starts a new length-2 chain.

Complexity:
- Time: O(n^2)
- Space: O(n^2) worst case for the per-index dictionaries

Alternative: brute force over (first element, difference) pairs and greedy
extension using a value->indices map; slower in general, used here as a checker.
"""
from typing import List
import random


def longestArithSeqLength(nums: List[int]) -> int:
    n = len(nums)
    dp = [dict() for _ in range(n)]
    best = 2
    for j in range(n):
        for i in range(j):
            d = nums[j] - nums[i]
            dp[j][d] = dp[i].get(d, 1) + 1
            if dp[j][d] > best:
                best = dp[j][d]
    return best


def bruteForce(nums: List[int]) -> int:
    """Exponential-ish reference: try each start pair and extend greedily (earliest)."""
    n = len(nums)
    best = min(n, 2)
    for i in range(n):
        for j in range(i + 1, n):
            d = nums[j] - nums[i]
            length, last = 2, nums[j]
            for k in range(j + 1, n):
                if nums[k] - last == d:
                    length += 1
                    last = nums[k]
            best = max(best, length)
    return best


if __name__ == "__main__":
    assert longestArithSeqLength([3, 6, 9, 12]) == 4
    assert longestArithSeqLength([9, 4, 7, 2, 10]) == 3
    assert longestArithSeqLength([20, 1, 15, 3, 10, 5, 8]) == 4
    assert longestArithSeqLength([1, 1]) == 2
    assert longestArithSeqLength([5, 5, 5, 5]) == 4
    assert longestArithSeqLength([0, 500]) == 2
    random.seed(1)
    for _ in range(300):
        arr = [random.randint(0, 20) for _ in range(random.randint(2, 12))]
        assert longestArithSeqLength(arr) == bruteForce(arr), arr
    print("All tests passed.")
