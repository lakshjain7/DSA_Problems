"""
Problem 300: Longest Increasing Subsequence
Difficulty: Medium
Topics: Dynamic Programming, Binary Search

O(n log n) patience sorting approach: maintain `tails` array where tails[i]
is the smallest tail of all LIS of length i+1. Binary search to update.
Complexity: O(n log n) time, O(n) space.
"""

import bisect
from typing import List


def length_of_lis(nums: List[int]) -> int:
    tails: List[int] = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


def length_of_lis_dp(nums: List[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


if __name__ == "__main__":
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7, 7, 7, 7]) == 1
    assert length_of_lis([1]) == 1
    assert length_of_lis([1, 2]) == 2
    assert length_of_lis([2, 1]) == 1
    assert length_of_lis([1, 3, 6, 7, 9, 4, 10, 5, 6]) == 6
    assert length_of_lis([-3, -2, -1, 0]) == 4
    test_cases = [[10, 9, 2, 5, 3, 7, 101, 18],[0, 1, 0, 3, 2, 3],[7, 7, 7, 7],[1, 3, 6, 7, 9, 4, 10, 5, 6]]
    for tc in test_cases:
        assert length_of_lis(tc) == length_of_lis_dp(tc)
    print("All tests passed for 300. Longest Increasing Subsequence")
