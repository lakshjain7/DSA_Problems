"""
474. Ones and Zeroes
Difficulty: Medium
Topics: Array, String, Dynamic Programming (0/1 Knapsack, 2D capacity)

Problem
-------
You are given an array of binary strings `strs` and two integers `m` and `n`.

Return the size of the largest subset of `strs` such that there are at most
`m` 0's and `n` 1's in the subset.

A set `x` is a subset of a set `y` if all elements of `x` are also elements of `y`.

Example 1:
    Input: strs = ["10","0001","111001","1","0"], m = 5, n = 3
    Output: 4
    Explanation: The largest subset with at most 5 0's and 3 1's is
    {"10", "0001", "1", "0"}, so the answer is 4.
    Other valid but smaller subsets include {"0001", "1"} and {"10", "1", "0"}.
    {"111001"} is an invalid subset because it contains 4 1's, greater than n = 3.

Example 2:
    Input: strs = ["10","0","1"], m = 1, n = 1
    Output: 2
    Explanation: The largest subset is {"0", "1"}, so the answer is 2.

Constraints:
    1 <= strs.length <= 600
    1 <= strs[i].length <= 100
    strs[i] consists only of digits '0' and '1'.
    1 <= m, n <= 100

Approach (0/1 knapsack with two capacities)
-------------------------------------------
Each string is an item with two "weights": its count of zeros (z) and ones (o),
and a value of 1. We want to maximise the number of items taken while the total
zeros <= m and total ones <= n -- a 0/1 knapsack with a 2-D capacity.

dp[i][j] = the largest subset size using at most i zeros and j ones among the
strings processed so far. For each string (z, o):

    dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)   for i >= z, j >= o

We iterate i and j *downwards* so that dp[i - z][j - o] still refers to the
state before this string was considered -- this guarantees each string is used
at most once (the classic 1-D knapsack trick, lifted to 2-D).

Complexity
----------
Time:  O(L + k * m * n), where k = len(strs) and L = total characters (counting).
Space: O(m * n) for the rolling DP table.

Alternative
-----------
Top-down memoised recursion over (index, zeros_left, ones_left): at each
string either skip it or take it if it fits. Same O(k * m * n) states, but uses
O(k * m * n) memory plus recursion depth k.
"""

from functools import lru_cache
from typing import List


class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for s in strs:
            zeros = s.count("0")
            ones = len(s) - zeros
            if zeros > m or ones > n:
                continue
            for i in range(m, zeros - 1, -1):
                row, prev = dp[i], dp[i - zeros]
                for j in range(n, ones - 1, -1):
                    cand = prev[j - ones] + 1
                    if cand > row[j]:
                        row[j] = cand
        return dp[m][n]

    def findMaxFormMemo(self, strs: List[str], m: int, n: int) -> int:
        counts = [(s.count("0"), s.count("1")) for s in strs]

        @lru_cache(maxsize=None)
        def go(idx: int, zl: int, ol: int) -> int:
            if idx == len(counts):
                return 0
            best = go(idx + 1, zl, ol)
            z, o = counts[idx]
            if z <= zl and o <= ol:
                best = max(best, 1 + go(idx + 1, zl - z, ol - o))
            return best

        return go(0, m, n)


if __name__ == "__main__":
    sol = Solution()
    cases = [
        (["10", "0001", "111001", "1", "0"], 5, 3, 4),
        (["10", "0", "1"], 1, 1, 2),
        (["111"], 1, 1, 0),                    # single string doesn't fit
        (["0", "0", "0"], 2, 0, 2),            # only zeros budget matters
        (["1", "1", "1"], 0, 3, 3),            # zero zeros allowed
        (["00", "11", "01", "10"], 2, 2, 2),
        (["0"] * 100, 100, 100, 100),          # everything fits
        (["10", "01", "0011"], 2, 2, 2),
    ]
    for strs, m, n, exp in cases:
        assert sol.findMaxForm(strs, m, n) == exp, (strs, m, n)
        assert sol.findMaxFormMemo(strs, m, n) == exp, (strs, m, n)

    # randomised cross-check against brute force
    import itertools
    import random

    random.seed(474)
    for _ in range(200):
        k = random.randint(1, 7)
        strs = ["".join(random.choice("01") for _ in range(random.randint(1, 4))) for _ in range(k)]
        m, n = random.randint(1, 6), random.randint(1, 6)
        brute = 0
        for r in range(k + 1):
            for comb in itertools.combinations(strs, r):
                z = sum(s.count("0") for s in comb)
                o = sum(s.count("1") for s in comb)
                if z <= m and o <= n:
                    brute = max(brute, r)
        assert sol.findMaxForm(strs, m, n) == brute
        assert sol.findMaxFormMemo(strs, m, n) == brute
    print("All tests passed for 474. Ones and Zeroes")
