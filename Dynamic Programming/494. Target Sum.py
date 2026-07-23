"""
494. Target Sum
Difficulty: Medium
Topics: Array, Dynamic Programming, Backtracking

Problem
-------
You are given an integer array `nums` and an integer `target`.

You want to build an expression out of nums by adding one of the symbols
'+' and '-' before each integer in nums and then concatenate all the integers.

    For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1
    and concatenate them to build the expression "+2-1".

Return the number of different expressions that you can build, which evaluates
to `target`.

Examples
--------
Example 1:
    Input:  nums = [1, 1, 1, 1, 1], target = 3
    Output: 5
    Explanation: There are 5 ways to assign symbols to make the sum of nums be 3.
        -1 + 1 + 1 + 1 + 1 = 3
        +1 - 1 + 1 + 1 + 1 = 3
        +1 + 1 - 1 + 1 + 1 = 3
        +1 + 1 + 1 - 1 + 1 = 3
        +1 + 1 + 1 + 1 - 1 = 3

Example 2:
    Input:  nums = [1], target = 1
    Output: 1

Constraints
-----------
    1 <= nums.length <= 20
    0 <= nums[i] <= 1000
    0 <= sum(nums[i]) <= 1000
    -1000 <= target <= 1000

Approach 1 — Subset-sum transformation (recommended)
----------------------------------------------------
Partition nums into a set P assigned '+' and a set N assigned '-'.
Let sum(P) = p and sum(N) = n, with p + n = S (total sum).
We need p - n = target.

Adding the two equations:  2p = target + S  =>  p = (target + S) / 2.

So the problem reduces to: count the number of subsets of nums whose sum equals
P = (target + S) / 2. This is a classic 0/1 knapsack "count subsets with given
sum" problem.

Edge cases that make the answer 0:
    - |target| > S  (unreachable)
    - (target + S) is odd  (P would not be an integer)

We then use a 1-D DP where dp[s] = number of subsets that sum to s.
Because nums[i] can be 0, we iterate over exact sums (0..P) and every number is
still processed exactly once, so zeros correctly double count (a 0 can take
either '+' or '-' and land on the same subset sum), which is the desired
behavior.

Complexity
----------
    Time:  O(n * P)  where P = (target + S) / 2  (bounded by O(n * S))
    Space: O(P)      single DP row

Approach 2 — Top-down memoization
---------------------------------
State (index, running_sum). At each index choose +nums[i] or -nums[i].
Memoize on (index, running_sum). Clear and intuitive; same time complexity.
"""

from functools import lru_cache
from typing import List


def find_target_sum_ways(nums: List[int], target: int) -> int:
    """Count sign assignments of nums that evaluate to target (subset-sum DP)."""
    total = sum(nums)
    # p = (target + total) / 2 must be a non-negative integer within range.
    if abs(target) > total or (target + total) % 2 != 0:
        return 0
    p = (target + total) // 2

    dp = [0] * (p + 1)
    dp[0] = 1
    for num in nums:
        # Traverse downward for 0/1 knapsack (each item used at most once).
        for s in range(p, num - 1, -1):
            dp[s] += dp[s - num]
    return dp[p]


def find_target_sum_ways_memo(nums: List[int], target: int) -> int:
    """Alternative: top-down memoization over (index, running_sum)."""

    @lru_cache(maxsize=None)
    def dfs(i: int, cur: int) -> int:
        if i == len(nums):
            return 1 if cur == target else 0
        return dfs(i + 1, cur + nums[i]) + dfs(i + 1, cur - nums[i])

    result = dfs(0, 0)
    dfs.cache_clear()
    return result


if __name__ == "__main__":
    # Example 1
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways_memo([1, 1, 1, 1, 1], 3) == 5

    # Example 2
    assert find_target_sum_ways([1], 1) == 1
    assert find_target_sum_ways_memo([1], 1) == 1

    # Single element, negative target
    assert find_target_sum_ways([1], -1) == 1

    # Target unreachable (|target| > sum)
    assert find_target_sum_ways([1, 2, 3], 100) == 0
    assert find_target_sum_ways_memo([1, 2, 3], 100) == 0

    # Parity mismatch -> 0
    assert find_target_sum_ways([1, 2], 2) == 0  # sum=3, target+sum=5 is odd

    # Zeros double the count (each zero can be + or -)
    assert find_target_sum_ways([0, 0, 0, 0, 0, 0, 0, 0, 1], 1) == 256
    assert find_target_sum_ways_memo([0, 0, 0, 0, 0, 0, 0, 0, 1], 1) == 256

    # Reaching zero
    assert find_target_sum_ways([1, 1], 0) == 2  # +1-1, -1+1

    # Cross-check the two approaches against brute force
    from itertools import product

    for arr in ([1, 2, 3], [0, 1, 2], [2, 2, 2], [1]):
        s = sum(arr)
        for t in range(-s - 1, s + 2):
            brute = sum(
                1
                for signs in product((1, -1), repeat=len(arr))
                if sum(sg * v for sg, v in zip(signs, arr)) == t
            )
            assert find_target_sum_ways(arr, t) == brute, (arr, t)
            assert find_target_sum_ways_memo(arr, t) == brute, (arr, t)

    print("All tests passed for 494. Target Sum")
