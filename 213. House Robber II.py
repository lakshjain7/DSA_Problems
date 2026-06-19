"""
Problem #213 — House Robber II
Difficulty : Medium
Topics     : Dynamic Programming, Arrays

─────────────────────────────────────────────────────────────────────────────
PROBLEM STATEMENT
─────────────────────────────────────────────────────────────────────────────
You are a professional robber planning to rob houses along a street. Each
house has a certain amount of money stashed. All houses are arranged in a
circle (the first house is the neighbour of the last one). Adjacent houses
have security systems connected, and if two adjacent houses were broken into
on the same night, the police will automatically be contacted.

Given an integer array nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the
police.

Examples:
  Input : nums = [2,3,2]        Output: 3
  Input : nums = [1,2,3,1]      Output: 4
  Input : nums = [1,2,3]        Output: 3

Constraints:
  1 <= nums.length <= 100
  0 <= nums[i] <= 1000

─────────────────────────────────────────────────────────────────────────────
APPROACH
─────────────────────────────────────────────────────────────────────────────
The circular constraint means we cannot rob BOTH house 0 and house n-1.
We break this into two independent linear House-Robber sub-problems:
  • Option A: rob houses 0 … n-2  (exclude last)
  • Option B: rob houses 1 … n-1  (exclude first)
The answer is max(A, B).

For each linear sub-problem we use the standard O(1)-space DP:
  • keep two variables: prev2 (dp[i-2]) and prev1 (dp[i-1])
  • dp[i] = max(prev1, prev2 + nums[i])

Edge case: if len(nums) == 1, return nums[0] directly.

─────────────────────────────────────────────────────────────────────────────
COMPLEXITY
─────────────────────────────────────────────────────────────────────────────
Time  : O(n)  — two linear passes
Space : O(1)  — only two variables per pass
"""

from typing import List


def rob(nums: List[int]) -> int:
    """Return the maximum amount robbable from a circular street of houses."""

    def rob_linear(houses: List[int]) -> int:
        """Standard House Robber I on a linear array."""
        prev2, prev1 = 0, 0
        for money in houses:
            prev2, prev1 = prev1, max(prev1, prev2 + money)
        return prev1

    n = len(nums)
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums)

    # Rob either houses[0..n-2] or houses[1..n-1]
    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE APPROACH — explicit DP array (same asymptotic complexity)
# ─────────────────────────────────────────────────────────────────────────────
def rob_dp_array(nums: List[int]) -> int:
    """
    Same idea but stores the full DP table for clarity.
    Useful when you need to reconstruct which houses were robbed.

    Time : O(n)   Space: O(n)
    """
    def rob_linear_full(houses: List[int]) -> int:
        if not houses:
            return 0
        if len(houses) == 1:
            return houses[0]
        dp = [0] * len(houses)
        dp[0] = houses[0]
        dp[1] = max(houses[0], houses[1])
        for i in range(2, len(houses)):
            dp[i] = max(dp[i - 1], dp[i - 2] + houses[i])
        return dp[-1]

    n = len(nums)
    if n == 1:
        return nums[0]
    return max(rob_linear_full(nums[:-1]), rob_linear_full(nums[1:]))


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Basic examples from the problem statement
    assert rob([2, 3, 2]) == 3,          "TC1 failed"
    assert rob([1, 2, 3, 1]) == 4,       "TC2 failed"
    assert rob([1, 2, 3]) == 3,          "TC3 failed"

    # Edge cases
    assert rob([0]) == 0,                "Single zero"
    assert rob([5]) == 5,                "Single house"
    assert rob([1, 1]) == 1,             "Two equal houses"
    assert rob([2, 7, 9, 3, 1]) == 11,  "Longer array"
    assert rob([0, 0, 0]) == 0,          "All zeros"
    assert rob([1000, 1000]) == 1000,    "Two max houses"

    # Alternative implementation gives same answers
    assert rob_dp_array([2, 3, 2]) == 3
    assert rob_dp_array([1, 2, 3, 1]) == 4
    assert rob_dp_array([2, 7, 9, 3, 1]) == 11

    print("All tests passed for 213. House Robber II ✓")
