"""
Problem Number: 198
Title: House Robber
Difficulty: Medium
Topics: Dynamic Programming, Array

Problem Statement:
------------------
You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed, the only constraint
stopping you from robbing each of them is that adjacent houses have
security systems connected and it will automatically contact the police
if two adjacent houses were broken into on the same night.

Given an integer array `nums` representing the amount of money of each
house, return the maximum amount of money you can rob tonight without
alerting the police.

Examples:
---------
Input: nums = [1, 2, 3, 1]
Output: 4
Explanation: Rob house 1 (money = 1) then rob house 3 (money = 3). Total = 1 + 3 = 4.

Input: nums = [2, 7, 9, 3, 1]
Output: 12
Explanation: Rob house 1 (money = 2), house 3 (money = 9), house 5 (money = 1). Total = 12.

Constraints:
------------
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 400

Approach:
---------
Dynamic Programming with O(1) space (space-optimised).

At each house i, we have two choices:
  1. Skip house i — take the best amount we had at house i-1.
  2. Rob house i  — take nums[i] plus the best amount at house i-2
                    (we cannot also take from i-1).

So:  dp[i] = max(dp[i-1], nums[i] + dp[i-2])

We only ever look back two steps, so we can keep just two variables
`prev2` (dp[i-2]) and `prev1` (dp[i-1]) instead of a full array.

Why it works:
Each sub-problem optimal choice feeds into the next, satisfying the
optimal-substructure property of DP.

Complexity Analysis:
--------------------
Time  : O(n)  — single pass through the array
Space : O(1)  — only two rolling variables

Alternative Approach:
---------------------
Full DP array (O(n) space):
    dp = [0] * (n + 1)
    dp[1] = nums[0]
    for i in range(2, n + 1):
        dp[i] = max(dp[i-1], nums[i-1] + dp[i-2])
    return dp[n]
This is equivalent but uses O(n) space — the space-optimised version
below is preferred.
"""

from typing import List


def rob(nums: List[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2 = 0
    prev1 = 0

    for amount in nums:
        current = max(prev1, amount + prev2)
        prev2 = prev1
        prev1 = current

    return prev1


def rob_full_dp(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0
    if n == 1:
        return nums[0]
    dp = [0] * n
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    for i in range(2, n):
        dp[i] = max(dp[i - 1], nums[i] + dp[i - 2])
    return dp[-1]


if __name__ == "__main__":
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
    assert rob([5]) == 5
    assert rob([1, 10]) == 10
    assert rob([0, 0, 0]) == 0
    assert rob([1, 2, 3, 4, 5]) == 9
    assert rob([5, 4, 3, 2, 1]) == 9
    assert rob([400] * 100) == 400 * 50
    for test in [[2, 7, 9, 3, 1], [1, 2, 3, 1], [5], [0, 0, 0]]:
        assert rob(test) == rob_full_dp(test)
    print("All tests passed!")
