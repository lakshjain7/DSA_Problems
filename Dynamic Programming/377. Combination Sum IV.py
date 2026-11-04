"""
377. Combination Sum IV
Difficulty: Medium
Topics: Array, Dynamic Programming

Problem:
Given an array of distinct integers nums and a target integer target, return
the number of possible combinations that add up to target. Different sequences
(orderings) are counted as different combinations. The answer is guaranteed to
fit in a 32-bit integer.

Examples:
    nums = [1,2,3], target = 4 -> 7
        (1,1,1,1) (1,1,2) (1,2,1) (1,3) (2,1,1) (2,2) (3,1)
    nums = [9], target = 3     -> 0

Constraints:
    1 <= nums.length <= 200
    1 <= nums[i] <= 1000, all distinct
    1 <= target <= 1000

Approach (bottom-up DP over the target, "permutation" knapsack):
    dp[t] = number of ordered sequences summing to t. The last element of such
    a sequence is some num <= t, leaving a sequence summing to t - num:
        dp[t] = sum(dp[t - num] for num in nums if num <= t),  dp[0] = 1.
    Iterating the target in the OUTER loop and nums in the INNER loop counts
    orderings (swapping the loops would count unordered combinations, as in
    Coin Change II).

Complexity:
    Time:  O(target * n)
    Space: O(target)
"""
from functools import lru_cache
from typing import List


def combinationSum4(nums: List[int], target: int) -> int:
    dp = [0] * (target + 1)
    dp[0] = 1
    for t in range(1, target + 1):
        for num in nums:
            if num <= t:
                dp[t] += dp[t - num]
    return dp[target]


def combinationSum4Memo(nums: List[int], target: int) -> int:
    """Alternative: top-down memoization."""
    @lru_cache(maxsize=None)
    def go(rem: int) -> int:
        if rem == 0:
            return 1
        return sum(go(rem - n) for n in nums if n <= rem)
    return go(target)


if __name__ == "__main__":
    for f in (combinationSum4, combinationSum4Memo):
        assert f([1, 2, 3], 4) == 7
        assert f([9], 3) == 0
        assert f([9], 9) == 1
        assert f([1], 10) == 1
        assert f([2], 3) == 0
        assert f([1, 2], 5) == 8   # Fibonacci-like
        assert f([4, 2, 1], 32) == 39882198
    print("All tests passed.")
