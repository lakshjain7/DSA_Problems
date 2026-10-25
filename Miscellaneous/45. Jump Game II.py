"""
45. Jump Game II
Difficulty: Medium
Topics: Array, Greedy, Dynamic Programming

You are given a 0-indexed array of integers nums of length n. You start at
nums[0]. Each nums[i] is the maximum length of a forward jump from index i.
Return the minimum number of jumps to reach nums[n - 1]. The test cases are
generated such that you can reach nums[n - 1].

Example 1:
    Input: nums = [2,3,1,1,4]
    Output: 2
Example 2:
    Input: nums = [2,3,0,1,4]
    Output: 2

Constraints:
    1 <= nums.length <= 10^4
    0 <= nums[i] <= 1000
    It's guaranteed that you can reach nums[n - 1].

Approach (greedy BFS by levels):
    Treat each jump as a BFS level. `cur_end` is the farthest index reachable
    with the current number of jumps; `farthest` is the farthest index
    reachable with one more jump. When we pass cur_end we must take another
    jump, and the best choice is the one that reaches `farthest`. Greedy works
    because reachable indices with k jumps always form a prefix.

Complexity: Time O(n), Space O(1).
"""
from typing import List


def jump(nums: List[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps


def jump_dp(nums: List[int]) -> int:
    """Alternative: O(n^2) DP. dp[i] = min jumps to reach i."""
    n = len(nums)
    dp = [float("inf")] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[-1]


if __name__ == "__main__":
    cases = [([2, 3, 1, 1, 4], 2), ([2, 3, 0, 1, 4], 2), ([0], 0),
             ([1], 0), ([1, 1, 1, 1], 3), ([5, 1, 1, 1, 1], 1),
             ([2, 1], 1), ([1, 2, 3], 2)]
    for arr, exp in cases:
        assert jump(arr) == exp, (arr, jump(arr), exp)
        assert jump_dp(arr) == exp, (arr, jump_dp(arr), exp)
    print("All tests passed.")
