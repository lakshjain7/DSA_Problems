"""
309. Best Time to Buy and Sell Stock with Cooldown
Difficulty: Medium
Topics: Array, Dynamic Programming

Problem:
You are given an array prices where prices[i] is the price of a given stock on
the ith day.

Find the maximum profit you can achieve. You may complete as many transactions
as you like (i.e., buy one and sell one share of the stock multiple times) with
the following restrictions:
    - After you sell your stock, you cannot buy stock on the next day
      (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e., you
must sell the stock before you buy again).

Example 1:
    Input: prices = [1,2,3,0,2]
    Output: 3
    Explanation: transactions = [buy, sell, cooldown, buy, sell]

Example 2:
    Input: prices = [1]
    Output: 0

Constraints:
    1 <= prices.length <= 5000
    0 <= prices[i] <= 1000

Approach (State-machine DP, O(1) space):
    At the end of each day we are in exactly one of three states:
      hold - we own a share
      sold - we sold a share today (so tomorrow is a forced cooldown)
      rest - we own nothing and did not sell today (free to buy tomorrow)

    Transitions for day price p:
      hold' = max(hold, rest - p)   # keep holding, or buy (only from rest)
      sold' = hold + p              # sell what we held
      rest' = max(rest, sold)       # keep resting, or finish a cooldown

    Buying is only allowed from `rest`, never directly from `sold`; that is
    exactly the one-day cooldown. Answer = max(sold, rest) at the end
    (ending while holding is never optimal).

    Why it works: the three states partition all valid histories, and each
    state's best profit only depends on the previous day's states, so the
    recurrence is optimal by induction.

Complexity:
    Time:  O(n)
    Space: O(1)

Alternative (Top-down memoised DFS):
    dfs(i, can_buy): on day i either skip, or buy (-> dfs(i+1, False)), or
    sell (-> dfs(i+2, True), skipping the cooldown day). O(n) time and space.
"""

from functools import lru_cache
from typing import List


def max_profit(prices: List[int]) -> int:
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return int(max(sold, rest))


def max_profit_memo(prices: List[int]) -> int:
    n = len(prices)

    @lru_cache(maxsize=None)
    def dfs(i: int, can_buy: bool) -> int:
        if i >= n:
            return 0
        skip = dfs(i + 1, can_buy)
        if can_buy:
            return max(skip, dfs(i + 1, False) - prices[i])
        return max(skip, dfs(i + 2, True) + prices[i])

    return dfs(0, True)


def _brute(prices: List[int]) -> int:
    """Exhaustive search for verification on small inputs."""
    n = len(prices)

    def go(i: int, holding: bool, cooldown: bool) -> int:
        if i == n:
            return 0
        best = go(i + 1, holding, False)
        if holding:
            best = max(best, prices[i] + go(i + 1, False, True))
        elif not cooldown:
            best = max(best, -prices[i] + go(i + 1, True, False))
        return best

    return go(0, False, False)


if __name__ == "__main__":
    import random

    cases = [
        ([1, 2, 3, 0, 2], 3),
        ([1], 0),
        ([5, 4, 3, 2, 1], 0),           # strictly falling: never trade
        ([1, 2, 3, 4, 5], 4),           # one long trade
        ([1, 2], 1),
        ([2, 1, 4], 3),
        ([1, 2, 4], 3),
        ([6, 1, 6, 4, 3, 0, 2], 7),     # sell at 6, cooldown, buy 0, sell 2
        ([0, 0, 0], 0),
    ]
    for prices, expected in cases:
        assert max_profit(prices) == expected, (prices, expected)
        assert max_profit_memo(prices) == expected, (prices, expected)

    random.seed(309)
    for _ in range(300):
        arr = [random.randint(0, 20) for _ in range(random.randint(1, 10))]
        b = _brute(arr)
        assert max_profit(arr) == b == max_profit_memo(arr), arr

    # large input sanity (memo version would hit recursion depth, so DP only)
    assert max_profit([i % 7 for i in range(5000)]) >= 0
    print("All tests passed for 309. Best Time to Buy and Sell Stock with Cooldown")
