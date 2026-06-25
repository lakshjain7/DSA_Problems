"""
Problem: 518. Coin Change II
Difficulty: Medium
Topics: Dynamic Programming, Array

Problem Statement:
You are given an integer array coins representing coins of different denominations
and an integer amount representing a total amount of money.
Return the number of combinations that make up that amount. If that amount of money
cannot be made up by any combination of the coins, return 0.
You may assume that you have an infinite number of each kind of coin.
The answer is guaranteed to fit in a signed 32-bit integer.

Examples:
    Input: amount = 5, coins = [1,2,5]
    Output: 4
    Explanation: 4 ways: 5=5; 5=2+2+1; 5=2+1+1+1; 5=1+1+1+1+1

    Input: amount = 3, coins = [2]
    Output: 0

    Input: amount = 10, coins = [10]
    Output: 1

Constraints:
    - 1 <= coins.length <= 300
    - 1 <= coins[i] <= 5000
    - All values in coins are unique.
    - 0 <= amount <= 5000

Approach (1D DP — Unbounded Knapsack):
    dp[j] = number of distinct combinations that sum to j.
    Base case: dp[0] = 1 (exactly one way to make 0: use no coins).

    For each coin (outer loop), update amounts from coin to amount:
        dp[j] += dp[j - coin]

    KEY INSIGHT — why coin-outer, amount-inner?
    If we iterate amount as the outer loop, we'd count permutations (orderings).
    By fixing the coin first, each combination is counted once in sorted/grouped order.
    This is the classic unbounded-knapsack ordering trick.

    Time: O(amount * len(coins))
    Space: O(amount)

Alternative (2D DP):
    dp[i][j] = ways to form amount j using the first i coins.
    Transition:
        dp[i][j] = dp[i-1][j]            # skip coin i
                 + dp[i][j - coins[i-1]] # use coin i (can reuse since unbounded)
    Space: O(n * amount), reducible to 1D.
"""

from typing import List


def change(amount: int, coins: List[int]) -> int:
    """1D DP — unbounded knapsack, counts combinations (not permutations)."""
    dp = [0] * (amount + 1)
    dp[0] = 1  # one way to make amount 0

    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]

    return dp[amount]


def change_2d(amount: int, coins: List[int]) -> int:
    """2D DP — explicit table for clarity."""
    n = len(coins)
    # dp[i][j] = ways to form amount j using coins[0..i-1]
    dp = [[0] * (amount + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 1  # always 1 way to make amount 0

    for i in range(1, n + 1):
        for j in range(amount + 1):
            dp[i][j] = dp[i - 1][j]                        # don't use coin i
            if j >= coins[i - 1]:
                dp[i][j] += dp[i][j - coins[i - 1]]        # use coin i (unbounded)

    return dp[n][amount]


if __name__ == "__main__":
    # Test 1: 4 combinations
    assert change(5, [1, 2, 5]) == 4, "Test 1 1D"
    assert change_2d(5, [1, 2, 5]) == 4, "Test 1 2D"

    # Test 2: impossible
    assert change(3, [2]) == 0, "Test 2 1D"
    assert change_2d(3, [2]) == 0, "Test 2 2D"

    # Test 3: single coin exact
    assert change(10, [10]) == 1, "Test 3 1D"
    assert change_2d(10, [10]) == 1, "Test 3 2D"

    # Test 4: amount = 0 always has 1 way
    assert change(0, [1, 2, 5]) == 1, "Test 4 1D"
    assert change_2d(0, [1, 2, 5]) == 1, "Test 4 2D"

    # Test 5: larger known value
    assert change(500, [1, 2, 5]) == 12701, "Test 5 1D"
    assert change_2d(500, [1, 2, 5]) == 12701, "Test 5 2D"

    # Test 6: single coin = 1, answer equals 1 for any amount
    assert change(7, [7]) == 1, "Test 6 1D"
    assert change_2d(7, [7]) == 1, "Test 6 2D"

    print("All tests passed!")
