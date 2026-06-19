"""
Problem #213 — House Robber II
Difficulty : Medium
Topics     : Dynamic Programming, Arrays

All houses are arranged in a circle. Cannot rob both first and last.
Solve two linear House Robber sub-problems: [0..n-2] and [1..n-1], take max.

Complexity: O(n) time, O(1) space.
"""

from typing import List


def rob(nums: List[int]) -> int:
    def rob_linear(houses: List[int]) -> int:
        prev2, prev1 = 0, 0
        for money in houses:
            prev2, prev1 = prev1, max(prev1, prev2 + money)
        return prev1

    n = len(nums)
    if n == 1:
        return nums[0]
    if n == 2:
        return max(nums)

    return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))


def rob_dp_array(nums: List[int]) -> int:
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


if __name__ == "__main__":
    assert rob([2, 3, 2]) == 3
    assert rob([1, 2, 3, 1]) == 4
    assert rob([1, 2, 3]) == 3
    assert rob([0]) == 0
    assert rob([5]) == 5
    assert rob([1, 1]) == 1
    assert rob([2, 7, 9, 3, 1]) == 11
    assert rob([0, 0, 0]) == 0
    assert rob([1000, 1000]) == 1000
    assert rob_dp_array([2, 3, 2]) == 3
    assert rob_dp_array([1, 2, 3, 1]) == 4
    assert rob_dp_array([2, 7, 9, 3, 1]) == 11
    print("All tests passed for 213. House Robber II ✓")
