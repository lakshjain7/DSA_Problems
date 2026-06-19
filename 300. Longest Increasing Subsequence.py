"""
Problem 300: Longest Increasing Subsequence
Difficulty: Medium
Topics: Dynamic Programming, Binary Search

Problem Statement:
Given an integer array nums, return the length of the longest strictly increasing subsequence.

Examples:
    Input: nums = [10,9,2,5,3,7,101,18]
    Output: 4
    Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

    Input: nums = [0,1,0,3,2,3]
    Output: 4

    Input: nums = [7,7,7,7,7,7,7]
    Output: 1

Constraints:
    - 1 <= nums.length <= 2500
    - -10^4 <= nums[i] <= 10^4

Approach (O(n log n) - Patience Sorting / Binary Search):
    Maintain a `tails` array where tails[i] is the smallest tail element of all
    increasing subsequences of length i+1.

    For each number x:
    - If x > tails[-1], it extends the longest subsequence → append.
    - Otherwise, binary search for the leftmost tail >= x and replace it with x.
      This keeps tails as small as possible, maximizing future extension potential.

    The length of `tails` at the end equals the LIS length.
    Note: `tails` itself is NOT necessarily a valid subsequence — it's a bookkeeping
    structure for computing the length.

Complexity:
    Time:  O(n log n) — n elements, each with a binary search over tails
    Space: O(n) — tails array at most length n
"""

import bisect
from typing import List


def length_of_lis(nums: List[int]) -> int:
    """O(n log n) patience-sort approach using binary search."""
    tails: List[int] = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


# Alternative Approach (O(n^2) DP):
# dp[i] = length of LIS ending at index i.
# dp[i] = 1 + max(dp[j] for j < i if nums[j] < nums[i]), else 1.
# Answer = max(dp).
# Simple to understand but too slow for n=2500 in tight contest settings.

def length_of_lis_dp(nums: List[int]) -> int:
    """O(n^2) classic DP approach."""
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


if __name__ == "__main__":
    # Basic examples
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7, 7, 7, 7]) == 1

    # Edge cases
    assert length_of_lis([1]) == 1
    assert length_of_lis([1, 2]) == 2
    assert length_of_lis([2, 1]) == 1
    assert length_of_lis([1, 3, 6, 7, 9, 4, 10, 5, 6]) == 6  # [1,3,6,7,9,10]
    assert length_of_lis([-3, -2, -1, 0]) == 4  # all increasing, negatives

    # Verify both approaches agree
    test_cases = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 3, 2, 3],
        [7, 7, 7, 7],
        [1, 3, 6, 7, 9, 4, 10, 5, 6],
    ]
    for tc in test_cases:
        assert length_of_lis(tc) == length_of_lis_dp(tc), f"Mismatch on {tc}"

    print("All tests passed for 300. Longest Increasing Subsequence")
