"""
123. Best Time to Buy and Sell Stock III
Difficulty: Hard
Topics: Array, Dynamic Programming

Problem Statement:
You are given an array `prices` where prices[i] is the price of a given stock
on the i-th day.

Find the maximum profit you can achieve. You may complete at most two
transactions.

Note: You may not engage in multiple transactions simultaneously (i.e., you
must sell the stock before you buy again).

Examples:
    Input: prices = [3,3,5,0,0,3,1,4]
    Output: 6
    Explanation: Buy on day 4 (price = 0) and sell on day 6 (price = 3),
    profit = 3-0 = 3. Then buy on day 7 (price = 1) and sell on day 8
    (price = 4), profit = 4-1 = 3. Total profit = 3 + 3 = 6.

    Input: prices = [1,2,3,4,5]
    Output: 4
    Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5),
    profit = 5-1 = 4. Only one transaction is needed since prices strictly
    increase; a second transaction cannot add more profit.

    Input: prices = [7,6,4,3,1]
    Output: 0
    Explanation: Prices only decrease, so no transaction is profitable.

Constraints:
    1 <= prices.length <= 10^5
    0 <= prices[i] <= 10^5

Approach (State-Machine DP, O(1) space):
Model four running states after processing each day, representing the best
profit achievable so far under each scenario:
    buy1  = max profit after the FIRST buy   (a negative "cost", we want it
             as close to 0 or as high as possible, i.e., least negative)
    sell1 = max profit after the FIRST sell
    buy2  = max profit after the SECOND buy  (funded by sell1's proceeds)
    sell2 = max profit after the SECOND sell

Initialize buy1 = buy2 = -infinity (or -prices[0]) and sell1 = sell2 = 0,
then for each price p, update in this exact order (so later states use the
same day's earlier states, correctly modeling "buy and sell same day is a
no-op" while still allowing "sell then immediately buy again same day"):
    buy1  = max(buy1,  -p)
    sell1 = max(sell1,  buy1 + p)
    buy2  = max(buy2,  sell1 - p)
    sell2 = max(sell2,  buy2 + p)

Why this works: each state only ever improves (max), so buy1 tracks "lowest
price seen so far" (as a negative cost), sell1 tracks the best profit from a
single completed transaction ending on or before today, buy2 tracks the best
"net worth" after buying a second time (using profit banked from the first
transaction), and sell2 tracks the best profit after completing up to two
transactions. Because buy2 depends on sell1, and sell1 already accounts for
one full transaction, sell2 naturally represents "at most two transactions."
Answer is `sell2` (using at most two transactions is always >= using
exactly one, since sell1 is folded into the buy2/sell2 computation - the
algorithm is free to not use the second transaction if it's unprofitable
since profits are only carried forward via max()).

Complexity:
    Time:  O(n)  - single pass over prices
    Space: O(1)  - four running scalars regardless of input size

Alternative Approach (Generalized DP table, supports k transactions):
Maintain dp[t][0/1] = max profit after day i, having completed at most `t`
transactions, where the second index is 0 (not holding stock) or 1 (holding
stock). For k=2 this is a 3 x 2 table (t = 0, 1, 2) updated per day:
    dp[t][1] = max(dp[t][1], dp[t-1][0] - price)   # buy on day i for tx t
    dp[t][0] = max(dp[t][0], dp[t][1] + price)     # sell on day i for tx t
This generalizes directly to "Best Time to Buy and Sell Stock IV" (k
transactions) and costs O(n*k) time, O(k) space (rolling by day). For k=2 it
is equivalent to the four-variable version above but more verbose; included
here to show how the specialized solution generalizes.
"""

from typing import List


def max_profit(prices: List[int]) -> int:
    if not prices:
        return 0

    buy1 = buy2 = float("-inf")
    sell1 = sell2 = 0

    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)

    return sell2


def max_profit_k_transactions(prices: List[int], k: int = 2) -> int:
    """Generalized DP supporting at most k transactions. k=2 matches this problem."""
    n = len(prices)
    if n == 0 or k == 0:
        return 0

    # If k is large enough, this degenerates to the unlimited-transactions
    # problem (Best Time to Buy and Sell Stock II), solvable greedily; cap k
    # to avoid wasted work, though correctness holds without this cap too.
    k = min(k, n // 2 + 1)

    hold = [float("-inf")] * (k + 1)
    cash = [0] * (k + 1)

    for price in prices:
        for t in range(1, k + 1):
            hold[t] = max(hold[t], cash[t - 1] - price)
            cash[t] = max(cash[t], hold[t] + price)

    return cash[k]


if __name__ == "__main__":
    # Example 1
    assert max_profit([3, 3, 5, 0, 0, 3, 1, 4]) == 6

    # Example 2 - strictly increasing, one transaction suffices
    assert max_profit([1, 2, 3, 4, 5]) == 4

    # Example 3 - strictly decreasing, no profit possible
    assert max_profit([7, 6, 4, 3, 1]) == 0

    # Single price - cannot transact
    assert max_profit([5]) == 0

    # Empty input
    assert max_profit([]) == 0

    # Two prices, profitable
    assert max_profit([1, 5]) == 4

    # Two disjoint profitable windows requiring both transactions
    assert max_profit([1, 4, 2, 8]) == 9  # buy1,sell4 (profit3)+buy2,sell8(profit6)=9

    # All same price - no profit
    assert max_profit([2, 2, 2, 2]) == 0

    # Cross-check specialized solution against generalized k=2 solution
    import random
    random.seed(7)
    for _ in range(50):
        arr = [random.randint(0, 100) for _ in range(random.randint(0, 15))]
        assert max_profit(arr) == max_profit_k_transactions(arr, 2), arr

    print("All test cases passed!")
