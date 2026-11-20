"""
1155. Number of Dice Rolls With Target Sum
Difficulty: Medium
Topics: Dynamic Programming

Problem:
You have n dice, and each die has k faces numbered from 1 to k.

Given three integers n, k, and target, return the number of possible ways (out
of the k^n total ways) to roll the dice so the sum of the face-up numbers
equals target. Since the answer may be too large, return it modulo 10^9 + 7.

Example 1:
    Input: n = 1, k = 6, target = 3
    Output: 1
    Explanation: Only one way to get a sum of 3 with one 6-faced die.

Example 2:
    Input: n = 2, k = 6, target = 7
    Output: 6
    Explanation: 1+6, 2+5, 3+4, 4+3, 5+2, 6+1.

Example 3:
    Input: n = 30, k = 30, target = 500
    Output: 222616187

Constraints:
    1 <= n, k <= 30
    1 <= target <= 1000

Approach (1-D DP with sliding-window prefix sum):
    Let dp[s] = number of ways to reach sum s using the dice rolled so far.
    Rolling one more die:
        new[s] = dp[s-1] + dp[s-2] + ... + dp[s-k]
    i.e. a sum over a window of width k on the previous row. Instead of
    looping over all k faces (O(n * target * k)), maintain a running window
    sum: add dp[s-1] as the window slides right, and drop dp[s-k-1] once it
    falls out. That gives O(n * target).

    Base case: dp[0] = 1 (zero dice, sum 0). After n rounds, dp[target] is the
    answer. Early exit: if target < n or target > n*k there are 0 ways.

Complexity:
    Time:  O(n * target)
    Space: O(target)
"""

from functools import lru_cache
from typing import List

MOD = 10**9 + 7


class Solution:
    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        if target < n or target > n * k:
            return 0
        dp: List[int] = [0] * (target + 1)
        dp[0] = 1
        for _ in range(n):
            new = [0] * (target + 1)
            window = 0
            for s in range(1, target + 1):
                window += dp[s - 1]
                if s - k - 1 >= 0:
                    window -= dp[s - k - 1]
                new[s] = window % MOD
            dp = new
        return dp[target]


class SolutionMemo:
    """
    Alternative: top-down memoization, trying every face of the current die.
    ways(i, t) = sum_{f=1..k} ways(i-1, t-f). Time O(n * target * k).
    """

    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        @lru_cache(maxsize=None)
        def ways(i: int, t: int) -> int:
            if i == 0:
                return 1 if t == 0 else 0
            if t < i or t > i * k:
                return 0
            return sum(ways(i - 1, t - f) for f in range(1, min(k, t) + 1)) % MOD

        return ways(n, target)


if __name__ == "__main__":
    from itertools import product

    for S in (Solution(), SolutionMemo()):
        f = S.numRollsToTarget
        assert f(1, 6, 3) == 1
        assert f(2, 6, 7) == 6
        assert f(30, 30, 500) == 222616187
        assert f(1, 1, 1) == 1          # single trivial die
        assert f(1, 6, 7) == 0          # target too large
        assert f(3, 6, 2) == 0          # target too small
        assert f(2, 5, 10) == 1         # max sum
        assert f(3, 2, 3) == 1          # min sum
        assert f(30, 30, 1000) == 0     # beyond n*k

    # brute-force cross-check on small inputs
    for n in range(1, 5):
        for k in range(1, 6):
            for t in range(1, n * k + 2):
                exp = sum(1 for r in product(range(1, k + 1), repeat=n) if sum(r) == t)
                assert Solution().numRollsToTarget(n, k, t) == exp, (n, k, t)
                assert SolutionMemo().numRollsToTarget(n, k, t) == exp, (n, k, t)

    print("All tests passed for 1155. Number of Dice Rolls With Target Sum")
