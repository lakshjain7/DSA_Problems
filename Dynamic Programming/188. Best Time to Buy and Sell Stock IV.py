"""
188. Best Time to Buy and Sell Stock IV
Difficulty: Hard
Topics: Array, Dynamic Programming

Problem Statement
-----------------
You are given an integer array `prices` where prices[i] is the price of a given
stock on the i-th day, and an integer `k`.

Find the maximum profit you can achieve. You may complete at most `k`
transactions: i.e. you may buy at most k times and sell at most k times.

Note: You may not engage in multiple transactions simultaneously (i.e., you
must sell the stock before you buy again).

Examples
--------
Example 1:
    Input:  k = 2, prices = [2,4,1]
    Output: 2
    Explanation: Buy on day 1 (price = 2) and sell on day 2 (price = 4),
    profit = 4 - 2 = 2.

Example 2:
    Input:  k = 2, prices = [3,2,6,5,0,3]
    Output: 7
    Explanation: Buy on day 2 (price = 2) and sell on day 3 (price = 6),
    profit = 4. Then buy on day 5 (price = 0) and sell on day 6 (price = 3),
    profit = 3. Total = 7.

Constraints
-----------
- 1 <= k <= 100
- 1 <= prices.length <= 1000
- 0 <= prices[i] <= 1000

Approach (DP over transactions x holding state)
-----------------------------------------------
This generalizes the classic stock problems. We track, for each allowed number
of transactions t (1..k), two running values while sweeping the prices:

- best_buy[t]:  the best value after having *bought* the stock for the t-th
                transaction. Since buying spends money, we store it as
                (profit_so_far - price), i.e. we want to maximize this.
- best_sell[t]: the best profit after having *sold* the stock for the t-th
                transaction.

For each price p we update, for t from 1..k:
    best_buy[t]  = max(best_buy[t],  best_sell[t-1] - p)   # buy for txn t
    best_sell[t] = max(best_sell[t], best_buy[t] + p)      # sell for txn t

best_sell[k] is the answer.

Optimization: if k >= len(prices) // 2, there is no transaction limit in
practice (you can capture every upward move), so we fall back to the greedy
"sum of all positive daily gains" solution to avoid an O(n*k) table with a
huge k.

Why it works
------------
best_sell[t-1] is the most money we can have before opening transaction t.
Subtracting the current price models the cash spent on buying; adding a later
price models selling. Taking maxima at each step ensures every buy is paired
with the best possible earlier state and every sell with the best buy, which
is exactly optimal substructure for at-most-k non-overlapping transactions.

Complexity
----------
Time:  O(n * k) in the general case, O(n) in the unlimited fallback.
Space: O(k) - two rolling arrays of length k+1.
"""

from typing import List


def max_profit(k: int, prices: List[int]) -> int:
    """Maximum profit with at most k non-overlapping transactions."""
    n = len(prices)
    if n == 0 or k == 0:
        return 0

    # Unlimited-transactions fallback: capture every positive daily gain.
    if k >= n // 2:
        return sum(
            max(0, prices[i] - prices[i - 1]) for i in range(1, n)
        )

    # best_buy[t]  = max (profit - price) after buying for transaction t
    # best_sell[t] = max profit after selling for transaction t
    best_buy = [float("-inf")] * (k + 1)
    best_sell = [0] * (k + 1)

    for price in prices:
        for t in range(1, k + 1):
            best_buy[t] = max(best_buy[t], best_sell[t - 1] - price)
            best_sell[t] = max(best_sell[t], best_buy[t] + price)

    return best_sell[k]


def max_profit_2d(k: int, prices: List[int]) -> int:
    """Alternative explicit 2D DP (clearer, O(n*k) time and O(n*k) space)."""
    n = len(prices)
    if n == 0 or k == 0:
        return 0
    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))

    # dp[t][i] = max profit using at most t transactions within prices[:i+1]
    dp = [[0] * n for _ in range(k + 1)]
    for t in range(1, k + 1):
        # best = max over j < i of (dp[t-1][j] - prices[j])
        best = -prices[0]
        for i in range(1, n):
            dp[t][i] = max(dp[t][i - 1], prices[i] + best)
            best = max(best, dp[t - 1][i] - prices[i])
    return dp[k][n - 1]


if __name__ == "__main__":
    # Provided examples
    assert max_profit(2, [2, 4, 1]) == 2
    assert max_profit(2, [3, 2, 6, 5, 0, 3]) == 7

    # No transactions allowed
    assert max_profit(0, [1, 2, 3]) == 0
    # Single day -> no profit possible
    assert max_profit(2, [5]) == 0
    # Monotonically decreasing -> no profit
    assert max_profit(2, [5, 4, 3, 2, 1]) == 0
    # Monotonically increasing with k=1 -> one transaction over whole range
    assert max_profit(1, [1, 2, 3, 4, 5]) == 4
    # Unlimited-style: large k captures every gain
    assert max_profit(100, [1, 2, 3, 4, 5]) == 4
    assert max_profit(2, [1, 2, 4, 2, 5, 7, 2, 4, 9, 0]) == 13
    # k larger than possible transactions
    assert max_profit(10, [3, 2, 6, 5, 0, 3]) == 7

    # Cross-check the two DP formulations on a batch of cases
    test_cases = [
        (2, [2, 4, 1]),
        (2, [3, 2, 6, 5, 0, 3]),
        (1, [1, 2, 3, 4, 5]),
        (2, [5, 4, 3, 2, 1]),
        (3, [1, 2, 4, 2, 5, 7, 2, 4, 9, 0]),
        (0, [1, 2, 3]),
        (2, [5]),
        (4, [6, 1, 3, 2, 4, 7]),
    ]
    for kk, pp in test_cases:
        assert max_profit(kk, pp) == max_profit_2d(kk, pp)

    print("All tests passed for 188. Best Time to Buy and Sell Stock IV")
