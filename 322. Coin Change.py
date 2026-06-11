"""
Problem 322: Coin Change
Difficulty: Medium
Topics: Array, Dynamic Programming, Breadth-First Search

Problem Statement:
-----------------
You are given an integer array `coins` representing coins of different
denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the coins,
return -1.

You may assume that you have an infinite number of each kind of coin.

Examples:
---------
Example 1:
  Input:  coins = [1, 2, 5], amount = 11
  Output: 3
  Explanation: 11 = 5 + 5 + 1

Example 2:
  Input:  coins = [2], amount = 3
  Output: -1

Example 3:
  Input:  coins = [1], amount = 0
  Output: 0

Constraints:
------------
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 2^31 - 1
- 0 <= amount <= 10^4

Approach: Bottom-Up Dynamic Programming (Unbounded Knapsack)
------------------------------------------------------------
Define dp[i] = minimum coins needed to make amount i.

Base case:  dp[0] = 0 (0 coins needed for amount 0)
Transition: dp[i] = min(dp[i - coin] + 1) for each coin <= i

We fill the table from 1 to amount. For each amount i, we try every coin:
  - If i - coin >= 0 and dp[i - coin] != infinity, then we can reach i
    using dp[i - coin] + 1 coins.
  - We take the minimum over all valid coins.

Why bottom-up instead of top-down memos?
  - Same asymptotic complexity but bottom-up avoids recursion overhead
    and is slightly faster in practice.

Complexity:
-----------
Time:  O(amount * len(coins)) — fill dp table
Space: O(amount) — dp array of size amount+1

Alternative: BFS Approach
--------------------------
Treat this as a shortest-path problem: each "state" is an amount,
and from amount x you can move to x+coin for each coin. BFS gives
the shortest path (fewest coins) from 0 to `amount`.

BFS is elegant but has the same complexity and uses more memory
due to the visited set and queue. Bottom-up DP is preferred.
"""

from typing import List
from collections import deque


def coinChange(coins: List[int], amount: int) -> int:
    """
    Bottom-up DP for minimum coin change.

    Args:
        coins:  Available coin denominations (unlimited supply each).
        amount: Target amount.

    Returns:
        Minimum number of coins to make `amount`, or -1 if impossible.
    """
    # Initialize with amount+1 as "infinity" (can't need more than amount coins)
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins for amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] <= amount else -1


# ---------------------------------------------------------------------------
# Alternative Approach: BFS
# ---------------------------------------------------------------------------

def coinChange_bfs(coins: List[int], amount: int) -> int:
    """
    BFS approach: shortest path from 0 to amount.
    Each coin denomination is an edge of weight 1.
    """
    if amount == 0:
        return 0

    visited = {0}
    queue = deque([0])
    steps = 0

    while queue:
        steps += 1
        for _ in range(len(queue)):
            curr = queue.popleft()
            for coin in coins:
                nxt = curr + coin
                if nxt == amount:
                    return steps
                if nxt < amount and nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

    return -1


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Basic examples from problem statement
    assert coinChange([1, 2, 5], 11) == 3      # 5+5+1
    assert coinChange([2], 3) == -1            # impossible
    assert coinChange([1], 0) == 0             # zero amount

    # Edge cases
    assert coinChange([1], 1) == 1
    assert coinChange([1], 2) == 2
    assert coinChange([2], 4) == 2             # 2+2

    # Greedy fails here — DP handles correctly
    # Greedy would pick 4, then fail. DP picks 3+3=6? No: 6=3+3, so 2 coins
    assert coinChange([1, 3, 4, 5], 7) == 2   # 3+4
    # Greedy: 5+1+1 = 3 coins. DP: 3+4 = 2 coins.

    # Large denomination only
    assert coinChange([5], 10) == 2
    assert coinChange([5], 3) == -1

    # Single coin equals amount
    assert coinChange([7], 7) == 1

    # All ones
    assert coinChange([1], 100) == 100

    # Compare BFS and DP on several inputs
    test_cases = [
        ([1, 2, 5], 11),
        ([2], 3),
        ([1, 3, 4, 5], 7),
        ([186, 419, 83, 408], 6249),
    ]
    for coins, amount in test_cases:
        dp_result = coinChange(coins, amount)
        bfs_result = coinChange_bfs(coins, amount)
        assert dp_result == bfs_result, (
            f"Mismatch: coins={coins}, amount={amount}: dp={dp_result}, bfs={bfs_result}"
        )

    print("All tests passed!")
